# Evidence Pipeline — GitHub Issues
## RoboCup Soccer Project | Planning Phase | Evidence Gathering Lead

> Paste each section below as a separate GitHub Issue.  
> Suggested labels: `evidence`, `planning`, `infrastructure`, `template`, `test-design`  
> Milestone: **Planning Phase (Week 9–11)**

---

## EP-01 · Define evidence requirements per milestone

**Labels:** `evidence` `planning` `requirements`  
**Assignee:** Evidence Gathering Lead  
**Milestone:** Planning Phase  
**Priority:** P0 — blocks all other evidence work

### Objective

Produce a living document that specifies, for **each feature or milestone** in the agreed project scope (Localisation, Vision, or Motion), exactly what constitutes sufficient evidence of completion — **before a single line of code is written.**

This document becomes the single source of truth that every run report, test scenario, and metrics logger is built against.

### Background

The project spec requires PG students to produce evidence sufficient for a published article, and UG students to demonstrate multiple solutions. Neither is achievable without knowing upfront what "sufficient" means. This issue creates that definition.

### Tasks

- [ ] Confirm chosen project scope with course coordinator (scope selection deadline: Week 9 Thursday workshop)
- [ ] List every milestone and feature in the chosen scope (e.g. for Localisation: initial pose estimation, continuous localisation, recovery from kidnap, etc.)
- [ ] For each milestone, define:
  - The **success metric** (e.g. "localisation error < 15 cm in 80% of trials")
  - The **minimum number of trials** needed to claim the result
  - The **artifact types** required (bag file, CSV, video, screenshot)
  - The **conditions** under which the test must be run (competition field, lighting, opponent robots present/absent)
- [ ] Document failure modes — what would falsify the claim?
- [ ] Get sign-off from all team members
- [ ] Link document from the repository root `README.md`

### Deliverable

`evidence/requirements/evidence_requirements.md`

### Acceptance Criteria

- [ ] Document created and merged to `main` before end of Week 10
- [ ] Every milestone has at least one **quantitative** success threshold
- [ ] Failure/falsification conditions documented for each milestone
- [ ] Document reviewed and approved by all team members (comments or approvals on the PR)
- [ ] Linked from `README.md`

### Dependencies

- Scope selection (no later than Week 9 Thursday workshop)
- Team agreement on chosen project component

---

## EP-02 · Design test scenarios for each evidence requirement

**Labels:** `evidence` `planning` `test-design`  
**Assignee:** Evidence Gathering Lead  
**Milestone:** Planning Phase  
**Priority:** P0 — must be complete before Week 11

### Objective

For each requirement defined in EP-01, write a **test scenario** with a defined setup, stimulus, expected observable output, and pass/fail threshold. Scenarios must be executable on the Booster K1 under competition-like conditions and must map 1:1 to the evidence requirements document.

### Background

Test scenarios are the bridge between abstract requirements and concrete evidence. Without them, test sessions become ad-hoc and produce incomparable results. Designing them upfront ensures every run contributes usable evidence.

### Tasks

- [ ] Read all requirements from EP-01
- [ ] For each requirement, write a scenario card containing:
  - **Scenario ID** (e.g. `LOC-01`, `VIS-01`) — used in all artifact filenames
  - **Environment setup** (field dimensions, lighting, landmark configuration)
  - **Robot starting state** (pose, battery level, any required initialisation)
  - **Action sequence** (step-by-step what happens during the test)
  - **Measured output** (which ROS2 topic or observable quantity is recorded)
  - **Pass threshold** (the quantitative value from EP-01)
  - **Failure conditions** (what terminates the run as a failure)
- [ ] Add at least one **edge-case or failure scenario** per feature (e.g. ball occluded, robot kidnapped, lighting change)
- [ ] Review scenario feasibility with the team — can each be run in the available lab time?
- [ ] Cross-reference: every requirement in EP-01 must have at least one scenario; every scenario must trace back to a requirement

### Deliverable

`evidence/scenarios/` — one `.md` file per scenario, named `<SCENARIO-ID>.md`

### Acceptance Criteria

- [ ] One scenario card per evidence requirement from EP-01
- [ ] Each card contains all six fields listed above
- [ ] At least one edge-case or failure scenario per feature
- [ ] All scenarios reviewed with the team and confirmed feasible before Week 11
- [ ] Traceability matrix (`evidence/scenarios/traceability.md`) shows requirement ↔ scenario mapping

### Dependencies

- EP-01 completed
- Access to Booster K1 or simulation environment confirmed with lab coordinator

---

## EP-03 · Set up ROS2 bag recording infrastructure

**Labels:** `evidence` `infrastructure` `ros2`  
**Assignee:** Evidence Gathering Lead (with dev team support for topic list)  
**Milestone:** Planning Phase  
**Priority:** P0 — must be ready before first test session

### Objective

Configure a `ros2 bag record` launch file that **automatically captures all relevant topics** during test sessions. Bag files must be named with run metadata and stored in a structured directory so they can be replayed and inspected at any time.

### Background

The RedBackBots codebase cannot be modified architecturally, but evidence capture nodes can be added as separate packages. ROS2 bag files are the primary artifact for post-hoc debugging, replaying, and demonstrating correct behaviour — they are the raw evidence that all other analysis is derived from.

### Tasks

- [ ] Get the canonical topic list from the development team (camera, localisation output, tf, command topics)
- [ ] Write a launch file that records a configurable subset of topics
- [ ] Implement the naming convention: `YYYY-MM-DD_<scenario-id>_run<N>.bag`
- [ ] Create the directory structure under `evidence/artifacts/bags/`
- [ ] Add a `.gitignore` entry so bag files are not committed (they are stored separately — document where)
- [ ] Document the bag storage location (network drive, external drive, cloud) and retention policy
- [ ] Test end-to-end: record a 60-second bag and replay it without errors
- [ ] Write a one-page "How to record a test session" guide in `evidence/docs/recording_guide.md`

### Deliverable

`evidence/launch/record_session.launch.py`  
`evidence/docs/recording_guide.md`

### Acceptance Criteria

- [ ] Launch file committed under `evidence/launch/`
- [ ] Bags include: camera topics, localisation output, tf transforms, action/command topics
- [ ] Naming convention documented and enforced by the launch file (auto-generates the filename)
- [ ] End-to-end test passed: 60-second bag recorded and replayed without error
- [ ] Storage location and retention policy documented in `evidence/docs/recording_guide.md`
- [ ] `.gitignore` updated — no binary bag files committed to the repository

### Dependencies

- Access to the RedBackBots codebase
- Topic list provided by the development team

---

## EP-04 · Set up automated frame capture node

**Labels:** `evidence` `infrastructure` `ros2` `vision`  
**Assignee:** Evidence Gathering Lead  
**Milestone:** Planning Phase  
**Priority:** P1 — needed for Vision and Localisation scenarios

### Objective

Create a ROS2 node that subscribes to the robot camera topic and saves labelled frames at configurable intervals **or** on trigger events (e.g. ball detected, goal scored, localisation jump). Frames must be saved with timestamps and scenario metadata embedded in the filename.

### Background

Video/image evidence is essential for demonstrating detection accuracy and for the report figures. Automated capture is preferable to manual screenshots because it is reproducible and does not require a human to be watching the screen during runs.

### Tasks

- [ ] Confirm camera topic name with the development team
- [ ] Confirm trigger event topics (e.g. detection confidence topic, state machine transitions)
- [ ] Implement the capture node with two modes:
  - **Interval mode:** save one frame every N seconds (configurable parameter)
  - **Event mode:** save a frame on each message to a trigger topic
- [ ] Filename convention: `<scenario-id>_<unix-timestamp>_<trigger-type>.png`
- [ ] Save to `evidence/artifacts/frames/<scenario-id>/`
- [ ] Benchmark CPU overhead — confirm it does not degrade robot performance
- [ ] Add node to `record_session.launch.py` (EP-03) as an optional component

### Deliverable

`evidence/nodes/frame_capture.py`  
(or `evidence/nodes/frame_capture_node.cpp` if C++ is preferred for performance)

### Acceptance Criteria

- [ ] Node committed under `evidence/nodes/`
- [ ] Both interval and event-based trigger modes working
- [ ] Filenames follow naming convention with correct metadata
- [ ] Tested: 10-second interval run produces ≥ expected frame count with correct naming
- [ ] CPU overhead benchmarked and documented — no observable impact on robot performance
- [ ] Node integrated into `record_session.launch.py` as an optional launch argument

### Dependencies

- EP-03 (logging infrastructure)
- Camera topic name confirmed with development team
- Trigger topic names confirmed with development team

---

## EP-05 · Set up quantitative metrics logger and CSV export

**Labels:** `evidence` `infrastructure` `ros2` `metrics`  
**Assignee:** Evidence Gathering Lead  
**Milestone:** Planning Phase  
**Priority:** P0 — needed for all PG statistical analysis

### Objective

Implement a lightweight metrics recorder that subscribes to key output topics and writes **timestamped CSV rows** for each run. A companion aggregation script must produce per-scenario summary statistics (mean, std-dev, min, max, n) across multiple runs, suitable for inclusion in the report.

### Background

Quantitative evidence is the backbone of the PG experimental evaluation requirement. The metrics logger operationalises the thresholds defined in EP-01 by producing machine-readable data that can be statistically tested. It also produces the figures and tables for the report.

### Tasks

- [ ] Identify the ROS2 topics that carry each metric defined in EP-01 (e.g. `/pose_estimate` for localisation error, `/detection_confidence` for vision)
- [ ] Implement `metrics_logger.py` — subscribes to all metric topics and writes one CSV row per observation with columns: `timestamp, scenario_id, run_number, <metric columns from EP-01>`
- [ ] Implement `aggregate_runs.py` — reads all CSVs matching a scenario ID pattern and produces a summary table
- [ ] Define and document the CSV schema in `evidence/docs/metrics_schema.md`
- [ ] Test: 5 simulated runs produce a merged CSV with correct statistics
- [ ] Ensure filenames match the convention from EP-03: `YYYY-MM-DD_<scenario-id>_run<N>_metrics.csv`

### Deliverable

`evidence/scripts/metrics_logger.py`  
`evidence/scripts/aggregate_runs.py`  
`evidence/docs/metrics_schema.md`

### Acceptance Criteria

- [ ] Logger script committed under `evidence/scripts/`
- [ ] CSV schema documented with column names matching the thresholds in EP-01
- [ ] Aggregation script produces mean, std-dev, min, max, and n per scenario
- [ ] Tested: 5 runs produce a merged CSV with correct statistics
- [ ] CSV filenames follow the EP-03 naming convention
- [ ] Schema document reviewed by PG team members to confirm it captures all required statistical variables

### Dependencies

- EP-01 (defines which metrics to capture)
- EP-03 (infrastructure context, naming conventions)
- Metric topic names confirmed with development team

---

## EP-06 · Create standardised run report template

**Labels:** `evidence` `template` `documentation`  
**Assignee:** Evidence Gathering Lead  
**Milestone:** Planning Phase  
**Priority:** P1 — must exist before first test session

### Objective

Design a markdown run report template that any team member fills out **after every test session**. The template structures the scenario ID, environment conditions, run outcomes, anomalies, and links to artifacts. All template fields must map directly to columns in the evidence requirements document from EP-01.

### Background

Without a standardised report, evidence from different team members is incomparable and hard to aggregate. A template ensures every session produces a citable, consistent record that can be referenced in the report's Results section.

### Tasks

- [ ] Draft the template with the following sections:
  - **Run metadata:** date, operator name, scenario ID, robot serial/config, git commit hash of the code under test
  - **Environment:** field setup, lighting conditions, any deviations from the standard scenario
  - **Outcomes table:** one row per run — run number, pass/fail, metric values, notes
  - **Artifact links:** bag file path, frames directory, metrics CSV path
  - **Anomalies:** anything unexpected that occurred during the session
  - **Next actions:** issues to investigate or changes to make before the next session
- [ ] Embed guidance notes as HTML comments (`<!-- ... -->`) inside the template so it is self-documenting
- [ ] Test the template by completing one trial run report (can use simulated data)
- [ ] Add instructions for using the template to `CONTRIBUTING.md`
- [ ] Store completed reports under `evidence/reports/YYYY-MM-DD_<scenario-id>/`

### Deliverable

`evidence/templates/run_report.md`

### Acceptance Criteria

- [ ] Template committed to `evidence/templates/run_report.md`
- [ ] All fields listed above present and clearly labelled
- [ ] Guidance comments embedded in the template
- [ ] Trial run report completed using the template before Week 11
- [ ] Usage instructions added to `CONTRIBUTING.md`
- [ ] Directory structure for storing completed reports documented

### Dependencies

- EP-01 (evidence requirements define what goes in the outcomes table)
- EP-02 (scenario IDs must be defined before the template is used)

---

## EP-07 · Create evidence checklist for Week 12 progress demonstration

**Labels:** `evidence` `template` `demo-prep`  
**Assignee:** Evidence Gathering Lead  
**Milestone:** Week 12 Progress Update  
**Priority:** P1 — must be completed by end of Week 11

### Objective

Produce a pre-demo checklist that the **whole team completes** before the Week 12 progress demonstration. The checklist functions as a gate — the demo does not proceed until all items are checked. It ensures all minimally viable evidence artifacts are collected, labelled, and accessible.

### Background

The Week 12 progress demonstration must show components of a minimally viable solution and a feasible plan for completion. Having a formal checklist prevents last-minute scrambling and demonstrates to the assessors that the team has a systematic approach to evidence collection — which is itself evidence of good engineering practice.

### Tasks

- [ ] Define what "minimally viable evidence" means for the chosen scope — at minimum: one complete run of each minimally viable scenario with all three artifact types (bag, frames, CSV)
- [ ] Draft the checklist with sections:
  - **Artifact completeness:** bag files present and replayable, frames captured, metrics CSVs exported
  - **Report traceability:** run reports completed for every session, all artifacts linked
  - **Repository hygiene:** code at a clean commit, evidence scripts tested and working
  - **Demo readiness:** demo script prepared, robot charged, launch files tested
- [ ] Add a sign-off field for each team member
- [ ] Schedule a dry-run of the checklist at least 3 days before the Week 12 demo
- [ ] Convert any gaps found during the dry-run into follow-up issues immediately

### Deliverable

`evidence/checklists/week12_demo_checklist.md`

### Acceptance Criteria

- [ ] Checklist committed to `evidence/checklists/week12_demo_checklist.md`
- [ ] Covers all artifact types: bags, frames, CSVs, run reports
- [ ] Includes a sign-off field for each team member
- [ ] Dry-run completed at least 3 days before the Week 12 demo
- [ ] All gaps found during dry-run converted into follow-up GitHub issues before the demo

### Dependencies

- EP-03, EP-04, EP-05 (infrastructure must exist to check artifacts against)
- EP-06 (run reports must exist to check completeness)

---

## EP-08 · Design PG experimental evaluation protocol

**Labels:** `evidence` `test-design` `pg-requirement` `experiment`  
**Assignee:** PG team members + Evidence Gathering Lead  
**Milestone:** Week 12 Progress Update (protocol must be presented)  
**Priority:** P0 for PG students

### Objective

Design a **formal experimental protocol** suitable for a published article, as required for PG students. The protocol specifies the independent variables, dependent variables, control conditions, sample sizes, statistical tests, and visualisation plan. It must be presented during the Week 12 progress update.

### Background

The project spec states: *"The standard of evaluation should collect evidence, including repeatable statistical measures, sufficient for a published article."* This issue operationalises that requirement. The protocol is designed upfront so that test infrastructure (EP-03–EP-05) captures exactly the data the experiment needs — not discovered retrospectively.

### Tasks

- [ ] Identify the **independent variables** (e.g. algorithm variant, field condition, opponent count)
- [ ] Identify the **dependent variables** (e.g. localisation RMSE, detection F1 score, kick success rate)
- [ ] Define **control conditions** — what is held constant across all conditions
- [ ] Determine **sample size** per condition:
  - Minimum 10 runs per condition for meaningful statistics
  - Justify the number with a brief power analysis or reference to comparable published work
- [ ] Specify the **statistical test** for each hypothesis (e.g. paired t-test, Mann-Whitney U, ANOVA)
- [ ] Write the **null hypotheses** being tested
- [ ] Plan the **visualisation** — which figures will appear in the report (box plots, confusion matrices, trajectory plots)
- [ ] Ensure the protocol maps directly to the Results and Analysis/Evaluation sections of the report structure
- [ ] Present the protocol during the Week 12 progress update for assessor feedback

### Deliverable

`evidence/experiments/pg_protocol.md`

### Acceptance Criteria

- [ ] Protocol document committed to `evidence/experiments/pg_protocol.md`
- [ ] Independent and dependent variables explicitly defined
- [ ] Null hypotheses stated formally
- [ ] Sample size justified (≥ 10 runs per condition)
- [ ] Statistical tests specified for each hypothesis
- [ ] Visualisation plan included
- [ ] Protocol maps to report structure (Results, Analysis & Evaluation sections)
- [ ] Protocol presented and noted at Week 12 progress update
- [ ] Protocol reviewed against the HSL Rules 2026 to confirm competition conditions are accurately modelled

### Dependencies

- EP-01 (evidence requirements define the metrics the experiment measures)
- EP-02 (test scenarios define the conditions)
- EP-05 (metrics logger must exist to capture experimental data)

---

## Suggested Repository Structure

```
evidence/
├── requirements/
│   └── evidence_requirements.md       # EP-01
├── scenarios/
│   ├── traceability.md                # EP-02
│   ├── LOC-01.md                      # EP-02 (example)
│   └── VIS-01.md                      # EP-02 (example)
├── launch/
│   └── record_session.launch.py       # EP-03
├── nodes/
│   └── frame_capture.py               # EP-04
├── scripts/
│   ├── metrics_logger.py              # EP-05
│   └── aggregate_runs.py              # EP-05
├── docs/
│   ├── recording_guide.md             # EP-03
│   └── metrics_schema.md             # EP-05
├── templates/
│   └── run_report.md                  # EP-06
├── checklists/
│   └── week12_demo_checklist.md       # EP-07
├── experiments/
│   └── pg_protocol.md                 # EP-08
└── artifacts/                         # gitignored — stored externally
    ├── bags/
    ├── frames/
    └── csvs/
```

---

## Milestone Timeline

| Week | Target |
|------|--------|
| 9    | Scope confirmed; EP-01 started |
| 10   | EP-01 merged; EP-02, EP-03, EP-06 in review |
| 11   | EP-02–EP-06 merged; EP-07 drafted; first trial run completed |
| 12   | EP-07 checklist dry-run; EP-08 protocol presented; all infrastructure tested end-to-end |