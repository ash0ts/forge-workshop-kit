const delay = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

// Confirm the public metadata before handing off to deploy-pages.
async function waitForPagesArtifact({ github, context, core, artifactId, sleep = delay }) {
  const expectedId = Number(artifactId);
  if (!Number.isSafeInteger(expectedId) || expectedId <= 0) {
    throw new Error('The Pages upload did not return a valid artifact ID.');
  }
  for (let attempt = 1; attempt <= 12; attempt += 1) {
    const artifacts = await github.paginate(github.rest.actions.listWorkflowRunArtifacts, {
      ...context.repo,
      run_id: context.runId,
      per_page: 100,
    });
    const matches = artifacts.filter((artifact) => artifact.name === 'github-pages');
    if (matches.length > 1) {
      throw new Error('More than one github-pages artifact exists in this run.');
    }
    if (matches.length === 1) {
      const artifact = matches[0];
      if (artifact.id !== expectedId || artifact.expired || artifact.size_in_bytes <= 0) {
        throw new Error('The visible Pages artifact does not match this upload.');
      }
      core.info(`Pages artifact ${expectedId} is visible in the workflow artifact list.`);
      // deploy-pages uses a separate internal listing; allow it to settle too.
      await sleep(5000);
      return artifact;
    }
    core.info(`Waiting for Pages artifact metadata (${attempt}/12).`);
    if (attempt < 12) await sleep(5000);
  }
  throw new Error('The uploaded Pages artifact was not visible after 12 checks. Retry publication from the saved build.');
}

module.exports = { waitForPagesArtifact };
