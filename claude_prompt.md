# Complete Next Todo List Prompt

Follow these instructions to complete the next todo list prompt.

## IMPORTANT CONTEXT

- The working folder for the feature spec, list of tasks, todo list, and individual task instructions is `{{working_folder}}`
- Tasks are defined as the list of instructions in a prompt file, as listed in the todo list.

## Instructions

1. Read the spec file for the feature: named `spec.md` to understand the feature you are implementing
2. Read the todo list for the feature: named `todo.md` to understand the tasks you need to complete. You can refer to this todo list to see the tasks already completed and those that are still pending.
3. Identify the next incomplete task in the todo list. Never jump ahead or skip a task. For each task, follow the instructions in the next section.

## How to complete a task in the todo list

1. Read the prompt for the task from the prompt file identified in the todo list task you are completing.
2. **Ultrathink** and use `context7` tool to find the relevant documentation for the task, as noted in the **Relative Documentation** section of the task prompt file.
3. Implement the prompt you found in step 1 to complete the task
4. Run the unit tests for the task to ensure everything is working as expected. If any unit test fails or throws an error, fix them.
5. Run all project unit tests to ensure you have not broken any previous tests. If any unit tests fail or throw an error, fix them.
6. Lint the project to ensure there are no linting errors. If there are linting errors, fix them.
7. Perform a git commit with a message that summarizes the changes you made for the task.

## Important Notes

- You are only complete when you have written unit tests for the task and all of those unit tests pass.
- You cannot mark your task as complete until you have written unit tests for the task and all of those unit tests pass.
- You cannot move on to the next task until you have marked the current task as complete.

## CLAUDE Rules & Memory

You must always follow these rules

{{claude_rules}}