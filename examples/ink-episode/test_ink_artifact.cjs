'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');

const adapter = path.resolve(__dirname,
  '../../skills/game-world-narrative-design/scripts/ink_artifact.cjs');
const fixtures = path.join(__dirname, 'fixtures');
const inkjsRoot = process.env.INKJS_ROOT;
assert.ok(inkjsRoot, 'Set INKJS_ROOT to the isolated, pinned inkjs 2.4.0 package; missing runtime is not a skipped pass');
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));

function workspace(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'ink-artifact-test-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  return directory;
}

function cli(command, args, expectedCode = 0) {
  const result = spawnSync(process.execPath, [adapter, command, ...args], {
    encoding: 'utf8', timeout: 12000, maxBuffer: 10 * 1024 * 1024,
  });
  assert.ifError(result.error);
  assert.equal(result.status, expectedCode, result.stdout + result.stderr);
  assert.equal(result.stderr, '');
  return JSON.parse(result.stdout);
}

function compile(directory, name, source = path.join(fixtures, 'listening-room.ink'), code = 0) {
  const out = path.join(directory, name);
  const receipt = cli('compile', ['--source', source, '--inkjs-root', inkjsRoot, '--out', out], code);
  return { out, receipt, compiled: path.join(out, 'story.json') };
}

function run(directory, name, compiled, scenario, options = {}) {
  const out = path.join(directory, name);
  const args = ['--compiled', compiled, '--scenario', scenario, '--inkjs-root', inkjsRoot, '--out', out];
  if (options.state) args.push('--state', options.state);
  if (options.timeout) args.push('--timeout-ms', String(options.timeout));
  const report = cli(options.state ? 'resume' : 'run', args, options.code ?? 0);
  return { out, report, reportPath: path.join(out, 'report.json'), state: path.join(out, 'state.json') };
}

function assessment(compiled, scenario, reportPath, code = 0) {
  return cli('assess', ['--compiled', compiled, '--scenario', scenario, '--report', reportPath], code);
}

function write(directory, name, value) {
  const file = path.join(directory, name);
  fs.writeFileSync(file, typeof value === 'string' ? value : JSON.stringify(value));
  return file;
}

function scenario(directory, name, overrides = {}) {
  return write(directory, name + '.json', { schema: 'ink-scenario/1', id: name,
    observe_variables: [], actions: [], checks: [], ...overrides });
}

function corruptUtf8(directory, name, bytes) {
  const marker = Buffer.from('�');
  const index = bytes.indexOf(marker);
  assert.notEqual(index, -1, 'The fixture must contain a real replacement character');
  const malformed = Buffer.concat([bytes.subarray(0, index), Buffer.from([0xff]),
    bytes.subarray(index + marker.length)]);
  const filename = path.join(directory, name);
  fs.writeFileSync(filename, malformed);
  return filename;
}

test('malformed UTF-8 cannot become supported evidence; real Unicode remains valid', t => {
  const directory = workspace(t);
  const text = 'Привет � 🎵';
  const source = write(directory, 'unicode.ink', text + '\n-> END\n');
  const built = compile(directory, 'compiled', source);
  const plan = scenario(directory, 'unicode-�', {
    checks: [{ kind: 'text', at: 0, includes: text }],
  });
  const executed = run(directory, 'executed', built.compiled, plan);
  assert.equal(assessment(built.compiled, plan, executed.reportPath).outcome, 'supported');

  const malformedReport = corruptUtf8(directory, 'bad-report.json', fs.readFileSync(executed.reportPath));
  assert.equal(assessment(built.compiled, plan, malformedReport, 2).failure.code, 'invalid_utf8');

  const malformedPlan = corruptUtf8(directory, 'bad-scenario.json', fs.readFileSync(plan));
  const linkedReport = read(executed.reportPath);
  linkedReport.scenario_sha256 = digest(fs.readFileSync(malformedPlan));
  const relinked = write(directory, 'relinked-report.json', linkedReport);
  assert.equal(assessment(built.compiled, malformedPlan, relinked, 2).failure.code, 'invalid_utf8');

  const malformedCompiled = corruptUtf8(directory, 'bad-story.json', fs.readFileSync(built.compiled));
  linkedReport.compiled_sha256 = digest(fs.readFileSync(malformedCompiled));
  linkedReport.scenario_sha256 = digest(fs.readFileSync(plan));
  const compiledReport = write(directory, 'compiled-report.json', linkedReport);
  assert.equal(assessment(malformedCompiled, plan, compiledReport, 2).failure.code, 'invalid_utf8');
});

test('compile, run, resume and dependency metadata reject malformed UTF-8 without success artifacts', t => {
  const directory = workspace(t);
  const source = write(directory, 'unicode.ink', 'Hello �\n* [Continue �]\nDone.\n-> END\n');
  const built = compile(directory, 'compiled', source);
  const plan = scenario(directory, 'pause-�');
  const executed = run(directory, 'executed', built.compiled, plan);
  const resumed = run(directory, 'resumed', built.compiled, plan, { state: executed.state });
  assert.equal(resumed.report.status, 'executed');

  const badSource = corruptUtf8(directory, 'bad.ink', fs.readFileSync(source));
  const rejectedSource = compile(directory, 'bad-source', badSource, 2);
  assert.equal(rejectedSource.receipt.failure.code, 'invalid_utf8');
  assert.equal(fs.existsSync(rejectedSource.compiled), false);

  for (const [name, compiled, selectedPlan, state] of [
    ['compiled', corruptUtf8(directory, 'bad-compiled.json', fs.readFileSync(built.compiled)), plan, null],
    ['scenario', built.compiled, corruptUtf8(directory, 'bad-plan.json', fs.readFileSync(plan)), null],
    ['state', built.compiled, plan, corruptUtf8(directory, 'bad-state.json', fs.readFileSync(executed.state))],
  ]) {
    const rejected = run(directory, 'bad-' + name, compiled, selectedPlan, { state, code: 2 });
    assert.equal(rejected.report.failure.code, 'invalid_utf8');
    assert.equal(fs.existsSync(rejected.state), false);
    assert.equal(rejected.report.status, 'unavailable');
  }

  const dependency = path.join(directory, 'dependency');
  fs.mkdirSync(dependency);
  const manifest = { name: 'inkjs', version: '2.4.0', description: 'Valid �' };
  const validManifest = write(dependency, 'package.json', manifest);
  fs.mkdirSync(path.join(dependency, 'dist'));
  fs.copyFileSync(path.join(inkjsRoot, 'dist/ink-full.js'), path.join(dependency, 'dist/ink-full.js'));
  const validOut = path.join(directory, 'valid-dependency');
  assert.equal(cli('compile', ['--source', source, '--inkjs-root', dependency, '--out', validOut]).status,
    'compiled');
  const malformedManifest = corruptUtf8(directory, 'bad-package.json', fs.readFileSync(validManifest));
  fs.copyFileSync(malformedManifest, validManifest);
  const badOut = path.join(directory, 'bad-dependency');
  const rejected = cli('compile', ['--source', source, '--inkjs-root', dependency, '--out', badOut], 2);
  assert.equal(rejected.failure.code, 'invalid_utf8');
  assert.equal(fs.existsSync(path.join(badOut, 'story.json')), false);
});

test('real Ink source → saved JSON → explicit choice → native state → fresh resume → consequence', t => {
  const directory = workspace(t);
  const built = compile(directory, 'compiled');
  assert.equal(built.receipt.status, 'compiled');
  assert.equal(built.receipt.component.version, '2.4.0');
  assert.equal(built.receipt.compiled_sha256, digest(fs.readFileSync(built.compiled)));
  assert.equal(read(built.compiled).inkVersion, 21);
  assert.deepEqual(built.receipt.diagnostics, []);

  const inspectPlan = path.join(fixtures, 'inspect.json');
  const inspected = run(directory, 'inspected', built.compiled, inspectPlan);
  assert.equal(assessment(built.compiled, inspectPlan, inspected.reportPath).outcome, 'supported');
  assert.deepEqual(inspected.report.observations[0].choices.map(choice => choice.text),
    ['Hear the introduction', 'Leave the room']);
  assert.deepEqual(inspected.report.observations[1].choices.map(choice => choice.text),
    ['Share the excerpt', 'Leave the room']);
  const saved = read(inspected.state);
  assert.equal(saved.compiled_sha256, built.receipt.compiled_sha256);
  assert.equal(saved.component.version, '2.4.0');
  assert.equal(saved.native_state_sha256, digest(saved.native_state_json));
  assert.ok(read(inspected.state).native_state_json.includes('inkSaveVersion'));

  const sharePlan = path.join(fixtures, 'resume-share.json');
  const shared = run(directory, 'shared', built.compiled, sharePlan, { state: inspected.state });
  assert.equal(assessment(built.compiled, sharePlan, shared.reportPath).outcome, 'supported');
  assert.equal(shared.report.input_state_sha256, digest(fs.readFileSync(inspected.state)));
  assert.deepEqual(shared.report.observations[0].choices, saved.checkpoint.choices);
  assert.deepEqual(shared.report.observations[0].variables, { disclosure_heard: true, excerpt_shared: false });
  assert.deepEqual(shared.report.observations[1].variables, { disclosure_heard: true, excerpt_shared: true });
  assert.equal(shared.report.observations[1].terminal, true);
  assert.equal(shared.report.actions[0].selected.text, 'Share the excerpt');

  // JSON member order is not a story-state change. Leave stays available after
  // the disclosure as well as before it; a saved choice is not a forced branch.
  const reorderedState = read(inspected.state);
  const { choices, variables, terminal } = reorderedState.checkpoint;
  reorderedState.checkpoint = { terminal, variables, choices };
  const reordered = write(directory, 'reordered-state.json', reorderedState);
  const leaveAfterPlan = scenario(directory, 'leave-after-disclosure', {
    observe_variables: ['disclosure_heard', 'excerpt_shared'], actions: [{ choice: 'Leave the room' }],
    checks: [{ kind: 'terminal', at: 1, equals: true },
      { kind: 'variable', at: 1, name: 'disclosure_heard', equals: true },
      { kind: 'variable', at: 1, name: 'excerpt_shared', equals: false }],
  });
  const leftAfter = run(directory, 'left-after', built.compiled, leaveAfterPlan, { state: reordered });
  assert.equal(assessment(built.compiled, leaveAfterPlan, leftAfter.reportPath).outcome, 'supported');
});

test('the same guard property refutes a runnable missing-guard mutant, while departure remains legitimate', t => {
  const directory = workspace(t);
  const source = fs.readFileSync(path.join(fixtures, 'listening-room.ink'), 'utf8');
  const mutantSource = source.replace('* {disclosure_heard} [Share the excerpt]', '* [Share the excerpt]');
  assert.notEqual(mutantSource, source);
  const mutant = compile(directory, 'mutant', write(directory, 'missing-guard.ink', mutantSource));
  const inspectPlan = path.join(fixtures, 'inspect.json');
  const inspected = run(directory, 'inspected-mutant', mutant.compiled, inspectPlan);
  assert.equal(inspected.report.status, 'executed');
  const assessed = assessment(mutant.compiled, inspectPlan, inspected.reportPath, 1);
  assert.equal(assessed.outcome, 'refuted');
  assert.deepEqual(assessed.checks.filter(check => check.outcome === 'refuted').map(check => check.index), [0]);

  const built = compile(directory, 'original');
  const leavePlan = path.join(fixtures, 'leave.json');
  const left = run(directory, 'left', built.compiled, leavePlan);
  assert.equal(assessment(built.compiled, leavePlan, left.reportPath).outcome, 'supported');
  assert.equal(left.report.observations.at(-1).terminal, true);
  assert.deepEqual(left.report.observations.at(-1).variables, { disclosure_heard: false, excerpt_shared: false });
});

test('a legal no-choice ending succeeds, but proves neither a required action nor an empty check set', t => {
  const directory = workspace(t);
  const built = compile(directory, 'closed', path.join(fixtures, 'closed-room.ink'));
  const terminalPlan = path.join(fixtures, 'terminal.json');
  const ended = run(directory, 'ended', built.compiled, terminalPlan);
  assert.equal(ended.report.actions.length, 0);
  assert.equal(ended.report.observations[0].terminal, true);
  assert.equal(assessment(built.compiled, terminalPlan, ended.reportPath).outcome, 'supported');
  const requiredPlan = scenario(directory, 'required-action', {
    checks: [{ kind: 'action_count', at_least: 1 }],
  });
  const noAction = run(directory, 'no-action', built.compiled, requiredPlan);
  assert.equal(assessment(built.compiled, requiredPlan, noAction.reportPath, 1).outcome, 'refuted');
  const noChecksPlan = scenario(directory, 'no-checks');
  const noChecks = run(directory, 'no-checks-run', built.compiled, noChecksPlan);
  assert.equal(assessment(built.compiled, noChecksPlan, noChecks.reportPath, 2).failure.code, 'no_checks');
  const extraActionPlan = scenario(directory, 'action-after-ending', { actions: [{ index: 0 }] });
  assert.equal(run(directory, 'extra-action', built.compiled, extraActionPlan, { code: 2 }).report.failure.code,
    'choice_unavailable');
});

test('different compiled bytes, dependency identity or altered native state cannot silently resume', t => {
  const directory = workspace(t);
  const built = compile(directory, 'original');
  const inspectPlan = path.join(fixtures, 'inspect.json');
  const inspected = run(directory, 'inspected', built.compiled, inspectPlan);
  const sharePlan = path.join(fixtures, 'resume-share.json');
  const closed = compile(directory, 'closed', path.join(fixtures, 'closed-room.ink'));
  assert.equal(run(directory, 'stale-story', closed.compiled, sharePlan,
    { state: inspected.state, code: 2 }).report.failure.code, 'state_story_mismatch');
  const versionState = read(inspected.state);
  versionState.component.version = '2.3.0';
  const wrongVersion = write(directory, 'wrong-version.json', versionState);
  assert.equal(run(directory, 'stale-version', built.compiled, sharePlan,
    { state: wrongVersion, code: 2 }).report.failure.code, 'component_mismatch');
  const checksumState = read(inspected.state);
  checksumState.native_state_json += ' ';
  const altered = write(directory, 'altered.json', checksumState);
  assert.equal(run(directory, 'bad-checksum', built.compiled, sharePlan,
    { state: altered, code: 2 }).report.failure.code, 'state_checksum_mismatch');
  const checkpointState = read(inspected.state);
  checkpointState.checkpoint.variables.disclosure_heard = false;
  const falseCheckpoint = write(directory, 'false-checkpoint.json', checkpointState);
  assert.equal(run(directory, 'bad-checkpoint', built.compiled, sharePlan,
    { state: falseCheckpoint, code: 2 }).report.failure.code, 'state_checkpoint_mismatch');
});

test('ambiguous labels require a current index; unavailable and malformed indices never select a fallback', t => {
  const directory = workspace(t);
  const source = '* [Listen]\nFirst voice.\n-> END\n* [Listen]\nSecond voice.\n-> END\n';
  const built = compile(directory, 'ambiguous', write(directory, 'ambiguous.ink', source));
  const textPlan = scenario(directory, 'ambiguous-text', { actions: [{ choice: 'Listen' }] });
  assert.equal(run(directory, 'ambiguous-run', built.compiled, textPlan, { code: 2 }).report.failure.code,
    'choice_ambiguous');
  const indexPlan = scenario(directory, 'second-voice', { actions: [{ index: 1 }],
    checks: [{ kind: 'text', at: 1, includes: 'Second voice.' }] });
  const selected = run(directory, 'index-run', built.compiled, indexPlan);
  assert.equal(assessment(built.compiled, indexPlan, selected.reportPath).outcome, 'supported');
  const missingPlan = scenario(directory, 'index-absent', { actions: [{ index: 2 }] });
  assert.equal(run(directory, 'out-of-range', built.compiled, missingPlan, { code: 2 }).report.failure.code,
    'choice_unavailable');
  for (const [name, index] of [['negative', -1], ['fractional', 0.5]]) {
    const plan = scenario(directory, name, { actions: [{ index }] });
    assert.equal(run(directory, name + '-run', built.compiled, plan, { code: 2 }).report.failure.code,
      'invalid_input');
  }
});

test('compiler and native runtime failures stay unavailable; INCLUDE and host calls have no resolver or binding', t => {
  const directory = workspace(t);
  const invalid = compile(directory, 'invalid', write(directory, 'invalid.ink', 'VAR broken =\n-> END\n'), 2);
  assert.equal(invalid.receipt.failure.code, 'compiler_error');
  assert.ok(invalid.receipt.diagnostics.some(item => item.severity === 'error'));
  assert.equal(fs.existsSync(invalid.compiled), false);
  const sentinel = write(directory, 'private-text.ink', 'PRIVATE_SENTINEL_MUST_NOT_BE_COMPILED\n-> END\n');
  const include = compile(directory, 'include', write(directory, 'include.ink', `INCLUDE ${sentinel}\n`), 2);
  assert.equal(include.receipt.failure.code, 'include_unavailable');
  assert.equal(JSON.stringify(include.receipt).includes('PRIVATE_SENTINEL'), false);
  assert.equal(fs.existsSync(include.compiled), false);
  const host = compile(directory, 'host', write(directory, 'host.ink',
    'EXTERNAL host_read()\n{host_read()}\n-> END\n'));
  const emptyPlan = scenario(directory, 'empty');
  const hostRun = run(directory, 'host-run', host.compiled, emptyPlan, { code: 2 });
  assert.equal(hostRun.report.failure.code, 'external_functions_unavailable');
  assert.equal(fs.existsSync(hostRun.state), false);

  const badRuntime = compile(directory, 'bad-runtime', write(directory, 'bad-runtime.ink',
    '{RANDOM(3, 1)}\n-> END\n'));
  const runtimeRun = run(directory, 'runtime-run', badRuntime.compiled, emptyPlan, { code: 2 });
  assert.equal(runtimeRun.report.failure.code, 'runtime_error');
  assert.ok(runtimeRun.report.diagnostics.some(item => item.severity === 'error'));
  assert.equal(fs.existsSync(runtimeRun.state), false);
  const validRuntime = compile(directory, 'valid-runtime', write(directory, 'valid-runtime.ink',
    '{RANDOM(3, 3)}\n-> END\n'));
  const validRun = run(directory, 'valid-runtime-run', validRuntime.compiled, emptyPlan);
  assert.deepEqual(validRun.report.diagnostics, []);
  assert.equal(validRun.report.observations[0].output.map(chunk => chunk.text).join('').trim(), '3');
});

test('continuation budget and worker deadline stop native loops without leaving a saved success', t => {
  const directory = workspace(t);
  const built = compile(directory, 'loop', write(directory, 'loop.ink', '-> loop\n=== loop ===\nAgain.\n-> loop\n'));
  const plan = scenario(directory, 'bounded-loop', { limits: { max_continue: 3 } });
  const bounded = run(directory, 'bounded', built.compiled, plan, { code: 2 });
  assert.equal(bounded.report.failure.code, 'continuation_limit');
  assert.equal(fs.existsSync(bounded.state), false);
  const silent = compile(directory, 'silent-loop', write(directory, 'silent-loop.ink',
    '-> loop\n=== loop ===\n-> loop\n'));
  const silentPlan = scenario(directory, 'silent');
  const timed = run(directory, 'timed', silent.compiled, silentPlan, { code: 2, timeout: 200 });
  assert.equal(timed.report.failure.code, 'deadline_exceeded');
  assert.equal(fs.existsSync(timed.state), false);
});

test('output collisions preserve existing files; stale or incomplete reports are not assessed', t => {
  const directory = workspace(t);
  const built = compile(directory, 'compiled');
  const originalBytes = fs.readFileSync(built.compiled);
  const collision = cli('compile', ['--source', path.join(fixtures, 'closed-room.ink'),
    '--inkjs-root', inkjsRoot, '--out', built.out], 2);
  assert.equal(collision.failure.code, 'EEXIST');
  assert.deepEqual(fs.readFileSync(built.compiled), originalBytes);
  assert.equal(fs.existsSync(path.join(built.out, 'failure.json')), false);
  const inspectPlan = path.join(fixtures, 'inspect.json');
  const inspected = run(directory, 'inspected', built.compiled, inspectPlan);
  const changedPlan = read(inspectPlan);
  changedPlan.id = 'different-scenario';
  const changed = write(directory, 'changed-plan.json', changedPlan);
  assert.equal(assessment(built.compiled, changed, inspected.reportPath, 2).failure.code,
    'report_identity_mismatch');
  const truncated = read(inspected.reportPath);
  truncated.observations.pop();
  const badReport = write(directory, 'truncated-report.json', truncated);
  assert.equal(assessment(built.compiled, inspectPlan, badReport, 2).failure.code, 'incomplete_run');
});
