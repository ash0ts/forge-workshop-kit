# Earlier workshop materials

Use [the current templates and setup](../README.md) for a new workshop. These links preserve earlier experiments and releases; they are not additional setup steps.

- [Workshop Kit releases](https://github.com/ash0ts/forge-workshop-kit/releases): pinned notebooks, package wheels, decks and release evidence.
- [Checks through v0.2.3](archive/release-checks-through-v023.md): the earlier rehearsals, captures and known limitations.
- [Pending November 12 and self-service releases](https://github.com/ash0ts/pending-inc-workshop/releases): the office workshop before the shared kit.
- [Operator archive](https://github.com/ash0ts/harness2-workshop/tree/codex/pending-inc-chambers): historical gateway implementations and deployment evidence. New templates do not import this code.

Current screenshots, recorded teaching examples and Solar data provenance stay in the kit. Existing attendee notebooks and their saved work remain unchanged. No Git history has been rewritten.

## November 13 rehearsals

Solar uses GOES-15 X-ray measurements and NASA SDO/AIA images, prepared for small CPU experiments. In the November 13 rehearsal, average error on the reserved image dates was 0.125762 for persistence, 0.122442 for the manually written model, and 0.110011 for the agent-selected model. The agent first changed the training loss to masked absolute error, then zero-initialized the residual head. Its final version had 10.2% lower error than the manual version under the same training budget.

That comparison covers 199 overlapping windows from two days, with one seed. It shows one completed research loop, not a reliable solar-forecasting result. The short GOES training run did worse than persistence. Both results stay in the workshop so you can inspect what the code produced. [Data and calculation details](solar-evidence.md).

Pending uses fictional accounts and payments, including a tool that changes account state before its response times out. All 12 final runs passed the state checks and explanation judgments in the November 13 rehearsal. The editor retained the earlier harness in round one, then revised its verification skill in round two. Those edits did not improve the already-passing final scores. Recorded examples are labeled separately from your own results.

- [Banking77 classifier comparison](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Route-customer-requests-and-learn-from-mistakes:-382ea260--VmlldzoxODMwNzYzNQ==)
- [PCB1 detector comparison](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Find-defective-parts-before-they-ship:-5ec44d92--VmlldzoxODMwNzU3Nw==)
- [Solar November 13 rehearsal Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/Build-a-research-loop,-then-give-it-an-agent:-6e768bbe--VmlldzoxODMwMzU3Nw==)
- [Pending November 13 rehearsal Report](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit/reports/pending-direct-teaching:-bc0ee4ab--VmlldzoxODMwMzUyNg==)
- Earlier rehearsal dashboards: [Solar](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=ogpa6vhy8db) · [Pending](https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=nkyxiy1o6wn). Their branch decisions differ from the November 13 walkthrough.
