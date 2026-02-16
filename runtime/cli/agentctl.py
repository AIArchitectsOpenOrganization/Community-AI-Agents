import sys
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml")
    print("Install it using: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / "agents"

REQUIRED_FIELDS = [
    "name",
    "slug",
    "description",
    "category",
    "maturity",
    "risk_level",
    "owner",
    "version",
    "license",
    "frameworks",
    "runtime",
]

def load_agent_yaml(agent_dir: Path) -> dict:
    agent_file = agent_dir / "agent.yaml"
    if not agent_file.exists():
        raise FileNotFoundError(f"Missing agent.yaml in {agent_dir}")
    with agent_file.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def validate_agent(agent: dict) -> list:
    errors = []
    for k in REQUIRED_FIELDS:
        if k not in agent:
            errors.append(f"Missing required field: {k}")
    if "slug" in agent and not isinstance(agent["slug"], str):
        errors.append("Field 'slug' must be a string")
    return errors

def cmd_list():
    if not AGENTS_DIR.exists():
        print("No agents/ directory found.")
        return
    agents = sorted([p for p in AGENTS_DIR.iterdir() if p.is_dir()])
    if not agents:
        print("No agents found.")
        return
    for p in agents:
        print(p.name)

def cmd_show(slug: str):
    agent_dir = AGENTS_DIR / slug
    agent = load_agent_yaml(agent_dir)
    print(json.dumps(agent, indent=2))

def cmd_validate(slug: str | None):
    targets = []
    if slug:
        targets = [AGENTS_DIR / slug]
    else:
        targets = sorted([p for p in AGENTS_DIR.iterdir() if p.is_dir()])

    any_errors = False
    for agent_dir in targets:
        if not agent_dir.exists():
            print(f"[FAIL] {agent_dir.name} (folder not found)")
            any_errors = True
            continue
        try:
            agent = load_agent_yaml(agent_dir)
            errors = validate_agent(agent)
            if errors:
                any_errors = True
                print(f"[FAIL] {agent_dir.name}")
                for e in errors:
                    print(f"  - {e}")
            else:
                print(f"[OK]   {agent_dir.name}")
        except Exception as ex:
            any_errors = True
            print(f"[FAIL] {agent_dir.name}: {ex}")

    if any_errors:
        sys.exit(2)

def cmd_run(slug: str, text: str):
    agent_dir = AGENTS_DIR / slug
    agent = load_agent_yaml(agent_dir)
    errors = validate_agent(agent)
    if errors:
        print("Agent metadata is invalid. Fix agent.yaml first:")
        for e in errors:
            print(f" - {e}")
        sys.exit(2)

    # This is a mock runner for now (Step 7 will add real LLM calls).
    # The goal is consistent execution and packaging.
    print(f"\n=== {agent['name']} ===")
    print(f"Slug: {agent['slug']}")
    print(f"Category: {agent['category']} | Risk: {agent['risk_level']} | Version: {agent['version']}")
    print("\n--- INPUT ---")
    print(text.strip())
    print("\n--- OUTPUT (mock) ---")
    if slug == "architecture-review-agent":
        print("- Key risks: (mock) security gaps; unclear scalability assumptions; missing observability")
        print("- Recommendations: add threat model; define SLOs; add logging/metrics/tracing")
        print("- Go/No-Go: Go with conditions (mock)")
    elif slug == "meeting-notes-agent":
        print("## Minutes of Meeting (mock)")
        print("- Decisions: ...")
        print("- Action items: ...")
        print("- Risks: ...")
    elif slug == "executive-summary-agent":
        print("## Executive Summary (mock)")
        print("- Context: ...")
        print("- Key points: ...")
        print("- Recommendations: ...")
    else:
        print(f"Processed by {agent['name']} (mock output).")

def usage():
    print("Usage:")
    print("  python runtime/cli/agentctl.py list")
    print("  python runtime/cli/agentctl.py show <agent-slug>")
    print("  python runtime/cli/agentctl.py validate [agent-slug]")
    print('  python runtime/cli/agentctl.py run <agent-slug> "<text>"')

def main():
    if len(sys.argv) < 2:
        usage()
        return

    cmd = sys.argv[1].lower()

    if cmd == "list":
        cmd_list()
    elif cmd == "show" and len(sys.argv) >= 3:
        cmd_show(sys.argv[2])
    elif cmd == "validate":
        slug = sys.argv[2] if len(sys.argv) >= 3 else None
        cmd_validate(slug)
    elif cmd == "run" and len(sys.argv) >= 4:
        slug = sys.argv[2]
        text = " ".join(sys.argv[3:])
        cmd_run(slug, text)
    else:
        usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
