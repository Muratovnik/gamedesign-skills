#!/usr/bin/env node
'use strict';

// Ink owns parsing, execution and save serialization. This adapter owns selected
// files, explicit actions, bounded observations and the identity of their handoff.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { parseArgs, isDeepStrictEqual, TextDecoder } = require('node:util');
const { Worker, isMainThread, parentPort, workerData } = require('node:worker_threads');

const COMPONENT = Object.freeze({
  name: 'inkjs', version: '2.4.0',
  npm_git_head: 'edccead8700e9f21be9825d87d8645d8c82a9936',
  bundle_sha256: '23d707b76e9b759a25803c193da8e32e04f727dd13a54ed1df8a6a59dd909b9e',
});
const MAX_FILE_BYTES = 8 * 1024 * 1024;
const DEFAULT_LIMITS = Object.freeze({ max_continue: 1000, max_output_chars: 100000 });
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const scalar = value => typeof value === 'boolean' || typeof value === 'string'
  || (typeof value === 'number' && Number.isFinite(value));

function fail(code, message) {
  const error = new Error(message);
  error.code = code;
  throw error;
}

function requireThat(condition, code, message) {
  if (!condition) fail(code, message);
}

function keys(value, required, optional, label) {
  requireThat(object(value), 'invalid_input', `${label} must be an object`);
  requireThat(required.every(key => own(value, key)), 'invalid_input', `${label} lacks a required field`);
  requireThat(Object.keys(value).every(key => required.includes(key) || optional.includes(key)),
    'invalid_input', `${label} has an unknown field`);
}

function boundedInteger(value, minimum, maximum, label) {
  requireThat(Number.isSafeInteger(value) && value >= minimum && value <= maximum,
    'invalid_input', `${label} must be an integer from ${minimum} through ${maximum}`);
}

function string(value, label) {
  requireThat(typeof value === 'string' && value.length > 0 && value.length <= 4096,
    'invalid_input', `${label} must be a nonempty string of at most 4096 characters`);
}

function parseJson(text, label) {
  try {
    return JSON.parse(text, (_key, value) => {
      if (typeof value === 'number' && !Number.isFinite(value)) throw new Error('Nonfinite number');
      return value;
    });
  } catch (error) {
    fail('invalid_json', `${label}: ${error.message}`);
  }
}

function decodeUtf8(bytes, label) {
  try {
    return new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    fail('invalid_utf8', `${label} must contain valid UTF-8`);
  }
}

function readFile(filename) {
  const descriptor = fs.openSync(filename, 'r');
  try {
    const stat = fs.fstatSync(descriptor);
    requireThat(stat.isFile() && stat.size <= MAX_FILE_BYTES, 'invalid_file',
      'Selected input must be a regular file of at most 8 MiB');
    const bytes = fs.readFileSync(descriptor);
    requireThat(bytes.length <= MAX_FILE_BYTES, 'invalid_file', 'Selected input exceeded 8 MiB');
    return bytes;
  } finally {
    fs.closeSync(descriptor);
  }
}

function writeNew(directory, name, bytes) {
  requireThat(Buffer.byteLength(bytes) <= MAX_FILE_BYTES, 'artifact_limit', 'Output exceeded 8 MiB');
  fs.writeFileSync(path.join(directory, name), bytes, { flag: 'wx' });
}

const jsonText = value => JSON.stringify(value, null, 2) + '\n';
const failure = error => ({ code: error.code || 'operation_failed', message: error.message });

function validateAction(action) {
  keys(action, [], ['choice', 'index'], 'action');
  requireThat(Object.keys(action).length === 1, 'invalid_input', 'Use exactly one choice text or index');
  if (own(action, 'choice')) string(action.choice, 'choice');
  else boundedInteger(action.index, 0, 100000, 'choice index');
}

function validateScenario(scenario) {
  keys(scenario, ['schema', 'id', 'observe_variables', 'actions', 'checks'], ['limits'], 'scenario');
  requireThat(scenario.schema === 'ink-scenario/1', 'invalid_input', 'Unsupported scenario schema');
  string(scenario.id, 'scenario id');
  requireThat(Array.isArray(scenario.observe_variables) && scenario.observe_variables.length <= 100,
    'invalid_input', 'observe_variables must contain at most 100 names');
  scenario.observe_variables.forEach(name => string(name, 'variable name'));
  requireThat(new Set(scenario.observe_variables).size === scenario.observe_variables.length,
    'invalid_input', 'Variable names must be unique');
  requireThat(Array.isArray(scenario.actions) && scenario.actions.length <= 1000,
    'invalid_input', 'actions must contain at most 1000 explicit choices');
  scenario.actions.forEach(validateAction);
  requireThat(Array.isArray(scenario.checks) && scenario.checks.length <= 1000,
    'invalid_input', 'checks must contain at most 1000 predicates');
  for (const check of scenario.checks) {
    requireThat(object(check), 'invalid_input', 'A check must be an object');
    switch (check.kind) {
      case 'choice':
        keys(check, ['kind', 'at', 'text', 'available'], [], 'choice check');
        string(check.text, 'choice check text');
        requireThat(typeof check.available === 'boolean', 'invalid_input', 'available must be boolean');
        break;
      case 'variable':
        keys(check, ['kind', 'at', 'name', 'equals'], [], 'variable check');
        requireThat(scenario.observe_variables.includes(check.name) && scalar(check.equals),
          'invalid_input', 'Variable check must select an observed scalar variable');
        break;
      case 'terminal':
        keys(check, ['kind', 'at', 'equals'], [], 'terminal check');
        requireThat(typeof check.equals === 'boolean', 'invalid_input', 'terminal equals must be boolean');
        break;
      case 'text':
        keys(check, ['kind', 'at', 'includes'], [], 'text check');
        string(check.includes, 'included text');
        break;
      case 'action_count':
        keys(check, ['kind', 'at_least'], [], 'action count check');
        boundedInteger(check.at_least, 1, 1000, 'minimum action count');
        break;
      default:
        fail('invalid_input', 'Unsupported check kind');
    }
    if (own(check, 'at')) boundedInteger(check.at, 0, scenario.actions.length, 'observation index');
  }
  if (own(scenario, 'limits')) {
    keys(scenario.limits, [], ['max_continue', 'max_output_chars'], 'limits');
    if (own(scenario.limits, 'max_continue'))
      boundedInteger(scenario.limits.max_continue, 1, 100000, 'max_continue');
    if (own(scenario.limits, 'max_output_chars'))
      boundedInteger(scenario.limits.max_output_chars, 1, 1000000, 'max_output_chars');
  }
  return { ...DEFAULT_LIMITS, ...scenario.limits };
}

function validateCompiled(text) {
  const compiled = parseJson(text, 'compiled story');
  requireThat(object(compiled) && compiled.inkVersion === 21 && Array.isArray(compiled.root),
    'unsupported_compiled_story', 'This route qualifies Ink JSON format 21 with a native root container');
}

function checkComponent(component) {
  requireThat(object(component) && Object.keys(COMPONENT).every(key => component[key] === COMPONENT[key]),
    'component_mismatch', 'Artifact does not match the qualified inkjs 2.4.0 bundle');
}

function dependencyBundle(root) {
  const manifest = parseJson(decodeUtf8(readFile(path.join(root, 'package.json')), 'inkjs package'), 'inkjs package');
  requireThat(manifest.name === COMPONENT.name && manifest.version === COMPONENT.version,
    'component_mismatch', 'Select the pinned inkjs 2.4.0 package root');
  const bundle = path.resolve(root, 'dist/ink-full.js');
  requireThat(sha256(readFile(bundle)) === COMPONENT.bundle_sha256, 'component_mismatch',
    'inkjs compiler/runtime bytes differ from the qualified npm bundle');
  return bundle;
}

function selectChoice(choices, action) {
  if (own(action, 'index')) {
    requireThat(action.index < choices.length, 'choice_unavailable', 'Requested choice index is not available');
    return choices[action.index];
  }
  const matches = choices.filter(choice => choice.text === action.choice);
  requireThat(matches.length !== 0, 'choice_unavailable', 'Requested choice text is not available');
  requireThat(matches.length === 1, 'choice_ambiguous', 'Choice text is ambiguous; supply its current index');
  return matches[0];
}

function checkpoint(observation) {
  return { choices: observation.choices, variables: observation.variables, terminal: observation.terminal };
}

function validateState(state, compiledSha256) {
  keys(state, ['schema', 'component', 'compiled_sha256', 'native_state_json', 'native_state_sha256',
    'observe_variables', 'checkpoint', 'saved_from'], [], 'state envelope');
  requireThat(state.schema === 'ink-state/1', 'invalid_input', 'Unsupported state schema');
  checkComponent(state.component);
  requireThat(state.compiled_sha256 === compiledSha256, 'state_story_mismatch',
    'Saved state belongs to different compiled story bytes');
  requireThat(typeof state.native_state_json === 'string'
    && sha256(state.native_state_json) === state.native_state_sha256,
  'state_checksum_mismatch', 'Native state checksum does not match its envelope');
  parseJson(state.native_state_json, 'native Ink state');
  requireThat(Array.isArray(state.observe_variables) && state.observe_variables.length <= 100
    && new Set(state.observe_variables).size === state.observe_variables.length,
  'invalid_input', 'Invalid saved variable selection');
  state.observe_variables.forEach(name => string(name, 'saved variable name'));
  requireThat(object(state.checkpoint), 'invalid_input', 'Missing saved checkpoint');
}

function executeNative(request) {
  const diagnostics = [];
  const observations = [];
  const actions = [];
  const result = { diagnostics, observations, actions };
  try {
    // Only this verified, bundled dependency is loaded. Ink receives no host
    // bindings or file resolver; the worker is a deadline boundary, not a sandbox.
    const { Compiler, Story } = require(request.bundle);
    const capture = (stage, message, type) => diagnostics.push({ stage,
      severity: type === 2 ? 'error' : type === 1 ? 'warning' : 'author', message });
    if (request.operation === 'compile') {
      let includeRequested = false;
      const denyInclude = () => {
        includeRequested = true;
        throw new Error('INCLUDE is unavailable in the single-file artifact route');
      };
      const compiler = new Compiler(request.source, {
        sourceFilename: null, pluginNames: [], countAllVisits: false,
        errorHandler: (message, type) => capture('compiler', message, type),
        fileHandler: { ResolveInkFilename: denyInclude, LoadInkFileContents: denyInclude },
      });
      let story;
      try { story = compiler.Compile(); }
      catch (error) {
        fail(includeRequested ? 'include_unavailable' : 'compiler_error', error.message);
      }
      requireThat(!includeRequested, 'include_unavailable', 'INCLUDE is unavailable in this route');
      requireThat(!diagnostics.some(item => item.severity === 'error'), 'compiler_error',
        'Ink compiler reported an error');
      result.compiled = story.ToJson();
      validateCompiled(result.compiled);
      result.status = 'compiled';
      return result;
    }

    const story = new Story(request.compiled);
    story.onError = (message, type) => capture('runtime', message, type);
    story.allowExternalFunctionFallbacks = false;
    try { story.ValidateExternalBindings(); }
    catch (error) { fail('external_functions_unavailable', error.message); }
    requireThat(!diagnostics.some(item => item.severity === 'error'), 'external_functions_unavailable',
      'Ink requested an external function; this route binds none');

    let continuationCount = 0;
    let outputChars = 0;
    let transcriptBytes = 0;
    const checkErrors = () => requireThat(!diagnostics.some(item => item.severity === 'error'),
      'runtime_error', 'Ink runtime reported an error; inspect diagnostics');
    const snapshot = names => {
      const variables = Object.fromEntries(names.map(name => {
        requireThat(story.variablesState.GlobalVariableExistsWithName(name), 'variable_unavailable',
          `Selected global variable is not declared: ${name}`);
        const value = story.variablesState.$(name);
        requireThat(scalar(value), 'variable_unavailable',
          `Selected variable is not a boolean, finite number or string: ${name}`);
        return [name, value];
      }));
      const choices = story.currentChoices.map(choice => ({ index: choice.index,
        text: choice.text, tags: choice.tags || [] }));
      return { choices, variables, terminal: !story.canContinue && choices.length === 0 };
    };
    const observe = step => {
      const output = [];
      while (story.canContinue) {
        requireThat(continuationCount < request.limits.max_continue, 'continuation_limit',
          'Continuation budget exhausted before a choice or ending');
        continuationCount++;
        const text = story.Continue();
        checkErrors();
        const tags = story.currentTags || [];
        outputChars += text.length + tags.reduce((sum, tag) => sum + tag.length, 0);
        requireThat(outputChars <= request.limits.max_output_chars, 'output_limit',
          'Runtime text/tag budget exhausted');
        output.push({ text, tags });
      }
      const observation = { step, output, ...snapshot(request.scenario.observe_variables) };
      transcriptBytes += Buffer.byteLength(jsonText(observation));
      requireThat(transcriptBytes <= 2 * 1024 * 1024, 'transcript_limit',
        'Observation transcript exceeded 2 MiB');
      observations.push(observation);
      return observation;
    };

    if (request.state) {
      story.state.LoadJson(request.state.native_state_json);
      checkErrors();
      requireThat(!story.canContinue, 'state_checkpoint_mismatch', 'Saved state is not at a completed observation');
      requireThat(isDeepStrictEqual(snapshot(request.state.observe_variables), request.state.checkpoint),
        'state_checkpoint_mismatch',
      'Fresh Ink runtime did not restore the recorded choices, variables and ending state');
    }
    let observation = observe(0);
    for (const [position, action] of request.scenario.actions.entries()) {
      const selected = selectChoice(observation.choices, action);
      story.ChooseChoiceIndex(selected.index);
      checkErrors();
      actions.push({ sequence: position + 1, requested: action,
        selected: { index: selected.index, text: selected.text } });
      observation = observe(position + 1);
    }
    result.native_state_json = story.state.ToJson();
    checkErrors();
    result.continuation_count = continuationCount;
    result.output_chars = outputChars;
    result.status = 'executed';
  } catch (error) {
    result.status = 'unavailable';
    result.failure = failure(error);
  }
  return result;
}

async function nativeWorker(request, timeoutMs) {
  const worker = new Worker(__filename, { workerData: request,
    resourceLimits: { maxOldGenerationSizeMb: 128 } });
  let timer;
  try {
    return await new Promise((resolve, reject) => {
      timer = setTimeout(() => reject(Object.assign(new Error('Ink operation exceeded its deadline'),
        { code: 'deadline_exceeded' })), timeoutMs);
      worker.once('message', resolve);
      worker.once('error', reject);
      worker.once('exit', code => reject(Object.assign(new Error(`Ink worker exited without a result (${code})`),
        { code: 'worker_unavailable' })));
    });
  } finally {
    clearTimeout(timer);
    await worker.terminate();
  }
}

function validateReport(report, scenario, compiledSha256, scenarioSha256, adapterSha256) {
  requireThat(object(report) && report.schema === 'ink-run/1' && report.status === 'executed',
    'incomplete_run', 'Assessment requires a completed Ink run');
  checkComponent(report.component);
  requireThat(report.compiled_sha256 === compiledSha256 && report.scenario_sha256 === scenarioSha256
    && report.adapter_sha256 === adapterSha256, 'report_identity_mismatch',
  'Report does not match the selected compiled story, scenario and adapter bytes');
  requireThat(Array.isArray(report.diagnostics)
    && report.diagnostics.every(item => object(item) && ['author', 'warning'].includes(item.severity)),
  'incomplete_run', 'Report contains invalid diagnostics or runtime errors');
  requireThat(Array.isArray(report.observations) && report.observations.length === scenario.actions.length + 1
    && Array.isArray(report.actions) && report.actions.length === scenario.actions.length,
  'incomplete_run', 'Report does not cover the complete explicit action sequence');
  for (const [step, observation] of report.observations.entries()) {
    requireThat(object(observation) && observation.step === step && Array.isArray(observation.output)
      && observation.output.every(chunk => object(chunk) && typeof chunk.text === 'string'
        && Array.isArray(chunk.tags) && chunk.tags.every(tag => typeof tag === 'string'))
      && Array.isArray(observation.choices) && observation.choices.every((choice, index) => object(choice)
        && choice.index === index && typeof choice.text === 'string' && Array.isArray(choice.tags)
        && choice.tags.every(tag => typeof tag === 'string'))
      && object(observation.variables)
      && Object.keys(observation.variables).length === scenario.observe_variables.length
      && scenario.observe_variables.every(name => own(observation.variables, name) && scalar(observation.variables[name]))
      && observation.terminal === (observation.choices.length === 0),
    'invalid_report', 'Malformed or incomplete runtime observation');
  }
  for (const [position, action] of scenario.actions.entries()) {
    const recorded = report.actions[position];
    const selected = selectChoice(report.observations[position].choices, action);
    requireThat(object(recorded) && recorded.sequence === position + 1
      && JSON.stringify(recorded.requested) === JSON.stringify(action)
      && object(recorded.selected) && recorded.selected.index === selected.index && recorded.selected.text === selected.text,
    'invalid_report', 'Reported action does not match an offered, explicitly requested choice');
  }
}

function assess(report, scenario) {
  requireThat(scenario.checks.length > 0, 'no_checks', 'No property was selected for assessment');
  const checks = scenario.checks.map((check, index) => {
    const observation = report.observations[check.at];
    let actual;
    let supported;
    switch (check.kind) {
      case 'choice':
        actual = observation.choices.filter(choice => choice.text === check.text).length;
        supported = (actual > 0) === check.available;
        break;
      case 'variable':
        actual = observation.variables[check.name];
        supported = actual === check.equals;
        break;
      case 'terminal':
        actual = observation.terminal;
        supported = actual === check.equals;
        break;
      case 'text':
        actual = observation.output.map(chunk => chunk.text).join('');
        supported = actual.includes(check.includes);
        break;
      case 'action_count':
        actual = report.actions.length;
        supported = actual >= check.at_least;
        break;
    }
    return { index, check, outcome: supported ? 'supported' : 'refuted', actual };
  });
  return { outcome: checks.every(check => check.outcome === 'supported') ? 'supported' : 'refuted', checks };
}

const USAGE = `Optional Ink artifact route (Node; exact external inkjs 2.4.0).
  compile --source FILE.ink --inkjs-root PACKAGE_DIR --out NEW_DIR
  run --compiled FILE.json --scenario PLAN.json --inkjs-root PACKAGE_DIR --out NEW_DIR
  resume --compiled FILE.json --state STATE.json --scenario PLAN.json --inkjs-root PACKAGE_DIR --out NEW_DIR
  assess --compiled FILE.json --scenario PLAN.json --report REPORT.json [--out NEW_DIR]
Native commands accept --timeout-ms 1..30000 (default 5000).
run/resume save native state and a bounded transcript; they do not choose actions.
Exit: native operation 0 completed / 2 unavailable; assess 0 supported / 1 refuted / 2 unavailable.
Every output directory must be new and have an existing parent. No outputs are overwritten.
`;

async function main() {
  let directory;
  let operation;
  let report;
  let reportName = 'failure.json';
  try {
    const options = Object.fromEntries(['source', 'compiled', 'scenario', 'state', 'report', 'out',
      'inkjs-root', 'timeout-ms'].map(name => [name, { type: 'string' }]));
    options.help = { type: 'boolean' };
    const parsed = parseArgs({ options, allowPositionals: true, strict: true });
    if (parsed.values.help) { process.stdout.write(USAGE); return 0; }
    requireThat(parsed.positionals.length === 1, 'invalid_input', 'Select one command; see --help');
    operation = parsed.positionals[0];
    requireThat(['compile', 'run', 'resume', 'assess'].includes(operation), 'invalid_input', 'Unknown command');
    const values = parsed.values;
    const required = operation === 'compile' ? ['source', 'inkjs-root', 'out']
      : operation === 'assess' ? ['compiled', 'scenario', 'report']
        : ['compiled', 'scenario', 'inkjs-root', 'out', ...(operation === 'resume' ? ['state'] : [])];
    const allowed = [...required, 'out', ...(operation !== 'assess' ? ['timeout-ms'] : [])];
    requireThat(required.every(key => values[key]) && Object.keys(values).every(key => allowed.includes(key)),
      'invalid_input', 'Missing or inapplicable command option; see --help');
    const timeoutMs = values['timeout-ms'] === undefined ? 5000 : Number(values['timeout-ms']);
    boundedInteger(timeoutMs, 1, 30000, 'timeout-ms');
    const adapterSha256 = sha256(readFile(__filename));
    if (values.out) {
      // Claim one fresh directory before writing. An existing file, directory or
      // symlink is a collision, including one left by an interrupted earlier run.
      const selected = path.resolve(values.out);
      fs.mkdirSync(selected);
      directory = selected;
    }
    reportName = operation === 'compile' ? 'receipt.json' : operation === 'assess' ? 'assessment.json' : 'report.json';
    report = { schema: operation === 'compile' ? 'ink-compile/1' : operation === 'assess' ? 'ink-assessment/1' : 'ink-run/1',
      operation, status: 'unavailable', run_id: crypto.randomUUID(), component: COMPONENT,
      adapter_sha256: adapterSha256, node: process.version };
    if (operation === 'compile') {
      const source = readFile(values.source);
      const sourceText = decodeUtf8(source, 'Ink source');
      report.source_sha256 = sha256(source);
      writeNew(directory, 'source.ink', source);
      const result = await nativeWorker({ operation, source: sourceText,
        bundle: dependencyBundle(values['inkjs-root']) }, timeoutMs);
      Object.assign(report, result);
      delete report.compiled;
      if (result.status === 'compiled') {
        writeNew(directory, 'story.json', result.compiled);
        // Consumer identity is computed from the saved artifact, not a guessed
        // compiler return value; later run/resume processes reopen this file.
        report.compiled_sha256 = sha256(readFile(path.join(directory, 'story.json')));
      }
    } else {
      const compiled = readFile(values.compiled);
      const compiledText = decodeUtf8(compiled, 'compiled story');
      validateCompiled(compiledText);
      const scenarioBytes = readFile(values.scenario);
      const scenario = parseJson(decodeUtf8(scenarioBytes, 'scenario'), 'scenario');
      const limits = validateScenario(scenario);
      report.compiled_sha256 = sha256(compiled);
      report.scenario_sha256 = sha256(scenarioBytes);
      if (operation === 'assess') {
        const reportBytes = readFile(values.report);
        const runReport = parseJson(decodeUtf8(reportBytes, 'run report'), 'run report');
        report.report_sha256 = sha256(reportBytes);
        validateReport(runReport, scenario, report.compiled_sha256, report.scenario_sha256, adapterSha256);
        Object.assign(report, assess(runReport, scenario), { status: 'assessed', inspected_run_id: runReport.run_id });
      } else {
        writeNew(directory, 'story.json', compiled);
        writeNew(directory, 'scenario.json', scenarioBytes);
        let state;
        report.input_state_sha256 = null;
        if (operation === 'resume') {
          const stateBytes = readFile(values.state);
          report.input_state_sha256 = sha256(stateBytes);
          state = parseJson(decodeUtf8(stateBytes, 'saved state envelope'), 'saved state envelope');
          validateState(state, report.compiled_sha256);
          writeNew(directory, 'input-state.json', stateBytes);
        }
        const result = await nativeWorker({ operation, compiled: compiledText, scenario,
          limits, state, bundle: dependencyBundle(values['inkjs-root']) }, timeoutMs);
        Object.assign(report, result, { limits, timeout_ms: timeoutMs });
        delete report.native_state_json;
        if (result.status === 'executed') {
          const last = result.observations.at(-1);
          const saved = { schema: 'ink-state/1', component: COMPONENT, compiled_sha256: report.compiled_sha256,
            native_state_json: result.native_state_json, native_state_sha256: sha256(result.native_state_json),
            observe_variables: scenario.observe_variables, checkpoint: checkpoint(last),
            saved_from: { run_id: report.run_id, scenario_sha256: report.scenario_sha256, step: last.step } };
          const stateText = jsonText(saved);
          report.output_state_sha256 = sha256(stateText);
          requireThat(Buffer.byteLength(stateText) <= MAX_FILE_BYTES
            && Buffer.byteLength(jsonText(report)) <= MAX_FILE_BYTES, 'artifact_limit',
          'State or report exceeded 8 MiB');
          writeNew(directory, 'state.json', stateText);
        }
      }
    }
    if (directory) writeNew(directory, reportName, jsonText(report));
    process.stdout.write(jsonText(report));
    return report.status === 'unavailable' ? 2 : report.outcome === 'refuted' ? 1 : 0;
  } catch (error) {
    const unavailable = { ...report, schema: report?.schema || 'ink-operation/1', operation,
      status: 'unavailable', outcome: 'unavailable', failure: failure(error) };
    if (directory) {
      try { writeNew(directory, reportName, jsonText(unavailable)); }
      catch (writeError) { unavailable.report_write_failure = failure(writeError); }
    }
    process.stdout.write(jsonText(unavailable));
    return 2;
  }
}

if (!isMainThread) parentPort.postMessage(executeNative(workerData));
else if (require.main === module) main().then(code => { process.exitCode = code; });
