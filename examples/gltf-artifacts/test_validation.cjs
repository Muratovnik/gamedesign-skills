'use strict';

const assert = require('node:assert/strict');
const { test } = require('node:test');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const http = require('node:http');
const { execFile } = require('node:child_process');
const { createHash } = require('node:crypto');

const fixtures = path.join(__dirname, 'fixtures');
const cli = process.env.GD_GLTF_SCRIPT
  ? path.resolve(process.env.GD_GLTF_SCRIPT)
  : path.resolve(__dirname, '../../skills/game-design/scripts/validate_gltf.cjs');
const fixture = (name) => path.join(fixtures, name);
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

async function workspace(t) {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'game-design-gltf-'));
  t.after(() => fs.rm(directory, { recursive: true, force: true }));
  const assets = path.join(directory, 'assets');
  await fs.mkdir(assets);
  await fs.copyFile(fixture('positions.bin'), path.join(assets, 'positions.bin'));
  return { directory, assets };
}

function run(args, script = cli, extraEnv = {}) {
  return new Promise((resolve, reject) => {
    execFile(process.execPath, [script, ...args], {
      timeout: 20000, maxBuffer: 8 * 1024 * 1024,
      env: { ...process.env, ...extraEnv },
    }, (error, stdout, stderr) => {
      if (error && (!Number.isInteger(error.code) || error.killed || error.signal)) {
        reject(error);
        return;
      }
      try {
        resolve({ code: error?.code || 0, report: JSON.parse(stdout), stdout, stderr });
      } catch (parseError) {
        reject(new Error(`CLI did not return JSON: ${stdout}\n${stderr}`, { cause: parseError }));
      }
    });
  });
}

async function externalAsset(assets, uri) {
  const document = JSON.parse(await fs.readFile(fixture('external.gltf'), 'utf8'));
  document.buffers[0].uri = uri;
  const filename = path.join(assets, 'external.gltf');
  await fs.writeFile(filename, `${JSON.stringify(document)}\n`);
  return filename;
}

function expectOutcome(result, status, code) {
  assert.equal(result.code, code, result.stdout);
  assert.equal(result.report.status, status, result.stdout);
}

test('the real validator accepts GLTF, GLB, empty and camera-only artifacts', async (t) => {
  for (const name of ['signal-wedge.gltf', 'signal-wedge.glb', 'empty.gltf', 'camera.gltf']) {
    await t.test(name, async () => {
      const result = await run([fixture(name)]);
      expectOutcome(result, 'supported', 0);
      assert.equal(result.report.validator_report.issues.numErrors, 0);
      assert.equal(result.report.dependency.runtime_version, '2.0.0-dev.3.10');
      assert.equal(result.report.artifact.sha256, sha256(await fs.readFile(fixture(name))));
      assert.equal(result.report.source.files['validate_gltf.cjs'].sha256, sha256(await fs.readFile(cli)));
      assert.match(result.report.dependency.files['gltf_validator.dart.js'].sha256, /^[a-f0-9]{64}$/);
      assert.equal(result.report.caller_predicate.status, 'not_evaluated');
      assert.deepEqual(result.report.coverage_limits, []);
      if (name.startsWith('signal-wedge')) {
        // This original fixture has exactly one triangle; it is not the CLI's acceptance rule.
        assert.equal(result.report.validator_report.info.totalTriangleCount, 1);
      } else {
        assert.equal(result.report.validator_report.info.totalTriangleCount || 0, 0);
      }
    });
  }
});

test('an accessor requiring four VEC3 values cannot fit the fixture\'s three values', async () => {
  const result = await run([fixture('bad-accessor.gltf')]);
  expectOutcome(result, 'refuted', 1);
  assert.ok(result.report.validator_report.issues.messages.some((issue) => issue.code === 'ACCESSOR_TOO_LONG'));
  assert.equal(result.report.resources.length, 0);
});

test('recognized invalid JSON is refuted; unrecognized or absent bytes are unavailable', async (t) => {
  const malformed = await run([fixture('malformed.gltf')]);
  expectOutcome(malformed, 'refuted', 1);
  assert.ok(malformed.report.validator_report.issues.messages.some((issue) => issue.code === 'INVALID_JSON'));
  const unrecognized = await run([fixture('unrecognized.dat')]);
  expectOutcome(unrecognized, 'unavailable', 2);
  assert.equal(unrecognized.report.validator_report, null);
  const { directory } = await workspace(t);
  const zero = path.join(directory, 'zero.gltf');
  await fs.writeFile(zero, '');
  expectOutcome(await run([zero]), 'unavailable', 2);
  const missing = await run([path.join(directory, 'absent.gltf')]);
  expectOutcome(missing, 'unavailable', 2);
  assert.equal(missing.report.stage, 'input');
  assert.equal(missing.report.validator_report, null);
});

test('explicit local sidecars are read and identified; missing permission is unavailable', async () => {
  const result = await run([fixture('external.gltf'), '--resource-root', fixtures]);
  expectOutcome(result, 'supported', 0);
  assert.equal(result.report.resources.length, 1);
  assert.equal(result.report.resources[0].status, 'read');
  assert.equal(result.report.resources[0].sha256, sha256(await fs.readFile(fixture('positions.bin'))));
  const noRoot = await run([fixture('external.gltf')]);
  expectOutcome(noRoot, 'unavailable', 2);
  assert.equal(noRoot.report.resources[0].error.code, 'resource_root_required');
});

test('a missing buffer remains unavailable even though the validator emits an IO_ERROR', async () => {
  const result = await run([fixture('missing-resource.gltf'), '--resource-root', fixtures]);
  expectOutcome(result, 'unavailable', 2);
  assert.ok(result.report.validator_report.issues.messages.some((issue) => issue.code === 'IO_ERROR'));
  assert.equal(result.report.resources[0].error.code, 'ENOENT');
  assert.equal(result.report.reason, 'resource_evidence_unavailable');
});

test('remote URIs are denied without contacting an available HTTP server', async (t) => {
  const { assets } = await workspace(t);
  let requests = 0;
  const server = http.createServer((_request, response) => {
    requests += 1;
    response.end(Buffer.alloc(36));
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  t.after(() => new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve())));
  const artifact = await externalAsset(assets, `http://127.0.0.1:${server.address().port}/positions.bin`);
  const result = await run([artifact, '--resource-root', assets]);
  expectOutcome(result, 'unavailable', 2);
  assert.equal(result.report.resources[0].error.code, 'remote_resource_denied');
  assert.equal(requests, 0);
  const https = await run([fixture('remote-resource.gltf'), '--resource-root', fixtures]);
  expectOutcome(https, 'unavailable', 2);
  assert.equal(https.report.resources[0].error.code, 'remote_resource_denied');
});

test('plain, encoded, and same-prefix outside-root paths are denied', async (t) => {
  const { directory, assets } = await workspace(t);
  await fs.copyFile(fixture('positions.bin'), path.join(directory, 'outside.bin'));
  await fs.mkdir(path.join(directory, 'assets-other'));
  await fs.copyFile(fixture('positions.bin'), path.join(directory, 'assets-other', 'positions.bin'));
  for (const uri of ['../outside.bin', '%2e%2e/outside.bin', '../assets-other/positions.bin']) {
    const artifact = await externalAsset(assets, uri);
    const result = await run([artifact, '--resource-root', assets]);
    expectOutcome(result, 'unavailable', 2);
    assert.equal(result.report.resources[0].error.code, 'resource_outside_root');
    assert.equal(result.report.resources[0].sha256, undefined);
  }
});

test('realpath containment rejects escaping symlinks and accepts an in-root symlink', async (t) => {
  const { directory, assets } = await workspace(t);
  await fs.copyFile(fixture('positions.bin'), path.join(directory, 'outside.bin'));
  await fs.symlink(path.join(directory, 'outside.bin'), path.join(assets, 'escape.bin'));
  let artifact = await externalAsset(assets, 'escape.bin');
  const escape = await run([artifact, '--resource-root', assets]);
  expectOutcome(escape, 'unavailable', 2);
  assert.equal(escape.report.resources[0].error.code, 'resource_outside_root');
  await fs.symlink(path.join(assets, 'positions.bin'), path.join(assets, 'inside.bin'));
  artifact = await externalAsset(assets, 'inside.bin');
  const inside = await run([artifact, '--resource-root', assets]);
  expectOutcome(inside, 'supported', 0);
  assert.equal(inside.report.resources[0].path, await fs.realpath(path.join(assets, 'positions.bin')));
});

test('URI decoding preserves a permitted local filename', async (t) => {
  const { assets } = await workspace(t);
  await fs.copyFile(fixture('positions.bin'), path.join(assets, 'signal positions.bin'));
  const artifact = await externalAsset(assets, 'signal%20positions.bin');
  const result = await run([artifact, '--resource-root', assets]);
  expectOutcome(result, 'supported', 0);
  assert.equal(result.report.resources[0].bytes, 36);
});

test('unsupported extension coverage cannot become a pass through zero errors', async () => {
  const result = await run([fixture('unsupported-extension.gltf')]);
  expectOutcome(result, 'unavailable', 2);
  assert.equal(result.report.validator_report.issues.numErrors, 0);
  assert.ok(result.report.coverage_limits.some((issue) => issue.code === 'UNSUPPORTED_EXTENSION'));
  assert.equal(result.report.reason, 'validator_coverage_incomplete');
});

test('a report reopens as the full receipt and cannot overwrite an existing file or symlink', async (t) => {
  const { directory } = await workspace(t);
  const output = path.join(directory, 'report.json');
  const first = await run([fixture('empty.gltf'), '--output', output]);
  expectOutcome(first, 'supported', 0);
  assert.deepEqual(JSON.parse(await fs.readFile(output, 'utf8')), first.report);
  const original = await fs.readFile(output);
  const second = await run([fixture('signal-wedge.gltf'), '--output', output]);
  expectOutcome(second, 'unavailable', 2);
  assert.equal(second.report.stage, 'report_output');
  assert.equal(second.report.error.code, 'EEXIST');
  assert.deepEqual(await fs.readFile(output), original);
  const link = path.join(directory, 'report-link.json');
  await fs.symlink(output, link);
  expectOutcome(await run([fixture('camera.gltf'), '--output', link]), 'unavailable', 2);
  assert.deepEqual(await fs.readFile(output), original);
  assert.deepEqual((await fs.readdir(directory)).filter((name) => name.startsWith('.gltf-report-')), []);
});

test('a report may not use the input path, including a currently missing input', async (t) => {
  const { directory } = await workspace(t);
  const input = path.join(directory, 'input.gltf');
  await fs.copyFile(fixture('empty.gltf'), input);
  const original = await fs.readFile(input);
  const result = await run([input, '--output', input]);
  expectOutcome(result, 'unavailable', 2);
  assert.equal(result.report.error.code, 'output_is_input');
  assert.deepEqual(await fs.readFile(input), original);
  const absent = path.join(directory, 'absent.gltf');
  expectOutcome(await run([absent, '--output', absent]), 'unavailable', 2);
  await assert.rejects(fs.stat(absent), { code: 'ENOENT' });
});

test('competing writers publish one complete report without replacement', async (t) => {
  const { directory } = await workspace(t);
  const output = path.join(directory, 'shared-report.json');
  const results = await Promise.all([
    run([fixture('empty.gltf'), '--output', output]),
    run([fixture('camera.gltf'), '--output', output]),
  ]);
  assert.deepEqual(results.map((result) => result.code).sort(), [0, 2]);
  const winner = results.find((result) => result.code === 0);
  assert.deepEqual(JSON.parse(await fs.readFile(output, 'utf8')), winner.report);
});

test('missing inputs reached through directory aliases or dangling links remain absent', async (t) => {
  const { directory, assets } = await workspace(t);
  const alias = path.join(directory, 'alias');
  await fs.symlink(assets, alias, 'dir');
  const missing = path.join(assets, 'missing.gltf');
  const throughAlias = await run([path.join(alias, 'missing.gltf'), '--output', missing]);
  expectOutcome(throughAlias, 'unavailable', 2);
  assert.equal(throughAlias.report.error.code, 'output_is_input');
  await assert.rejects(fs.stat(missing), { code: 'ENOENT' });
  const dangling = path.join(directory, 'dangling.gltf');
  await fs.symlink(missing, dangling);
  const throughLink = await run([dangling, '--output', missing]);
  expectOutcome(throughLink, 'unavailable', 2);
  assert.equal(throughLink.report.error.code, 'output_is_input');
  await assert.rejects(fs.stat(missing), { code: 'ENOENT' });
  const separate = path.join(assets, 'receipt.json');
  const allowed = await run([path.join(alias, 'missing.gltf'), '--output', separate]);
  expectOutcome(allowed, 'unavailable', 2);
  assert.equal(allowed.report.stage, 'input');
  assert.deepEqual(JSON.parse(await fs.readFile(separate, 'utf8')), allowed.report);
  await assert.rejects(fs.stat(missing), { code: 'ENOENT' });
});

test('a missing adjacent dependency is unavailable and is not replaced by an ambient install', async (t) => {
  const { directory } = await workspace(t);
  for (const name of ['validate_gltf.cjs', 'package.json', 'package-lock.json']) {
    await fs.copyFile(path.join(path.dirname(cli), name), path.join(directory, name));
  }
  const isolatedCli = path.join(directory, 'validate_gltf.cjs');
  const result = await run([fixture('empty.gltf')], isolatedCli, {
    NODE_PATH: path.join(path.dirname(cli), 'node_modules'),
  });
  expectOutcome(result, 'unavailable', 2);
  assert.equal(result.report.stage, 'dependency');
  assert.equal(result.report.validator_report, null);
});
