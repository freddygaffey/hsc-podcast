---
title: "Open and Closed Loop Control"
module: PM11
year: 11
lesson: "9.1"
kind: lesson
supplementary: supplementary.md
---

NARRATOR: Welcome back. Five minutes of recap first — spaced repetition is the engine of this series — and then we finally write the part we've been circling the whole module: the Thinking.

NARRATOR: The review episode closed the first half. You've got the spine, Sense-Think-Act; the four fields, S-M-E-M; the hardware — microcontroller versus central processing unit, the registers, fetch-decode-execute; the devices, the S-A-E trio, with the actuator-versus-end-effector distinction; the data, M-C-D-O, with diagnostic versus optimisation; and the power and wiring, including never running an actuator off a controller pin. Notice what we've built: the body of the machine and its data. What we have not written yet is its mind — the algorithm that decides what to do. That's this whole chapter.

NARRATOR: And the very first decision in control is a fork in the road. The dot-point: "Explore the algorithmic patterns, code, and applications for open and closed control systems." Outcomes S-E-eleven-oh-two — explaining how structural elements develop code — and S-E-eleven-oh-one — planning and engineering the solution. Open loop or closed loop: it's the most fundamental choice in control, and the marquee line for the whole chapter is this — closed loops listen; open loops are blind. Hold that.

NARRATOR: Objectives. By the end you'll be able to: define open-loop and closed-loop control and classify real systems as one or the other; explain feedback and the measure-compare-correct cycle; define setpoint, error, gain, and proportional control; and explain how gain affects stability.

QUESTION: Start simple. A microwave heats for the time you set, then stops — whether the food is scalding or still frozen. What's missing from that, compared to, say, a thermostat?

NARRATOR: What's missing is feedback. The microwave never checks the result — it runs a predetermined action and stops. That's open-loop control: it acts only on the input command, with no feedback from the output, so it cannot correct for anything going wrong. It's simple, cheap, and needs no sensor — but it's blind. A toaster on a timer, a garden sprinkler on a schedule, a basic 3D printer following a fixed path — all open loop. A thermostat, by contrast, measures the actual temperature and keeps adjusting to hold your target. That's closed-loop control, and the difference is feedback.

NARRATOR: Let me define closed loop properly, because this is the heart of the chapter. A closed-loop system continuously measures its output and adjusts to reach the desired result. Here's the cycle, and the hook is M-C-C: Measure, Compare, Correct. Measure the actual output with a sensor. Compare it to the setpoint — the target value — and the difference is the error: error equals setpoint minus measured. Then correct: change the actuator to reduce that error. Then loop back and measure again, forever. Measure, compare, correct. That feedback loop is exactly Sense-Think-Act with the result fed back into the next decision — the loop is closed because the output flows back to the input.

QUESTION: So how does it know how hard to push? If the room is ten degrees too cold versus half a degree too cold, surely it shouldn't react the same?

NARRATOR: Exactly right, and that's proportional control — the simplest and most important pattern. The correction is made proportional to the error: the bigger the error, the harder you push; as the error shrinks, you ease off. Ten degrees too cold, full power; half a degree off, a gentle nudge. The strength of that response has a name — the gain — how much actuator output you apply per unit of error. Proportional control with a sensible gain is the workhorse of closed-loop systems, and we'll build it for real in the implementation chapter.

NARRATOR: Listing 1 makes the whole thing concrete and runnable — an open-loop and a closed-loop heater, side by side, driving the same simple room model. The open-loop one runs full power for a fixed time and never looks; it sails straight past the target to nearly twenty-nine degrees when the goal was twenty-five — blind, and overshooting. The closed-loop one measures, computes the error against the setpoint, and corrects proportionally each step; it settles close to twenty-five and holds there, correcting itself. Same goal, same room — one listens, one's blind. Listing 2 writes that closed loop out as a NESA-style pseudocode algorithm: read the sensor, compute the error, and branch — too low, push harder; too high, ease off; within tolerance, hold. That measure-compare-correct loop is the examinable algorithm.

QUESTION: Time to test yourself. Pause the player. Classify each of these as open loop or closed loop, and say why: one, a coffee machine that brews for five minutes regardless; two, a robot vacuum that uses sensors to steer around furniture; three, a sprinkler that waters for thirty minutes every evening; four, car headlights that switch on based on how dark it is. Work through all four, then play.

NARRATOR: Here they are. One, the coffee machine: open loop — fixed time, no feedback about the coffee's strength. Two, the robot vacuum: closed loop — it senses obstacles and adjusts its path in real time. Three, the sprinkler: open loop — a fixed schedule, with no feedback about soil moisture or rain. Four, the headlights: closed loop — a light sensor's reading decides when they switch on. The test every time: is there a sensor feeding the result back to change the action? If yes, closed; if no, open. If you got all four with that reasoning, you've nailed the core skill of the lesson.

NARRATOR: One more concept, because it's where closed loops get hard — stability. Feedback in control is normally negative feedback, meaning the correction opposes the error and pulls the system back to target; that's what makes it stable. There's also positive feedback, which amplifies a change rather than opposing it — useful for things like oscillators, but destabilising in a control loop. And the gain matters enormously: too little gain and the system responds sluggishly, crawling to the target; too much gain and it overshoots, then over-corrects the other way, and can oscillate or even go unstable. Tuning the gain to be fast but stable is the central craft of closed-loop control — and a recurring exam point: high gain is not simply better.

NARRATOR: Two threads. Backward: that integrated thermostat from the review episode — reject a bad reading, smooth the data, decide the fan — was a closed loop in miniature; and the feedback it acts on is exactly the measurement and sensor data from the data chapter. Closed loop is also Sense-Think-Act with the loop joined up — the Sensing feeds the Thinking which drives the Acting which changes what's Sensed. Forward: next episode is autonomous control, which is a closed loop running with no human in the loop at all; then control patterns like state machines; and in the build chapter we implement a proportional closed-loop controller in real code and meet its upgrade, P-I-D. And a Year-Twelve warning we'll tell in full later: a famous automatic flight-control system acted on a single faulty sensor with nothing to cross-check it — a control system is only as trustworthy as the sensor feeding it.

NARRATOR: Consolidate — takeaways. One: open-loop control acts on a predetermined command with no feedback — simple, cheap, blind; closed-loop control measures its output and corrects — accurate, adaptive, more complex. Closed loops listen; open loops are blind. Two: the closed-loop cycle is Measure, Compare, Correct — error equals setpoint minus measured, and you correct proportionally to that error. Three: control uses negative feedback to stay stable; gain sets how hard it pushes — too little is sluggish, too much overshoots and oscillates. Four: classify any system by asking whether the result is fed back to change the action. Listing 3 is your one-page reference.

NARRATOR: Now exam-style questions. Pen down, attempt before the model answer.

QUESTION: Question one. Distinguish between open-loop and closed-loop control systems, giving an example of each. Four marks.

NARRATOR: An open-loop system executes a predetermined action based only on its input command, with no feedback from the output, so it cannot correct for disturbances — for example a microwave that heats for a set time regardless of the food's temperature. A closed-loop system measures its output and feeds that back to continuously adjust its action towards a target, correcting for disturbances — for example a thermostat that measures room temperature and switches heating to hold a setpoint. For four marks: define both, state that the key difference is feedback, and give a correct distinct example of each.

QUESTION: Question two. Explain the role of feedback in a closed-loop control system. Pause, write, then play.

NARRATOR: Feedback provides the system with information about its actual output, which it compares against the desired setpoint to compute the error. The controller uses that error to adjust the actuator — reducing the error each cycle — so the system can reach and maintain the target and correct for disturbances it could not have predicted. Without feedback the system would be open loop and blind to whether it was succeeding. The marks are for: feedback supplies the measured output, it's compared to the setpoint to find the error, and the error drives a correction — the measure-compare-correct loop.

QUESTION: Question three. Define setpoint and error, and explain what proportional control means.

NARRATOR: The setpoint is the target value the system is trying to achieve — for example a target speed or temperature. The error is the difference between the setpoint and the measured value — how far off the system currently is. Proportional control means the size of the correction is made proportional to the error: a large error produces a large corrective action, and as the error shrinks the correction eases off, so the system approaches the target smoothly. The mark-earning points: setpoint equals target, error equals setpoint minus measured, and proportional means correction scales with the error.

QUESTION: Question four. In a closed-loop system, explain what is likely to happen if the control gain is set too high.

NARRATOR: If the gain is too high, the system over-reacts to the error: it applies too large a correction, overshoots the setpoint, then over-corrects in the opposite direction, producing oscillation around the target rather than settling on it — and if the gain is high enough, the oscillations can grow and the system becomes unstable. The mark is recognising that excessive gain causes overshoot and oscillation or instability, so gain must be tuned to balance speed against stability — higher is not simply better.

NARRATOR: That's the fork at the start of control. Open loop acts blind on a fixed command; closed loop listens — it measures, compares to a setpoint, and corrects proportionally to the error, using negative feedback to stay stable. Closed loops listen; open loops are blind. We've given Sense-Think-Act its Think. Next episode we let the machine run that loop entirely on its own — autonomous control, and what an algorithm needs to make its own decisions safely. See you there.
