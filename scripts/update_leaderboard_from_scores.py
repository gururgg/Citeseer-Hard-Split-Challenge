"""
Update leaderboard from scores file.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# ----------------------------
# Load existing leaderboard
# ----------------------------
leaderboard_file = Path("leaderboard.json")

if leaderboard_file.exists():
    with open(leaderboard_file, "r") as f:
        leaderboard = json.load(f)
else:
    leaderboard = {
        "last_updated": None,
        "submissions": []
    }

existing_map = {
    sub["team"]: sub for sub in leaderboard.get("submissions", [])
}

# ----------------------------
# Load scores
# ----------------------------
scores_file = Path("results/scores.txt")

if not scores_file.exists():
    print("No scores file found")
    sys.exit(1)

with open(scores_file, "r") as f:
    for line in f:
        parts = line.strip().split(":")

        if len(parts) != 4:
            print(f"Skipping malformed line: {line.strip()}")
            continue

        team = parts[0]
        challenge_acc = float(parts[1])
        original_acc = float(parts[2])
        gap = float(parts[3])

        # Safety check (optional but recommended)
        computed_gap = abs(challenge_acc - original_acc)
        if abs(gap - computed_gap) > 1e-4:
            print(f"Warning: gap mismatch for team {team}, using computed gap")
            gap = computed_gap

        entry = {
            "team": team,
            "challenge_acc": challange_acc,
            "original_acc": original_acc,
            "gap": gap,
            "timestamp": datetime.now().isoformat()
        }

        # Keep best challenge accuracy only
        if (
            team not in existing_map
            or challenge_acc > existing_map[team]["challenge_acc"]
        ):
            existing_map[team] = entry
            print(f"Updated entry for {team}: challenge_acc={challenge_acc:.4f}")

# ----------------------------
# Sort & save leaderboard
# ----------------------------
submissions = list(existing_map.values())
submissions.sort(key=lambda x: x["challenge_acc"], reverse=True)

leaderboard = {
    "last_updated": datetime.now().isoformat(),
    "submissions": submissions
}

with open(leaderboard_file, "w") as f:
    json.dump(leaderboard, f, indent=2)

print(f"Leaderboard updated with {len(submissions)} team(s)")
