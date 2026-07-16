---
name: gemini-md-kickstarter
description: Bootstraps, initializes, or populates a project-specific GEMINI.md context file. Use when a new project is started, when a local GEMINI.md file is missing or empty, or when the current GEMINI.md lacks important context or structure.
---

# Gemini.md Kickstarter

## Overview
This skill automates the creation and enrichment of a local `GEMINI.md` context file when a project is initialized or lacks comprehensive context. A well-populated `GEMINI.md` prevents the agent from hallucinating tech stacks, tool versions, and conventions.

## When to Use
Use when:
- A new project workspace is opened or started.
- The `GEMINI.md` file does not exist in the root folder.
- The existing `GEMINI.md` is empty, incomplete, or missing key sections (Project Goals, Tool Use, Best Practices, Key Documentation, or Essential Reading).

Do **not** use for:
- Appending one-off coding style rules during development (use normal memory/rules files).
- Editing global instructions in `~/.gemini/GEMINI.md`.

## Core Process

### 1. Perform initial directory scan
Run the project scanner helper script to analyze the directory and output the metadata in JSON format:
```bash
python3 scripts/kickstart_gemini_md.py --json
```
This lets you identify if there are any existing configuration files, packages, or documentation files (`README.md`, `PRD.md`) that detail the tech stack and project name.

### 2. Interview the user for goals and tools
Start a step-by-step dialogue with the user to construct the context:
1. **Ask for Project Goals**: Present any goals you auto-detected from existing files (like `README.md`) and ask the user what the main project goals are.
2. **Determine Tools**: Present the auto-detected tech stack (languages, frameworks) and ask what tools, platforms, or libraries should be used. Ask specifically if they intend to use ADK, React, FastAPI, or Gemini Enterprise Agent Platform.
3. **Ask for additions**: Ask if there are any other specific tools, APIs, or libraries they would like to include in the project scope.

### 3. Generate the draft based on templates
Based on the user's choices:
- If the project uses ADK, Gemini Enterprise, or Agent Platform, use `references/adk-gemini-enterprise-template.md` as the template.
- Otherwise, use `references/generic-template.md` as the template.
- Run the generator script with the selected template to scaffold the draft `GEMINI.md` file:
```bash
python3 scripts/kickstart_gemini_md.py --template gemini-md-kickstarter/references/<selected-template>.md --force
```

### 4. Search and populate readings
Based on the determined tools and goals:
- Run Google Search queries to find official, high-quality documentation links for any non-standard tools/libraries mentioned by the user.
- If ADK or Gemini Enterprise is used, ensure the 10 standard essential reading links from the template are present.
- Enumerate available MCP servers in the environment and project skills, and add them to the `Tool Use` or `Essential Reading` sections.

### 5. Finalize and present draft
Present the completed goals, tools, and reading list to the user. Ask if they have any specific modifications, style instructions, or additional links to add before writing the file.

### 6. Write the final GEMINI.md
Save the final, validated `GEMINI.md` file to the root of the project workspace.

### 7. Self-update reference blueprint
After the user confirms they are happy with the generated file:
- Extract the project-specific goals, tool setup, and essential readings.
- Ask the user explicitly: *"Would you like to save this project profile as a reusable blueprint reference inside the skill? This will update the skill itself for future project initializations."*
- If approved, save a new reference file under `references/<project-name>-blueprint.md`.
- Append a link to this new reference blueprint in the `## Reference Files` section at the bottom of the skill's `SKILL.md` file.

### 8. Harness reload and project initiation
As the final step, instruct the user to:
1. Reload their agentic harness (e.g., run `/memory reload` or restart their CLI/IDE harness) to ensure the newly generated `GEMINI.md` file is actively loaded.
2. Create a new conversation / clean chat session to start the actual project with the fully loaded `GEMINI.md` context.


## Red Flags
Stop and rework if you notice:
- A `## Blog` section was included in the generated `GEMINI.md` (this section is not needed and must be removed).
- The `Essential Reading` table only has placeholder links instead of real, verified URLs.
- The script overwrites custom instructions already present in a pre-existing `GEMINI.md` file.
- The final step misses asking the user to reload their harness and start a new conversation.

## Verification
Ship only when every box is checked:
- [ ] `GEMINI.md` exists in the project root.
- [ ] `GEMINI.md` contains `# [Project Name]`, `## Project Goals`, `## Key Internal Documentation`, and `## Essential Reading`.
- [ ] If ADK or Gemini Enterprise is used, the file has the `## Tool Use` section detailing lifecycle skills and platform APIs.
- [ ] No `## Blog` section exists in the generated file.
- [ ] All documentation files listed in `Key Internal Documentation` link correctly using `file:///` URLs.
- [ ] The agent asked the user if they want to save the project profile to the skill's references.
- [ ] The agent explicitly told the user to reload the harness (e.g., `/memory reload`) and start a new conversation.
- [ ] `python scripts/validate_skill.py <dir> --strict` exits 0.

## Reference Files
- [ADK & Gemini Enterprise Agent Platform Template](references/adk-gemini-enterprise-template.md) — Standard goals, tools, UI best practices, and essential reading lists for agentic projects.
- [Generic GEMINI.md Template](references/generic-template.md) — Simple template structure for non-agentic projects.




