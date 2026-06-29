---
title: "Module Review — Mechatronic Hardware and Data"
module: PM11
year: 11
lesson: "7–8"
kind: module-review
supplementary: supplementary.md
---

NARRATOR: Welcome back. This is a review episode — the first checkpoint of the mechatronics module, pulling together Chapters Seven and Eight. No new content today; instead we consolidate the foundations and the data layer, drill the mnemonics with retrieval practice, and walk one integrated example. This is the half-time whistle before we start writing control algorithms. Get a pen — there's a lot of pausing.

NARRATOR: Here's the map of where we've been. Chapter Seven was foundations: what mechatronics is, the hardware that runs it, and the devices that sense and act. Chapter Eight was data and integration: the data those devices produce, the power and wiring that drive them, and designing for the people who use them. Across these two chapters we've touched five Year-Eleven outcomes — S-E-eleven-oh-one through oh-five: planning and engineering, structural elements, hardware, safe data, and the social and ethical side. Underneath all six lessons is one spine, and that's where we start.

QUESTION: First retrieval. What is the spine that every single mechatronic system follows — the three-word cycle — and what are the four fields a real build draws on?

NARRATOR: The spine is Sense-Think-Act, S-T-A: a sensor senses the world, the controller thinks by running an algorithm, an actuator or end-effector acts on the world. And the four fields are S-M-E-M — Software, Mechanical, Electronics, and Maths. If you froze and couldn't produce those, that's your signal to relisten to episode one before going on — everything hangs off this.

NARRATOR: Chapter Seven, lesson two was the brain. Let me drill the distinctions, because the exam lives on them.

QUESTION: Distinguish a microcontroller from a central processing unit. And separately: what's the difference between an address register and a data register?

NARRATOR: A central processing unit is just the processor. A microcontroller is a whole computer on a chip — your hook was C-M-I: a central-processing-unit core, Memory, and Input-output pins — so a microcontroller contains a central processing unit, it isn't merely one. And the registers: an address register holds where — a memory location, like the program counter — while a data register holds what — a value, like the accumulator. Address is where, data is what. The processor runs through opcodes from its instruction set on the fetch-decode-execute beat, F-D-E.

QUESTION: Lesson three, the devices. Here's the distinction examiners reach for most: what's the difference between an actuator and an end-effector? And while you're at it — name the three motion sensors we covered.

NARRATOR: An actuator creates motion or force — it's the muscle, like a motor or a hydraulic piston. An end-effector is the tool that motion drives — the hand, like a gripper. A motor is an actuator; the gripper it opens and closes is the end-effector. The trio is S-A-E — Sensor, Actuator, End-effector. And the three motion sensors: the passive-infrared sensor for movement, the accelerometer for tilt and acceleration, and the encoder for precise position. To choose any component you weigh P-C-R-I — Performance, Cost, Reliability, Integration — then decide on the dominant requirement.

QUESTION: Now Chapter Eight. The data chapter's headline distinction: what's the difference between diagnostic data and optimisation data?

NARRATOR: Diagnostic data answers "is it healthy?" — fault logs, error codes, used to detect and fix problems. Optimisation data answers "can it do better?" — performance history used to tune. And the subtle point worth the top mark: the same numbers can be either — the purpose decides. The four streams overall are M-C-D-O: Measurement, Control, Diagnostic, Optimisation. Data is obtained by polling or interrupts — polling asks, interrupts tell — then processed by calibrating, filtering, and validating, and stored safely with a Timestamp, Identity, and Units, T-I-U.

QUESTION: Lesson two of Chapter Eight, power and wiring. Two-parter. What's the one equation for power? And why can you never wire a motor straight to a controller's output pin?

NARRATOR: Power equals voltage times current — watts equals volts times amps, the V-I-P relationship. And you never wire a motor to a controller pin because the pin can supply only a few milliamps while a motor needs amps — hundreds of times more; you'd do nothing or destroy the pin. Instead the pin's small signal switches a driver that feeds the motor from the main supply. Remember the wiring picture: power lines feed, data lines talk, on one common ground; and when sizing a battery, amp-hours over amps gives hours, with the actuator dominating the power budget.

QUESTION: And lesson three, accessibility. What is the golden rule of accessible design, and what does the checklist S-A-I-D stand for?

NARRATOR: The golden rule is design with users, not for them — consult the real users throughout. And S-A-I-D is Safety, Adaptability, Independence, and Diverse inputs and outputs — plus reliability and affordability in your back pocket. Offer alternative inputs — switch, voice, eye-gaze — and multi-modal feedback, V-A-H, Visual, Audio, Haptic; and design universally, because the curb-cut effect means building for the margins helps everyone. Listing 1 is the full master mnemonic table for both chapters — the single sheet to revise from.

NARRATOR: Now let's see the threads working together, because the exam loves a scenario that crosses lessons. Listing 2 is one integrated, runnable example — a thermostat. Watch how many chapters it touches. It takes a temperature reading — that's measurement data from a sensor, Chapter Seven and eight-point-one. It rejects a wild out-of-range reading as a fault — that's the diagnostic, validate step. It smooths the good readings with a moving average — the filter step. And then it makes a decision: the fan runs only while the smoothed temperature is above the setpoint — that's the Think, the controller deciding the actuator. Sense, clean, decide. In the listing, a stream that settles above the setpoint turns the fan on; one that sits below leaves it off; and a glitch reading is thrown away before it can do harm. That little class is the whole first half of the module in one object — and it's a direct preview of the closed-loop control we build next chapter.

QUESTION: Your turn — the integrated task. Pause the player. Picture an automatic plant-watering robot: it checks soil moisture and waters a pot when the soil is dry. Name its Sensor, its Actuator, and its End-effector; then name one data line and one power line you'd draw in its wiring diagram. Work it out, then play.

NARRATOR: A strong answer. Sensor: a soil-moisture sensor — that's the Sense, producing measurement data. Actuator: a pump or a motor that drives water — the mover. End-effector: the nozzle or watering spout that actually delivers the water — the tool at the end. For the wiring: a data line carries the moisture sensor's reading into the controller — thin, low current; a power line carries the supply to the pump — and because the pump is a hungry actuator, it gets its own power path switched by a driver, not run off a controller pin. If you named one device in each of the three S-A-E roles and separated a data line from a power line, that's the full set of marks. Notice you just used Chapter Seven's devices and Chapter Eight's wiring in one answer — that's exactly the integration examiners want.

NARRATOR: Listing 3 is your key-terms checklist, lesson by lesson — tick each box you can explain without notes; the ones you can't are tonight's revision.

NARRATOR: Now a few full exam-style questions across the two chapters. Pen down, attempt before the answer.

QUESTION: Question one. Outline the fetch-decode-execute cycle, and explain the role of registers within it. Four marks.

NARRATOR: The fetch-decode-execute cycle is how a processor runs a program: it fetches the next instruction from the memory address held in an address register, the program counter; decodes the opcode to determine the operation; and executes it, typically working with values in data registers such as the accumulator, before the program counter advances to the next instruction and the cycle repeats. Registers are the fast internal stores the processor works in — address registers hold the locations, data registers hold the values. For four marks: name the three stages, and explain both register types with the program counter and accumulator as examples.

QUESTION: Question two. A robotic system reads a distance sensor and drives a motor. Explain two ways the system handles its data safely and reliably, referring to processing and storage. Pause, write, then play.

NARRATOR: First, processing: each raw reading is validated against a sensible range and filtered with a moving average, so a single glitched or noisy reading is rejected or smoothed out rather than causing the motor to react wrongly. Second, storage: readings are logged with a timestamp, the sensor's identity, and units, in a consistent format, with backups of calibration data — so the data can be interpreted and the system diagnosed later. The marks come from naming a specific processing step and a specific safe-storage practice, each tied to why it matters — validation and filtering against bad readings, timestamp-identity-units for usable logs.

QUESTION: Question three. Explain why an actuator such as a motor requires a separate power supply path from the microcontroller, and how this is achieved in a wiring diagram.

NARRATOR: A motor draws far more current than a microcontroller's output pin can supply — amps versus milliamps — so powering it from the pin would fail or damage the controller. It needs a separate power path drawn from the battery's own supply line. In the wiring diagram this is achieved by running the motor on its own power line and having the controller's signal switch a driver — a transistor or motor-driver — that connects that power line to the motor; the controller decides, the driver delivers. The mark-earning points: the current mismatch, and a driver fed from the main supply switched by the control signal.

QUESTION: Question four. A company is designing a powered exoskeleton to help people with limited mobility walk. Describe two specialist requirements that should shape its design, and justify each. Four marks.

NARRATOR: One: robust, redundant safety with low-force emergency stops and force limiting — justified because the device physically moves a person who may not be able to react to a fault quickly, so it must fail safe and be stoppable with minimal effort. Two: adaptability to the individual — adjustable fit, strength of assistance, and pace — justified because users differ in body size and ability and their needs change, so a one-size setting would exclude people or be unsafe. You could also cite reliability, since the user depends on it to move, or designing with users through trials. For four marks: two distinct requirements, each tied to a specific feature of this user and task — not generic usability.

NARRATOR: That's the first half of Programming Mechatronics consolidated. You can define a mechatronic system on the Sense-Think-Act spine across the four S-M-E-M fields; you know the hardware — microcontroller versus central processing unit, registers, fetch-decode-execute; the devices — the S-A-E trio, actuator versus end-effector; the data — M-C-D-O, diagnostic versus optimisation, obtained, processed, and stored safely; the power and wiring — power lines versus data lines, never an actuator off a pin; and accessible design — S-A-I-D, with users not for them. We have the body of the machine and its data. Next chapter we write its mind: control algorithms — open and closed loops, and autonomous control. That's where Sense-Think-Act finally gets its Think. See you there.
