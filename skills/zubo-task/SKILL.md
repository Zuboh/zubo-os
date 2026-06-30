# Zubo Task Skill

Manage tasks and projects via vault notes.

## What I can do

- Add a task: "aggiungi task: descrizione"
- List active tasks: "lista tasks aperti"
- Complete a task: "completa task nome"

## How I work

Use `read_file` on `projects/tasks.md` to load the task list.
Use `write_file` to update `projects/tasks.md` after changes.
Use `search_vault` with query "TODO" to find tasks across all notes.
