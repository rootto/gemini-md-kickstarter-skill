# {{PROJECT_NAME}}

## Project Goals

{{PROJECT_GOALS}}

## Tool Use

List project-specific tools, available local skills, and MCP servers here:
- [Describe tool/skill 1]
- [Describe tool/skill 2]

## Key Internal Documentation

{{KEY_INTERNAL_DOCUMENTATION}}

## Essential Reading

Below are the recommended reading resources for this project:

| Resource | Description and Relevance |
| -------- | ------------------------- |
| [Pending Search] | Let the agent run Google Search to identify relevant resources |

## Security & Environment Variables

- **ALWAYS** use a `.env` file for environment variables and secrets.
- **NEVER** hardcode configuration parameters, API keys, credentials, or secrets in the codebase.

## Other Notes

- "Vertex AI" no longer exists as a product; the replacement is Gemini Enterprise Agent Platform.
- "Vertex AI Agent Engine" is no more; the replacement is "Agent Runtime", which is a part of the Gemini Enterprise Agent Platform.
- But APIs and legacy resource names may still refer to legacy names, e.g. `reasoningEngine` rather than Agent Runtime. Always use the new names when creating documentation, but be mindful that we may need to use old names in API calls and certain resource definitions.

## Appendices & Learnings

> [!NOTE]
> Any new learnings, guidelines, project updates, or rules discovered during development must be appended to the end of this file (after the existing sections).

