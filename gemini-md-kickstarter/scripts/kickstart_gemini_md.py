#!/usr/bin/env python3
"""Project scanner and GEMINI.md generator.

Scans the current directory to identify languages, frameworks, package managers,
documentation, and target tools, and then generates GEMINI.md from a template
by replacing placeholders:
- {{PROJECT_NAME}}
- {{PROJECT_GOALS}}
- {{KEY_INTERNAL_DOCUMENTATION}}
"""

import os
import sys
import re
import json
from pathlib import Path

# Common directories to ignore during scanning
IGNORE_DIRS = {
    ".git", ".gemini", "node_modules", ".venv", "venv", "env",
    "__pycache__", "build", "dist", "out", "target", "gemini-md-kickstarter",
    ".idea", ".vscode", "tmp", "temp"
}

# Standard documents we look for and map in the documentation table
STANDARD_DOCS = {
    "README.md": "Project README; the developer's front door",
    "TODO.md": "High level plan for the project",
    "PRD.md": "The product spec",
    "architecture-and-walkthrough.md": "The main architecture, including design decisions",
    "architecture.md": "System architecture and design decisions",
    "DESIGN.md": "Where we will capture the UI design",
    "testing.md": "Where we will document test strategy, summary of tests, testing instructions, and manual verification",
    "docs/blog.md": "A blog post document built along the way"
}

def scan_project(root_path: Path):
    """Walks the directory and gathers details about the project."""
    tech_stack = set()
    docs = []
    has_react = False
    has_adk = False
    has_gemini_enterprise = False
    project_name = root_path.name
    project_goals = []

    # Walk directory
    for path in root_path.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue

        if path.is_file():
            ext = path.suffix.lower()
            if ext == ".py":
                tech_stack.add("Python")
            elif ext in (".js", ".jsx"):
                tech_stack.add("JavaScript")
                if ext == ".jsx":
                    has_react = True
            elif ext in (".ts", ".tsx"):
                tech_stack.add("TypeScript")
                if ext == ".tsx":
                    has_react = True
            elif ext == ".go":
                tech_stack.add("Go")
            elif ext == ".rs":
                tech_stack.add("Rust")
            elif ext in (".cpp", ".cc", ".cxx", ".h"):
                tech_stack.add("C++")
            elif ext in (".java", ".kt"):
                tech_stack.add("Java/Kotlin")
            elif path.name in ("BUILD", "BUILD.bazel"):
                tech_stack.add("Bazel/Blaze")

            if path.name == "package.json":
                tech_stack.add("Node.js")
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if "name" in data:
                            project_name = data["name"]
                        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                        if "react" in deps:
                            has_react = True
                        if "@google/adk" in deps or "adk" in deps:
                            has_adk = True
                except Exception:
                    pass
            elif path.name == "requirements.txt":
                tech_stack.add("Python")
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().lower()
                        if "google-genai" in content or "google-generativeai" in content or "google-labs-adk" in content:
                            has_adk = True
                except Exception:
                    pass
            elif path.name == "go.mod":
                tech_stack.add("Go")
            elif path.name == "Cargo.toml":
                tech_stack.add("Rust")

            if ext == ".md" and path.name != "GEMINI.md":
                rel_path = path.relative_to(root_path)
                docs.append(rel_path)

    readme_path = root_path / "README.md"
    prd_path = root_path / "PRD.md"
    doc_to_read = readme_path if readme_path.exists() else (prd_path if prd_path.exists() else None)

    if doc_to_read:
        try:
            with open(doc_to_read, "r", encoding="utf-8") as f:
                content = f.read()
                h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if h1_match:
                    project_name = h1_match.group(1).strip()
                
                goals_section = re.search(r"##\s+(?:Project\s+)?Goals(.*?)(?=##|$)", content, re.DOTALL | re.IGNORECASE)
                if goals_section:
                    goals_text = goals_section.group(1)
                    bullets = re.findall(r"^[-*+]\s+(.+)$", goals_text, re.MULTILINE)
                    project_goals = [b.strip() for b in bullets]
                
                content_lower = content.lower()
                if "adk" in content_lower or "agent development kit" in content_lower:
                    has_adk = True
                if "gemini enterprise" in content_lower or "agent runtime" in content_lower:
                    has_gemini_enterprise = True
        except Exception:
            pass

    return {
        "project_name": project_name,
        "tech_stack": list(tech_stack),
        "docs": [str(d) for d in docs],
        "has_react": has_react,
        "has_adk": has_adk or has_gemini_enterprise,
        "has_gemini_enterprise": has_gemini_enterprise,
        "project_goals": project_goals
    }

def format_goals(goals):
    if not goals:
        return "To create a solution that:\n- [Describe key objective 1]\n- [Describe key objective 2]"
    return "\n".join(f"- {goal}" for goal in goals)

def format_docs(docs, root_path, output_path):
    if not docs:
        return "No documentation files found. Define your main documentation files here."
    
    lines = ["| Resource | Description |", "| -------- | ----------- |"]
    for doc in sorted(docs):
        doc_name = os.path.basename(doc)
        desc = STANDARD_DOCS.get(doc_name, "Project documentation file")
        lines.append(f"| [{doc_name}](file:///{output_path.parent / doc}) | {desc} |")
    return "\n".join(lines)

def main():
    args = sys.argv[1:]
    show_json = "--json" in args
    force = "--force" in args
    pos_args = [a for a in args if not a.startswith("-")]
    
    root = Path.cwd()
    if pos_args:
        root = Path(pos_args[0]).resolve()
        
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    scan_results = scan_project(root)
    
    if show_json:
        print(json.dumps(scan_results, indent=2))
        return

    # Find template path
    template_path = None
    if "--template" in args:
        idx = args.index("--template")
        if idx + 1 < len(args):
            template_path = Path(args[idx + 1]).resolve()
            
    if not template_path:
        script_dir = Path(__file__).resolve().parent
        skill_dir = script_dir.parent
        
        if scan_results["has_adk"]:
            template_path = skill_dir / "references" / "adk-gemini-enterprise-template.md"
        else:
            template_path = skill_dir / "references" / "generic-template.md"

    if not template_path.exists():
        print(f"Error: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    output_file = root / "GEMINI.md"
    if output_file.exists() and not force:
        print(f"Error: GEMINI.md already exists at {output_file}. Use --force to overwrite.", file=sys.stderr)
        sys.exit(2)

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        project_name = scan_results["project_name"]
        project_goals = format_goals(scan_results["project_goals"])
        key_docs = format_docs(scan_results["docs"], root, output_file)
        
        output_content = template_content
        output_content = output_content.replace("{{PROJECT_NAME}}", project_name)
        output_content = output_content.replace("{{PROJECT_GOALS}}", project_goals)
        output_content = output_content.replace("{{KEY_INTERNAL_DOCUMENTATION}}", key_docs)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_content)
            
        print(f"Successfully generated GEMINI.md at {output_file} using template {template_path.name}", file=sys.stderr)
        print(json.dumps(scan_results, indent=2))
        
    except Exception as e:
        print(f"Error processing template: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
