---
title: "Supplementary Materials — Computing Hardware: Microcontrollers, CPUs and Registers"
module: PM11
year: 11
lesson: "7.2"
script: script.md
---

# Supplementary Materials

The read-along reference for the hardware lesson. Nothing here is spoken in the audio — the
narration points at each listing by label only. Listing 1 traces one Python line down to the
processor's steps; Listing 2 is a runnable model of the fetch-decode-execute cycle; Listing 3
is the revision reference table.

### Listing 1 — One line of Python, and what the processor actually does underneath (reference)
```text
THE PYTHON YOU WRITE (one line):
    total = reading_a + reading_b          # add two sensor readings

WHAT THE PROCESSOR DOES (several machine instructions, each one fetch-decode-execute):

  Step  Opcode        Plain meaning                          Register changed
  ----  -----------   ------------------------------------   ----------------------------------
  1     LOAD  25       put reading_a into the accumulator     DATA register (accumulator) = 25
  2     ADD   30       add reading_b to the accumulator       DATA register (accumulator) = 55
  3     STORE 10       copy the accumulator out to memory     ADDRESS register points at slot 10;
                                                              memory[10] = 55

  ADDRESS register = WHERE   (which memory slot, slot 10)
  DATA    register = WHAT    (the value being worked on, 25 then 55)

  Every step is one turn of the FETCH -> DECODE -> EXECUTE cycle:
    FETCH the instruction from memory · DECODE what it means · EXECUTE it · advance the program counter.
```

### Listing 2 — A runnable model of a processor running the fetch-decode-execute cycle (Python)
```python
class SimpleProcessor:
    """A simplified microcontroller core: registers + memory, running fetch-decode-execute."""

    def __init__(self):
        self.accumulator = 0                 # a DATA register — the value being worked on
        self.program_counter = 0             # an ADDRESS register — WHICH instruction is next
        self.zero_flag = False               # status flag set by COMPARE
        self.memory = [0] * 100              # 100 memory slots
        self.program = []

    def load_program(self, instructions):
        self.program = instructions
        self.program_counter = 0

    def fetch(self):
        # FETCH: read the instruction the program counter points at, then advance it.
        if self.program_counter < len(self.program):
            instruction = self.program[self.program_counter]
            self.program_counter += 1
            return instruction
        return None

    def decode_and_execute(self, instruction):
        # DECODE: split the opcode from its operand. EXECUTE: act on the registers/memory.
        opcode, *rest = instruction.split()
        if opcode == "LOAD":
            self.accumulator = int(rest[0])
        elif opcode == "ADD":
            self.accumulator += int(rest[0])
        elif opcode == "STORE":
            self.memory[int(rest[0])] = self.accumulator
        elif opcode == "COMPARE":
            self.zero_flag = (self.accumulator == int(rest[0]))

    def run(self):
        while True:
            instruction = self.fetch()       # FETCH
            if instruction is None:
                break
            self.decode_and_execute(instruction)   # DECODE + EXECUTE
        return self.accumulator


# Program: add three sensor readings (25 + 30 + 15), store the total, check it equals 70.
processor = SimpleProcessor()
processor.load_program([
    "LOAD 25",       # accumulator = 25
    "ADD 30",        # accumulator = 55
    "ADD 15",        # accumulator = 70
    "STORE 10",      # memory[10] = 70
    "COMPARE 70",    # zero_flag = True (it matched)
])
total = processor.run()

assert total == 70                     # final accumulator value
assert processor.memory[10] == 70      # stored where the address operand said
assert processor.zero_flag is True     # COMPARE 70 matched
print("Fetch-decode-execute simulation passed: total =", total)
```

### Listing 3 — Revision reference: microcontroller vs CPU, registers, instruction sets (reference)
```text
MICROCONTROLLER  vs  CPU
                      CPU (e.g. a laptop chip)        Microcontroller (e.g. Arduino, Pico)
  What it is          just the processor (the brain)  a WHOLE computer on one chip
  On the chip         the processing core only        CPU core + Memory + I/O pins (+ timers)
  Power / cost        high power, expensive            low power, cheap
  Operating system    runs Windows/Linux              usually none — starts instantly
  Best for            general computing                one dedicated control task
  -> In mechatronics, the microcontroller usually wins: low power, instant start, reliable, cheap.
     A microcontroller CONTAINS a CPU; it is not "a CPU". (Common trap.)

INSTRUCTION SET & OPCODES
  Instruction set = the full vocabulary of operations a processor understands.
  Opcode          = the numeric code for ONE operation (LOAD, ADD, STORE, COMPARE...).
  RISC = few, simple, fast instructions (most microcontrollers).  CISC = richer, more complex single instructions.

REGISTERS  (tiny, fastest stores INSIDE the processor — its workbench)
  ADDRESS register = WHERE : holds a memory location (e.g. the program counter = address of the next instruction)
  DATA    register = WHAT  : holds the value being worked on (e.g. the accumulator = result of a calculation)
  Status register          : flags about the last operation (zero? negative?)

THE HEARTBEAT:  FETCH -> DECODE -> EXECUTE  (F-D-E), millions/billions of times per second.

WHY IT SHAPES YOUR CODE: little memory + no OS + a fixed clock  =>  keep code lean, avoid heavy
libraries, mind timing. Tiny per-instruction costs matter in a real-time control loop.
```
