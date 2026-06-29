---
title: "Supplementary Materials — Analysing Written Algorithms (Logic, Structure, Connections)"
module: PF11
year: 11
lesson: "2.6"
script: script.md
---

# Supplementary Materials

The worked algorithm, its connection map, two completed trace tables, and runnable code.
Nothing here is spoken in the audio — it's the read-along reference. The narration points at
each by label only. Diagrams are drawn in text (no images, per the format).

### Listing 1 — Student Course Management System (NESA pseudocode, abridged)
```text
BEGIN StudentCourseManagement
    WHILE systemRunning = true DO
        choice ← DisplayMenuAndGetChoice()                 // FUNCTION

        IF choice = "enroll" THEN
            studentID ← GetStudentID()                     // FUNCTION
            courseCode ← GetCourseCode()                    // FUNCTION
            canEnroll ← CheckEnrollmentEligibility(studentID, courseCode)  // FUNCTION
            IF canEnroll = true THEN
                ProcessEnrollment(studentID, courseCode)    // PROCEDURE
                DisplayConfirmation("Enrollment successful")// PROCEDURE
            ELSE
                reason ← GetEnrollmentBlockReason(studentID, courseCode)   // FUNCTION
                DisplayError("Cannot enroll: " + reason)    // PROCEDURE
            ENDIF

        ELSE IF choice = "withdraw" THEN
            studentID ← GetStudentID()
            courseCode ← GetCourseCode()
            isEnrolled ← CheckCurrentEnrollment(studentID, courseCode)     // FUNCTION
            IF isEnrolled = true THEN
                allowed ← CheckWithdrawalDeadline(courseCode)              // FUNCTION
                IF allowed = true THEN
                    ProcessWithdrawal(studentID, courseCode)               // PROCEDURE
                    DisplayConfirmation("Withdrawal successful")
                ELSE
                    DisplayError("Withdrawal deadline has passed")
                ENDIF
            ELSE
                DisplayError("Student not enrolled in this course")
            ENDIF

        ELSE IF choice = "viewEnrollments" THEN
            studentID ← GetStudentID()
            enrollments ← GetStudentEnrollments(studentID)                 // FUNCTION
            DisplayEnrollmentList(enrollments)                            // PROCEDURE

        ELSE IF choice = "exit" THEN
            systemRunning ← false
        ENDIF
    ENDWHILE
END StudentCourseManagement

BEGIN FUNCTION CheckEnrollmentEligibility(studentID, courseCode)
    hasPrerequisites   ← CheckPrerequisites(studentID, courseCode)
    hasCapacity        ← CheckCourseCapacity(courseCode)
    noConflicts        ← CheckScheduleConflicts(studentID, courseCode)
    notAlreadyEnrolled ← NOT CheckCurrentEnrollment(studentID, courseCode)
    RETURN hasPrerequisites AND hasCapacity AND noConflicts AND notAlreadyEnrolled
END FUNCTION
```

### Listing 2 — Subprogram connection map (call hierarchy + data dependencies)
```text
CALL HIERARCHY (who calls whom), grouped by role:

  [ Main Algorithm ]
        |
        |-- USER INTERFACE (procedures + input functions)
        |     DisplayMenuAndGetChoice() · GetStudentID() · GetCourseCode()
        |     DisplayConfirmation() · DisplayError() · DisplayEnrollmentList()
        |
        |-- VALIDATION (functions, return true/false)
        |     CheckEnrollmentEligibility()
        |          |-- CheckPrerequisites()
        |          |-- CheckCourseCapacity()
        |          |-- CheckScheduleConflicts()
        |          |-- CheckCurrentEnrollment()
        |     CheckWithdrawalDeadline()
        |
        |-- BUSINESS LOGIC
        |     ProcessEnrollment()  ProcessWithdrawal()  GetEnrollmentBlockReason()
        |          |-- (ProcessEnrollment calls:)
        |              AddToEnrollmentDatabase() · UpdateCourseCapacity() · SendEnrollmentNotification()
        |
        |-- DATA ACCESS
              AddToEnrollmentDatabase() · UpdateCourseCapacity() · SendEnrollmentNotification()

DATA DEPENDENCIES (whose result feeds / gates whom):
  CheckEnrollmentEligibility -> returns true only if ALL of (Prerequisites, Capacity,
       Conflicts-free, Not-already-enrolled) are true  (aggregates four helpers with AND)
  ProcessEnrollment runs ONLY IF CheckEnrollmentEligibility returned true   (eligibility GATES enrolment)
  GetEnrollmentBlockReason is meaningful ONLY AFTER eligibility returned false
```

### Listing 3 — Desk check: successful enrolment scenario
```text
Inputs: choice="enroll", studentID="S12345", courseCode="CS101" (eligible)

Step  Call / Action                                   Returns / Effect          choice/canEnroll
----  ----------------------------------------------  ------------------------  ----------------
 1    DisplayMenuAndGetChoice()                       "enroll"                  choice="enroll"
 2    GetStudentID()                                  "S12345"                  -
 3    GetCourseCode()                                 "CS101"                   -
 4    CheckEnrollmentEligibility("S12345","CS101")    true                      canEnroll=true
 5    canEnroll = true -> take the IF branch          -                         -
 6    ProcessEnrollment("S12345","CS101")             updates DB (effect)       -
 7    DisplayConfirmation("Enrollment successful")    prints message            -

Output: "Enrollment successful"
```

### Listing 4 — Desk check: failed enrolment scenario (course full)
```text
Inputs: choice="enroll", studentID="S67890", courseCode="CS101" (course is FULL)

Step  Call / Action                                   Returns / Effect          canEnroll/reason
----  ----------------------------------------------  ------------------------  ----------------
 1    DisplayMenuAndGetChoice()                       "enroll"                  -
 2    GetStudentID()                                  "S67890"                  -
 3    GetCourseCode()                                 "CS101"                   -
 4    CheckEnrollmentEligibility("S67890","CS101")    false (capacity fails)    canEnroll=false
 5    canEnroll = false -> take the ELSE branch       -                         -
 6    GetEnrollmentBlockReason("S67890","CS101")      "Course is full"          reason="Course is full"
 7    DisplayError("Cannot enroll: Course is full")   prints message            -

Output: "Cannot enroll: Course is full"
Note: ProcessEnrollment is NEVER called — eligibility GATED it (a data dependency).
```

### Listing 5 — The enrolment core as runnable Python (connections made concrete)
```python
# Four independent checks (each a pure FUNCTION returning a boolean):
def check_prerequisites(student, course):  return course not in student["missing_prereqs"]
def check_capacity(course, full_courses):  return course not in full_courses
def check_no_conflict(student, course):    return course not in student["clashes"]
def not_already_enrolled(student, course): return course not in student["enrolled"]


def check_eligibility(student, course, full_courses):     # FUNCTION: aggregates the four
    return (check_prerequisites(student, course)
            and check_capacity(course, full_courses)
            and check_no_conflict(student, course)
            and not_already_enrolled(student, course))


def get_block_reason(student, course, full_courses):      # FUNCTION: mirrors the four checks
    if not check_prerequisites(student, course):
        return "Missing prerequisites"
    elif not check_capacity(course, full_courses):
        return "Course is full"
    elif not check_no_conflict(student, course):
        return "Schedule conflict"
    elif not not_already_enrolled(student, course):
        return "Already enrolled"
    else:
        return "Unknown reason"


def enroll(student, course, full_courses):                # PROCEDURE-ish: acts, returns a message
    if check_eligibility(student, course, full_courses):
        student["enrolled"].append(course)                # ProcessEnrollment effect
        return "Enrollment successful"
    return "Cannot enroll: " + get_block_reason(student, course, full_courses)


alice = {"missing_prereqs": [], "clashes": [], "enrolled": []}
assert enroll(alice, "CS101", set()) == "Enrollment successful"
assert "CS101" in alice["enrolled"]                       # the effect happened

bob = {"missing_prereqs": [], "clashes": [], "enrolled": []}
assert enroll(bob, "CS101", {"CS101"}) == "Cannot enroll: Course is full"

carol = {"missing_prereqs": ["CS101"], "clashes": [], "enrolled": []}
assert enroll(carol, "CS101", set()) == "Cannot enroll: Missing prerequisites"

dan = {"missing_prereqs": [], "clashes": [], "enrolled": ["CS101"]}
assert enroll(dan, "CS101", set()) == "Cannot enroll: Already enrolled"
print("All enrolment-core assertions passed.")
```
