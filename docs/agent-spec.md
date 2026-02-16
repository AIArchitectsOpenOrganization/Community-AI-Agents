# Agent Specification (agent.yaml)

Every agent in this repository MUST have an `agent.yaml` file at:

agents/<agent_slug>/agent.yaml

## Required fields

- name: Human-friendly agent name
- slug: unique id; same as folder name
- description: one paragraph
- category: one of [architecture, delivery, leadership, writing, learning, other]
- maturity: one of [draft, stable]
- risk_level: one of [low, medium, high]
- owner: GitHub handle or community name
- version: semver like 0.1.0
- license: MIT (default) or specify
- frameworks: list like [strands] or [langchain] or [semantic-kernel] or [none]
- runtime: how to run (cli entry name)

## Optional fields

- tags: list of keywords
- inputs: list of inputs (text, files)
- outputs: list of outputs
- tools: list of tool slugs used (from /tools)
- knowledge: local files used for RAG (within agent folder)
- evals: how to test quality
- limitations: what it cannot do / known issues

## Folder structure per agent

agents/<slug>/
  agent.yaml
  README.md
  prompts/        (optional)
  knowledge/      (optional)
  tools/          (optional wrapper code)
  tests/          (optional)
  demo/           (optional sample inputs/outputs)
