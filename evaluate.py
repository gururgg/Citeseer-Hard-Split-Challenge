import os
import base64
import numpy as np
import torch
import pandas as pd
import json
from datetime import datetime
from sklearn.metrics import accuracy_score

# -----------------------------
# Helper: decode tensor from base64 secret
# -----------------------------
def decode_tensor(secret_name, dtype=np.int64):
    b64 = os.environ[secret_name]
    bytes_data = base64.b64decode(b64)
    arr = np.frombuffer(bytes_data, dtype=dtype)
    return torch.from_numpy(arr)

# -----------------------------
# Load secrets
# -----------------------------
y = decode_tensor("PRIVATE_Y", dtype=np.int64)
test_mask_challenge = decode_tensor("PRIVATE_TEST_MASK_CHALLENGE", dtype=np.bool_)
test_mask = decode_tensor("PRIVATE_TEST_MASK", dtype=np.bool_)

# -----------------------------
# Load participant submission
# -----------------------------
submission_csv = "submissions/submission.csv"  # modify if needed
submission = pd.read_csv(submission_csv)

# Assumes CSV columns: 'pred_challenge', 'pred_original'
preds = torch.tensor(submission.values, dtype=torch.int64)

# -----------------------------
# Extract predictions for masks
# -----------------------------
pred_challenge = preds[test_mask_challenge]
pred_original  = preds[test_mask]

# True labels for masks
y_challenge = y[test_mask_challenge]
y_original  = y[test_mask]

# -----------------------------
# Compute accuracy
# -----------------------------
acc_challenge = accuracy_score(y_challenge, pred_challenge.numpy())
acc_casual    = accuracy_score(y_original, pred_original.numpy())
discrepancy   = acc_challenge - acc_casual

print(f"Challenge Accuracy: {acc_challenge:.4f}")
print(f"Casual Accuracy: {acc_casual:.4f}")
print(f"Discrepancy: {discrepancy:.4f}")


entry = {
    "user": os.environ.get("GITHUB_ACTOR", "unknown"),
    "challenge_acc": float(challenge_acc),
    "original_acc": float(original_acc),
    "gap": float(original_acc - challenge_acc),
    "timestamp": datetime.utcnow().isoformat()
}

leaderboard_path = "leaderboard.json"

if os.path.exists(leaderboard_path):
    with open(leaderboard_path) as f:
        board = json.load(f)
else:
    board = []

# keep best score per user
board = [b for b in board if b["user"] != entry["user"]]
board.append(entry)

board = sorted(board, key=lambda x: x["challenge_acc"], reverse=True)

with open(leaderboard_path, "w") as f:
    json.dump(board, f, indent=2)
