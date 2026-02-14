"""
Update leaderboard from scores file (Kaggle-style ranking).
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
# Load new scores
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

        # Safety check
        computed_gap = abs(challenge_acc - original_acc)
        if abs(gap - computed_gap) > 1e-6:
            print(f"Warning: gap mismatch for team {team}, using computed gap")
            gap = computed_gap

        entry = {
            "team": team,
            "challenge_acc": challenge_acc,
            "original_acc": original_acc,
            "gap": gap,
            "timestamp": datetime.now().isoformat()
        }

        # Keep BEST challenge accuracy only
        if (
            team not in existing_map
            or challenge_acc > existing_map[team]["challenge_acc"]
        ):
            existing_map[team] = entry
            print(f"Updated entry for {team}: challenge_acc={challenge_acc:.6f}")

# ----------------------------
# Convert to list and sort
# ----------------------------
submissions = list(existing_map.values())

# Sort by challenge accuracy descending
# If tie, earlier submission wins (stable ranking)
submissions.sort(
    key=lambda x: (-x["challenge_acc"], x["timestamp"])
)

# ----------------------------
# Kaggle Ranking (Standard Competition Ranking)
# ----------------------------
rank = 0
previous_score = None

for index, sub in enumerate(submissions):
    score = sub["challenge_acc"]

    if previous_score is None or score < previous_score:
        rank = index + 1

    sub["rank"] = rank
    previous_score = score

# ----------------------------
# Save leaderboard
# ----------------------------
leaderboard = {
    "last_updated": datetime.now().isoformat(),
    "submissions": submissions
}

with open(leaderboard_file, "w") as f:
    json.dump(leaderboard, f, indent=2)

print(f"Leaderboard updated with {len(submissions)} team(s)")
