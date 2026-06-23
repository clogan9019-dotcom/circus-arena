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
    
    # Generate simulation data
    simulation_data = []
    
    for i, rev in enumerate(revisions):
        for fb in rev.get('feedback', []):
            simulation_data.append({
                "type": "feedback",
                "round": rev.get('round', 0),
                "text": fb[:300]
            })
    
    rooms_json = json.dumps(rooms)
    items_json = json.dumps(items)
    npcs_json = json.dumps(npcs)
    
    performers_json = json.dumps([
        {
            "name": p.name,
            "color": ["#4169E1", "#FF6347", "#32CD32", "#FFD700"][i % 4],
            "start_room": world.get('start_room', 'room_1')
        }
        for i, p in enumerate(performers)
    ])
    
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
        
        /* MAIN LAYOUT */
        .viewer-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }}
        
        /* MAP VIEW */
        .map-view {{
            background: #0d0d1a;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        
        .map-title {{
            font-size: 1.3em;
            color: #ffd700;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .map-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            max-width: 500px;
            margin: 0 auto;
        }}
        
        .map-cell {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            min-height: 80px;
            position: relative;
            border: 2px solid transparent;
            transition: all 0.3s;
        }}
        
        .map-cell.active {{
            border-color: #ffd700;
            background: rgba(255,215,0,0.1);
            transform: scale(1.05);
        }}
        
        .map-cell.current {{
            box-shadow: 0 0 20px rgba(78,205,196,0.5);
        }}
        
        .cell-name {{ font-weight: bold; font-size: 0.85em; margin-bottom: 5px; }}
        .cell-icon {{ font-size: 1.5em; }}
        .cell-items {{ font-size: 0.7em; color: #ffd700; margin-top: 5px; }}
        
        /* PERFORMER TOKENS */
        .performer-token {{
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid #fff;
            animation: bounce 1s ease-in-out infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        /* PERFORMERS PANEL */
        .performers-panel {{
            background: #0d0d1a;
            border-radius: 20px;
            padding: 25px;
        }}
        
        .panel-title {{
            font-size: 1.2em;
            color: #4ecdc4;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .performer-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid;
        }}
        
        .performer-name {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .performer-stats {{
            color: #aaa;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .performer-thought {{
            color: #888;
            font-style: italic;
            font-size: 0.85em;
            margin-top: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
        }}
        
        /* ACTION LOG */
        .action-log {{
            grid-column: 1 / -1;
            background: #0d0d1a;
            border-radius: 20px;
            padding: 25px;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .log-entry {{
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            gap: 15px;
            animation: slideIn 0.3s ease;
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        .log-turn {{
            background: #ffd700;
            color: #000;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .log-performer {{
            font-weight: bold;
            min-width: 100px;
        }}
        
        .log-action {{
            color: #4ecdc4;
        }}
        
        /* SIMULATION CONTROLS */
        .controls-bar {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }}
        
        .ctrl-btn {{
            padding: 12px 25px;
            font-size: 1.1em;
            background: linear-gradient(145deg, #3a3a5a, #2a2a4a);
            border: 2px solid #4a4a6a;
            border-radius: 10px;
            color: #fff;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .ctrl-btn:hover {{
            transform: scale(1.05);
            border-color: #ffd700;
        }}
        
        .ctrl-btn.play {{ background: linear-gradient(145deg, #6bcb77, #4a9a57); }}
        .ctrl-btn.pause {{ background: linear-gradient(145deg, #ff6b6b, #cc5555); }}
        
        /* PROGRESS BAR */
        .progress-container {{
            background: #333;
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4ecdc4, #ffd700);
            transition: width 0.3s;
        }}
        
        /* 3D ROOM VIEW */
        .room-3d {{
            grid-column: 1 / -1;
            background: #0d0d1a;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
        }}
        
        .room-name {{
            font-size: 2em;
            color: #ffd700;
            margin-bottom: 10px;
        }}
        
        .room-desc {{
            color: #ccc;
            margin-bottom: 20px;
        }}
        
        .room-3d-view {{
            perspective: 800px;
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .room-box {{
            transform-style: preserve-3d;
            transform: rotateX(-10deg) rotateY(-15deg);
            transition: transform 0.5s;
        }}
        
        .face {{
            position: absolute;
            background: linear-gradient(145deg, #2a2a4a, #1a1a3a);
            border: 1px solid #3a3a5a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3em;
        }}
        
        .floor {{ width: 180px; height: 180px; transform: rotateX(90deg) translateZ(-30px); }}
        .ceiling {{ width: 180px; height: 180px; transform: rotateX(90deg) translateZ(60px); }}
        .front {{ width: 180px; height: 90px; transform: translateZ(90px); }}
        .back {{ width: 180px; height: 90px; transform: translateZ(-90px) rotateY(180deg); }}
        .left {{ width: 180px; height: 90px; transform: translateX(-90px) rotateY(-90deg); }}
        .right {{ width: 180px; height: 90px; transform: translateX(90px) rotateY(90deg); }}
        
        /* FEEDBACK SECTION */
        .feedback-section {{
            grid-column: 1 / -1;
            background: linear-gradient(145deg, rgba(255,107,107,0.1), rgba(0,0,0,0.3));
            border-radius: 20px;
            padding: 25px;
        }}
        
        .feedback-title {{
            color: #ff6b6b;
            font-size: 1.2em;
            margin-bottom: 15px;
        }}
        
        .feedback-item {{
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        
        footer {{ text-align: center; padding: 20px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎪 SPECTATE: AI PERFORMERS PLAY! 🎪</h1>
            <p style="color: #aaa;">Watch the 0.5B models explore the ringmaster's world</p>
        </header>
        
        <!-- CONTROLS -->
        <div class="controls-bar">
            <button class="ctrl-btn" onclick="stepBack()">⏮️</button>
            <button class="ctrl-btn play" id="playBtn" onclick="togglePlay()">▶️ PLAY</button>
            <button class="ctrl-btn" onclick="stepForward()">⏭️</button>
            <button class="ctrl-btn" onclick="resetSim()">🔄</button>
        </div>
        
        <div class="progress-container">
            <div class="progress-fill" id="progress" style="width: 0%"></div>
        </div>
        
        <div class="viewer-grid">
            <!-- MAP VIEW -->
            <div class="map-view">
                <div class="map-title">🗺️ WORLD MAP</div>
                <div class="map-grid" id="mapGrid">
                    <!-- Generated by JS -->
                </div>
            </div>
            
            <!-- PERFORMERS -->
            <div class="performers-panel">
                <div class="panel-title">🎭 AI PERFORMERS</div>
                <div id="performersList">
                    <!-- Generated by JS -->
                </div>
            </div>
            
            <!-- 3D ROOM VIEW -->
            <div class="room-3d">
                <div class="room-name" id="currentRoomName">-</div>
                <div class="room-desc" id="currentRoomDesc">-</div>
                <div class="room-3d-view">
                    <div class="room-box" id="roomBox">
                        <div class="face floor">⬛</div>
                        <div class="face ceiling">⬛</div>
                        <div class="face front">🚪</div>
                        <div class="face back">🧱</div>
                        <div class="face left">🧱</div>
                        <div class="face right">🧱</div>
                    </div>
                </div>
            </div>
            
            <!-- ACTION LOG -->
            <div class="action-log">
                <div class="panel-title">📜 ACTION LOG</div>
                <div id="actionLog">
                    <div class="log-entry">
                        <span class="log-turn">START</span>
                        <span class="log-action">🧠 Ringmaster created: {world.get('title', 'Unknown')}</span>
                    </div>
                </div>
            </div>
            
            <!-- FEEDBACK SECTION -->
            <div class="feedback-section">
                <div class="feedback-title">💬 FEEDBACK TO RINGMASTER</div>
                <div id="feedbackList">
                    <!-- Generated by JS -->
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        🎪 Circus Arena Spectator Mode | Watching {len(performers)} performers explore
    </footer>

    <script>
        const gameData = {{
            world: {{
                title: "{world.get('title', 'Unknown')}",
                rooms: {rooms_json},
                items: {items_json},
                npcs: {npcs_json},
                startRoom: "{world.get('start_room', 'room_1')}"
            }},
            performers: {performers_json},
            feedback: {json.dumps([fb for rev in revisions for fb in rev.get('feedback', [])])},
            revisions: {json.dumps([{{"round": r.get('round', 0), "improvements": r.get('improvements', '')}} for r in revisions])}
        }};
        
        let currentStep = 0;
        let isPlaying = false;
        let playInterval = null;
        
        // Generate simulation steps
        const simulationSteps = generateSimulation();
        
        function generateSimulation() {{
            const steps = [];
            
            // Add performer movements (simulated based on feedback)
            const rooms = gameData.world.rooms;
            const performers = gameData.performers;
            
            // Generate a path for each performer
            performers.forEach((p, pIdx) => {{
                let pos = gameData.world.startRoom;
                const visitedRooms = new Set();
                
                // Simulate exploration
                for (let i = 0; i < 8; i++) {{
                    const currentRoom = rooms.find(r => r.id === pos);
                    const exits = ['north', 'south', 'east', 'west'].filter(d => currentRoom?.[d]);
                    
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
                    visitedRooms.add(pos);
                }}
            }});
            
            // Add feedback events
            gameData.feedback.forEach((fb, idx) => {{
                steps.push({{
                    type: 'feedback',
                    performer: performers[idx % performers.length].name,
                    text: fb,
                    turn: steps.length + 1
                }});
            }});
            
            // Add improvement events
            gameData.revisions.forEach(rev => {{
                steps.push({{
                    type: 'improvement',
                    round: rev.round,
                    text: rev.improvements,
                    turn: steps.length + 1
                }});
            }});
            
            return steps.sort((a, b) => a.turn - b.turn);
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
            
            grid.innerHTML = rooms.map(room => {{
                const roomItems = room.items?.map(id => {{
                    const item = gameData.world.items.find(i => i.id === id);
                    return item ? item.name : id;
                }}).join(', ') || '';
                
                return `
                <div class="map-cell" id="cell-{room.id}">
                    <div class="cell-icon">🚪</div>
                    <div class="cell-name">{room.name}</div>
                    <div class="cell-items">{roomItems}</div>
                </div>`;
            }}).join('');
        }}
        
        function renderPerformers() {{
            const list = document.getElementById('performersList');
            list.innerHTML = gameData.performers.map((p, idx) => `
                <div class="performer-card" style="border-color: {p.color}">
                    <div class="performer-name" style="color: {p.color}">
                        🎭 {p.name}
                    </div>
                    <div class="performer-stats">
                        📍 Current: <span id="performer-room-{idx}">Starting...</span>
                    </div>
                    <div class="performer-stats">
                        👟 Steps: <span id="performer-steps-{idx}">0</span>
                    </div>
                </div>
            `).join('');
        }}
        
        function renderFeedback() {{
            const list = document.getElementById('feedbackList');
            if (gameData.feedback.length === 0) {{
                list.innerHTML = '<p style="color: #888;">No feedback collected yet...</p>';
                return;
            }}
            
            list.innerHTML = gameData.feedback.slice(0, 5).map((fb, idx) => `
                <div class="feedback-item">
                    <strong>💬 Feedback from Performer {idx + 1}:</strong>
                    <p style="margin-top: 10px; color: #ccc;">{fb.substring(0, 200)}...</p>
                </div>
            `).join('');
        }}
        
        function updateView() {{
            const step = simulationSteps[currentStep] || simulationSteps[0];
            
            // Update map - highlight current rooms for performers
            document.querySelectorAll('.map-cell').forEach(cell => {{
                cell.classList.remove('current');
            }});
            
            // Update performers
            gameData.performers.forEach((p, idx) => {{
                const roomEl = document.getElementById(`performer-room-{idx}`);
                const stepsEl = document.getElementById(`performer-steps-{idx}`);
                if (roomEl) roomEl.textContent = step?.to || gameData.world.startRoom;
                if (stepsEl) stepsEl.textContent = idx + 1;
                
                // Highlight on map
                const cell = document.getElementById(`cell-{step?.to || gameData.world.startRoom}`);
                if (cell && idx === 0) cell.classList.add('current');
            }});
            
            // Update 3D room
            const room = gameData.world.rooms.find(r => r.id === (step?.to || gameData.world.startRoom));
            document.getElementById('currentRoomName').textContent = room?.name || 'Room';
            document.getElementById('currentRoomDesc').textContent = room?.description || '';
            
            // Update log
            if (step) {{
                const log = document.getElementById('actionLog');
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                
                if (step.type === 'move') {{
                    entry.innerHTML = `
                        <span class="log-turn">{step.turn}</span>
                        <span class="log-performer" style="color: {gameData.performers[step.performerIdx]?.color}">🎭 {step.performer}</span>
                        <span class="log-action">➡️ Moved {step.direction} to {step.to}</span>
                    `;
                }} else if (step.type === 'feedback') {{
                    entry.innerHTML = `
                        <span class="log-turn">FB</span>
                        <span class="log-performer">💬 {step.performer}</span>
                        <span class="log-action">Gave feedback!</span>
                    `;
                }} else if (step.type === 'improvement') {{
                    entry.innerHTML = `
                        <span class="log-turn">✨</span>
                        <span class="log-performer">🧠 Ringmaster</span>
                        <span class="log-action">Improved world!</span>
                    `;
                }}
                
                log.insertBefore(entry, log.firstChild);
            }}
            
            // Update progress
            const progress = (currentStep / simulationSteps.length) * 100;
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
            document.getElementById('actionLog').innerHTML = `
                <div class="log-entry">
                    <span class="log-turn">START</span>
                    <span class="log-action">🧠 Ringmaster created: {gameData.world.title}</span>
                </div>
            `;
            updateView();
        }}
        
        function togglePlay() {{
            const btn = document.getElementById('playBtn');
            
            if (isPlaying) {{
                clearInterval(playInterval);
                isPlaying = false;
                btn.textContent = '▶️ PLAY';
                btn.className = 'ctrl-btn play';
            }} else {{
                isPlaying = true;
                btn.textContent = '⏸️ PAUSE';
                btn.className = 'ctrl-btn pause';
                
                playInterval = setInterval(() => {{
                    if (currentStep < simulationSteps.length - 1) {{
                        stepForward();
                    }} else {{
                        togglePlay();
                    }}
                }}, 1500);
            }}
        }}
        
        // Initialize
        init();
    </script>
</body>
</html>'''
    
    return html


def save_viewer(game_engine, filename: str = "spectate.html") -> str:
    """Save the spectator viewer"""
    html = generate_viewer(game_engine)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    return filename
