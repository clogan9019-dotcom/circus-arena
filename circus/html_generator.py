"""
HTML Generator - Creates visual game show interface showing the feedback loop
"""
import json


def generate_html_game(world_data: dict) -> str:
    """Generate the game show HTML with feedback loop visualization"""
    
    title = world_data.get('title', 'Circus Arena')
    rounds = world_data.get('rounds', [])
    performers = world_data.get('performers', [])
    revisions = world_data.get('revisions', [])
    
    rounds_html = ""
    for r in rounds:
        rounds_html += f'''
        <div class="round-card">
            <span class="round-badge">Round {r['id']}</span>
            <div class="round-name">{r['name']}</div>
            <div class="round-obj">{r.get('objective', '')}</div>
        </div>'''
    
    performers_html = ""
    for p in performers:
        performers_html += f'''
        <div class="performer-card">
            <div class="performer-icon">🎭</div>
            <div class="performer-name">{p['name']}</div>
            <div class="performer-info">
                📍 {p.get('room', 'unknown')} | 
                🎒 {", ".join(p.get('inventory', [])) or "empty"} |
                👟 {p.get('steps', 0)} steps
            </div>
        </div>'''
    
    feedback_html = ""
    for i, rev in enumerate(revisions):
        feedback_html += f'''
        <div class="revision-card">
            <div class="revision-header">
                <span class="revision-num">🔄 Revision {i + 1}</span>
                <span class="revision-round">After Round {rev.get('round', i) + 1}</span>
            </div>
            <div class="feedback-list">'''
        
        for fb in rev.get('feedback', []):
            feedback_html += f'<div class="feedback-item">💬 {fb[:200]}...</div>'
        
        feedback_html += f'''
            </div>
            <div class="improvement-note">🧠 Ringmaster improved based on feedback</div>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎪 {title} - Circus Arena</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: #fff;
            min-height: 100vh;
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        header {{
            text-align: center;
            padding: 40px 0;
        }}
        
        h1 {{
            font-size: 3em;
            background: linear-gradient(90deg, #ffd700, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .loop-flow {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
            padding: 30px;
            background: linear-gradient(145deg, rgba(255,215,0,0.1), rgba(78,205,196,0.1));
            border-radius: 20px;
            margin: 30px 0;
        }}
        
        .loop-step {{
            text-align: center;
            padding: 20px;
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
            min-width: 180px;
        }}
        
        .loop-icon {{ font-size: 2.5em; }}
        .loop-role {{ font-size: 1.2em; font-weight: bold; margin: 10px 0 5px; }}
        .loop-model {{ color: #888; font-size: 0.85em; }}
        .loop-desc {{ color: #aaa; font-size: 0.8em; margin-top: 5px; }}
        
        .loop-arrow {{ font-size: 2em; color: #ffd700; }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .panel {{
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .panel-title {{
            font-size: 1.3em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .ringmaster-panel {{
            border-color: rgba(255,215,0,0.3);
            background: linear-gradient(145deg, rgba(255,215,0,0.05), rgba(0,0,0,0.3));
        }}
        
        .setting-text {{
            color: #aaa;
            font-style: italic;
            margin-bottom: 20px;
            line-height: 1.6;
        }}
        
        .round-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            border-left: 3px solid #ffd700;
        }}
        
        .round-badge {{
            font-size: 0.8em;
            color: #ffd700;
            background: rgba(255,215,0,0.2);
            padding: 3px 8px;
            border-radius: 10px;
        }}
        
        .round-name {{ font-weight: bold; margin: 8px 0 5px; }}
        .round-obj {{ color: #888; font-size: 0.9em; }}
        
        .performers-panel {{
            border-color: rgba(78,205,196,0.3);
            background: linear-gradient(145deg, rgba(78,205,196,0.05), rgba(0,0,0,0.3));
        }}
        
        .performer-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .performer-icon {{ font-size: 2em; }}
        .performer-name {{ font-weight: bold; color: #4ecdc4; }}
        .performer-info {{ color: #888; font-size: 0.9em; }}
        
        .feedback-section {{
            grid-column: 1 / -1;
            background: linear-gradient(145deg, rgba(255,107,107,0.1), rgba(0,0,0,0.3));
            border-color: rgba(255,107,107,0.3);
        }}
        
        .revision-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .revision-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }}
        
        .revision-num {{ font-weight: bold; color: #ff6b6b; font-size: 1.1em; }}
        .revision-round {{ color: #ffd700; }}
        
        .feedback-list {{ margin: 15px 0; }}
        
        .feedback-item {{
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            margin-bottom: 8px;
            color: #ccc;
            font-style: italic;
        }}
        
        .improvement-note {{
            color: #4ecdc4;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .win-info {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 25px;
            background: linear-gradient(145deg, rgba(107,203,119,0.1), rgba(0,0,0,0.3));
            border-radius: 15px;
        }}
        
        .win-title {{ color: #6bcb77; font-size: 1.2em; }}
        .win-text {{ font-size: 1.3em; margin-top: 10px; }}
        
        footer {{ text-align: center; padding: 30px; color: #666; }}
        
        @media (max-width: 768px) {{
            .content-grid {{ grid-template-columns: 1fr; }}
            .loop-flow {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎪 CIRCUS ARENA 🎪</h1>
            <p style="color: #aaa;">Ringmaster Edition - AI Creates, Performs, Improves!</p>
        </header>
        
        <div class="loop-flow">
            <div class="loop-step">
                <div class="loop-icon">🧠</div>
                <div class="loop-role">Ringmaster</div>
                <div class="loop-model">14B model</div>
                <div class="loop-desc">Creates world</div>
            </div>
            <div class="loop-arrow">→</div>
            <div class="loop-step">
                <div class="loop-icon">🎭</div>
                <div class="loop-role">Performers</div>
                <div class="loop-model">0.5B models</div>
                <div class="loop-desc">Play the game</div>
            </div>
            <div class="loop-arrow">→</div>
            <div class="loop-step">
                <div class="loop-icon">💬</div>
                <div class="loop-role">Feedback</div>
                <div class="loop-model">→ Ringmaster</div>
                <div class="loop-desc">Report what worked</div>
            </div>
            <div class="loop-arrow">→</div>
            <div class="loop-step">
                <div class="loop-icon">✨</div>
                <div class="loop-role">Improve</div>
                <div class="loop-model">Ringmaster</div>
                <div class="loop-desc">Fixes & adjusts</div>
            </div>
            <div class="loop-arrow">↻</div>
        </div>
        
        <div class="content-grid">
            <div class="panel ringmaster-panel">
                <div class="panel-title"><span>🧠</span> Ringmaster Creates</div>
                <div class="setting-text">{world_data.get('setting', '')}</div>
                {rounds_html if rounds_html else '<div style="color:#888;">Adventure created...</div>'}
            </div>
            
            <div class="panel performers-panel">
                <div class="panel-title"><span>🎭</span> Performers Play</div>
                {performers_html if performers_html else '<div style="color:#888;">Waiting...</div>'}
                <div style="margin-top:15px; padding:10px; background:rgba(0,0,0,0.3); border-radius:8px; color:#888; font-size:0.9em;">
                    Model: qwen2.5:0.5b
                </div>
            </div>
            
            <div class="win-info">
                <div class="win-title">🎯 Win Condition</div>
                <div class="win-text">{world_data.get('win_condition', 'Complete the adventure')}</div>
            </div>
            
            <div class="panel feedback-section" style="grid-column: 1 / -1;">
                <div class="panel-title"><span>💬</span> Feedback Loop History</div>
                {feedback_html if feedback_html else '<div style="color:#888;">No feedback collected yet...</div>'}
            </div>
        </div>
    </div>
    
    <footer>
        Circus Arena | Ringmaster: Qwen2.5-Coder-14B | Performers: qwen2.5:0.5b
    </footer>
</body>
</html>'''
    
    return html


def save_html_game(world_data: dict, filename: str = "circus_arena.html") -> str:
    """Save the HTML game"""
    html = generate_html_game(world_data)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    return filename
