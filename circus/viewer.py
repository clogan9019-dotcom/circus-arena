"""
Viewer - 3D Spectator view with local server!
"""
import json
import os


def generate_viewer(game_engine) -> str:
    """Generate 3D spectator viewer with A-Frame"""
    
    world = game_engine.world
    performers = game_engine.performers
    revisions = game_engine.revisions
    
    rooms = world.get('world', {}).get('rooms', [])
    items = world.get('world', {}).get('items', [])
    npcs = world.get('world', {}).get('npcs', [])
    start_room = world.get('start_room', 'room_1')
    
    title = world.get('title', 'Unknown')
    
    rooms_json = json.dumps(rooms)
    items_json = json.dumps(items)
    npcs_json = json.dumps(npcs)
    
    performers_json = json.dumps([
        {"name": p.name, "color": ["#4169E1", "#FF6347", "#32CD32", "#FFD700"][i % 4]}
        for i, p in enumerate(performers)
    ])
    
    feedback_data = json.dumps([fb for rev in revisions for fb in rev.get('feedback', [])])
    
    # Generate room positions for 3D grid
    room_positions = []
    grid_size = 4
    for i, room in enumerate(rooms):
        x = (i % grid_size) * 10 - (grid_size * 10) / 2
        z = (i // grid_size) * 10 - (len(rooms) // grid_size) * 5
        room_positions.append({"id": room['id'], "x": x, "z": z, "name": room['name']})
    
    room_pos_json = json.dumps(room_positions)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎪 3D Spectate: {title}</title>
    <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            height: 100vh;
            overflow: hidden;
        }}
        
        #game-container {{
            width: 100%;
            height: 60vh;
            position: relative;
        }}
        
        #controls-panel {{
            height: 40vh;
            background: #0d0d1a;
            padding: 20px;
            overflow-y: auto;
        }}
        
        .controls-bar {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .ctrl-btn {{
            padding: 10px 20px;
            font-size: 1em;
            background: linear-gradient(145deg, #3a3a5a, #2a2a4a);
            border: 2px solid #4a4a6a;
            border-radius: 8px;
            color: #fff;
            cursor: pointer;
        }}
        
        .ctrl-btn:hover {{ transform: scale(1.05); border-color: #ffd700; }}
        .ctrl-btn.play {{ background: linear-gradient(145deg, #6bcb77, #4a9a57); border-color: #6bcb77; }}
        
        .progress-container {{
            background: #333;
            border-radius: 5px;
            height: 6px;
            margin-bottom: 15px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4ecdc4, #ffd700);
            transition: width 0.3s;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        
        .info-panel {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 15px;
        }}
        
        .panel-title {{
            font-size: 1.1em;
            color: #ffd700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .performer-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 3px solid;
        }}
        
        .performer-name {{ font-weight: bold; }}
        .performer-info {{ color: #aaa; font-size: 0.9em; margin-top: 5px; }}
        
        .action-log {{
            max-height: 150px;
            overflow-y: auto;
        }}
        
        .log-entry {{
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 0.9em;
        }}
        
        .log-turn {{ background: #ffd700; color: #000; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; margin-right: 8px; }}
        
        .feedback-item {{
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            font-size: 0.9em;
            color: #ccc;
        }}
        
        .current-room {{
            font-size: 1.5em;
            color: #4ecdc4;
            text-align: center;
            padding: 10px;
        }}
        
        .speed-control {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .speed-control input {{
            width: 100px;
        }}
    </style>
</head>
<body>
    <div id="game-container">
        <a-scene embedded>
            <a-entity id="rig" position="0 5 20" rotation="-20 0 0">
                <a-camera></a-camera>
            </a-entity>
            
            <!-- Sky -->
            <a-sky color="#0f0c29"></a-sky>
            
            <!-- Ground -->
            <a-plane position="0 0 0" rotation="-90 0 0" width="100" height="100" color="#1a1a2e"></a-plane>
            
            <!-- Rooms will be added here by JavaScript -->
            <a-entity id="rooms-container"></a-entity>
            
            <!-- Performer markers -->
            <a-entity id="performers-container"></a-entity>
            
            <!-- Lighting -->
            <a-light type="ambient" color="#404040"></a-light>
            <a-light type="directional" position="1 1 1" intensity="0.5"></a-light>
        </a-scene>
    </div>
    
    <div id="controls-panel">
        <div class="current-room" id="currentRoomName">🎪 {title}</div>
        
        <div class="controls-bar">
            <button class="ctrl-btn" onclick="stepBack()">⏮️ Back</button>
            <button class="ctrl-btn play" id="playBtn" onclick="togglePlay()">▶️ Play</button>
            <button class="ctrl-btn" onclick="stepForward()">⏭️ Forward</button>
            <button class="ctrl-btn" onclick="resetSim()">🔄 Reset</button>
        </div>
        
        <div class="controls-bar">
            <div class="speed-control">
                <span>Speed:</span>
                <input type="range" id="speedSlider" min="500" max="3000" value="1500" onchange="setSpeed(this.value)">
                <span id="speedValue">1.5s</span>
            </div>
        </div>
        
        <div class="progress-container">
            <div class="progress-fill" id="progress" style="width: 0%"></div>
        </div>
        
        <div class="info-grid">
            <div class="info-panel">
                <div class="panel-title">🎭 Performers</div>
                <div id="performersList"></div>
            </div>
            
            <div class="info-panel">
                <div class="panel-title">📜 Action Log</div>
                <div class="action-log" id="actionLog"></div>
            </div>
            
            <div class="info-panel" style="grid-column: 1 / -1;">
                <div class="panel-title">💬 Feedback to Ringmaster</div>
                <div id="feedbackList"></div>
            </div>
        </div>
    </div>

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
            roomPositions: {room_pos_json},
            feedback: {feedback_data}
        }};
        
        let currentStep = 0;
        let isPlaying = false;
        let playInterval = null;
        let stepDelay = 1500;
        
        const simulationSteps = generateSimulation();
        
        // Initialize A-Frame scene
        document.querySelector('a-scene').addEventListener('loaded', function() {{
            init();
        }});
        
        function init() {{
            renderRooms();
            renderPerformers();
            renderFeedback();
            addLog('START', '🧠 Ringmaster created: {title}');
            updateView();
            
            // Auto-rotate camera
            let angle = 0;
            setInterval(function() {{
                if (!isPlaying) {{
                    angle += 0.1;
                    const rig = document.getElementById('rig');
                    const radius = 25;
                    rig.setAttribute('position', (Math.sin(angle * 0.5) * radius) + ' 5 ' + (Math.cos(angle * 0.5) * radius));
                    rig.setAttribute('rotation', '-20 ' + (angle * 30) + ' 0');
                }}
            }}, 50);
        }}
        
        function renderRooms() {{
            const container = document.getElementById('rooms-container');
            const roomPositions = gameData.roomPositions;
            
            roomPositions.forEach(function(roomPos, idx) {{
                const room = gameData.world.rooms.find(function(r) {{ return r.id === roomPos.id; }});
                if (!room) return;
                
                // Room box
                const roomEl = document.createElement('a-box');
                roomEl.setAttribute('position', roomPos.x + ' 1.5 ' + roomPos.z);
                roomEl.setAttribute('width', '6');
                roomEl.setAttribute('height', '3');
                roomEl.setAttribute('depth', '6');
                roomEl.setAttribute('color', getRoomColor(room.theme || 'default'));
                roomEl.setAttribute('opacity', '0.8');
                roomEl.setAttribute('id', 'room-' + room.id);
                container.appendChild(roomEl);
                
                // Room label
                const label = document.createElement('a-text');
                label.setAttribute('value', room.name);
                label.setAttribute('position', roomPos.x + ' 4 ' + roomPos.z);
                label.setAttribute('align', 'center');
                label.setAttribute('color', '#ffd700');
                label.setAttribute('width', '8');
                container.appendChild(label);
                
                // Add exits as arrows
                const exits = ['north', 'south', 'east', 'west'];
                exits.forEach(function(dir) {{
                    if (room[dir]) {{
                        const arrow = document.createElement('a-cone');
                        const offset = {{'north': [0, 0, 3], 'south': [0, 0, -3], 'east': [3, 0, 0], 'west': [-3, 0, 0]}};
                        const rotation = {{'north': [90, 0, 0], 'south': [-90, 0, 0], 'east': [90, 90, 0], 'west': [90, -90, 0]}};
                        arrow.setAttribute('position', (roomPos.x + offset[dir][0]) + ' 0.5 ' + (roomPos.z + offset[dir][2]));
                        arrow.setAttribute('rotation', rotation[dir].join(' '));
                        arrow.setAttribute('radius-bottom', '0.3');
                        arrow.setAttribute('radius-top', '0');
                        arrow.setAttribute('height', '0.5');
                        arrow.setAttribute('color', '#4ecdc4');
                        container.appendChild(arrow);
                    }}
                }});
            }});
        }}
        
        function getRoomColor(theme) {{
            const colors = {{
                'fire': '#8B0000',
                'water': '#00008B',
                'mystic': '#4B0082',
                'temple': '#556B2F',
                'cave': '#2F4F4F',
                'default': '#2a2a4a'
            }};
            return colors[theme] || colors['default'];
        }}
        
        function renderPerformers() {{
            const list = document.getElementById('performersList');
            let html = '';
            
            gameData.performers.forEach(function(p, idx) {{
                html += '<div class="performer-card" style="border-color: ' + p.color + '">' +
                    '<div class="performer-name" style="color: ' + p.color + '">🎭 ' + p.name + '</div>' +
                    '<div class="performer-info">📍 <span id="perf-room-' + idx + '">Starting...</span></div>' +
                    '</div>';
            }});
            
            list.innerHTML = html;
            
            // Create 3D performer markers
            const container = document.getElementById('performers-container');
            gameData.performers.forEach(function(p, idx) {{
                const marker = document.createElement('a-sphere');
                marker.setAttribute('radius', '0.5');
                marker.setAttribute('color', p.color);
                marker.setAttribute('position', '0 2 0');
                marker.setAttribute('id', 'performer-' + idx);
                
                // Add glow
                const glow = document.createElement('a-sphere');
                glow.setAttribute('radius', '0.8');
                glow.setAttribute('color', p.color);
                glow.setAttribute('opacity', '0.3');
                glow.setAttribute('id', 'performer-glow-' + idx);
                
                container.appendChild(marker);
                container.appendChild(glow);
            }});
        }}
        
        function renderFeedback() {{
            const list = document.getElementById('feedbackList');
            if (gameData.feedback.length === 0) {{
                list.innerHTML = '<div class="feedback-item">No feedback collected yet...</div>';
                return;
            }}
            
            let html = '';
            gameData.feedback.slice(0, 3).forEach(function(fb, idx) {{
                html += '<div class="feedback-item"><strong>💬 ' + gameData.performers[idx % gameData.performers.length].name + ':</strong> ' + fb.substring(0, 150) + '...</div>';
            }});
            
            list.innerHTML = html;
        }}
        
        function updateView() {{
            const step = simulationSteps[currentStep];
            const targetRoom = step ? step.to : gameData.world.startRoom;
            const roomPos = gameData.roomPositions.find(function(rp) {{ return rp.id === targetRoom; }});
            
            // Update performer 3D positions
            gameData.performers.forEach(function(p, idx) {{
                const performer = document.getElementById('performer-' + idx);
                const glow = document.getElementById('performer-glow-' + idx);
                
                if (performer && roomPos) {{
                    const offsetX = (idx - 0.5) * 1.5;
                    performer.setAttribute('position', (roomPos.x + offsetX) + ' 2 ' + roomPos.z);
                    glow.setAttribute('position', (roomPos.x + offsetX) + ' 2 ' + roomPos.z);
                    
                    // Bounce animation
                    performer.setAttribute('animation', 'property: position; to: ' + (roomPos.x + offsetX) + ' 2.5 ' + roomPos.z + '; dir: alternate; dur: 500; loop: true');
                }}
                
                const roomEl = document.getElementById('perf-room-' + idx);
                if (roomEl) roomEl.textContent = roomPos ? roomPos.name : targetRoom;
            }});
            
            // Highlight current room
            document.querySelectorAll('[id^="room-"]').forEach(function(el) {{
                el.setAttribute('opacity', '0.5');
            }});
            const currentRoomEl = document.getElementById('room-' + targetRoom);
            if (currentRoomEl) currentRoomEl.setAttribute('opacity', '1');
            
            // Update current room display
            const room = gameData.world.rooms.find(function(r) {{ return r.id === targetRoom; }});
            document.getElementById('currentRoomName').textContent = room ? '📍 ' + room.name : '🎪 ' + gameData.world.title;
            
            // Update log
            if (step) {{
                if (step.type === 'move') {{
                    addLog(step.turn, '🎭 ' + step.performer + ' moved ' + step.direction + ' to ' + step.to);
                }} else if (step.type === 'feedback') {{
                    addLog('FB', '💬 ' + step.performer + ' gave feedback');
                }} else if (step.type === 'improvement') {{
                    addLog('✨', '🧠 Ringmaster improved the world');
                }}
            }}
            
            // Progress bar
            const progress = (currentStep / Math.max(simulationSteps.length, 1)) * 100;
            document.getElementById('progress').style.width = progress + '%';
        }}
        
        function addLog(turn, message) {{
            const log = document.getElementById('actionLog');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = '<span class="log-turn">' + turn + '</span>' + message;
            log.insertBefore(entry, log.firstChild);
            
            // Keep only last 20 entries
            while (log.children.length > 20) {{
                log.removeChild(log.lastChild);
            }}
        }}
        
        function generateSimulation() {{
            const steps = [];
            const rooms = gameData.world.rooms;
            
            gameData.performers.forEach(function(p, pIdx) {{
                let pos = gameData.world.startRoom;
                
                for (let i = 0; i < 12; i++) {{
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
                    performer: gameData.performers[idx % gameData.performers.length].name,
                    text: fb,
                    turn: steps.length + 1
                }});
            }});
            
            return steps;
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
            document.getElementById('actionLog').innerHTML = '';
            addLog('START', '🧠 Ringmaster created: ' + gameData.world.title);
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
                }}, stepDelay);
            }}
        }}
        
        function setSpeed(value) {{
            stepDelay = parseInt(value);
            document.getElementById('speedValue').textContent = (value / 1000) + 's';
            
            if (isPlaying) {{
                clearInterval(playInterval);
                playInterval = setInterval(stepForward, stepDelay);
            }}
        }}
    </script>
</body>
</html>'''
    
    return html


def save_viewer(game_engine, filename: str = "spectate.html") -> str:
    html = generate_viewer(game_engine)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    return filename
