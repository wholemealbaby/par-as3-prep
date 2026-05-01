# RoboCup Soccer — Project Specification

## General Assignment Information

**Course:** Programming Autonomous Robots  
**Course Codes:** COSC2781 (PG) | COSC2814 (UG)  
**Semester:** Semester 1 2026  
**Assessment Type:** Group Assessment  
**Weight:** 50% of the final course mark  

### Key Dates

| Event | Date |
|---|---|
| Project Selection | No later than Thursday Workshop in Week 9 |
| Progress Update | During Workshops in Week 12 |
| Demonstration | During Week 15 (by appointment) |
| Report Due | 23:59, Sunday June 21st 2026 (Week 15) |

### Learning Outcomes (CLOs 1–5)

- **CLO1:** Discuss and critically analyse software architectures and algorithms for solving typical problems in autonomous robot systems; discuss and critically analyse the strengths and limitations of these architectures and algorithms.
- **CLO2:** Discuss and critically analyse the challenges of designing and developing software for a variety of robot systems of different complexities, including noise, uncertainty, and computational power.
- **CLO3:** Research, discuss, and use new and novel algorithms for solving problems with autonomous robot systems.
- **CLO4:** Use pre-existing robot software to solve common problems on simulated and real-world robots; develop and implement new algorithms and software for solving problems on simulated and real-world robots; integrate this software in the ROS framework.
- **CLO5:** Develop skills for further self-directed learning in the general context of software, algorithms, and architectures for autonomous robot systems; adapt experience and knowledge to and from other computer science contexts such as artificial intelligence, machine learning, and software design.

### Group Work

- Groups of **3–4 students** (UG and PG students may be mixed).
- Individual contributions are graded separately — record each member's contribution in the report.
- Use suitable group work tools (MS Teams, Task Planner/Trello, Git Repository).
- Work closely together so every team member understands all parts of the final system.

### Use of AI Tools

- AI tools may be used for ROS2 boilerplate code, node templates, package/configuration files, syntax checking, and debugging compilation errors.
- All AI use **must be acknowledged and referenced**.
- A **log of generative AI use** must be submitted with the assessment.
- Work significantly produced by AI without attribution may result in academic misconduct allegations.

---

## Assessment Requirements (Applies to All Projects)

### 1. Investigation and Research

- Research algorithms/techniques related to your project.
- Implement and adapt existing techniques to your particular needs.
- Record findings and cite relevant research in your report.

### 2. Original Implementation

- Complete an **original implementation** of at least one significant element of the autonomous software.
- Work cannot consist entirely of off-the-shelf software (e.g., existing ROS2 packages).
- The original implementation may:
  - Significantly modify or adapt existing techniques and algorithms for practical use on a robot.
  - Be a novel implementation of your own creation.

### 3. Robot Software Architecture

- Choose an appropriate robot software architecture (e.g., SPA, Subsumption, or three-tier architecture).
- Describe and justify your choice in the report.
- Show that your project adheres to this architecture.

### 4. Autonomy

- Your software should be **fully autonomous** unless the project scope says otherwise.

### 5. Open-ended Exploration

- Projects are open-ended — more complex solutions displaying more sophisticated autonomous software will receive higher grades.

### 6. Demonstration & Analysis

- Complete a live demonstration of your autonomous software.
- Provide an analysis in your report that:
  - Highlights strengths and capabilities.
  - Identifies limitations or weaknesses.
- Collect evidence to support the capability of your project.

### 7. Report

- Structure similar to a research paper:
  - Introduction
  - Related Work (Existing Methods)
  - Methodology
  - Results
  - Analysis & Evaluation
  - Conclusion
- Include data tables and figures (legible at 100% PDF zoom and in black-and-white).
- **Format:** No more than 10 pages, single column, ≥1.5 cm margins, ≥11 pt font.

### 8. Risk Assessments

- Complete an **Activity Risk Assessment (ARA)** before development activities begin.
- ARA must be approved by the course coordinator before work can commence.

### 9. Working in Other Labs

- May require working in the VXLab (Ground floor, Building 91) or Bundoora spaces.
- Requires coordination with staff, completing inductions, and complying with safety requirements.

---

## PG vs UG Requirements

### ROS2 Infrastructure & Robot Software Architecture (UG)

- Some platforms require UG students to implement additional infrastructure to enable working with the platform.
- This includes data structures and ROS2 nodes that enforce the flow of sensing information and behaviour generation.

### Extended/Additional Algorithm Implementation (UG)

- UG students are expected to implement **multiple solutions** to their project if the infrastructure implementation is not sufficiently significant.
- Scope discussed with the course coordinator on a per-project basis.

### Experimental Design and Evaluation (PG)

- PG students must design an experiment that explicitly highlights both the **strengths** and **limitations** of their work.
- The standard of evaluation should collect evidence, including repeatable statistical measures, sufficient for a published article.
- PG students must propose their experiment methodology during the **Week 12 progress update**.

### Grading of PG/UG Students in the Same Group

- Each student is graded according to the rubric for their level of study.
- All students in the group generally receive the same grade for overlapping rubric components.
- Students of the same study level receive the same grades for their level-specific components.

---

## RoboCup Soccer Project (Section 4.2)

### Overview

Enable the **Booster K1** robots to compete in the **RoboCup HSL 2026 competition**. See the [HSL Rules 2026](https://github.com/RoboCup-HumanoidSoccerLeague/HSL-Rules/) for details. The competition includes both the soccer competition proper and technical challenges.

### Scope

In negotiation with the course coordinator, this project will select a **component of the rules** to complete. The following aspects are available:

1. **Localisation** — Localisation of the robot on the soccer field.
2. **Robot Vision & Detection** — Detection of field features, ball, and other robots.
3. **Motion** — Reliable movement and kicking.

### Existing Codebase

- You **must** use the existing **RedBackBots RoboCup codebase**.
- This codebase already contains a defined robot software architecture, which **is not permitted to be modified** to prevent interference with preparations for the RoboCup competition held in July 2026.

### UG Requirements

- Since the architecture cannot be modified, UG students will need to explore **multiple solutions** to their problem.

### PG Requirements

- PG students must consider how to effectively design an experiment for **competition conditions**.

### Demonstration

- You must demonstrate your final code on the **Booster K1 robot** under **competition conditions**.

---

## Demonstrations

### Week 12 Progress Demonstration

- Show that the project is on-track according to the project scope.
- Demonstrate components for a **minimally viable solution**.
- Discuss:
  - A feasible plan for completion.
  - Improvements beyond the minimally viable solution.
  - Intended deliverables for the final demonstration.
  - (UG) Extended infrastructure, architecture, and/or implementation plans.
  - (PG) Proposed experimental evaluation.
- Submit on Canvas:
  - A complete copy of your current software.
  - Your plan for completion.
  - A record of evidence of your individual work.

### Final Demonstration (Week 15)

- Show that the project meets the scoped requirements.
- Distinguish your original implementation from existing literature/software/dependencies.
- Showcase the capabilities of your implementation.
- (UG) Discuss/showcase extended infrastructure, architecture, and/or implementation.
- (PG) Discuss/showcase the results of your experimental evaluation.
- Be well-prepared with minimal time lost for setup, configuration, and restarts.

---

## Marking Guidelines

| Component | Weight |
|---|---|
| **Progress Update — Demonstration** | 10/50 |
| **Final Demonstration — Implementation** | 10/50 |
| **Final Demonstration — Evaluation & Results** | 5/50 |
| **Individual Contribution** | 5/50 |
| **Report — Methodology** | 5/50 |
| **Report — Analysis & Evaluation** | 10/50 |
| **Report — Writing & Referencing** | 5/50 |

---

## Submission

- Submit via **Canvas** following the submission instructions provided there.
- **Late submissions:** 10% penalty per day up to 5 business days, after which all marks are lost.
- Extensions given only in exceptional cases (refer to Special Consideration process).
