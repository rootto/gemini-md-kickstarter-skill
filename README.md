# Gemini.md Kickstarter Skill

An autonomous agent skill designed to initialize, populate, and self-update project-specific `GEMINI.md` context files when starting new projects with tools like **Antigravity 2**, **Antigravity IDE**, or **Antigravity CLI**.

A well-populated `GEMINI.md` provides critical situational awareness, tech stack details, tool setups, and coding conventions to future agent instances in the workspace, preventing hallucinations and context degradation.

---

## Installation

### 1. Antigravity / Gemini CLI
To install this skill for Antigravity or Gemini CLI, place the `gemini-md-kickstarter` folder in your skills directory:

*   **Workspace-specific**: `.agents/skills/gemini-md-kickstarter/` (or `.gemini/skills/`)
*   **User-global**: `~/.agents/skills/gemini-md-kickstarter/` (or `~/.gemini/skills/`)

### 2. Running via npx
To run the kickstart tool as a project initializer in Node.js/web projects:
```bash
npx gemini-md-kickstarter
```
*(This can be configured to run the scanning script and scaffold the default `GEMINI.md` directly in the target directory).*

---

## File Structure

```
gemini-md-kickstarter/
├── SKILL.md                 # Core skill definition (triggering rules and process steps)
├── scripts/
│   └── kickstart_gemini_md.py  # Python scanner and context generator
├── references/
│   └── adk-gemini-enterprise-blueprint.md  # Standard agentic & Gemini Enterprise templates
└── evals/
    └── trigger_evals.json   # Structural and trigger boundary tests
```

---

## How It Works (The Core Process)

1.  **Scanner Invocation**: The skill triggers when a local `GEMINI.md` file is missing, empty, or incomplete. It runs the [kickstart_gemini_md.py](file:///usr/local/google/home/nicolasalvo/projects/dev/gemini.md-kickstarter-skill/gemini-md-kickstarter/scripts/kickstart_gemini_md.py) script.
2.  **Tech Stack Detection**: The script scans the files, configuration manifests (`package.json`, `requirements.txt`, etc.), and existing documentation files to auto-detect language patterns, React usage, and ADK/Gemini Enterprise agent frameworks.
3.  **Dynamic Template Injection**:
    *   If **ADK / Gemini Enterprise** is detected, the script automatically populates standard lifecycle skills, APIs, and the 10 recommended essential reading resource links.
    *   If **React** is also detected, it appends ADK + React UI Best Practices (BFF, A2UI, Stitch).
4.  **Reference Self-Updating**: After you are happy with the generated `GEMINI.md`, the agent asks if you would like to save the configuration as a reusable blueprint inside the skill's `references/` directory.
5.  **Reload and Start**: As the final step, the agent instructs you to reload your harness (e.g., via `/memory reload` or restarting the CLI/IDE harness) and start a new conversation/session to begin the actual project with the new context active.
