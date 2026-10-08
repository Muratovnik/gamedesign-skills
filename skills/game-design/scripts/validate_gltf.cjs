#!/usr/bin/env node
'use strict';

const fs = require('node:fs/promises');
const { constants } = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const { parseArgs } = require('node:util');
const { fileURLToPath, pathToFileURL } = require('node:url');

const EXIT = { supported: 0, refuted: 1, unavailable: 2 };
const COVERAGE_CODES = new Set(['UNSUPPORTED_EXTENSION', 'INCOMPLETE_EXTENSION_SUPPORT']);
const HELP = `Usage: node validate_gltf.cjs ARTIFACT [--resource-root DIRECTORY] [--output REPORT]

Calls the pinned Khronos gltf-validator on actual glTF/GLB bytes.
Embedded data URIs are handled by the validator. External files require an
explicit resource root; remote resources are never fetched. REPORT must be new.
Exit 0: supported checks; 1: conformance refuted; 2: unavailable evidence or output.
This does not assess a game's mesh, scale, collision, appearance, or other needs.
`;

function problem(code, message) {
  return Object.assign(new Error(message), { code });
}

function errorRecord(error) {
  return { code: error?.code || 'operation_failed', message: String(error?.message || error) };
}

function identity(bytes) {
  return { bytes: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex') };
}

async function readRegular(filename) {
  // Read and identify the same opened regular file, never a device or FIFO.
  const handle = await fs.open(filename, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
  try {
    if (!(await handle.stat()).isFile()) throw problem('not_a_regular_file', filename);
    return await handle.readFile();
  } finally {
    await handle.close();
  }
}

function contained(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative !== '..' && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

async function prospectivePath(filename, links = 0) {
  const absolute = path.resolve(filename);
  try {
    return await fs.realpath(absolute);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    // realpath alone cannot identify a missing target reached through an alias.
    // Follow dangling links too, then resolve the nearest existing ancestor.
    try {
      const info = await fs.lstat(absolute);
      if (info.isSymbolicLink()) {
        if (links >= 40) throw problem('path_link_limit', 'Cannot resolve the input/output destination.');
        return prospectivePath(path.resolve(path.dirname(absolute), await fs.readlink(absolute)), links + 1);
      }
    } catch (entryError) {
      if (entryError.code !== 'ENOENT') throw entryError;
    }
    const parent = path.dirname(absolute);
    if (parent === absolute) throw error;
    return path.join(await prospectivePath(parent, links), path.basename(absolute));
  }
}

async function loadValidator(receipt) {
  const sourceFiles = {};
  const sourceBytes = {};
  for (const name of ['validate_gltf.cjs', 'package.json', 'package-lock.json']) {
    const bytes = await readRegular(path.join(__dirname, name));
    sourceFiles[name] = identity(bytes);
    sourceBytes[name] = bytes;
  }
  receipt.source = { files: sourceFiles };
  const manifest = JSON.parse(sourceBytes['package.json']);
  const lock = JSON.parse(sourceBytes['package-lock.json']);
  const expected = manifest.dependencies?.['gltf-validator'];
  const locked = lock.packages?.['node_modules/gltf-validator'];
  if (!expected || locked?.version !== expected || !locked.integrity) {
    throw problem('dependency_lock_mismatch', 'The manifest and locked validator version must agree.');
  }
  // An adjacent install is deliberate. Do not silently use a parent/global package.
  const packageRoot = await fs.realpath(path.join(__dirname, 'node_modules', 'gltf-validator'));
  const files = {};
  let metadata;
  for (const name of ['package.json', 'index.js', 'gltf_validator.dart.js', 'LICENSE', 'NOTICES']) {
    const bytes = await readRegular(path.join(packageRoot, name));
    files[name] = identity(bytes);
    if (name === 'package.json') metadata = JSON.parse(bytes);
  }
  receipt.dependency = {
    name: 'gltf-validator', expected_version: expected,
    installed_version: metadata.version, license: metadata.license,
    package_root: packageRoot, files,
    locked_package: { version: locked.version, resolved: locked.resolved, integrity: locked.integrity },
  };
  if (metadata.name !== 'gltf-validator' || metadata.version !== expected) {
    throw problem('dependency_version_mismatch', 'Install the exact adjacent locked dependency.');
  }
  const validator = require(path.join(packageRoot, 'index.js'));
  receipt.dependency.runtime_version = validator.version();
  receipt.dependency.supported_extensions = validator.supportedExtensions();
  if (validator.version() !== expected) {
    throw problem('dependency_runtime_mismatch', 'The validator runtime disagrees with its package version.');
  }
  return validator;
}

function resourceLoader(artifactPath, root, receipt) {
  return async (uri) => {
    const resource = { uri };
    receipt.resources.push(resource);
    try {
      if (!root) throw problem('resource_root_required', 'External files require --resource-root.');
      if (uri.includes('\\')) throw problem('resource_uri_not_file_path', 'Use URI path separators.');
      const url = new URL(uri, pathToFileURL(artifactPath));
      if (url.protocol !== 'file:' || url.hostname) {
        throw problem('remote_resource_denied', 'Only local files within the explicit resource root are allowed.');
      }
      if (url.search || url.hash) {
        throw problem('resource_uri_not_file_path', 'Query strings and fragments are not local file paths.');
      }
      const requestedPath = fileURLToPath(url);
      if (!contained(root, requestedPath)) throw problem('resource_outside_root', 'Resource is outside the explicit root.');
      const realPath = await fs.realpath(requestedPath);
      if (!contained(root, realPath)) throw problem('resource_outside_root', 'Resource symlink escapes the explicit root.');
      const bytes = await readRegular(realPath);
      Object.assign(resource, { status: 'read', path: realPath, ...identity(bytes) });
      return new Uint8Array(bytes);
    } catch (error) {
      Object.assign(resource, { status: 'unavailable', error: errorRecord(error) });
      throw error;
    }
  };
}

async function validateArtifact(artifact, resourceRoot) {
  const receipt = {
    schema: 'game-design-gltf-conformance/1',
    status: 'unavailable', stage: 'input',
    claim: 'Conformance checks implemented by the recorded gltf-validator, with requested resources available',
    runtime: { node: process.version, platform: process.platform, architecture: process.arch },
    artifact: { requested_path: path.resolve(artifact) },
    source: null, dependency: null,
    resource_policy: { root: null, embedded_data: 'validator', network: 'denied' },
    resources: [], coverage_limits: [], validator_report: null,
    caller_predicate: { status: 'not_evaluated', reason: 'The consumer must check its own required game properties separately.' },
    limitations: [
      'No target-engine import, round trip, rendering, collision, scale, or human-experience claim.',
      'Warnings and information remain in the validator report; zero errors is not a universal proof of conformance.',
      'Use stable task-owned files; path checks are not an operating-system sandbox against concurrent filesystem changes.',
    ],
  };
  try {
    const artifactPath = await fs.realpath(artifact);
    const bytes = await readRegular(artifactPath);
    Object.assign(receipt.artifact, { path: artifactPath, ...identity(bytes) });
    if (resourceRoot) {
      const root = await fs.realpath(resourceRoot);
      if (!(await fs.stat(root)).isDirectory()) throw problem('resource_root_not_directory', root);
      receipt.resource_policy.root = root;
    }
    receipt.stage = 'dependency';
    const validator = await loadValidator(receipt);
    receipt.stage = 'validation';
    const report = await validator.validateBytes(new Uint8Array(bytes), {
      uri: path.basename(artifactPath), writeTimestamp: false, maxIssues: 0,
      externalResourceFunction: resourceLoader(artifactPath, receipt.resource_policy.root, receipt),
    });
    receipt.validator_report = report;
    if (!Number.isInteger(report?.issues?.numErrors) || !Array.isArray(report.issues.messages)) {
      throw problem('invalid_validator_report', 'The official validator did not return the expected issue report.');
    }
    receipt.coverage_limits = report.issues.messages.filter((issue) => COVERAGE_CODES.has(issue.code));
    if (receipt.resources.some((resource) => resource.status === 'unavailable') ||
        report.issues.messages.some((issue) => issue.code === 'IO_ERROR')) {
      receipt.reason = 'resource_evidence_unavailable';
    } else if (receipt.coverage_limits.length || report.issues.truncated) {
      receipt.reason = 'validator_coverage_incomplete';
    } else {
      receipt.status = report.issues.numErrors ? 'refuted' : 'supported';
      receipt.reason = report.issues.numErrors ? 'validator_reported_errors' : 'no_errors_in_implemented_checks';
    }
  } catch (error) {
    receipt.error = errorRecord(error);
    receipt.reason = `${receipt.stage}_unavailable`;
  }
  return receipt;
}

async function writeNewReport(filename, text) {
  const parent = await fs.realpath(path.dirname(path.resolve(filename)));
  const target = path.join(parent, path.basename(filename));
  const temporary = await fs.mkdtemp(path.join(parent, '.gltf-report-'));
  try {
    const staged = path.join(temporary, 'report.json');
    await fs.writeFile(staged, text, { flag: 'wx', mode: 0o600 });
    // A same-filesystem hard link publishes complete bytes and fails if the name exists.
    await fs.link(staged, target);
  } finally {
    await fs.rm(temporary, { recursive: true, force: true });
  }
}

async function main() {
  let args;
  try {
    args = parseArgs({
      options: { 'resource-root': { type: 'string' }, output: { type: 'string' }, help: { type: 'boolean', short: 'h' } },
      allowPositionals: true,
    });
    if (args.values.help) { process.stdout.write(HELP); return; }
    if (args.positionals.length !== 1) throw problem('invalid_arguments', HELP.trim());
    if (args.values.output && await prospectivePath(args.values.output) === await prospectivePath(args.positionals[0])) {
      throw problem('output_is_input', 'The report must have a separate new path.');
    }
  } catch (error) {
    process.stdout.write(`${JSON.stringify({ status: 'unavailable', stage: 'arguments', error: errorRecord(error) })}\n`);
    process.exitCode = 2;
    return;
  }
  const receipt = await validateArtifact(args.positionals[0], args.values['resource-root']);
  const text = `${JSON.stringify(receipt, null, 2)}\n`;
  if (args.values.output) {
    try {
      await writeNewReport(args.values.output, text);
    } catch (error) {
      process.stdout.write(`${JSON.stringify({ status: 'unavailable', stage: 'report_output', error: errorRecord(error), validation: receipt }, null, 2)}\n`);
      process.exitCode = 2;
      return;
    }
  }
  process.stdout.write(text);
  process.exitCode = EXIT[receipt.status];
}

if (require.main === module) main().catch((error) => {
  process.stderr.write(`${JSON.stringify({ status: 'unavailable', error: errorRecord(error) })}\n`);
  process.exitCode = 2;
});
