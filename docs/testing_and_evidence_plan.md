# RoboCup Soccer — Testing & Evidence Collection Plan

> **References:** [`robocup_soccer_spec.md`](robocup_soccer_spec.md), [`assignment_spec.txt`](assignment_spec.txt)  
> **Project:** RoboCup HSL 2026 — Booster K1  
> **Scope Component:** *(Select one: Localisation | Vision & Detection | Motion)*

---

## 1. Purpose

This document outlines a systematic plan for **collecting evidence** through **structured testing** to support the claims made in the final report. The evidence gathered here directly feeds into the **Results** and **Analysis & Evaluation** sections of the report (worth **15/50 marks** combined).

Each test is designed to:

- Demonstrate **strengths and capabilities** of the implementation.
- Expose **limitations and weaknesses** (required for PG experimental design).
- Produce **repeatable, statistical measures** suitable for a published article (PG requirement).
- Provide **visual evidence** (screenshots, logs, plots, video stills) for the report.

---

## 2. Evidence Collection Framework

### 2.1 Types of Evidence

| Type | Format | Use in Report |
|------|--------|---------------|
| **Quantitative metrics** | Tables, plots, histograms | Results section |
| **Qualitative observations** | Annotated screenshots, video stills | Analysis section |
| **ROS bag recordings** | `.bag` files (replayable) | Supplementary / demo backup |
| **Log files** | `.csv`, `.txt` | Raw data for statistical analysis |
| **Video recordings** | `.mp4` (robot POV + external) | Demonstration supplement |

### 2.2 Tools for Data Capture

- **ROS2 CLI:** `ros2 bag record` for topic data (odometry, vision detections, cmd_vel).
- **Custom logging nodes:** Write a lightweight node that logs timestamps, key state variables, and results to CSV.
- **Screen recording:** OBS Studio or `ffmpeg` for external camera footage.
- **Robot's onboard camera:** Record raw and annotated video streams.

### 2.3 Repeatability & Statistical Rigour

- Each test scenario must be run a minimum of **N ≥ 10 trials** (or as specified per test).
- Report **mean**, **standard deviation**, **min**, and **max** for all quantitative metrics.
- For PG: include **confidence intervals** and/or **statistical significance tests** (e.g., paired t-test when comparing two methods).

---

## 3. Test Categories

Tests are organised by the three possible scope components. Select the tests relevant to your chosen component.

---

### 3.1 Localisation Tests

**Goal:** Evaluate the robot's ability to estimate its pose (x, y, θ) on the field under competition conditions.

#### Test L1 — Static Localisation Accuracy

| Parameter | Value |
|-----------|-------|
| **Description** | Place the robot at known, marked positions on the field. Record estimated pose from the localisation system. Compare to ground truth. |
| **Ground truth** | Manual measurement from field markings (grid lines, centre circle, penalty area). |
| **Metric** | Euclidean distance error (m) = √((x̂ − x)² + (ŷ − y)²); heading error (rad) = |θ̂ − θ|. |
| **Trials** | 10 positions × 5 repeats = 50 measurements. |
| **Conditions** | Static robot, good lighting, no occlusions. |

#### Test L2 — Dynamic Localisation Drift

| Parameter | Value |
|-----------|-------|
| **Description** | Command the robot to follow a known path (e.g., straight line 2 m, 90° turn, square loop). Record estimated trajectory vs. expected path. |
| **Metric** | Final position error (m), cumulative drift (m/m travelled). |
| **Trials** | 10 runs per path type. |
| **Conditions** | Flat, clean field surface; slow speed (~0.3 m/s). |

#### Test L3 — Localisation Under Occlusion

| Parameter | Value |
|-----------|-------|
| **Description** | Introduce temporary visual occlusions (another robot, person standing near field lines). Measure how pose estimate degrades and whether it recovers. |
| **Metric** | Error during occlusion (m), recovery time (s) to return to <0.1 m error. |
| **Trials** | 10 occlusion events per scenario. |
| **Conditions** | Vary occlusion duration (2 s, 5 s, 10 s). |

#### Test L4 — Re-localisation After Kidnapping

| Parameter | Value |
|-----------|-------|
| **Description** | "Kidnap" the robot (pick it up and place it elsewhere on the field). Measure time and accuracy of re-localisation. |
| **Metric** | Re-localisation success rate (%), time to converge (s), final error (m). |
| **Trials** | 20 kidnap events across different field locations. |
| **Conditions** | Robot starts from lost state; global localisation required. |

---

### 3.2 Vision & Detection Tests

**Goal:** Evaluate the robot's ability to detect field features, the ball, and other robots.

#### Test V1 — Ball Detection Range & Precision

| Parameter | Value |
|-----------|-------|
| **Description** | Place the orange ball at known distances (0.5–5.0 m) directly in front of the robot. Record whether the ball is detected and the estimated (x, y) position. |
| **Metric** | Detection rate (%), false-positive rate (%), distance estimation error (m), angular error (rad). |
| **Trials** | 10 distances × 10 repeats = 100 measurements. |
| **Conditions** | Uniform green field background; vary lighting (bright, overcast, shadowed). |

#### Test V2 — Ball Detection in Clutter

| Parameter | Value |
|-----------|-------|
| **Description** | Place the ball near field lines, other robots, or field markings. Measure detection performance in visually cluttered scenes. |
| **Metric** | Detection rate (%), false-positive rate (%), precision–recall curve. |
| **Trials** | 10 clutter configurations × 10 repeats. |
| **Conditions** | Competition-like clutter (lines, robots, goalposts). |

#### Test V3 — Field Feature Detection

| Parameter | Value |
|-----------|-------|
| **Description** | Evaluate detection of goalposts, field lines, corners, and penalty area markings. |
| **Metric** | Per-feature detection rate (%), localisation accuracy of detected features (m). |
| **Trials** | 5 field zones × 10 frames per zone = 50 measurements. |
| **Conditions** | Robot stationary at different field positions. |

#### Test V4 — Robot Detection

| Parameter | Value |
|-----------|-------|
| **Description** | Place another Booster K1 (or obstacle) at known positions. Measure detection of other robots. |
| **Metric** | Detection rate (%), distance/heading estimation error. |
| **Trials** | 8 positions × 5 repeats = 40 measurements. |
| **Conditions** | Static and moving target robot; varying distances (1–4 m). |

#### Test V5 — Frame Rate & Latency

| Parameter | Value |
|-----------|-------|
| **Description** | Record the camera frame rate and the end-to-end latency from image capture to published detection topic. |
| **Metric** | Mean FPS, 95th-percentile latency (ms), dropped-frame rate (%). |
| **Trials** | 3-minute continuous recording, repeated 3 times. |
| **Conditions** | Normal operation; also test under high CPU load. |

---

### 3.3 Motion Tests

**Goal:** Evaluate the robot's ability to move reliably, walk, and kick.

#### Test M1 — Walking Speed & Stability

| Parameter | Value |
|-----------|-------|
| **Description** | Command the robot to walk forward at increasing speed settings. Measure actual ground speed and observe stability (falls). |
| **Metric** | Achieved speed (m/s) vs. commanded speed, fall rate (falls per 10 m). |
| **Trials** | 5 speed levels × 10 runs = 50 runs. |
| **Conditions** | Flat field surface; straight-line walking. |

#### Test M2 — Turning Accuracy

| Parameter | Value |
|-----------|-------|
| **Description** | Command the robot to turn by specified angles (30°, 45°, 90°, 180°). Measure actual heading change. |
| **Metric** | Angular error (deg) = |commanded − achieved|, standard deviation across trials. |
| **Trials** | 4 angles × 10 repeats = 40 measurements. |
| **Conditions** | Stationary start; turn in place. |

#### Test M3 — Walking to a Target Point

| Parameter | Value |
|-----------|-------|
| **Description** | Command the robot to walk to a specified (x, y) target on the field. Measure final position error. |
| **Metric** | Final Euclidean error (m), path length vs. straight-line distance (efficiency), completion time (s). |
| **Trials** | 8 target positions × 5 repeats = 40 runs. |
| **Conditions** | No obstacles; targets at 1–4 m distance. |

#### Test M4 — Kicking Accuracy & Power

| Parameter | Value |
|-----------|-------|
| **Description** | Place the ball at the robot's feet. Command a kick toward a target zone. Measure where the ball stops. |
| **Metric** | Angular deviation from target (deg), distance travelled (m), success rate (ball enters target zone). |
| **Trials** | 3 target directions × 20 kicks = 60 kicks. |
| **Conditions** | Ball stationary; robot stationary; vary kick type (left foot, right foot). |

#### Test M5 — Walking on Different Surfaces

| Parameter | Value |
|-----------|-------|
| **Description** | Test walking on the competition carpet, hard floor, and slightly uneven surfaces (if available). |
| **Metric** | Speed (m/s), fall rate, gait stability (IMU pitch/roll variance). |
| **Trials** | 3 surfaces × 10 runs = 30 runs. |
| **Conditions** | Same commanded speed across all surfaces. |

---

## 4. Integrated / System-Level Tests

These tests evaluate how components work together under competition-like conditions.

#### Test S1 — Ball Approach & Kick

| Parameter | Value |
|-----------|-------|
| **Description** | Place the ball at varying positions relative to the robot. The robot must detect the ball, walk to it, and kick it toward a goal. |
| **Metric** | End-to-end success rate (%), time from start to kick (s), final ball placement accuracy. |
| **Trials** | 20 trials with randomised ball positions. |
| **Conditions** | Ball within 3 m; no obstacles. |

#### Test S2 — Localise, Navigate, Detect, Kick

| Parameter | Value |
|-----------|-------|
| **Description** | Full pipeline: robot starts at a known position, localises, navigates to the ball, detects it, approaches, and kicks. |
| **Metric** | Overall success rate (%), per-stage timing, failure mode analysis. |
| **Trials** | 15 full runs. |
| **Conditions** | Competition-like field setup. |

#### Test S3 — Robustness to Disturbances

| Parameter | Value |
|-----------|-------|
| **Description** | Introduce disturbances during operation: push the robot slightly, block its camera briefly, change lighting. |
| **Metric** | Recovery time (s), success/failure of the overall task. |
| **Trials** | 5 disturbance types × 5 runs = 25 runs. |
| **Conditions** | Disturbances applied at random times during execution. |

---

## 5. Data Recording Template

For each test, create a CSV log with the following columns (adapt as needed):

```
trial_id, timestamp, metric_name, metric_value, condition, notes
```

Example for Test L1:

```
1, 00:00.000, euclidean_error_m, 0.082, position_A, good_lighting
1, 00:00.000, heading_error_rad, 0.031, position_A, good_lighting
2, 00:05.000, euclidean_error_m, 0.095, position_A, good_lighting
...
```

### Summary Table Template

| Test ID | Metric | Mean | Std Dev | Min | Max | N |
|---------|--------|------|---------|-----|-----|---|
| L1 | Euclidean error (m) | 0.087 | 0.021 | 0.052 | 0.134 | 50 |
| L1 | Heading error (rad) | 0.034 | 0.012 | 0.011 | 0.062 | 50 |
| ... | ... | ... | ... | ... | ... | ... |

---

## 6. Evidence for Report Sections

| Report Section | Relevant Tests | Evidence to Include |
|----------------|----------------|---------------------|
| **Methodology** | All | Description of test setup, parameters, and rationale. |
| **Results** | L1–L4, V1–V5, M1–M5, S1–S3 | Summary tables, plots (bar charts, box plots, scatter plots), key statistics. |
| **Analysis & Evaluation** | All | Compare against baselines (if multiple methods implemented — UG requirement). Discuss failure cases. Highlight strengths and limitations. |
| **Conclusion** | S1–S3 | Overall system capability summary. |

---

## 7. PG-Specific: Experimental Design

PG students must design an experiment that:

1. **Explicitly highlights limitations** — e.g., Test L3 (occlusion) or Test V2 (clutter) are designed to probe the boundaries of performance.
2. **Produces publishable-quality evidence** — include statistical tests (t-test, ANOVA) comparing performance across conditions.
3. **Is proposed during Week 12** — document the experimental methodology here and prepare a short presentation.

### Suggested PG Experiment: "Impact of Visual Occlusion on Localisation Accuracy"

- **Hypothesis:** Localisation error increases significantly (p < 0.05) when >30% of the field view is occluded.
- **Independent variable:** Occlusion level (0%, 15%, 30%, 50% of camera FOV).
- **Dependent variables:** Position error (m), heading error (rad), recovery time (s).
- **Statistical test:** One-way ANOVA with post-hoc Tukey HSD.
- **Expected outcome:** Quantify the degradation and demonstrate the robot's ability to recover.

---

## 8. Timeline & Milestones

| Week | Activity | Deliverable |
|------|----------|-------------|
| 9 | Define scope; set up RedBackBots codebase | Scope agreement |
| 10 | Implement core algorithm; write logging nodes | Basic logging infrastructure |
| 11 | Run preliminary tests (L1, V1, M1) | Preliminary results |
| 12 | **Progress update** — show MVP + test plan | Demo + test plan document |
| 13 | Run full test suite; collect all data | Raw data + ROS bags |
| 14 | Analyse data; produce plots and tables | Draft Results section |
| 15 | **Final demo** + submit report | Final demonstration + report |

---

## 9. Checklist

- [ ] Scope component selected and agreed with course coordinator.
- [ ] Logging nodes implemented (CSV output, ROS bag recording).
- [ ] Test environment prepared (field markings, ball, obstacles).
- [ ] Baseline measurements taken (e.g., ground-truth field dimensions).
- [ ] All relevant tests executed with N ≥ 10 trials.
- [ ] Raw data saved and backed up.
- [ ] Summary statistics computed.
- [ ] Plots and tables generated for the report.
- [ ] Failure cases documented (video, screenshots, logs).
- [ ] PG: Statistical analysis completed.
- [ ] PG: Experimental methodology presented in Week 12.

---

*Document version 1.0 — Adapt as the project scope is finalised.*
