---
title: "User Interfaces for Control"
module: PM11
year: 11
lesson: "10.4"
kind: lesson
supplementary: supplementary.md
---

NARRATOR: Welcome back. Five minutes of recap first — spaced repetition is the engine of this series — and then we hand the controls to a human.

NARRATOR: Last episode we integrated the devices: the controller drives the sensors, actuators, and end-effector through clean interfaces — program to the interface, not the device — so the system is modular and testable, running the S-A-E sequence, sense then act then effect, in order. Before that, the brain: a P-I-D closed-loop controller. And the machine can run autonomously — deciding with no human in the loop. But "no human in the loop" is rarely the whole story: someone usually has to start it, watch it, command it, and stop it. That human-facing layer is the user interface, and it's today's topic.

NARRATOR: The dot-point: "Design, develop and implement a user interface, a U-I, to control a mechatronic system." Outcomes S-E-eleven-oh-six — applying tools and resources to design and develop — and S-E-eleven-oh-seven — implementing safe and secure solutions. And this is where accessibility, from the data chapter, comes back, because a control interface is exactly something that must work for everyone.

NARRATOR: Objectives. By the end you'll be able to: explain what a control user interface is and the forms it takes; design one using a clear set of principles; and explain why safety features like an emergency stop and command validation belong in the interface.

QUESTION: Start with what it's for. Your robot works perfectly on the inside — it senses, thinks, and acts. Why does it still need a user interface at all?

NARRATOR: Because the interface is the system's voice — it's how a person tells the system what to do and understands what it's doing. Without it, even a perfect machine is a black box: you can't command it, and worse, you can't tell whether it's about to do something dangerous. Control interfaces come in many forms, from the simplest to the richest: a single status light; a command-line interface, where you type commands, which is precise and easy to log; physical buttons and indicators on a panel; or a full graphical dashboard on a screen. Different forms, same job — commands in, status out.

NARRATOR: So how do you design a good one? Here's a hook that's also the priority list — S-A-F-E. S, Status: always show clearly what the system is doing — never hide its state from the operator, because an operator who can't see what the machine is doing can't keep it safe. A, Abort: an emergency stop that is always available, obvious, and takes minimal force — it must halt the system instantly, no matter what it's doing. F, Feedback: turn raw sensor data into information the operator actually understands, and flag faults and warnings rather than burying them. And E, Errors: validate every command before it acts — reject unsafe or invalid input with a clear message, and confirm genuinely dangerous actions. Status, Abort, Feedback, Errors — and the whole thing spells what a control interface must be: safe. Plus, from the accessibility episode: design it with users, and offer alternative inputs and multi-modal feedback so everyone can operate it.

NARRATOR: Listing 1 builds the commands-in half — a command-line control panel for the system. You type a command, and notice what it does with it. A move command isn't trusted blindly: it's validated — the right number of arguments, an actual number, and within a safe range — and anything that fails is rejected with a clear error, never sent to the machine. The stop command always works, immediately, and once stopped, every motion command is refused until you reset — the abort and the safe-state behaviour built right into the interface. And a status command reports the system's state on demand. That's S-A-F-E in working code: status, abort, validated errors, all in one small handler.

NARRATOR: Listing 2 is the status-out half — taking the sensor readings and formatting them into clear feedback for the operator. And it does the one thing you must never forget: when a sensor has no reading — a fault — it flags it with a warning, rather than quietly showing nothing. Hiding system state is the dangerous mistake; a good interface surfaces a problem loudly, because the operator can only act on what they can see.

QUESTION: Pause the player and design a little. You're building the control interface for a robot arm that moves near people. Name two features the interface must have, and say why each matters for safety. Work it out, then play.

NARRATOR: Strong features. One — an emergency stop that's always available and instant: because the arm moves near people, the operator must be able to halt it immediately the moment something looks wrong, without hunting through menus or pressing hard. Two — a clear, live status display: the operator needs to see what the arm is doing and any fault or warning, because you cannot react to a hazard you can't see. You could also name command validation — rejecting an unsafe move before it executes — or accessible controls so any operator can use them. The marks come from naming a genuine interface feature and tying it to the specific safety reason — not just "make it user-friendly."

NARRATOR: One more design idea worth a mark. The interface is a layer on top of the control logic, not the logic itself. A command-line "move" command and a graphical "Move" button issue the very same underlying command; a printed status line and an on-screen gauge show the very same sensor value. So you design the control logic once, and the user interface — text, buttons, or graphical — is a skin over it. That separation is why you can build a simple text interface first to test the system, then add a polished graphical one later without changing how the machine works underneath.

NARRATOR: Two threads. Backward: this is the manual, human-control complement to the autonomous control from the control chapter — even a fully autonomous system needs an interface to monitor, override, and stop it; the emergency stop is the safety mechanism from the power and accessibility episodes, now in software; command validation is the never-trust-a-raw-value rule from the data episode, applied to operator input; and accessibility — design with users, alternative inputs, multi-modal feedback — comes straight from the accessible-design episode. Forward: next episode we unit-test components like this command handler, asserting it rejects bad commands exactly as the listing does; and in Year Twelve, user-interface design — usability and accessibility — is assessed in the software engineering project.

NARRATOR: Consolidate — takeaways. One: a control user interface is the system's voice — commands in, status out — and comes in forms from a status light to a command line to a graphical dashboard. Two: design it S-A-F-E — Status always visible, an Abort that's always available, clear Feedback that flags faults, and Errors caught by validating commands — plus accessible for all users. Three: never hide system state; surface faults loudly. Four: the interface is a skin over the control logic, so the same model drives a text or a graphical version. Listing 3 is your one-page reference.

NARRATOR: Now exam-style questions. Pen down, attempt before the model answer.

QUESTION: Question one. Describe three features that a user interface for controlling a mechatronic system should have. Three marks.

NARRATOR: One: a clear status display that shows what the system is currently doing and any warnings, so the operator always understands its state. Two: an emergency stop that is always accessible and halts the system immediately, so the operator can prevent harm at any moment. Three: command validation, which checks operator input and rejects unsafe or invalid commands with a clear message before they reach the hardware. Other valid features include accessible controls and clear feedback from sensor data. For three marks, name three distinct features, each with its purpose — not just a list of words.

QUESTION: Question two. Explain why an emergency stop is an essential feature of a control interface. Pause, write, then play.

NARRATOR: An emergency stop is essential because a mechatronic system can behave unexpectedly or encounter a hazard — a person in the way, a fault, a wrong command — and the operator must be able to halt all motion instantly to prevent injury or damage. It must be always available, obvious, and operable with minimal effort, so it works even in a panic and even when the rest of the interface is busy or unresponsive. The marks are for: systems can become dangerous, the operator needs an immediate always-available way to stop them, and that this overrides whatever the system is doing.

QUESTION: Question three. Explain why a control interface should always display the system's state, and the risk of hiding it.

NARRATOR: A control interface should display the system's state so the operator can understand what the system is doing and detect problems early enough to respond — for example seeing a rising temperature or a failed sensor before it causes harm. The risk of hiding state is that the operator is left blind: a developing fault goes unnoticed until it becomes a failure or a danger, and the operator cannot make informed decisions or intervene in time. The mark-earning point: visible state enables monitoring and timely intervention, whereas hidden state prevents the operator from detecting and responding to problems.

QUESTION: Question four. Explain how validating commands in the user interface contributes to the safety of a mechatronic system.

NARRATOR: Validating commands means the interface checks each operator input — its format, type, and whether its values are within safe limits — before passing it to the control system, and rejects anything invalid or unsafe with a clear message. This prevents an erroneous or dangerous command, such as a move beyond the system's safe range or a malformed instruction, from ever reaching the actuators, where it could cause damage or unsafe motion. The mark is recognising that validation stops bad input at the interface so it never drives the hardware — the same never-trust-raw-input principle applied to the operator.

NARRATOR: That's the human layer. A control interface is the system's voice — commands in, status out — designed to be S-A-F-E: Status always visible, an Abort always available, clear Feedback that flags faults, and Errors caught by validating every command, all accessible to every user. And it's a skin over the control logic, so one model can drive a text or a graphical version. The machine can now be commanded and watched safely. One episode left: unit testing — proving each piece works, and works the same way every time. See you there.
