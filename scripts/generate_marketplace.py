#!/usr/bin/env python3
import json
from pathlib import Path

def generate_marketplace():
    # Define paths
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"
    output_dir = repo_root / ".claude-plugin"
    output_file = output_dir / "marketplace.json"

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Initialize plugins list with the root plugin first.
    # Per the Claude Code marketplace spec:
    #   - plugins must be an array of {name, source} objects
    #   - owner must be an object with a name field
    #   - source paths resolve relative to the marketplace root (repo root),
    #     not relative to .claude-plugin/ — use "./" prefixes, not "../"
    plugins = [
        {"name": "zephyr-skills", "source": "./"}
    ]

    # Scan for valid skills
    if skills_dir.exists():
        # Sort for deterministic output across filesystems/OS.
        for item in sorted(skills_dir.iterdir(), key=lambda p: p.name):
            if item.is_dir() and (item / "SKILL.md").exists():
                skill_name = item.name
                plugins.append({"name": skill_name, "source": f"./skills/{skill_name}"})

    marketplace = {
        "name": "zephyr-agent-skills",
        "owner": {
            "name": "beriberikix"
        },
        "plugins": plugins
    }

    # Write JSON file
    with open(output_file, "w") as f:
        json.dump(marketplace, f, indent=2)
        f.write("\n")  # Add trailing newline

    print(f"Generated marketplace.json at {output_file}")
    print(f"Total plugins: {len(plugins)}")

if __name__ == "__main__":
    generate_marketplace()
