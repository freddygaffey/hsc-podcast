---
title: "Implementing Closed Loop Control"
module: PM11
year: 11
lesson: "10.2"
kind: lesson
supplementary: supplementary.md
---

NARRATOR: Welcome back. Five minutes of recap first — spaced repetition is the engine of this series — and then we write a real closed-loop controller and make it genuinely good.

NARRATOR: Last episode was simulation — simulate before you build, because it's S-C-F: Safe, Cheap, Fast. We learned to model the system in software, the plant, validate it against known results, and test control code against it with no hardware. And back in the control chapter we met the closed loop itself — Measure, Compare, Correct — error equals setpoint minus measured, with feedback keeping it on target, and a warning that too much gain causes overshoot and oscillation. Today those two threads meet: we implement a closed-loop controller in real code, and we tune it safely in the simulation.

NARRATOR: This is the heart of the build chapter. Two dot-points at once: "Design, develop and implement programming code for a closed loop control system," and "Implement specific control algorithms that enhance the performance of a mechatronic system." Outcomes S-E-eleven-oh-seven — implementing safe and secure solutions — S-E-eleven-oh-two — structural elements in code — and S-E-eleven-oh-eight — applying language structures to refine code, which is exactly what "enhance performance" means.

NARRATOR: Objectives. By the end you'll be able to: implement a proportional closed-loop controller in code; explain its main limitation; and refine it into a P-I-D controller that performs better — and say what each of the three terms does.

NARRATOR: Start with the simplest real controller — proportional control. Listing 1 implements it, and it's just the Measure-Compare-Correct loop turned into code. Each cycle: read the sensor for the measured value; compute the error as setpoint minus measured; set the command to a gain times that error — the proportional gain decides how hard you push; and then, crucially, clamp that command to the actuator's safe range before sending it. That clamp is outcome S-E-eleven-oh-seven in one line — a safe, secure implementation never lets a big error drive the actuator past its limit. In the listing, a proportional controller drives a simulated heater from eighteen degrees toward a setpoint of twenty-five.

QUESTION: But run it and there's a catch. The heater climbs, slows, and settles — but it settles at about twenty-four point four, not twenty-five. It's stuck just short of the target. Why would proportional control never quite arrive?

NARRATOR: Because with proportional control alone, the only thing producing output is the error itself — so the output can only stay non-zero if the error stays non-zero. As the temperature approaches the setpoint, the error shrinks, so the push shrinks, until the push is just enough to hold it a little below target, balancing the heat loss. That permanent gap is called steady-state error — a steady offset the proportional controller can't close, because closing it would remove the very error producing the output. Proportional control gets you close, but not exactly there. To fix it, we refine the algorithm — and that refinement is the famous P-I-D controller.

NARRATOR: P-I-D stands for Proportional, Integral, Derivative, and here's the hook for what the three terms do — P for the present, I for the past, D predicts the future. The Proportional term reacts to the present error, as before. The Integral term sums up the past error — it accumulates how long and how far you've been off — and that accumulation keeps growing while any offset remains, driving extra output until the steady-state error is gone. That's the term that finally closes the gap. And the Derivative term looks at how fast the error is changing — it anticipates, easing off as you approach the target so you don't overshoot and oscillate. P present, I past, D predicts the future.

NARRATOR: Listing 2 is the refinement — the same controller with the integral and derivative terms added. This is outcome S-E-eleven-oh-eight in action: taking working code and refining its structure to enhance performance. Run it and the difference is clear: where the proportional-only version stalled at twenty-four point four, the P-I-D version settles right on twenty-five — the integral term has eliminated the steady-state offset — and it barely overshoots on the way, peaking only a fraction above target because the derivative term damps the approach. Offset gone, overshoot tiny. That progression — start with proportional, add integral to kill the offset, add derivative to smooth the approach — is the standard way you enhance a control algorithm.

QUESTION: Pause the player and reason it out. A proportional controller for a drone's altitude always settles about half a metre below the target height. Which of the three P-I-D terms would fix that, and why? Work it out, then play.

NARRATOR: The integral term. The half-metre gap is a steady-state error — a persistent offset that proportional control alone can't remove, because the shrinking error gives a shrinking push. The integral term accumulates that persistent error over time, and as the accumulation grows it adds exactly the extra output needed to lift the drone the last half-metre and hold it at the target, driving the steady-state error to zero. The marks come from naming the integral term and explaining that it accumulates the persistent error to eliminate the offset — not just "it makes it more accurate."

NARRATOR: Two practical points to carry. First, always clamp the output — every controller in the listings limits its command to the actuator's safe range, because a controller that can command an impossible or dangerous output is a safety bug, not just a performance one. Second, tuning. The gains — how strong each term is — have to be chosen, and get them wrong and you're back to the overshoot and oscillation from the control chapter: too much gain and it hunts around the target instead of settling. And this is exactly why the previous episode mattered — you tune those gains in the simulation, safely and in seconds, before the controller ever drives real hardware.

NARRATOR: Two threads. Backward: this is the closed loop from the control chapter — Measure, Compare, Correct — finally written as code, with the gain and overshoot ideas from there made concrete; the clamp is the actuator limit from the power-and-wiring episode; and we tune it in the simulation from last episode. Forward: next we integrate this controller with the actual sensor and actuator devices in code — driving real, or simulated, hardware; and in the testing episode we unit-test the controller, asserting it reaches the setpoint, exactly as the listings here already do. Into Year Twelve, this measure-and-correct discipline underpins the control and automation you'll meet again.

NARRATOR: Consolidate — takeaways. One: a closed-loop controller in code is the Measure-Compare-Correct loop — read the sensor, compute error as setpoint minus measured, set the command proportional to the error, clamp it, and drive the actuator. Two: proportional control alone leaves a steady-state error — it settles close to, but not on, the target. Three: P-I-D refines it — P for the present, I for the past which removes the offset, D predicts the future which damps overshoot. Four: always clamp the output, and tune the gains safely in simulation. Listing 3 is your one-page reference with the pseudocode.

NARRATOR: Now exam-style questions. Pen down, attempt before the model answer.

QUESTION: Question one. Describe how a proportional closed-loop controller calculates its output each cycle. Three marks.

NARRATOR: Each cycle, the controller reads the measured value from a sensor, calculates the error as the setpoint minus the measured value, and sets its output to the proportional gain multiplied by that error — so a larger error produces a larger corrective output. The output is then limited to the actuator's safe range before being applied. For three marks: read-and-find-error, output equals gain times error, and the output is applied to the actuator, ideally mentioning that it's clamped to a safe range.

QUESTION: Question two. Explain the main limitation of proportional-only control and how it can be overcome. Pause, write, then play.

NARRATOR: The main limitation is steady-state error: because the output is proportional to the error, as the system nears the setpoint the error and therefore the output shrink, leaving a small permanent offset where the reduced output just balances the system's losses, so it never quite reaches the target. It is overcome by adding an integral term — making it a P-I controller or full P-I-D — which accumulates the persistent error over time and adds output until that offset is driven to zero. The marks are for naming steady-state error, explaining why proportional control causes it, and giving the integral term as the fix.

QUESTION: Question three. State what the proportional, integral, and derivative terms of a P-I-D controller each respond to.

NARRATOR: The proportional term responds to the present error — the current difference between setpoint and measured value. The integral term responds to the accumulated past error — the sum of error over time — which eliminates steady-state offset. The derivative term responds to the rate of change of the error — how fast it is changing — which reduces overshoot and oscillation by anticipating the approach to the target. The mark-earning summary: P is the present error, I is the accumulated past error, D is the rate of change — present, past, and future.

QUESTION: Question four. Explain why a control algorithm should limit, or clamp, its output, referring to safety.

NARRATOR: A controller can compute a very large output when the error is large — for example at startup — but actuators have physical limits, and commanding beyond them can damage hardware, cause unsafe motion, or have no effect while the controller's internal state grows unchecked. Clamping the output to the actuator's safe minimum and maximum ensures the command is always physically valid and safe, which is part of implementing a safe and secure solution. The mark is linking the possibility of an excessive command to a safety or hardware risk, and clamping as the safeguard.

NARRATOR: That's a real, good closed-loop controller. You implement the Measure-Compare-Correct loop as proportional control, clamp the output for safety, then refine it into P-I-D — P for the present, I for the past that kills the steady-state offset, D predicts the future and damps the overshoot — and you tune it safely in simulation. Next episode we wire this brain to the body in code: integrating the sensors, actuators, and end-effectors so the controller actually drives the devices. See you there.
