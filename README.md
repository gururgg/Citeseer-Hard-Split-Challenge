# 🧠 Citeseer Hard Split Challenge

Welcome to the **Citeseer Hard Split Challenge**!  
In this challenge, participants perform a **node classification task** on the well-known **CiteSeer citation network dataset** using **Graph Neural Networks (GNNs)** or any other graph-based approach, but test nodes are significantly different than the publicly used version.

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
- Comparing the structural or feature properties between:
  - original test set
  - challenge test set  
  can provide useful insights and hints. 

🎯 **Bonus objective:**  
Achieve a **small performance gap** between the challenge task and the original task, indicating strong generalization.

---

## 📁 How to Submit?

Train your model using the data inside the **data** folder. Predict labels for every node and write the predictions in the following format :

```csv
preds
3
1
2
...
```
Save it as a `.csv` file (e.g. `my_submission.csv`) in the **`submissions/`** folder.  
**Note:** `.csv` files in `submissions/` are git-ignored, so your raw submission will not be pushed. You will submit an **encrypted** version instead.

From the project root, run the encryption script so it can find your CSV and the encryption key:

**Linux / macOS:**
```bash
cd submissions
python encrypt_submissions.py
cd ..
```

**Windows (Command Prompt):**
```cmd
cd submissions
python encrypt_submissions.py
cd ..
```

**Windows (PowerShell):**
```powershell
cd submissions
python encrypt_submissions.py
cd ..
```
This creates a `.enc` file next to each `.csv` in `submissions/` (e.g. `my_submission.csv.enc`). Only `.enc` files are tracked by git; your `.csv` stays local. Please rename your `.enc` file such that it is **github_name.enc**

---

## 🏆 Evaluation
- Submit your `.enc` file with `metadata.json` under the `submissions/`
- Submissions are evaluated automatically using **GitHub Actions**
- True labels are stored securely and are **never exposed**
- Results are displayed on the **public leaderboard**

---

Good luck, and enjoy the challenge! 🧩  

## 🏆 Leaderboard

The leaderboard is automatically updated when you submit your solution via Pull Request.


**[🏆 View Live Leaderboard](https://gururgg.github.io/GNN-Mini-Challange/leaderboard.html)**


The leaderboard shows:
- **Rank**: Your position based on challange test set accuracy
- **Team Name**: Your Github username (without .csv)
- **Challenge Acc**: Challenge task test set accuracy
- **Original Acc**: Original task test set accuracy
- **Gap**: Performance gap between the challenge task and the original task


