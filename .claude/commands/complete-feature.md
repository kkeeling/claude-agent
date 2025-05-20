# Complete Feature

Follow these instructions to fully implement a feature.

## IMPORTANT CONTEXT

- The working folder for the feature spec, list of tasks, todo list, and individual task instructions is `$ARGUMENTS`
- Tasks are defined as the list of instructions in a prompt file, as listed in the todo list.

## Instructions

1. Read the spec file for the feature: named `spec.md` to understand the feature you are implementing
2. Read the todo list for the feature: named `todo.md` to understand the tasks you need to complete. You can refer to this todo list to see the tasks already completed and those that are still pending.
3. Starting with the first incomplete task in the todo list, complete every task in the todo list in the order they are listed. Never jump ahead or skip a task. For each task, follow the instructions in the next section.
4. **ALWAYS** After completing a task, move on to the next task in the todo list.

## How to complete tasks in the todo list

1. Read the prompt for the task from prompt file
2. **Ultrathink** and use `context7` tool to find the relevant documentation for the task, as noted in the **Relative Documentation** section of the task prompt file.
3. Implement the prompt you found in step 1 to complete the task
4. Run the unit tests for the task to ensure everything is working as expected. If any unit test fails or throws an error, fix them.
5. Run all project unit tests to ensure you have not broken any previous tests. If any unit tests fail or throw an error, fix them.
6. Run the Frontend Dev Server. If running the frontend dev server fails to run or contains errors, fix the errors. Do not move on to the next instruction until the frontend dev server runs without errors. Even if the errors are not related to the task you are completing, fix them.
7. Run the Backend Dev Server. If running the backend dev server fails to run or contains errors, fix the errors. Do not move on to the next instruction until the backend dev server runs without errors. Even if the errors are not related to the task you are completing, fix them.
8. Mark the task as complete in the todo list
9. Perform a git commit with a message that summarizes the changes you made for the task.

## Important Notes

- You are only complete when you have written unit tests for the task and all of those unit tests pass.
- You cannot mark your task as complete until you have written unit tests for the task and all of those unit tests pass.
- You cannot move on to the next task until you have marked the current task as complete.
- You must always follow the rules in `CLAUDE.md`
