const { test } = require('node:test');
const assert = require('node:assert/strict');
const { waitForPagesArtifact } = require('../.github/scripts/pages-artifact.cjs');

const artifact = { id: 42, name: 'github-pages', expired: false, size_in_bytes: 1024 };

function fixture(responses, artifactId = 42) {
  const reads = [];
  const waits = [];
  return {
    reads,
    waits,
    options: {
      artifactId,
      context: { repo: { owner: 'test', repo: 'workshops' }, runId: 10 },
      core: { info() {} },
      sleep: async (milliseconds) => waits.push(milliseconds),
      github: {
        rest: { actions: { listWorkflowRunArtifacts: 'list' } },
        paginate: async (method, args) => {
          reads.push({ method, args });
          return responses[Math.min(reads.length - 1, responses.length - 1)];
        },
      },
    },
  };
}

test('retries absent metadata and hands off only the matching current-run upload', async () => {
  const f = fixture([[], [], [artifact]]);
  assert.equal(await waitForPagesArtifact(f.options), artifact);
  assert.equal(f.reads.length, 3);
  assert.deepEqual(f.reads[0].args, { owner: 'test', repo: 'workshops', run_id: 10, per_page: 100 });
  assert.deepEqual(f.waits, [5000, 5000, 5000]);
});

test('stops after twelve attempts without calling deployment', async () => {
  const f = fixture([[]]);
  await assert.rejects(waitForPagesArtifact(f.options), /not visible after 12 checks/);
  assert.equal(f.reads.length, 12);
  assert.equal(f.waits.length, 11);
});

test('rejects a different, expired, empty, or duplicated Pages artifact', async () => {
  for (const response of [
    [{ ...artifact, id: 99 }],
    [{ ...artifact, expired: true }],
    [{ ...artifact, size_in_bytes: 0 }],
    [artifact, { ...artifact, id: 99 }],
  ]) {
    const f = fixture([response]);
    await assert.rejects(waitForPagesArtifact(f.options), /does not match|More than one/);
    assert.equal(f.waits.length, 0);
  }
});

test('rejects a missing upload ID without making an API call', async () => {
  const f = fixture([[artifact]], '');
  await assert.rejects(waitForPagesArtifact(f.options), /valid artifact ID/);
  assert.equal(f.reads.length, 0);
});
