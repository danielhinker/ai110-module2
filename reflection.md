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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
