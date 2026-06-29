---
title: "Module Review — Programming and Building Mechatronics"
module: PM11
year: 11
lesson: "7–10"
kind: module-review
supplementary: supplementary.md
---

NARRATOR: Welcome back — and welcome to the end. This is the whole-module review for Programming Mechatronics, Chapters Seven through Ten, and it's the capstone of Year Eleven: the third and final module of the preliminary course. No new content today. We consolidate the entire module, drill every mnemonic with retrieval, walk one real-world build from problem to tested system, and pull in the case studies. Get a pen — there's a lot of pausing. This review touches the full Year-Eleven outcome set, S-E-eleven-oh-one through oh-nine — the only module that exercises all nine.

NARRATOR: Here's the shape of the journey. Chapter Seven was foundations — what mechatronics is, the hardware, the devices. Chapter Eight was data and integration — the data, the power and wiring, accessibility. Chapter Nine was control algorithms — the thinking. Chapter Ten was programming and building — simulate, implement, integrate, interface, test. And one spine runs through all of it. Let's drill.

QUESTION: The spine first. What three-word cycle does every mechatronic system follow, and what four fields does a real build fuse?

NARRATOR: Sense-Think-Act, S-T-A — sense the world, think with an algorithm, act through actuators and end-effectors. And the four fields are S-M-E-M: Software, Mechanical, Electronics, Maths. Every single lesson hangs off those two. If they didn't come instantly, that's your first revision job.

QUESTION: Chapter Seven, rapid fire. Distinguish a microcontroller from a central processing unit. And distinguish an actuator from an end-effector.

NARRATOR: A central processing unit is just the processor; a microcontroller is a whole computer on a chip — C-M-I: a central-processing-unit core, Memory, and Input-output pins — so it contains a central processing unit rather than being one. And an actuator creates motion or force — the muscle, like a motor — while an end-effector is the tool that motion drives — the hand, like a gripper. The trio is S-A-E: Sensor, Actuator, End-effector. The processor runs on fetch-decode-execute, F-D-E, and remember: address registers hold where, data registers hold what.

QUESTION: Chapter Eight. Distinguish diagnostic data from optimisation data. And why can you never wire a motor straight to a controller's output pin?

NARRATOR: Diagnostic data asks "is it healthy?" — fault logs, error codes; optimisation data asks "can it do better?" — performance tuning; and the same numbers can be either, the purpose decides. The four streams are M-C-D-O: Measurement, Control, Diagnostic, Optimisation. And you never wire a motor to a controller pin because the pin supplies milliamps while a motor needs amps — you switch a driver fed from the main supply. Remember the wiring: power lines feed, data lines talk, on one common ground; the electrical basics are V-I-P, power equals voltage times current; and you size a battery with amp-hours over amps gives hours.

QUESTION: And the social one from Chapter Eight — what's the golden rule of accessible design, and the checklist?

NARRATOR: Design with users, not for them. The checklist is S-A-I-D: Safety, Adaptability, Independence, Diverse inputs and outputs — plus reliability and affordability. Offer alternative inputs and multi-modal feedback, V-A-H, Visual, Audio, Haptic; and remember the curb-cut effect — build for the margins and everyone benefits.

QUESTION: Chapter Nine, the thinking. Distinguish open-loop from closed-loop control, and name the features of an autonomous algorithm.

NARRATOR: Closed loops listen; open loops are blind. Open-loop acts on a fixed command with no feedback; closed-loop measures its output and corrects — Measure, Compare, Correct, M-C-C, where error equals setpoint minus measured. Autonomous control adds deciding with no human in the loop, and its features are S-D-A-F: continuous Sensing, Decision logic, Adapt by self-correcting, and Fail-safe. The decision logic is usually a state machine — S-T-E-A: States, Transitions, Events, Actions. And the physical limits: degrees of freedom, D-O-F, the independent ways a thing can move, within its motion constraints, composing subsystems under one conductor with clean interfaces.

QUESTION: Chapter Ten, the build. Why simulate before building? What do the three letters of P-I-D do? And what two things does a unit test check?

NARRATOR: Simulate first because it's S-C-F: Safe, Cheap, Fast. P-I-D — P for the present error, I for the past, which removes the steady-state offset, D predicts the future, which damps overshoot. And a unit test checks E-R: Effectiveness — does it reach its goal — and Repeatability — same input, same result every run, which is why you test against mocks, not hardware. Two more from the build: program to the interface, not the device, when you integrate; and design the control interface to be S-A-F-E — Status, Abort, Feedback, Errors. Listing 1 is the master mnemonic table with all of it, grouped by chapter — the single sheet to revise from.

NARRATOR: Now let's see it all work together, because the exam — and the real project — is a whole system, not one lesson. Picture the build: an accessible line-following delivery robot, carrying items along a marked path in a workplace. Walk it through Sense-Think-Act. It senses with line sensors — the S-A-E sensor. It thinks: an autonomous state machine decides which way to steer to stay on the line, self-correcting like a closed loop, with a fail-safe if it loses the line and an emergency stop. And it acts: drive motors move it, an end-effector carries the load. Listing 2 is the runnable heart of that robot — its decision core — and it ties the module together: autonomous decision logic, the fail-safe when the line is lost, and the emergency stop overriding everything, all checked by a unit test across every case. Effectiveness, fail-safe, and safety, in one tested component.

NARRATOR: And the full build is every chapter in sequence. Listing 3 walks it end to end: define the system and its dominant requirement; choose the microcontroller brain; pick the S-A-E devices; handle the data; budget the power and draw the wiring; design it accessibly, with users; design the control — open versus closed, autonomous, the state machine, within the degrees of freedom; simulate it safely; implement the closed-loop controller with P-I-D; integrate the devices through clean interfaces; give it a S-A-F-E user interface; and unit-test every component for effectiveness and repeatability, documenting the results. That sequence — from a real problem to a tested, documented system — is the whole module, and it's outcome S-E-eleven-oh-nine, managing and documenting a real build.

QUESTION: Pause the player — the integrated task. For that delivery robot, name one device for each part of Sense-Think-Act, and name one safety feature it must have and why. Work it out, then play.

NARRATOR: A strong answer. Sense: a line sensor, or light sensors, to detect the marked path — the sensor. Think: a microcontroller running the autonomous steering algorithm — the controller. Act: drive motors to move and steer — the actuators — and a tray or gripper to carry the delivery — the end-effector. And a safety feature: an emergency stop that halts it instantly, essential because it moves through a space with people who might step into its path; or a fail-safe that stops it when it loses the line, so it doesn't career off. The marks come from one device in each Sense-Think-Act role and a safety feature tied to the real risk of a robot moving among people.

QUESTION: The case studies tie this together. What does each of the three cautionary tales teach about mechatronics?

NARRATOR: Three stories, three lessons. The aircraft system, the 737 MAX, acted on a single faulty sensor with nothing to cross-check it — autonomy is only as trustworthy as its sensors, and one input with no redundancy is a deathtrap. The Therac-25 radiation machine trusted software control with missing safety interlocks and inadequate testing — a control system that moves real-world energy must have hardware safeguards and be tested on its failure paths, not just the happy path. And the DARPA Grand Challenge — self-driving cars that all failed in the desert one year and succeeded the next — shows autonomy is engineered through relentless simulation and iteration, not got right first try. Sensors and redundancy, safety and testing, simulate-and-iterate — the whole module's warnings in three stories.

NARRATOR: Consolidate — the module in four lines. One: every mechatronic system is Sense-Think-Act across the four S-M-E-M fields, built from S-A-E devices on a microcontroller. Two: it runs on data — M-C-D-O — and real power and wiring, designed accessibly, with users. Three: its thinking is control — closed loops that listen, autonomous S-D-A-F, state machines, within degrees of freedom. Four: you build it by simulating first, implementing P-I-D control, integrating to interfaces, giving it a S-A-F-E interface, and unit-testing for effectiveness and repeatability. Listing 1 is the exam-dump; Listing 3 is the build checklist.

NARRATOR: Now exam-style questions across the whole module. Pen down, attempt before the model answer.

QUESTION: Question one. Define a mechatronic system and explain the Sense-Think-Act cycle, using an example. Four marks.

NARRATOR: A mechatronic system is an integrated system combining mechanical components, electronics, and software-based control — the S-M-E-M fields — to sense its environment, make decisions, and act on the physical world. It follows the Sense-Think-Act cycle: it senses through sensors, thinks by running a control algorithm on a microcontroller, and acts through actuators and end-effectors. For example, an automatic door senses approach with a motion sensor, decides to open if the path is clear, and acts by driving a motor. For four marks: define it across the integrated fields, name the three stages, and map them to a concrete example.

QUESTION: Question two. A team is building an autonomous robot that moves among people. Explain three things they must do to make it safe. Pause, write, then play.

NARRATOR: First, fail-safes and an emergency stop: the system must detect problems — a lost signal, a sensor fault — and enter a safe state, with an always-available emergency stop, since no human supervises every moment. Second, robust sensing and not trusting a single input: validate and filter sensor data, and avoid depending on one sensor with no cross-check — the lesson of the aircraft case. Third, thorough testing of failure paths: unit-test the control and safety logic against faulty and boundary inputs in simulation, not just the normal case — the lesson of the Therac-25. The marks come from three distinct, justified safety measures — interlocks and emergency stop, trustworthy sensing, and failure-path testing.

QUESTION: Question three. Distinguish open-loop from closed-loop control, and explain why a closed-loop controller might use P-I-D rather than proportional control alone.

NARRATOR: Open-loop control executes a fixed command with no feedback, so it cannot correct for disturbances; closed-loop control measures its output and continuously corrects toward a setpoint — closed loops listen, open loops are blind. A closed-loop controller uses P-I-D rather than proportional alone because proportional control leaves a steady-state error — it settles near but not on the target — so the integral term is added to accumulate that residual error and eliminate the offset, and the derivative term to damp overshoot and oscillation. The marks: open versus closed is the presence of feedback, and P-I-D's integral removes the steady-state error proportional control leaves.

QUESTION: Question four. Explain how simulation and unit testing together make a mechatronic system safe and reliable to build. Five marks.

NARRATOR: Simulation lets developers model the system in software and test control code against it without hardware — safely, cheaply, and quickly, S-C-F — so dangerous and edge-case behaviours can be explored and most bugs caught before any device runs. Unit testing then verifies each component's control algorithm in isolation for effectiveness, that it achieves its goal, and repeatability, that it behaves identically every run — using simulated devices behind clean interfaces so the tests are fast, safe, and repeatable, and covering boundary and faulty inputs and failure paths, not just the normal case. Documented together, they give evidence the system works and the confidence to change it. For five marks: simulation tests logic safely before hardware; unit tests check effectiveness and repeatability in isolation with mocks; both cover edge and failure cases; and documentation provides evidence and supports safe change.

NARRATOR: And that completes Programming Mechatronics — and with it, the whole of Year Eleven. You can take a real problem and engineer a mechatronic system end to end: Sense-Think-Act across the four fields; the hardware, devices, data, power, and accessible design; the control — closed loops, autonomy, state machines, within physical constraints; and the build — simulate, implement P-I-D, integrate to interfaces, a S-A-F-E interface, and unit-tested, documented components. Your algorithms left the screen and learned to move the world. Into Year Twelve, these threads carry forward: autonomy and control become artificial intelligence and automation in Software Automation; safety and safe data become Secure Software Architecture; and the discipline of building, managing, and documenting a real system becomes the Software Engineering Project. You've built the foundation. Now go build on it.
