# 🧠 GNN Mini Challenge: Node Classification on CiteSeer

Welcome to the **GNN Mini Challenge**!  
In this challenge, participants perform a **node classification task** on the well-known **CiteSeer citation network dataset** using **Graph Neural Networks (GNNs)** or any other graph-based approach.

---

## 📊 Dataset: CiteSeer

The **CiteSeer** dataset is a widely used benchmark in graph representation learning and node classification tasks.

It consists of:
- **3,327 nodes** (scientific publications)
- **4,732 edges** (citation links between publications)
- **3,703-dimensional binary node features**, representing word occurrences in document abstracts
- **6 node classes**, corresponding to different research topics

CiteSeer has been extensively used in **state-of-the-art GNN papers**, including GCN, GAT, GraphSAGE, and many others.

In the **original setup**, the dataset comes with predefined:
- training nodes
- validation nodes
- test nodes  

These splits are commonly used to benchmark node classification performance.

---

## 🎯 Challenge Setup

In this challenge, we define a **new and harder classification task**.

Instead of using the original dataset splits, we introduce:
- `train_mask_challenge`
- `val_mask_challenge`
- `test_mask_challenge`

These masks define **new train, validation, and test nodes**, making the task **more challenging than the original CiteSeer benchmark**.

### 🔒 Hidden Labels
- Node **features and graph structure are fully accessible**
- However, the **labels of challenge nodes are hidden**
- Hidden labels are set to **`-1`**, meaning:
  > You do not have direct access to the true labels of challenge nodes

Participants must **infer labels purely from graph structure and node features**.

---

## 🧪 Objective

The **main goal** is to achieve the **highest classification accuracy on `test_mask_challenge`**.

In addition:
- You may use the **original CiteSeer masks** for analysis
- Comparing performance between:
  - original test set
  - challenge test set  
  can provide useful insights and hints

🎯 **Bonus objective:**  
Achieve a **small performance gap** between the challenge task and the original task, indicating strong generalization.

---

## 📁 Submission Format

Participants must submit their predictions in a file named:

## 🏆 Evaluation

- Submissions are evaluated automatically using **GitHub Actions**
- True labels are stored securely and are **never exposed**
- Only the **best challenge accuracy per participant** is kept
- Results are displayed on the **public leaderboard**

---

## 🚀 Getting Started

1. Load the **CiteSeer graph** and node features
2. Train your model using the provided **challenge masks**
3. Generate predictions for **all nodes**
4. Save your predictions in `submission.csv`
5. Submit your file via a **Pull Request** to the `submissions/` folder

---

Good luck, and enjoy the challenge! 🧩  
If you have ideas, insights, or improvements — feel free to share them!


**[🏆 View Live Leaderboard](https://samuelmatia.github.io/gnn-role-transition-challenge/leaderboard.html)**



## 🏆 Leaderboard

The leaderboard is automatically updated when you submit your solution via Pull Request.

👉 **[View Live Leaderboard](https://gururgg.github.io/GNN-Mini-Challange/leaderboard.html)**

The leaderboard shows:
- **Rank**: Your position based on Weighted Macro-F1 score
- **Team Name**: Your submission filename (without .csv)
- **Weighted Macro-F1**: Primary evaluation metric
- **Overall Macro-F1**: Overall performance across all transitions
- **Rare Transitions F1**: Performance on rare transitions (< 5% frequency)


