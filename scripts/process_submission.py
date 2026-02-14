import os
import sys

# Get absolute project root (one level above /scripts)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Add project root to Python path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from encryption.decrypt import decrypt_file_content

SUBMISSION_DIR = os.path.join(project_root, "submissions")


class SubmissionError(Exception):
    pass


def get_single_encrypted_submission():
    files = [f for f in os.listdir(SUBMISSION_DIR) if f.endswith(".enc")]

    if len(files) == 0:
        raise SubmissionError("No encrypted (.enc) submission found.")

    if len(files) > 1:
        raise SubmissionError(
            "Multiple encrypted submissions detected. Only ONE .enc file is allowed per PR."
        )

    return os.path.join(SUBMISSION_DIR, files[0])


def extract_team_name(filename):
    """
    Extract team name from:
        teamname.csv.enc  -> teamname
        teamname.enc      -> teamname
    """
    name = filename

    if name.endswith(".csv.enc"):
        name = name[:-8]  # remove ".csv.enc"
    elif name.endswith(".enc"):
        name = name[:-4]  # remove ".enc"

    return name


def decrypt_submission(encrypted_path):
    decrypted_content = decrypt_file_content(encrypted_path)

    # Always produce teamname.csv
    team_name = extract_team_name(os.path.basename(encrypted_path))
    decrypted_path = os.path.join(SUBMISSION_DIR, f"{team_name}.csv")

    with open(decrypted_path, "wb") as f:
        f.write(decrypted_content)

    return decrypted_path, team_name


def process_submission():
    encrypted_file = get_single_encrypted_submission()

    filename = os.path.basename(encrypted_file)
    team_name = extract_team_name(filename)

    print(f"🔐 Processing submission for team: {team_name}")

    decrypted_file, team_name = decrypt_submission(encrypted_file)

    print(f"✅ Decrypted file created: {decrypted_file}")

    # Export outputs for GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"team_name={team_name}\n")
            f.write(f"csv_path={decrypted_file}\n")

    return decrypted_file, team_name


if __name__ == "__main__":
    try:
        process_submission()
    except SubmissionError as e:
        print(f"❌ Submission Error: {e}")
        sys.exit(1)
