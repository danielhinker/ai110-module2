# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to do:
1. Enter owner and pet information.
2. Add or edit tasks for a pet (duration and priority at minimum, with optional things like description and time availability).
3. Generate and view a daily schedule based on those tasks.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The main classes are Owner, Pet, Task, and Scheduler.

- Owner holds the owner's info and links to their pets.
- Pet stores pet details and a list of associated tasks.
- Task represents a single care activity and at minimum has a duration and priority but things like description and time window are worth adding.
- Scheduler pulls tasks together and builds the daily plan based on priority and duration.

For the relationships, an owner can have many pets, and a pet can have many tasks. If multiple people share a pet, that could become many-to-many but I'd keep it simple for now and handle that as an edge case later.

Edge cases I'm thinking about are zero or invalid durations, tasks that won't fit in the available time, and the schedule needing to rebuild whenever a task is changed.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

due_date was added to Task to support recurring tasks and scheduled_time was changed to a string in "HH:MM" format to keep things simple for now.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers three things which are the priority level, scheduled time, and completion status but completed tasks are excluded from the daily plan. Priority is weighted first where a high priority task always come before a low priority task even if the low priority task is scheduled earlier in the day, and time is used as the tie breaker if they have the same priority level.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The conflict detection only flags tasks that share the exact same scheduled time but it doesn't check for overlapping durations. So a 30 minute task at 08:00 and a 5 minute task at 08:15 would pass through without a warning even though they technically overlap.

The tradeoff is simplicity where exact time is easy to find because overlap detection would need a start and end time and is more likely to produce false positives for tasks that could actually run at the same time. This is a reasonable tradeoff because the user can always manually check for overlaps if they want to be more precise.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI agent for the design to code steps like turning my ideas into a UML class list into pawpal_system.py then implementing the scheduler methods. I think the most helpful was for creating documentation and tests. It was also helpful when I was specific with my prompts like asking for a sorted solution for HH:MM strings or asking for tests that check scheduling behavior. Using separate chat sessions for different phases kept decisions isolated and clean like system design, core logic, and UI each got their own context.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One thing I didn't keep as suggested was conflict detection. I decided to keep it lightweight like exact time matches only because full overlap detection would require start/end time math and could easily warn too often. I verified AI suggestions by running main.py to check the schedule output then tests to confirm the key behaviors held like recurrence and sorting.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I focused on the behaviors that are most important, which are marking tasks complete, attaching tasks to pets, sorting by time, advancing a daily recurring task's due date, flagging two tasks at the same time, and getting an empty schedule when there's nothing to run. I picked these because they're the kinds of things that would mess up the user's schedule right away. These are core functionalities that the scheduler is supposed to do for a real user.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm around 4/5 confident for the flows we test in pytest. If I had more time I'd add tests for weekly recurrence, filter_tasks by pet name and completion, and maybe priority ordering inside build_schedule with identical times.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

My favorite part is that the system actually works end to end like tasks get stored in classes, the scheduler can sort/filter/warn, and the tests give me confidence the important pieces don't break. It also felt like being the architect because I had to decide what the AI built versus what I verified and kept clean.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had more time I'd address a few things like parsing real times so HH:MM becomes proper datetime objects, adding overlap-based conflict detection, and making the UI support editing tasks in place rather than just adding or marking them complete.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned to keep expectations grounded like AI can help with scaffolding and even whole methods, but the validation still falls on me like running tests, reviewing output, and making choices about tradeoffs like keeping conflict detection simple versus making it more accurate but harder to maintain.
