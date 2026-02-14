import os
import json
import sys
from pathlib import Path

class SubmissionError(Exception):
    pass

def validate():
    repo_root = Path(__file__).parent.parent
    submissions_dir = repo_root / "submissions"

    if not submissions_dir.exists():
        raise SubmissionError("submissions/ directory not found.")

    enc_files = list(submissions_dir.glob("*.enc"))
    metadata_file = submissions_dir / "metadata.json"

    # 1️⃣ Exactly one .enc file
    if len(enc_files) == 0:
        raise SubmissionError("No .enc file found.")
    if len(enc_files) > 1:
        raise SubmissionError("Only ONE .enc file allowed.")

    enc_file = enc_files[0]
    team_name = enc_file.stem.lower()

    # 2️⃣ Filename must match GitHub username
    github_actor = os.environ.get("GITHUB_ACTOR")

    if not github_actor:
        raise SubmissionError("GITHUB_ACTOR not found in environment.")

    github_actor = github_actor.lower()


    if team_name != github_actor:
        raise SubmissionError(
            f"Filename must match GitHub username. "
            f"Expected: {github_actor}.enc"
        )

    # 3️⃣ metadata.json must exist
    if not metadata_file.exists():
        raise SubmissionError("metadata.json is required.")

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    # Validate required fields
    required_fields = ["team", "submission_type"]

    for field in required_fields:
        if field not in metadata:
            raise SubmissionError(f"metadata.json missing field: {field}")

    if metadata["team"].lower() != github_actor:
        raise SubmissionError("metadata team must match GitHub username.")

    if metadata["submission_type"] not in ["human", "llm", "human + llm"]:
        raise SubmissionError(
            "submission_type must be: human | llm | human + llm"
        )

    print("✅ Submission structure validated successfully.")

if __name__ == "__main__":
    try:
        validate()
    except SubmissionError as e:
        print(f"❌ Submission Error: {e}")
        sys.exit(1)
