# EP-01 Sub-Issues — Information Discovery for Evidence Requirements

> These sub-issues identify the information the team needs to gather **before** the evidence requirements document (`evidence/requirements/evidence_requirements.md`) can be written.
>
> Each sub-issue is a self-contained investigation task. Assign to the team member best positioned to answer the question.
>
> **Parent:** [`EP-01`](.issues/evidence_planning.md) · Define evidence requirements per milestone
> **Reference:** [`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md)
> **Labels:** `evidence` `planning` `information-gathering`
> **Milestone:** Planning Phase (Week 9–11)

---

## EP-01-S01 · Confirm project scope selection with course coordinator

**Labels:** `evidence` `planning` `information-gathering`  
**Assignee:** Team Lead / Coordinator Liaison  
**Priority:** P0 — blocks all other EP-01 work  
**Due:** Week 9 Thursday workshop

### Objective

Confirm with the course coordinator which **component of the RoboCup HSL rules** our team will implement. The spec ([`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md:141)) lists three available aspects:

1. **Localisation** — Localisation of the robot on the soccer field
2. **Robot Vision & Detection** — Detection of field features, ball, and other robots
3. **Motion** — Reliable movement and kicking

We may also negotiate a combination or a sub-component of one of these.

### Questions to Answer

- [ ] Which component (or combination) has the course coordinator approved for our team?
- [ ] Is there a pre-existing scope document or rubric for this component that the coordinator can share?
- [ ] Are there any constraints on scope (e.g., must be achievable with the existing RedBackBots architecture)?
- [ ] What is the deadline for final scope confirmation? (Spec says "no later than Thursday Workshop in Week 9" — confirm exact date.)
- [ ] Does the coordinator have any preferences or guidance on which sub-problems to prioritise?

### Deliverable

A short summary (3–5 bullet points) posted in the team's communication channel, confirming:
- The chosen scope component
- Any sub-components or features included
- Coordinator's name and confirmation date

### Dependencies

- None (this is the first dependency for all other EP-01 work)

---

## EP-01-S02 · Audit the RedBackBots codebase for existing capabilities and topics

**Labels:** `evidence` `infrastructure` `information-gathering`  
**Assignee:** Developer with access to the RedBackBots codebase  
**Priority:** P0 — needed to define what evidence infrastructure is required  
**Due:** Week 9 Friday (after scope is confirmed)

### Objective

Audit the existing RedBackBots RoboCup codebase to understand what is already implemented, what ROS2 topics are available, and what the architecture constraints are. This directly informs what evidence we need to collect (EP-01) and what infrastructure we need to build (EP-03–EP-05).

### Questions to Answer

- [ ] What ROS2 topics are already published? Specifically:
  - Camera/image topics (topic name, message type, frame rate)
  - Localisation/pose estimate topics
  - Detection topics (ball, robots, field features)
  - Command/action topics (motion commands, kick commands)
  - TF transform tree
- [ ] What is the existing robot software architecture? (Spec says it cannot be modified — we need to understand its structure to add evidence-capture nodes.)
- [ ] What launch files already exist? Can we extend them or must we create separate launch files?
- [ ] Is there an existing simulation environment (Gazebo, Webots, etc.) we can use for testing?
- [ ] What is the git repository URL and branch structure?
- [ ] Are there any existing test scripts, bag recording setups, or logging utilities?
- [ ] What programming language(s) is the codebase in? (Python, C++?)
- [ ] What ROS2 distribution is being used? (Humble, Iron, Rolling?)

### Deliverable

A document (`docs/codebase_audit.md`) or a detailed team message covering:
- Topic list with names, types, and frame rates
- Architecture diagram or description
- Simulation availability
- Key constraints for evidence collection

### Dependencies

- EP-01-S01 (scope must be confirmed to know which parts of the codebase to focus on)
- Access to the RedBackBots GitHub repository

---

## EP-01-S03 · Determine team composition (UG vs PG members)

**Labels:** `evidence` `planning` `information-gathering`  
**Assignee:** Team Lead  
**Priority:** P0 — affects evidence requirements scope and rigour  
**Due:** Week 9 Friday

### Objective

Determine the study level of each team member (UG vs PG) so that the evidence requirements document can be scoped appropriately. The spec ([`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md:106-128)) has different requirements:

- **UG students:** Must implement multiple solutions if the infrastructure implementation is not sufficiently significant (line 115). Need to demonstrate extended infrastructure/architecture/implementation.
- **PG students:** Must design an experiment that highlights both strengths and limitations, with evidence sufficient for a published article (line 120-122). Must propose experiment methodology during Week 12 progress update.
- **Mixed groups:** Each student graded according to their level's rubric (line 126-128).

### Questions to Answer

- [ ] How many UG vs PG students are in the group?
- [ ] For UG students: what is their expected "multiple solutions" requirement? Has the course coordinator specified a minimum number of approaches to implement?
- [ ] For PG students: what statistical rigour is expected? (Spec says "repeatable statistical measures, sufficient for a published article.")
- [ ] Are there any students who have prior RoboCup or RedBackBots experience?
- [ ] What are each member's strengths/interests? (Vision, motion control, localisation, ROS infrastructure, etc.)

### Deliverable

A team roster document or message listing:
- Each member's name and study level (UG/PG)
- Any prior relevant experience
- Preferred role / area of contribution

### Dependencies

- EP-01-S01 (scope may influence role allocation)

---

## EP-01-S04 · Research HSL Rules 2026 competition conditions

**Labels:** `evidence` `planning` `information-gathering`  
**Assignee:** Evidence Gathering Lead  
**Priority:** P1 — needed to define test conditions for evidence requirements  
**Due:** Week 10 Monday

### Objective

Review the [HSL Rules 2026](https://github.com/RoboCup-HumanoidSoccerLeague/HSL-Rules/) to extract the specific competition conditions that will affect evidence collection. The spec ([`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md:136)) requires demonstrating code on the Booster K1 under **competition conditions**.

### Questions to Answer

- [ ] What are the **field dimensions** and markings? (This affects localisation test scenarios.)
- [ ] What are the **lighting conditions** expected at competition? (Affects vision detection thresholds.)
- [ ] What is the **ball type and colour**? (Affects vision/detection parameters.)
- [ ] What are the **robot dimensions and weight limits**? (Affects motion constraints.)
- [ ] What are the **rules for kicking**? (Distance, direction, number of kicks per possession?)
- [ ] What are the **game duration and stoppage rules**? (Affects how long the robot must operate autonomously.)
- [ ] Are there **technical challenges** that are part of the competition? (Spec mentions "technical challenges" at line 136.)
- [ ] What are the **network/communication rules**? (Any restrictions on WiFi, off-board processing?)
- [ ] What **safety requirements** apply? (Emergency stop, robot behaviour rules?)

### Deliverable

A summary document (`docs/hsl2026_conditions_summary.md`) covering:
- Key competition parameters relevant to our chosen scope
- Specific conditions that must be replicated in test scenarios
- Any rules that constrain how evidence can be collected (e.g., no external cameras)

### Dependencies

- EP-01-S01 (scope determines which rules are most relevant)
- Access to the HSL Rules 2026 repository

---

## EP-01-S05 · Determine Booster K1 robot hardware and sensor specifications

**Labels:** `evidence` `infrastructure` `information-gathering`  
**Assignee:** Hardware Lead / Lab Coordinator Liaison  
**Priority:** P1 — needed to define feasible success metrics  
**Due:** Week 10 Monday

### Objective

Gather the hardware specifications of the **Booster K1** robot that will be used for the demonstration. The spec ([`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md:134)) requires demonstrating final code on this platform. Understanding its sensors, computational power, and physical capabilities is essential for setting realistic evidence thresholds.

### Questions to Answer

- [ ] What **sensors** does the Booster K1 have?
  - Camera(s): type, resolution, field of view, frame rate, mounting position
  - IMU: type, update rate, axes
  - Encoders: wheel/ joint encoders?
  - Any other sensors (LiDAR, sonar, pressure sensors in feet?)
- [ ] What is the **onboard computer**? (CPU, RAM, GPU if any)
- [ ] What is the **battery life** under typical operation? (Affects how many test runs we can do per session.)
- [ ] What **actuators** does it have? (Degrees of freedom, joint limits, max speed.)
- [ ] What is the **physical size and weight** of the robot?
- [ ] Is there a **technical manual or datasheet** available?
- [ ] How many Booster K1 robots does the lab have? Can we use more than one?
- [ ] What is the **network setup**? (Onboard WiFi? Ethernet tether? Off-board processing allowed?)
- [ ] Are there any **known hardware limitations** or common failure modes?

### Deliverable

A hardware specification sheet (`docs/booster_k1_specs.md`) covering all of the above. Include photos or diagrams if available.

### Dependencies

- Access to the lab and/or Booster K1 documentation
- Lab coordinator contact

---

## EP-01-S06 · Confirm lab access, scheduling, and risk assessment requirements

**Labels:** `evidence` `planning` `information-gathering`  
**Assignee:** Team Lead / Lab Coordinator Liaison  
**Priority:** P1 — affects how many test sessions we can schedule  
**Due:** Week 10 Monday

### Objective

Determine the practical logistics for running test sessions. The spec ([`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md:94-103)) requires:

- An **Activity Risk Assessment (ARA)** approved before development activities begin (line 96-97)
- May require working in the **VXLab** (Ground floor, Building 91) or **Bundoora spaces** (line 101-102)
- Requires **coordination with staff**, completing **inductions**, and complying with **safety requirements** (line 102)

### Questions to Answer

- [ ] Which lab(s) can we use for testing? (VXLab, Bundoora, other?)
- [ ] What are the **booking procedures**? How far in advance must we book?
- [ ] What are the **lab hours**? Can we access evenings/weekends?
- [ ] What **inductions** are required? Have all team members completed them?
- [ ] What is the **ARA process**? Who prepares it, who approves it, and what is the typical turnaround time?
- [ ] Is there a **competition field** set up in the lab, or do we need to build/borrow one?
- [ ] What **lighting conditions** can we control in the lab? (Important for vision testing.)
- [ ] Is there **network access**? Can we use WiFi for remote monitoring?
- [ ] Are there **storage facilities** for equipment?
- [ ] What is the **lab coordinator's name and contact**?

### Deliverable

A logistics summary (`docs/lab_access_plan.md`) covering:
- Lab location(s) and booking process
- Induction status of each team member
- ARA status and timeline
- Available test session slots mapped to the project timeline

### Dependencies

- Lab coordinator contact
- Course coordinator contact (for ARA process)

---

## EP-01-S07 · Define success metrics and thresholds for the chosen scope

**Labels:** `evidence` `planning` `requirements`  
**Assignee:** Evidence Gathering Lead (with input from all team members)  
**Priority:** P0 — this is the core output of EP-01  
**Due:** Week 10 Friday

### Objective

Using the information gathered from EP-01-S01 through EP-01-S06, define the **quantitative success metrics** and **evidence thresholds** for each feature/milestone in the chosen scope. This sub-issue synthesises all the discovery work into the draft evidence requirements document.

### Inputs Required (from other sub-issues)

- [ ] **EP-01-S01:** Confirmed scope — which features/milestones we're implementing
- [ ] **EP-01-S02:** Codebase audit — what topics exist for measuring performance
- [ ] **EP-01-S03:** Team composition — UG vs PG requirements for evidence rigour
- [ ] **EP-01-S04:** HSL Rules 2026 — competition conditions that define test parameters
- [ ] **EP-01-S05:** Booster K1 specs — hardware constraints on feasible metrics
- [ ] **EP-01-S06:** Lab access — how many test sessions we can realistically run

### Tasks

- [ ] List every milestone and feature in the chosen scope (e.g., for Localisation: initial pose estimation, continuous localisation, recovery from kidnap)
- [ ] For each milestone, define:
  - The **success metric** (e.g., "localisation error < 15 cm in 80% of trials")
  - The **minimum number of trials** needed to claim the result
  - The **artifact types** required (bag file, CSV, video, screenshot)
  - The **conditions** under which the test must be run (competition field, lighting, opponent robots present/absent)
- [ ] Document **failure modes** — what would falsify the claim?
- [ ] Distinguish between **UG-level** and **PG-level** evidence requirements
- [ ] Get sign-off from all team members
- [ ] Create the deliverable: `evidence/requirements/evidence_requirements.md`

### Deliverable

`evidence/requirements/evidence_requirements.md` — the living document specified in EP-01.

### Dependencies

- All EP-01-S01 through EP-01-S06 must be complete
- Team-wide review and sign-off

---

## Dependency Graph

```
EP-01-S01 (Scope confirmation)
    ├── EP-01-S02 (Codebase audit)
    ├── EP-01-S03 (Team composition)
    ├── EP-01-S04 (HSL Rules research)
    ├── EP-01-S05 (Booster K1 specs)
    ├── EP-01-S06 (Lab access & ARA)
    └── EP-01-S07 (Success metrics — synthesises all above)
```

**Critical path:** S01 → S02/S03/S04/S05/S06 (parallel) → S07

---

## Suggested Labels

All sub-issues should use: `evidence`, `planning`, `information-gathering`

Additionally:
- S02: `infrastructure`, `ros2`
- S04: `research`
- S05: `hardware`
- S06: `logistics`
- S07: `requirements`
