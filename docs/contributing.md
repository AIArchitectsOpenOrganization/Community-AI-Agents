\# Contributing to Community AI Agents



Thank you for contributing. This repo is a community catalog of AI agents for architects and managers.



\## Quick start (add a new agent)



1\) Fork the repository on GitHub

2\) Clone your fork locally

3\) Create a new folder:



agents/<your-agent-slug>/



4\) Copy the template files from:

templates/agent-template/



5\) Required files inside your agent folder:

\- agents/<slug>/agent.yaml

\- agents/<slug>/README.md



\## Agent requirements (must pass review)



\### agent.yaml

\- Must follow the required fields in docs/agent-spec.md

\- `slug` must match the folder name

\- `risk\_level` must be set (low/medium/high)

\- `version` must be semver (example: 0.1.0)



\### README.md

Must include:

\- What it does

\- Who it is for

\- How to run

\- Example prompts (minimum 3)



\## No secrets / no sensitive data

\- Do NOT include passwords, tokens, API keys, or internal URLs in code or examples.

\- Use placeholders like: YOUR\_API\_KEY



\## Local validation before PR

From repo root, run:



python runtime/cli/agentctl.py validate



Optional: run your agent (if supported):

python runtime/cli/agentctl.py run <agent-slug> "test input"



\## How to submit

1\) Commit changes to your fork

2\) Open a Pull Request to the main repo

3\) Fill the PR checklist



\## Review criteria

PRs are merged if:

\- Required files exist

\- Metadata is complete

\- Agent description is clear and useful

\- Safety and limitations are documented



