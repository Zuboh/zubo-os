# Zubo Fitness Skill

Track workouts, weight, and fitness goals using vault notes.

## What I can do

- Log today's weight: "log weight 76.5kg"
- Plan a workout: "pianifica allenamento per domani"  
- Show weekly progress: "mostra progressi settimana"

## How I work

Use `write_file` to save logs to `daily/YYYY-MM-DD.md` (append fitness section).
Use `read_file` to load previous sessions before planning.
Use `search_vault` with query "allenamento" to find past workouts.
