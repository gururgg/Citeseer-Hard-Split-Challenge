import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

# -----------------------------
# Load public data
# -----------------------------
DATA_PATH = "data/citeseer_challenge_public.pt"
data = torch.load(DATA_PATH)

# -----------------------------
# Simple 2-layer GCN
# -----------------------------
class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return x

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data = data.to(device)
model = GCN(in_channels=data.x.size(1), hidden_channels=16, out_channels=int(data.y.max().item()+1)).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# -----------------------------
# Training loop
# -----------------------------
model.train()
for epoch in range(100):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[data.train_mask_challange], data.y[data.train_mask_challange])
    loss.backward()
    optimizer.step()
    if (epoch+1) % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# -----------------------------
# Evaluation
# -----------------------------
model.eval()
with torch.no_grad():
    logits = model(data.x, data.edge_index)
    preds = logits.argmax(dim=1)

# Challenge validation
val_challenge_mask = data.val_mask_challange
acc_challenge = (preds[val_challenge_mask] == data.y[val_challenge_mask]).float().mean().item()

# Normal/causal validation
val_mask = data.val_mask
acc_original = (preds[val_mask] == data.y[val_mask]).float().mean().item()

print(f"Validation Accuracy (Challenge): {acc_challenge:.4f}")
print(f"Validation Accuracy (Original): {acc_original:.4f}")
