---
title: "Mechanical Constraints and Subsystem Composition"
module: PM11
year: 11
lesson: "9.4"
kind: lesson
supplementary: supplementary.md
---

NARRATOR: Welcome back. Five minutes of recap first — spaced repetition is the engine of this series — and then we run our control algorithms into the hard wall of physical reality.

NARRATOR: The last three episodes built the Thinking. Episode one of the chapter: open versus closed loop — closed loops listen, open loops are blind, running Measure, Compare, Correct. Then autonomous control — deciding with no human in the loop, with the features S-D-A-F: Sensing, Decision, Adapt, Fail-safe. Then the patterns you write that decision logic with — above all the state machine, S-T-E-A: States, Transitions, Events, Actions, plus threshold control with hysteresis. So we can write a controller. But a controller commands physical hardware — and hardware has limits, and usually comes in pieces that must work together.

NARRATOR: That's today, and it closes the control chapter. The dot-point: "Experiment with software to control interactions and dependencies within mechatronic systems" — including motion constraints, degrees of freedom, the combination of subsystems, and the combination of sensors, actuators, and end-effectors into viable subsystems. Outcomes S-E-eleven-oh-one — planning and engineering the solution — and S-E-eleven-oh-two — structural elements in code.

NARRATOR: Objectives. By the end you'll be able to: define degrees of freedom and count them for a device; explain motion constraints and how software respects them; and explain how subsystems are combined into one coordinated system.

QUESTION: Start with a term you'll be asked to define. A door hinge can only swing one way; a drone can move up-down, left-right, forward-back, and rotate. How would you put a number on "how many ways can this thing move"?

NARRATOR: That number is the degrees of freedom — and here's the marquee definition: degrees of freedom, D-O-F, is the number of independent ways a system can move. A door hinge has one degree of freedom — rotation about a single axis. A 3D printer head has three — translation in X, Y, and Z. A gripper has one — open and close. A six-axis industrial arm has six — full position and orientation in space. The trick to counting them: count the independent movements, and usually each one has its own actuator driving it. Listing 1 models a robot arm with three joints and a gripper — that's four degrees of freedom — and you can see each degree of freedom is a separate axis the software controls.

QUESTION: So the software can move each joint independently — but can it move them anywhere it likes?

NARRATOR: No — and that's the second key idea: motion constraints. Every real mechanism has physical limits the software must respect. A joint can only rotate so far — a minimum and maximum angle. The arm can only reach so far out, and not too close in — a maximum and minimum reach, its workspace. There are payload limits and speed limits. And parts can collide. So the controller's job isn't just to compute a desired position — it must validate every commanded move against these constraints before sending it, or it'll drive a joint past its stop, or crash the arm into itself. In Listing 1, the arm model carries each joint's allowed angle range, and it rejects a command that's out of range — an elbow asked to bend to two hundred degrees when its limit is one hundred and thirty-five is refused. That check-before-you-move is exactly the kind of validation you met with sensor data, now guarding motion. Constraints are the limits the software must respect.

QUESTION: Pause the player and try this. Take a pan-and-tilt security camera — the kind that swivels left-right and tips up-down. How many degrees of freedom does it have, and name one motion constraint on it. Work it out, then play.

NARRATOR: Two degrees of freedom: pan, rotating left and right, and tilt, tipping up and down — two independent movements, each with its own motor. A motion constraint: each axis has a limited range — the tilt can't flip all the way over backwards, and the pan may not rotate a full continuous circle if its cable would wind up. You could also mention a speed limit so it doesn't jerk. The marks come from counting the independent movements correctly — two — and naming a genuine physical limit, like the angular range of an axis.

NARRATOR: Now the second half — combining subsystems. A real mechatronic system isn't one lump; it's several subsystems that must cooperate. A mobile manipulator robot might have a drive subsystem to move around, an arm subsystem to manipulate, and a vision subsystem to see. And here's the lovely connection: this is exactly the composition idea from the object-oriented module — has-a. The robot has-a drive, has-an arm, has-a vision system; each is a module behind a clean interface, and you compose them rather than welding everything into one tangle. Listing 2 does exactly that: a robot that holds three subsystems, each behind the same simple interface — command it, or stop it.

NARRATOR: But composition needs coordination, and there are principles, with a hook — one conductor, clean interfaces. One conductor means a single control authority: one coordinator decides what each subsystem does, so they don't fight each other. Clean interfaces means each subsystem talks through a clear, modular protocol, so you can swap one out without rewriting the rest. And critically, failure detection that spans them all: in Listing 2, one emergency stop propagates to every subsystem at once — they all halt together, because a robot where the arm keeps moving after the drive has faulted is dangerous. One conductor, clean interfaces, and a stop that reaches everything.

NARRATOR: Two more terms to lock in. A viable subsystem is a working combination of sensor, actuator, and end-effector — the S-A-E trio from the devices episode — that actually achieves a job: a vision sensor plus the arm's actuators plus a gripper makes a pick subsystem that can see and grab. And dependencies: when subsystems share a workspace, they can interfere — the arm could swing into the drive base, or two arms into each other — so their movements have a dependency, and the software must coordinate their timing and keep a safety margin so moving parts don't collide.

NARRATOR: Two threads. Backward: the control algorithm from last episode now runs inside these limits — the state machine commands a joint, but only within the constraints checked here; combining subsystems is the object-oriented has-a composition and the clean-interface idea applied to hardware instead of classes; and a viable subsystem is the S-A-E trio from Chapter Seven, working as a unit, sharing the power and wiring from Chapter Eight. Forward: this is the doorway to the build chapter — next we start programming and building for real, beginning with simulating and prototyping; then we integrate sensors, actuators, and end-effectors in code, which is this composition actually realised; and we drive multiple devices together, where coordinating subsystems earns its keep.

NARRATOR: Consolidate — takeaways. One: degrees of freedom, D-O-F, is the number of independent ways a system can move — count the independent movements, one actuator each. Two: motion constraints are the physical limits — joint ranges, reach, payload, speed, collisions — and the software must validate every move against them before acting. Three: combine subsystems by composition — has-a, behind clean interfaces — coordinated by one conductor: a single control authority, with failure detection that stops everything. Four: a viable subsystem is a working sensor-actuator-end-effector combination, and shared workspaces create dependencies you must coordinate. Listing 3 is your one-page reference.

NARRATOR: Now exam-style questions. Pen down, attempt before the model answer.

QUESTION: Question one. Define degrees of freedom, and state how many a six-axis robot arm has and why. Three marks.

NARRATOR: Degrees of freedom is the number of independent ways a system can move. A six-axis robot arm has six degrees of freedom because it has six independently controlled joints, which together allow it to position its end-effector anywhere in its reach and at any orientation — three for position and three for orientation in three-dimensional space. For three marks: define degrees of freedom as independent movements, state six, and justify it by the six independent joints giving full position and orientation.

QUESTION: Question two. Explain how software ensures a mechatronic system respects its motion constraints. Pause, write, then play.

NARRATOR: The software stores the physical limits of the system — such as each joint's minimum and maximum angle, the maximum and minimum reach, and speed limits — and before executing any commanded movement it validates the command against those limits, rejecting or clamping any motion that would exceed them. This prevents the system from driving a joint past its mechanical stop, over-reaching, or moving unsafely. The marks come from: the software holds the constraint values, and it checks each commanded move against them before acting, rather than blindly executing.

QUESTION: Question three. Explain how multiple subsystems are combined into a single coordinated mechatronic system.

NARRATOR: Multiple subsystems — for example drive, manipulation, and vision — are combined by composition: the overall system contains each subsystem as a module accessed through a clear, standard interface, so they remain independent but cooperate. Coordination is provided by a single control authority that issues commands to each subsystem and integrates their feedback, using defined communication protocols and shared safety handling such as a system-wide emergency stop. The mark-earning points: composition with clean modular interfaces, and a single coordinating authority managing the subsystems and their safety together.

QUESTION: Question four. Explain why mechanical interference must be considered when two subsystems share a workspace, and how it can be managed.

NARRATOR: When two subsystems share a workspace — for example a robot arm and the mobile base it sits on, or two arms — their movements are not independent: one can physically collide with the other, causing damage or failure. This dependency must be managed by coordinating their movements through the single controller, checking planned motions for collisions, and maintaining a safety margin between moving parts, so that only compatible movements happen at the same time. The mark is recognising the shared-workspace dependency and naming coordination, collision checking, or a safety margin as the management strategy.

NARRATOR: That closes the control chapter. Your algorithms now live in the physical world: they respect degrees of freedom and motion constraints, and they coordinate subsystems composed has-a behind clean interfaces, under one conductor, with a stop that reaches everything. We've designed the whole machine — sensing, thinking, acting, powered, wired, and coordinated. The final chapter is where we build it for real: simulating, implementing closed-loop control in code, integrating the devices, giving it a user interface, and unit-testing every piece. Next episode: simulations and prototypes for testing. See you there.
