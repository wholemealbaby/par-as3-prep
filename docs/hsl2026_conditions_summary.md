# HSL 2026 Competition Conditions Summary

> **Source:** [`docs/hsl-rulebook.txt`](docs/hsl-rulebook.txt) — RoboCup Humanoid Soccer League 2026 Working Rules (DRAFT 2026-04-30)
> **Parent Issue:** [#17](https://github.com/wholemealbaby/par-as3-prep/issues/17) — EP-01-S04
> **Purpose:** Extract competition conditions relevant to evidence collection for the Booster K1 project.
> **Scope Component:** *(To be confirmed via EP-01-S01)*

---

## 1. Field Dimensions and Markings

### Field Sizes (Table 1, §1.6)

| Division | Field Type | Width (m) | Length (m) |
|----------|-----------|-----------|------------|
| Small    | S-Field   | 6         | 9          |
| Middle   | M-Field   | 6–9       | 9–14       |
| Large    | L-Field   | 9–14      | 14–22      |

The Booster K1 is an approved standard platform (§3.6) and falls under the **Middle Division** (Htop ≤ 1.25 m, §3.5.2). Middle Division can be played on the S-Field or M-Field.

### Exemplary M-Field Dimensions (Table 2, §1.6)

| ID | Description              | M-Field (m) |
|----|--------------------------|-------------|
| A  | Field length             | 14.0        |
| B  | Field width              | 9.0         |
| C  | Goal length (depth)      | 0.7–1.2     |
| D  | Goal width               | 2.4–2.6     |
| E  | Goal Area length         | 1.0         |
| F  | Goal Area width          | 4.0         |
| G  | Penalty Area length      | 3.0         |
| H  | Penalty Area width       | 6.0         |
| I  | Penalty Mark distance    | 2.0         |
| J  | Center Circle diameter   | 3.0         |
| K  | Border strip width (min) | 1.0         |
| L  | Corner Arc radius        | 0.5         |
|    | Line width               | 0.05–0.12   |
|    | Penalty/center mark size | 0.10–0.15   |

### Field Surface (§1.1)
- **Material:** Artificial turf, height 20–30 mm (Middle/Large) or 8–12 mm (Small)
- **Colour:** Green — must contrast well with field markings and ball; should not be very dark

### Field Markings (§1.2)
- **Colour:** White (tape, paint, or white turf)
- **Line width:** 5–12 cm, all lines same width
- **Lines belong to the areas they bound** — measurements from outside of lines (§1.6)

### Goals (§1.7, Table 3)
- **Middle Division goal dimensions:** Width 2.4–2.6 m, Height 1.5–1.9 m, Depth 0.7–1.2 m
- **Colour:** Goalposts and crossbar must be white
- **Nets:** White, gray, or black
- **Post/crossbar width:** 7–12 cm

### Key Implications for Testing
- Test field must be at least 9 m × 6 m (S-Field minimum for Middle Division)
- White lines on green turf — vision system must detect these reliably
- Goal dimensions constrain where goals appear in camera frame
- Centre circle diameter 3.0 m affects kick-off positioning rules

---

## 2. Lighting Conditions (§1.11)

### Official Rules
- **No mandated/controlled lighting** — venue-dependent
- Minimum **300 lx** (preferably **400 lx**) over most of the field
- Lighting may include **glare, brightness, shadows, or mixed lighting** that can change during a match
- Lighting must be **predominantly white** — coloured lighting that changes perceived colour of field/ball is not allowed
- Natural and non-natural light must be free to reach the field
- Fields should be placed near or under windows where possible
- Ceiling lights provided as necessary

### Key Implications for Testing
- **Vision systems must handle varying illumination** — test under multiple lighting conditions
- Shadows and glare are expected — include these in test scenarios
- No coloured/controlled lighting can be assumed
- Ball colour constancy under different lighting is critical
- **Test conditions should include:** bright overhead, overcast/dim, mixed (sunlight + artificial), and shadowed scenarios

---

## 3. Ball Type and Colour (§2)

### Ball Specifications by Division (Table 4)

| Division | Ball Type       |
|----------|-----------------|
| Small    | FIFA Mini Ball  |
| Middle   | **FIFA size 3 or 4** |
| Large    | FIFA size 5     |

> **Note:** The TC and OC will decide on only **one ball type per division** for the 2026 competition (§2.3).

### Ball Properties (§2.1)
- Must be **spherical**
- Made of or resembles leather or other suitable material
- Must match weight, form, movement characteristics, and appearance of a standard ball

### Key Implications for Testing
- For Middle Division, use a **FIFA size 3 or size 4** ball
- Standard orange/white colour scheme expected (typical RoboCup ball)
- Ball detection must work against green turf background
- Ball movement characteristics affect kicking tests — use official ball type

---

## 4. Robot Dimensions and Weight Limits (§3.5)

### Booster K1 Classification
The Booster K1 is an **approved standard platform** (§3.6, Table — Booster K1 listed with no restrictions).

### Size Restrictions (§3.5.2)

| Division | Max Height (Htop) |
|----------|-------------------|
| Small    | ≤ 1.1 m           |
| Middle   | ≤ 1.25 m          |
| Large    | ≤ 1.9 m           |

**Leg length:** 0.35·Htop ≤ Hleg ≤ 0.7·Htop
**Arm span:** 0.8·Htop ≤ Aspan ≤ 1.2·Htop
**Head height:** 0.1·Htop ≤ Hhead ≤ 0.3·Htop

### Weight Restrictions (§3.5.3)

| Division | Max Weight | BMI Range |
|----------|-----------|-----------|
| Small    | 15 kg      | 5–30      |
| Middle   | **25 kg**  | 5–30      |
| Large    | 80 kg      | 5–30      |

BMI = M / Htop² (M in kg, Htop in m)

### Body Design Requirements (§3.5.1)
- Human-like body shape: torso, head, two arms, two legs
- Human-like symmetry and proportions
- Must stand upright on feet, walk on legs, recover from falls
- Only allowed locomotion: bipedal walking, running, jumping
- Arms must permit human-comparable behaviours (getting up, throwing ball)
- Arms must **not** provide continuous support for locomotion

### Key Implications for Testing
- Booster K1 fits Middle Division — use Middle Division field dimensions
- Motion tests must respect the robot's physical capabilities
- Fall recovery is a required capability — include in robustness tests
- Weight limits affect what additional hardware (e.g., sensors) can be added

---

## 5. Rules for Kicking

### General Kicking Rules
- Kicking is an allowed soccer-related movement (§3.5.1)
- **Kick-off rules (§8.1):**
  - Ball placed on centre mark, stationary
  - A goal may **not** be scored directly from kick-off
  - If the kicking team has ≥3 robots on field, **two different robots** must touch the ball before scoring
  - If ≤2 robots, the kicking robot must touch the ball at least once **outside the centre circle** before scoring
- **Free kicks (§13):**
  - Direct free kick: goal can be scored directly (corner kick, goal kick, pushing free kick)
  - Indirect free kick: ball must be touched by another player first (kick-in/throw-in)
  - 45 s time limit to execute a free kick
  - Avoidance region = centre circle radius (1.5 m for M-Field)
- **Penalty kick (§14):**
  - 60 s time limit after play begins
  - Striker may not touch ball a second time after it has clearly moved
  - Goalkeeper must stay on goal line until striker touches ball

### Ball Holding (§12.2.6)
- Goalkeeper in own penalty area: **10 s** max hold
- All other robots: **5 s** max hold
- Ball is "held" if convex hull of robot covers >50% of ball
- Repeated quick release-and-hold treated as one continuous hold

### Key Implications for Testing
- Kicking tests should measure both distance and angular accuracy
- Test scenarios should include kick-off, free kick, and penalty kick conditions
- Ball holding time limits affect behaviour timing
- Two-touch rule for kick-off affects multi-robot coordination

---

## 6. Game Duration and Stoppage Rules (§7)

### Match Structure (§7.2)
- **Two halves** of **10 minutes** each (Playing state)
- **Half-time break:** minimum 10 minutes
- Teams change sides at half-time

### Game States (§7.1)
| State     | Duration | Key Behaviour |
|-----------|----------|---------------|
| Initial   | Before game | No locomotion; head movement/calibration allowed |
| Ready     | 45 s     | Move to positions; must reach legal positions before Set |
| Set       | Until whistle | Stationary; no leg movement (except standing up) |
| Playing   | 10 min   | Active play; all normal rules apply |
| Penalized | Variable | Removed from field; stationary outside; 30 s + 15 s increments |
| Finished  | —        | Cease all game-related activity |
| Stop      | As needed | Emergency stop; all motion ceases immediately |

### Allowance for Time Lost (§7.6)
- At head referee's discretion
- Announced in final minute of each half, in whole minutes
- Covers: substitutions, injuries, wasting time, external circumstances

### Timeout (§7.7)
- **Team timeout:** 1 per game, max 5 minutes
- **Referee timeout:** At head referee's discretion

### Mercy Rule (§7.8)
- Game ends when goal difference reaches **10**

### Ball Stop Rule (§7.10)
- If period would end while ball is in motion, period extends until ball stops or leaves field

### Key Implications for Testing
- Robot must operate autonomously for **10+ minutes** continuously
- Must handle state transitions (Initial → Ready → Set → Playing)
- Must respond to GameController commands
- Penalty timing (30 s base + 15 s increments) affects behaviour design
- Test scenarios should include full-duration runs

---

## 7. Technical Challenges

The spec ([`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md:136)) mentions technical challenges as part of the competition. The rulebook references technical challenges in the context of referee calls (§5.2.1, footnote 3):

> "The exception to this are technical challenges that depend on the calls as specified."

Technical challenges are separate competition events alongside the main soccer competition. They typically test specific robot capabilities (e.g., walking, kicking accuracy, obstacle avoidance). The rulebook does not provide detailed technical challenge specifications — these are published separately by the Organizing Committee.

### Key Implications for Testing
- If technical challenges are in scope, additional test scenarios beyond standard gameplay may be needed
- Technical challenges may have specific rules about referee calls and signals
- Check with course coordinator if technical challenges are part of the project scope

---

## 8. Network/Communication Rules (§3.9)

### Core Principle
- **Robots must act autonomously** during a game (§3.9)
- No external power supply, teleoperation, remote control, remote processing, or remote brain

### Wireless Communication (§3.9.2)
- WiFi via field-provided access point only
- Each team assigned a range of IP addresses
- Network config (IPs, channels, SSIDs, encryption) announced at competition
- **No other 2.4 GHz or 5 GHz radio equipment** (including Bluetooth) allowed close to the field
- Organizers provide wireless equipment and access points

### Robot-to-Robot Communication (§3.9.3)
- Allowed via field access points only — **ad-hoc mode prohibited**
- Messages must be sent via **UDP broadcast**
- **Max payload:** 512 B per message
- **Max messages:** 12,000 per game (in Ready, Set, Playing states only)
- Each team allocated one UDP port (10000 + team's GameController number)
- **Unicast communication prohibited**

### GameController Communication (§3.9.4)
- GameController broadcasts at **2 packets/second**
- Robots must respond to GameController messages and send status updates

### Debug Communication (§3.9.5)
- Each robot may send debug info via **single UDP packet** to one team device on wired network
- **Max 1 packet/second**
- Packet size within max UDP packet size (~64 kB)

### Key Implications for Testing
- **No off-board processing allowed** — all perception and decision-making must be on-board
- WiFi is available but restricted to field access point
- Communication budget limits (12,000 messages/game) affect multi-robot coordination design
- Evidence collection must use **on-board logging** — no external cameras for primary data
- Debug channel available at 1 packet/s for monitoring

---

## 9. Safety Requirements (§3.10)

### Dangerous Equipment (§3.10.1)
- No equipment dangerous to the player or others

### Physical Stop (§3.10.2)
- Robot handlers must be able to **immediately and physically stop** a robot at any time
- Teams must demonstrate this ability on request
- **Passive features:** Grips/handles on back for safe holding
- **Active features:** Physical button, emergency switch, or remote emergency button
- Remote emergency button: one per robot, no additional functions, worn around neck or belt

### GameController Stop (§3.10.3)
- Robots must comply with GameController protocol and immediately assume safe pose when commanded

### Key Implications for Testing
- All test sessions require a **safety stop mechanism** (physical button or remote E-stop)
- Test operators must be able to physically restrain the robot
- Emergency stop behaviour must be implemented and tested
- Risk assessment (ARA) must address these safety requirements

---

## 10. Constraints on Evidence Collection

### What is Allowed
- On-board cameras (RGB, stereo, event cameras) — §3.8.2
- On-board IMU, gyro, accelerometer — §3.8.4
- On-board microphones — §3.8.5
- On-board force/touch sensors — §3.8.6
- Debug communication (1 packet/s to team computer) — §3.9.5
- ROS bag recording on the robot's onboard computer
- External video recording of demonstrations (for report evidence)

### What is NOT Allowed (during competition)
- ❌ Off-board processing or remote brain — §3.9
- ❌ External cameras for robot perception — §3.7
- ❌ Teleoperation or remote control — §3.9
- ❌ Additional sensors beyond those originally installed — §3.7
- ❌ Compass/magnetic sensors — §3.8.4, Table 6
- ❌ Active depth sensors (discouraged, may be prohibited) — §3.8.3
- ❌ More than 4 one-dimensional distance sensors — §3.8.7
- ❌ Bluetooth or other 2.4/5 GHz radio near field — §3.9.2

### Implications for Evidence Collection
- **Primary evidence must come from on-board sensors and logging**
- External cameras can be used for **ground truth** and **demonstration video** but not as robot perception
- ROS bag files recorded on the robot's computer are the primary data source
- Debug channel (1 packet/s) can stream key metrics to a monitoring laptop
- Test scenarios should be recorded with an external camera for report figures/video

---

## 11. Summary of Key Parameters for Test Scenarios

| Parameter | Value | Source |
|-----------|-------|--------|
| Field size (Middle Div.) | 9–14 m × 6–9 m | §1.6, Table 1 |
| Exemplary M-Field | 14 m × 9 m | Table 2 |
| Centre circle diameter | 3.0 m | Table 2 |
| Penalty mark distance | 2.0 m | Table 2 |
| Goal dimensions (Middle) | W: 2.4–2.6 m, H: 1.5–1.9 m | Table 3 |
| Line width | 5–12 cm | §1.2 |
| Turf colour | Green | §1.1 |
| Line colour | White | §1.2 |
| Ball (Middle Div.) | FIFA size 3 or 4 | Table 4 |
| Lighting | ≥300 lx, uncontrolled, mixed | §1.11 |
| Game duration | 2 × 10 min halves | §7.2 |
| Ready state duration | 45 s | §7.1.2 |
| Penalty time | 30 s + 15 s increments | §12.2 |
| Free kick time limit | 45 s | §13.3.4 |
| Penalty kick time limit | 60 s | §14.1.1 |
| Ball hold (field player) | 5 s max | §12.2.6 |
| Ball hold (goalkeeper) | 10 s max | §12.2.6 |
| Max robot height (Middle) | 1.25 m | §3.5.2 |
| Max robot weight (Middle) | 25 kg | §3.5.3 |
| Max comms messages | 12,000 per game | §3.9.3 |
| Max UDP payload | 512 B | §3.9.3 |
| Debug channel rate | 1 packet/s | §3.9.5 |
| Max players (Middle Foundation) | 3 per team | Table 5 |
| Max players (Middle Advanced) | 5 per team | Table 5 |

---

## 12. References

- [`docs/hsl-rulebook.txt`](docs/hsl-rulebook.txt) — Full HSL 2026 rulebook
- [`docs/robocup_soccer_spec.md`](docs/robocup_soccer_spec.md) — Project specification
- [`docs/testing_and_evidence_plan.md`](docs/testing_and_evidence_plan.md) — Testing and evidence collection plan
- [HSL Rules 2026 Repository](https://github.com/RoboCup-HumanoidSoccerLeague/HSL-Rules/) — Official source
- [GameController Protocol](https://github.com/RoboCup-HumanoidSoccerLeague/GameController/) — GC message format
