# Build an agent you can inspect, then test changes to its harness

Pending, Inc. has hired an AI employee to handle refunds and account access. Management considers the job delegated. We still need to write the code that lets the employee do it.

The workshop starts with two fictional customer tickets. Acme has two captured payments of 4,900 cents for the same invoice and wants the duplicate refunded. Fern wants Alex added to its account, but the access tool can commit the change and then time out. We can inspect every account, payment, refund, and membership, so we can check the employee's work independently of its reply.

You'll build that employee in an editable Python notebook, instrument its work in Agent Lens, and compare changes to its instructions. Then another agent will propose changes to those instructions. The interesting question is whether the resulting employee handles the account correctly, including when a tool's response leaves the situation unclear.

## Give the employee something it can use

An agent's harness includes the instructions it receives, available tools, skill files it can read, and code that carries observations into subsequent requests. Those pieces affect execution in different ways. Registering a tool makes an action available. Writing a Python function supplies its implementation. Saving a skill file does not mean the model has read it.

Start with the invoice tool. The notebook asks you to implement this function:

```python
def my_invoice_tool(state, account_id, invoice_id):
    account = state["accounts"][account_id]
    return {
        "payments": [
            p for p in account["payments"]
            if p["invoice_id"] == invoice_id
        ],
        "refunds": account["refunds"],
    }
```

The account lookup happens before the invoice filter. That's deliberate: different accounts can have the same invoice identifier. The free check tests both accounts, an absent invoice, and whether the function accidentally mutates the account.

Next, connect a chosen action to that function and return its observation to the model. These are separate steps. If you call Python and discard the result, the model's next request still lacks the payment records. The notebook exposes both `my_dispatch` and `my_observation`, then shows the action, arguments, return value, and next request together.

![Agent Lens shows the account argument and returned payment records for a recorded billing run.](https://ash0ts.github.io/forge-workshop-kit/pending/images/visual-v030-pending-lookup.png)

*Recorded example: the employee chose the registered `get_account` tool here. This capture does not show it choosing the learner's `lookup_invoice` function. Open the [conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/c2458ce8b6bb52274d29b5c5a691424b/spans) and find the account identifier in both the input and returned record.*

You also write tracing scopes that preserve real arguments, results, errors, and timing. Compare those spans with the notebook's saved execution events. A trace is helpful only if it describes the operation that ran.

## Recover from a write whose response was lost

The second ticket uses onboarding tools discovered and called through local MCP. MCP supplies a way to discover and invoke the tools; you still need to understand each tool's behavior.

In the resettable timeout exercise, `provision_member` adds Alex before returning an error. The starter recovery function adds `-retry` to the operation identifier and sends the write again. The simulator treats that as a different operation and adds Alex twice.

The repaired function keeps the original identity and checks the account:

```python
def recover_access(arguments, call_tool):
    receipt = call_tool("provision_member", dict(arguments))
    return call_tool(
        "onboarding_status",
        {"account_id": arguments["account_id"]},
    )
```

In this simulator, reusing the identifier returns the saved receipt without adding another membership. The subsequent read verifies the account. The [recorded local comparison](https://github.com/ash0ts/forge-workshop-kit/blob/main/evidence/pending-retry-repair.json) contains two memberships before the repair and one afterward. This is a deterministic code exercise with no model calls, so you can predict the result, change the function, and immediately check it.

![A recorded onboarding tool call has a timeout even though the simulated write may have committed.](https://ash0ts.github.io/forge-workshop-kit/pending/images/visual-v030-pending-timeout.png)

*A separate recorded agent run encounters the same kind of timeout. In [its conversation](https://forge.coreweave.com/agent-lens/wandb/forge-workshop-kit/conversations/481ae944f1062c5381870a00319f65a3/spans), inspect the operation identifier, the error, and the following account read. The red error alone does not establish whether access was granted.*

## Check the account and the explanation separately

For the billing development case, you write a state check requiring exactly one full 4,900-cent refund. A partial refund should fail even if the employee confidently says the problem is resolved.

The explanation judge answers another question: does the reply accurately describe the recorded work and unresolved issues? You write its rubric and validate its structured response. Boolean fields and a nonempty reason make an answer parseable. They don't establish that the judgment is correct. If the judge produces no answer, its score remains unavailable.

The employee also has a `check_work` tool. That is feedback available during its execution. Your development scorer and the independent final grader run outside that conversation. Keeping these roles separate lets you ask whether the employee checked its work, whether the account is correct, and whether its explanation is accurate without collapsing them into one success flag.

## Test an instruction change before automating the editing

Choose an event from a development ticket and write the procedure you'd want the employee to follow next time. The notebook installs it as a verification skill. In the next run, look for `read_skill` and inspect the following model request. If no read occurred, don't attribute a changed tool sequence to text the employee never received.

Rerun both tickets from their original account states. Keep the model and tested executor fixed while changing the harness. Now you can compare the instruction diff with the tool sequence and checked account state.

The editor agent then proposes two competing harness changes. You review their actual diffs, probe both on isolated copies, and ask the editor which changes to keep or combine. A composition needs its own test. Retaining the current version is also valid. A second round carries the chosen harness and a saved lesson into onboarding.

Agent Lens exposes the editor's evidence reads and decisions. Artifacts preserve the files that ran. The branch view connects a proposal to its test and eventual selection, including rejected candidates. The research pattern is Propose, Probe, and Compose, adapted here to two office tasks rather than presented as a replication of an upstream benchmark.

## What happened in the recorded comparison

We froze the starting, manually revised, and agent-selected harnesses, then ran each on the same four final tickets. In the current [recorded rehearsal](https://github.com/ash0ts/forge-workshop-kit/blob/main/decks/pending/data/recorded-final.json), all three passed all four account checks and explanation judgments. Their tool-call totals were 12, 13, and 13.

The extra call in the revised versions did not produce a measured task-quality gain on this suite. The deterministic timeout repair above demonstrates an implementation improvement; the harness comparison demonstrates a tie. Four tickets in one rehearsal cannot establish that the versions are generally equivalent.

![Native EvalTables aligns one ticket across starting, manually revised, and agent-selected harnesses.](https://ash0ts.github.io/forge-workshop-kit/pending/images/evaltables-native-detail.png)

*In this aligned case, each version asks for missing access details. Open the [saved comparison](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=qeo6ytk9yxz), inspect the questions and account check, then follow a conversation link. These are instructor results, not outcomes from your edits.*

The notebook includes two optional ARIA investigations: explain a development result, then check the frozen conclusion. Select specific records and verify one cited claim. ARIA's interpretation does not become a score or automatically change the harness. Recorded investigations are available if your project lacks ARIA access.

## Run it in your own project

Open the [Pending, Inc. notebook](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view), choose **Copy to project**, and open your editable copy. Use **Run all stale cells** to create the controls, inspect the opening example, and check that the displayed destination is your project. Exercise buttons start execution explicitly.

You need basic Python, project write access, notebook compute, and inference access. The adjustable $8 notebook inference allowance does not include compute or ARIA usage. No workshop gateway or remote Sandbox entitlement is required. The [setup guide](https://github.com/ash0ts/forge-workshop-kit/blob/main/docs/setup.md) includes the laptop path, access checks, and saved-work recovery; the [deck](https://ash0ts.github.io/forge-workshop-kit/pending/) accompanies the four-hour workshop.

This is a technical preview with external-account checks and participant rehearsals still outstanding. Start with the invoice function and free handoff check, then follow your own run into Agent Lens.
