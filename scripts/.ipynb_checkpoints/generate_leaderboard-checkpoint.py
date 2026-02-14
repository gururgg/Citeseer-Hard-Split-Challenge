"""
Generate leaderboard from evaluation results.
"""
import json
from datetime import datetime
from pathlib import Path

def format_datetime(iso_string):
    """Format ISO datetime string to human-readable format."""
    if not iso_string:
        return "Never"
    
    try:
        # Parse ISO format (handle both with and without timezone)
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        # Format: "December 20, 2025 at 22:56:05"
        return dt.strftime("%B %d, %Y at %H:%M:%S")
    except (ValueError, AttributeError):
        # If parsing fails, return as-is or try alternative format
        try:
            dt = datetime.strptime(iso_string.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            return dt.strftime("%B %d, %Y at %H:%M:%S")
        except:
            return iso_string

def load_evaluation_results():
    """Load evaluation results."""
    results_file = Path(__file__).parent.parent / 'evaluation_results.json'
    if results_file.exists():
        with open(results_file, 'r') as f:
            return json.load(f)
    return []

def load_existing_leaderboard():
    """Load existing leaderboard."""
    leaderboard_file = Path(__file__).parent.parent / 'leaderboard.json'
    if leaderboard_file.exists():
        with open(leaderboard_file, 'r') as f:
            return json.load(f)
    return {"last_updated": None, "submissions": []}

def generate_leaderboard():
    """Generate leaderboard from all results."""
    results = load_evaluation_results()
    existing = load_existing_leaderboard()
    
    # Create a map of existing submissions
    existing_map = {sub['team']: sub for sub in existing.get('submissions', [])}
    
    # Process new results
    for result in results:
        team = result['team']
        scores = result['scores']
        
        entry = {
            'team': team,
            'submission_file': result['file'],
            'challenge_accuracy': scores.get('challenge_accuracy', 0.0),
            'original_accuracy': scores.get('original_accuracy', 0.0),
            'gap': scores.get('accuracy_gap', 0.0),
            'timestamp': datetime.now().isoformat()
        }
        
        # Update if better score or new team
        if team not in existing_map or entry['challenge_accuracy'] > existing_map[team]['challenge_accuracy']:
            existing_map[team] = entry
    
    # Convert to list and sort
    submissions = list(existing_map.values())
    submissions.sort(key=lambda x: x['challenge_accuracy'], reverse=True)
    
    leaderboard = {
        'last_updated': datetime.now().isoformat(),
        'submissions': submissions
    }
    
    # Save JSON
    leaderboard_file = Path(__file__).parent.parent / 'leaderboard.json'
    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f, indent=2)
    
    # Generate HTML
    generate_html(leaderboard)
    
    print(f"Generated leaderboard with {len(submissions)} teams")
    return leaderboard

def generate_html(leaderboard):
    """Generate simple HTML leaderboard (no animations, no canvas)."""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GNN Mini Challenge – Leaderboard</title>
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f4f6f8;
            padding: 40px;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        table {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        thead {
            background-color: #2c3e50;
            color: white;
        }

        th, td {
            padding: 14px 16px;
            text-align: left;
        }

        th {
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.05em;
        }

        tbody tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .num {
            font-family: "Courier New", monospace;
            font-weight: bold;
        }

        .gap {
            color: #c0392b;
        }

        .footer {
            max-width: 900px;
            margin: 30px auto 0;
            text-align: center;
            padding: 20px;
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 4px;
            font-size: 1em;
        }

        .footer a {
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
        }

        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

<h1>🏆 GNN Mini Challenge Leaderboard</h1>

<table>
    <thead>
        <tr>
            <th>Rank</th>
            <th>Team Name</th>
            <th>Challenge Accuracy</th>
            <th>Original Accuracy</th>
            <th>Gap</th>
            <th>Submission Time</th>
        </tr>
    </thead>
    <tbody>
"""

    submissions = leaderboard.get("submissions", [])

    if not submissions:
        html += """
        <tr>
            <td colspan="6" style="text-align:center; padding: 40px;">
                No submissions yet. Be the first! 🚀
            </td>
        </tr>
"""
    else:
        for idx, entry in enumerate(submissions, start=1):
            timestamp = entry.get("timestamp", "")
            if timestamp:
                timestamp = format_datetime(timestamp)

            html += f"""
        <tr>
            <td>{idx}</td>
            <td><strong>{entry['team']}</strong></td>
            <td class="num">{entry['challenge_acc']:.4f}</td>
            <td class="num">{entry['original_acc']:.4f}</td>
            <td class="num gap">{entry['gap']:.4f}</td>
            <td>{timestamp}</td>
        </tr>
"""

    html += """
    </tbody>
</table>

<div class="footer">
    <p>Submit your solution via Pull Request to appear on the leaderboard!</p>
    <p style="margin-top: 10px; font-size: 0.95em;">
        <a href="https://github.com/gururgg/GNN-Mini-Challange"
           target="_blank"
           rel="noopener noreferrer">
            🔗 View Repository on GitHub
        </a>
    </p>
</div>

</body>
</html>
"""
    
    html_file = Path(__file__).parent.parent / 'leaderboard.html'
    with open(html_file, 'w') as f:
        f.write(html)
    
    print(f"Generated {html_file}")

if __name__ == '__main__':
    generate_leaderboard()

