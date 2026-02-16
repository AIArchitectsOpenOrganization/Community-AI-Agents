import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "agents"
CATALOG_DIR = REPO_ROOT / "catalog"
OUTPUT_FILE = CATALOG_DIR / "index.json"

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

ALLOWED_RISK = {"low", "medium", "high"}

def load_yaml(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def validate_agent(agent: dict, folder_name: str) -> list[str]:
    errs = []
    for k in REQUIRED_FIELDS:
        if k not in agent:
            errs.append(f"Missing required field '{k}'")

    slug = agent.get("slug")
    if isinstance(slug, str):
        if slug != folder_name:
            errs.append(f"slug '{slug}' must match folder '{folder_name}'")
    else:
        errs.append("Field 'slug' must be a string")

    risk = agent.get("risk_level")
    if isinstance(risk, str) and risk.lower() not in ALLOWED_RISK:
        errs.append("risk_level must be one of: low, medium, high")

    return errs

def main() -> int:
    if not AGENTS_DIR.exists():
        print("agents/ folder not found")
        return 2

    agents_index = []
    any_errors = False

    for agent_dir in sorted([p for p in AGENTS_DIR.iterdir() if p.is_dir()]):
        agent_yaml = agent_dir / "agent.yaml"
        readme = agent_dir / "README.md"

        if not agent_yaml.exists():
            print(f"[FAIL] {agent_dir.name}: missing agent.yaml")
            any_errors = True
            continue
        if not readme.exists():
            print(f"[FAIL] {agent_dir.name}: missing README.md")
            any_errors = True
            continue

        agent = load_yaml(agent_yaml)
        errs = validate_agent(agent, agent_dir.name)
        if errs:
            any_errors = True
            print(f"[FAIL] {agent_dir.name}")
            for e in errs:
                print(f"  - {e}")
            continue

        agents_index.append({
            "name": agent["name"],
            "slug": agent["slug"],
            "description": agent["description"],
            "category": agent["category"],
            "maturity": agent["maturity"],
            "risk_level": agent["risk_level"],
            "owner": agent["owner"],
            "version": agent["version"],
            "license": agent["license"],
            "frameworks": agent.get("frameworks", []),
            "runtime": agent.get("runtime", {}),
            "tags": agent.get("tags", []),
            "tools": agent.get("tools", []),
        })

        print(f"[OK]   {agent_dir.name}")

    if any_errors:
        print("\nValidation failed. Fix errors above.")
        return 2

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "generated_from": "catalog/build_catalog.py",
        "count": len(agents_index),
        "agents": agents_index,
    }

    OUTPUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote catalog: {OUTPUT_FILE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
