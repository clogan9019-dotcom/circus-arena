"""
Viewer - Spectate the AI performers playing through the adventure!
"""
import json


def generate_viewer(game_engine) -> str:
    """Generate an animated viewer to watch AI performers play"""
    
    world = game_engine.world
    performers = game_engine.performers
    revisions = game_engine.revisions
    
    rooms = world.get('world', {}).get('rooms', [])
    items = world.get('world', {}).get('items', [])
    npcs = world.get('world', {}).get('npcs', [])
    
    rooms_json = json.dumps(rooms)
    items_json = json.dumps(items)
    npcs_json = json.dumps(npcs)
    start_room = world.get('start_room', 'room_1')
    
    performers_json = json.dumps([
        {
            "name": p.name,
            "color": ["#4169E1", "#FF6347", "#32CD32", "#FFD700"][i % 4],
            "start_room": start_room
        }
        for i, p in enumerate(performers)
    ])
    
    feedback_data = json.dumps([fb for rev in revisions for fb in rev.get('feedback', [])])
    revisions_data = json.dumps([{"round": r.get('round', 0), "improvements": r.get('improvements', '')} for r in revisions])
    
    title = world.get('title', 'Unknown')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎪 Watch AI Performers Play! - Circus Arena</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            min-height: 100vh;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        
        header {{
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        h1 {{ font-size: 2.5em; }}
        
        .viewer-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }}
        
        .map-view, .performers-panel, .action-log, .feedback-section {{
            background: #0d0d1a;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        
        .map-title {{ font-size: 1.3em; color: #ffd700; margin-bottom: 20px; text-align: center; }}
        
        .map-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .map-cell {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            min-height: 80px;
            border: 2px solid transparent;
            transition: all 0.3s;
        }}
        
        .map-cell.current {{ border-color: #4ecdc4; background: rgba(78,205,196,0.1); }}
        
        .cell-name {{ font-weight: bold; font-size: 0.85em; margin-bottom: 5px; }}
        .cell-icon {{ font-size: 1.5em; }}
        .cell-items {{ font-size: 0.7em; color: #ffd700; margin-top: 5px; }}
        
        .panel-title {{ font-size: 1.2em; color: #4ecdc4; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
        
        .performer-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid;
        }}
        
        .performer-name {{ font-weight: bold; font-size: 1.1em; }}
        .performer-stats {{ color: #aaa; font-size: 0.9em; margin-top: 10px; }}
        
        .action-log {{ grid-column: 1 / -1; max-height: 250px; overflow-y: auto; }}
        
        .log-entry {{
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .log-turn {{ background: #ffd700; color: #000; padding: 3px 10px; border-radius: 10px; font-size: 0.8em; font-weight: bold; }}
        .log-performer {{ font-weight: bold; min-width: 100px; }}
        .log-action {{ color: #4ecdc4; }}
        
        .controls-bar {{ display: flex; justify-content: center; gap: 15px; margin: 20px 0; }}
        
        .ctrl-btn {{ padding: 12px 25px; font-size: 1.1em; background: linear-gradient(145deg, #3a3a5a, #2a2a4a); border: 2px solid #4a4a6a; border-radius: 10px; color: #fff; cursor: pointer; transition: all 0.2s; }}
        .ctrl-btn:hover {{ transform: scale(1.05); border-color: #ffd700; }}
        .ctrl-btn.play {{ background: linear-gradient(145deg, #6bcb77, #4a9a57); }}
        
        .progress-container {{ background: #333; border-radius: 10px; height: 8px; overflow: hidden; margin: 10px 0; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #4ecdc4, #ffd700); transition: width 0.3s; }}
        
        .feedback-section {{ grid-column: 1 / -1; background: linear-gradient(145deg, rgba(255,107,107,0.1), rgba(0,0,0,0.3)); }}
        .feedback-title {{ color: #ff6b6b; font-size: 1.2em; margin-bottom: 15px; }}
        .feedback-item {{ background: rgba(0,0,0,0.3); border-radius: 10px; padding: 15px; margin-bottom: 10px; }}
        
        .room-view {{ grid-column: 1 / -1; text-align: center; padding: 20px; }}
        .room-name {{ font-size: 1.8em; color: #ffd700; margin-bottom: 10px; }}
        .room-desc {{ color: #ccc; }}
        
        footer {{ text-align: center; padding: 20px; color: #666; }}
        
        @media (max-width: 768px) {{ .viewer-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎪 SPECTATE: AI PERFORMERS PLAY! 🎪</h1>
            <p style="color: #aaa;">Watch the 0.5B models explore the ringmaster's world</p>
        </header>
        
        <div class="controls-bar">
            <button class="ctrl-btn" onclick="stepBack()">⏮️ Back</button>
            <button class="ctrl-btn play" id="playBtn" onclick="togglePlay()">▶️ Play</button>
            <button class="ctrl-btn" onclick="stepForward()">⏭️ Forward</button>
            <button class="ctrl-btn" onclick="resetSim()">🔄 Reset</button>
        </div>
        
        <div class="progress-container">
            <div class="progress-fill" id="progress" style="width: 0%"></div>
        </div>
        
        <div class="viewer-grid">
            <div class="map-view">
                <div class="map-title">🗺️ WORLD MAP</div>
                <div class="map-grid" id="mapGrid"></div>
            </div>
            
            <div class="performers-panel">
                <div class="panel-title">🎭 AI PERFORMERS</div>
                <div id="performersList"></div>
            </div>
            
            <div class="room-view">
                <div class="room-name" id="currentRoomName">-</div>
                <div class="room-desc" id="currentRoomDesc">-</div>
            </div>
            
            <div class="action-log">
                <div class="panel-title">📜 ACTION LOG</div>
                <div id="actionLog">
                    <div class="log-entry">
                        <span class="log-turn">START</span>
                        <span class="log-action">🧠 Ringmaster created: {title}</span>
                    </div>
                </div>
            </div>
            
            <div class="feedback-section">
                <div class="feedback-title">💬 FEEDBACK TO RINGMASTER</div>
                <div id="feedbackList"></div>
            </div>
        </div>
    </div>
    
    <footer>🎪 Circus Arena | Watching {len(performers)} performers explore</footer>

    <script>
        const gameData = {{
            world: {{
                title: "{title}",
                rooms: {rooms_json},
                items: {items_json},
                npcs: {npcs_json},
                startRoom: "{start_room}"
            }},
            performers: {performers_json},
            feedback: {feedback_data},
            revisions: {revisions_data}
        }};
        
        let currentStep = 0;
        let isPlaying = false;
        let playInterval = null;
        const simulationSteps = generateSimulation();
        
        function generateSimulation() {{
            const steps = [];
            const rooms = gameData.world.rooms;
            const performers = gameData.performers;
            
            performers.forEach(function(p, pIdx) {{
                let pos = gameData.world.startRoom;
                
                for (let i = 0; i < 6; i++) {{
                    const currentRoom = rooms.find(function(r) {{ return r.id === pos; }});
                    const exits = ['north', 'south', 'east', 'west'].filter(function(d) {{ return currentRoom && currentRoom[d]; }});
                    
                    if (exits.length === 0) break;
                    
                    const nextDir = exits[Math.floor(Math.random() * exits.length)];
                    const nextRoom = currentRoom[nextDir];
                    
                    steps.push({{
                        type: 'move',
                        performer: p.name,
                        performerIdx: pIdx,
                        from: pos,
                        to: nextRoom,
                        direction: nextDir,
                        turn: steps.length + 1
                    }});
                    
                    pos = nextRoom;
                }}
            }});
            
            gameData.feedback.forEach(function(fb, idx) {{
                steps.push({{
                    type: 'feedback',
                    performer: performers[idx % performers.length].name,
                    text: fb,
                    turn: steps.length + 1
                }});
            }});
            
            gameData.revisions.forEach(function(rev) {{
                steps.push({{
                    type: 'improvement',
                    round: rev.round,
                    text: rev.improvements,
                    turn: steps.length + 1
                }});
            }});
            
            return steps;
        }}
        
        function init() {{
            renderMap();
            renderPerformers();
            renderFeedback();
            updateView();
        }}
        
        function renderMap() {{
            const grid = document.getElementById('mapGrid');
            const rooms = gameData.world.rooms;
            let html = '';
            
            rooms.forEach(function(room) {{
                const roomItems = room.items ? room.items.map(function(id) {{
                    const item = gameData.world.items.find(function(i) {{ return i.id === id; }});
                    return item ? item.name : id;
                }}).join(', ') : '';
                
                html += '<div class="map-cell" id="cell-' + room.id + '">' +
                    '<div class="cell-icon">🚪</div>' +
                    '<div class="cell-name">' + room.name + '</div>' +
                    '<div class="cell-items">' + roomItems + '</div>' +
                    '</div>';
            }});
            
            grid.innerHTML = html;
        }}
        
        function renderPerformers() {{
            const list = document.getElementById('performersList');
            let html = '';
            
            gameData.performers.forEach(function(p, idx) {{
                html += '<div class="performer-card" style="border-color: ' + p.color + '">' +
                    '<div class="performer-name" style="color: ' + p.color + '">🎭 ' + p.name + '</div>' +
                    '<div class="performer-stats">📍 <span id="performer-room-' + idx + '">Starting...</span></div>' +
                    '<div class="performer-stats">👟 Steps: <span id="performer-steps-' + idx + '">0</span></div>' +
                    '</div>';
            }});
            
            list.innerHTML = html;
        }}
        
        function renderFeedback() {{
            const list = document.getElementById('feedbackList');
            if (gameData.feedback.length === 0) {{
                list.innerHTML = '<p style="color: #888;">No feedback collected yet...</p>';
                return;
            }}
            
            let html = '';
            gameData.feedback.slice(0, 5).forEach(function(fb, idx) {{
                html += '<div class="feedback-item"><strong>💬 Feedback from Performer ' + (idx + 1) + ':</strong>' +
                    '<p style="margin-top: 10px; color: #ccc;">' + fb.substring(0, 200) + '...</p></div>';
            }});
            
            list.innerHTML = html;
        }}
        
        function updateView() {{
            const step = simulationSteps[currentStep];
            const targetRoom = step ? step.to : gameData.world.startRoom;
            
            document.querySelectorAll('.map-cell').forEach(function(cell) {{
                cell.classList.remove('current');
            }});
            
            gameData.performers.forEach(function(p, idx) {{
                const roomEl = document.getElementById('performer-room-' + idx);
                const stepsEl = document.getElementById('performer-steps-' + idx);
                if (roomEl) roomEl.textContent = targetRoom;
                if (stepsEl) stepsEl.textContent = idx + 1;
            }});
            
            const room = gameData.world.rooms.find(function(r) {{ return r.id === targetRoom; }});
            if (document.getElementById('currentRoomName')) {{
                document.getElementById('currentRoomName').textContent = room ? room.name : 'Room';
            }}
            if (document.getElementById('currentRoomDesc')) {{
                document.getElementById('currentRoomDesc').textContent = room ? room.description : '';
            }}
            
            if (step) {{
                const log = document.getElementById('actionLog');
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                
                if (step.type === 'move') {{
                    const performer = gameData.performers[step.performerIdx];
                    entry.innerHTML = '<span class="log-turn">' + step.turn + '</span>' +
                        '<span class="log-performer" style="color: ' + (performer ? performer.color : '#fff') + '">🎭 ' + step.performer + '</span>' +
                        '<span class="log-action">➡️ Moved ' + step.direction + ' to ' + step.to + '</span>';
                }} else if (step.type === 'feedback') {{
                    entry.innerHTML = '<span class="log-turn">FB</span>' +
                        '<span class="log-performer">💬 ' + step.performer + '</span>' +
                        '<span class="log-action">Gave feedback!</span>';
                }} else if (step.type === 'improvement') {{
                    entry.innerHTML = '<span class="log-turn">✨</span>' +
                        '<span class="log-performer">🧠 Ringmaster</span>' +
                        '<span class="log-action">Improved world!</span>';
                }}
                
                log.insertBefore(entry, log.firstChild);
            }}
            
            const progress = (currentStep / Math.max(simulationSteps.length, 1)) * 100;
            document.getElementById('progress').style.width = progress + '%';
        }}
        
        function stepForward() {{
            if (currentStep < simulationSteps.length - 1) {{
                currentStep++;
                updateView();
            }}
        }}
        
        function stepBack() {{
            if (currentStep > 0) {{
                currentStep--;
                updateView();
            }}
        }}
        
        function resetSim() {{
            currentStep = 0;
            document.getElementById('actionLog').innerHTML = '<div class="log-entry"><span class="log-turn">START</span><span class="log-action">🧠 Ringmaster created: ' + gameData.world.title + '</span></div>';
            updateView();
        }}
        
        function togglePlay() {{
            const btn = document.getElementById('playBtn');
            
            if (isPlaying) {{
                clearInterval(playInterval);
                isPlaying = false;
                btn.textContent = '▶️ Play';
                btn.className = 'ctrl-btn play';
            }} else {{
                isPlaying = true;
                btn.textContent = '⏸️ Pause';
                btn.className = 'ctrl-btn';
                btn.style.background = 'linear-gradient(145deg, #ff6b6b, #cc5555)';
                
                playInterval = setInterval(function() {{
                    if (currentStep < simulationSteps.length - 1) {{
                        stepForward();
                    }} else {{
                        togglePlay();
                    }}
                }}, 1500);
            }}
        }}
        
        init();
    </script>
</body>
</html>'''
    
    return html


def save_viewer(game_engine, filename: str = "spectate.html") -> str:
    html = generate_viewer(game_engine)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    return filename
