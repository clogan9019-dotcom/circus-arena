"""
HTML Generator - Creates PLAYABLE interactive adventure game!
"""
import json


def generate_html_game(world_data: dict) -> str:
    """Generate a fully playable HTML5 adventure game"""
    
    title = world_data.get('title', 'Circus Arena Adventure')
    setting = world_data.get('setting', '')
    world = world_data.get('world', {})
    rooms = world.get('rooms', [])
    items = world.get('items', [])
    npcs = world.get('npcs', [])
    
    start_room = world_data.get('start_room', rooms[0]['id'] if rooms else 'room_1')
    
    rooms_json = json.dumps(rooms)
    items_json = json.dumps(items)
    npcs_json = json.dumps(npcs)
    
    win_condition = world_data.get('win_condition', 'Explore and complete the adventure')
    rounds_html = ""
    for r in world_data.get('rounds', []):
        rounds_html += f'<p style="color:#ffd700;">Round {r["id"]}: {r["name"]} - {r.get("objective", "")}</p>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎪 {title} - PLAY NOW!</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        
        header {{
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 3s linear infinite;
        }}
        
        @keyframes shine {{ to {{ background-position: 200% center; }} }}
        
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .subtitle {{ color: #aaa; font-size: 1.1em; font-style: italic; }}
        
        .viewport {{
            background: #0d0d1a;
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            border: 2px solid rgba(255,255,255,0.1);
        }}
        
        .room-header {{ text-align: center; margin-bottom: 20px; }}
        
        .room-name {{
            font-size: 2em;
            color: #ffd700;
            text-shadow: 0 0 20px rgba(255,215,0,0.5);
        }}
        
        .room-desc {{
            color: #ccc;
            line-height: 1.6;
            margin: 15px 0;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }}
        
        .room-3d {{
            perspective: 1000px;
            height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        }}
        
        .room-box {{
            transform-style: preserve-3d;
            transform: rotateX(-15deg) rotateY(-20deg);
            transition: all 0.5s ease;
        }}
        
        .room-face {{
            position: absolute;
            background: linear-gradient(145deg, #2a2a4a, #1a1a3a);
            border: 1px solid #3a3a5a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
        }}
        
        .floor {{ width: 200px; height: 200px; transform: rotateX(90deg) translateZ(-30px); background: repeating-linear-gradient(45deg, #1a1a2e, #1a1a2e 20px, #252540 20px, #252540 40px); }}
        .ceiling {{ width: 200px; height: 200px; transform: rotateX(90deg) translateZ(80px); background: #0a0a15; }}
        .wall-front {{ width: 200px; height: 110px; transform: translateZ(100px); background: linear-gradient(to bottom, #1a1a3a, #2a2a4a); }}
        .wall-back {{ width: 200px; height: 110px; transform: translateZ(-100px) rotateY(180deg); background: linear-gradient(to bottom, #1a1a3a, #2a2a4a); }}
        .wall-left {{ width: 200px; height: 110px; transform: translateX(-100px) rotateY(-90deg); background: linear-gradient(to bottom, #252545, #353560); }}
        .wall-right {{ width: 200px; height: 110px; transform: translateX(100px) rotateY(90deg); background: linear-gradient(to bottom, #252545, #353560); }}
        
        .controls {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            max-width: 250px;
            margin: 20px auto;
        }}
        
        .btn {{ padding: 15px; font-size: 1.2em; background: linear-gradient(145deg, #3a3a5a, #2a2a4a); border: 2px solid #4a4a6a; border-radius: 10px; color: #fff; cursor: pointer; transition: all 0.2s; }}
        .btn:hover {{ transform: scale(1.05); box-shadow: 0 5px 20px rgba(255,215,0,0.3); border-color: #ffd700; }}
        .btn:active {{ transform: scale(0.95); }}
        .btn.move {{ background: linear-gradient(145deg, #3a5a8a, #2a4a7a); }}
        
        .status-bar {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0; }}
        
        .status-box {{ background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; text-align: center; }}
        .status-title {{ font-size: 0.9em; color: #888; margin-bottom: 5px; }}
        .status-value {{ font-size: 1.2em; color: #4ecdc4; }}
        
        .entities {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        
        .entity-card {{ background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; text-align: center; cursor: pointer; transition: all 0.2s; }}
        .entity-card:hover {{ background: rgba(255,255,255,0.1); transform: translateY(-5px); }}
        .entity-icon {{ font-size: 2.5em; }}
        .entity-name {{ font-weight: bold; margin: 10px 0 5px; }}
        .entity-desc {{ font-size: 0.85em; color: #aaa; }}
        
        .exits {{ display: flex; justify-content: center; gap: 15px; margin: 20px 0; flex-wrap: wrap; }}
        
        .exit-btn {{ padding: 10px 20px; background: linear-gradient(145deg, #2a4a6a, #1a3a5a); border: 2px solid #3a5a8a; border-radius: 8px; color: #4ecdc4; cursor: pointer; transition: all 0.2s; }}
        .exit-btn:hover {{ background: linear-gradient(145deg, #3a6a9a, #2a5a8a); box-shadow: 0 5px 15px rgba(78,205,196,0.3); }}
        
        .log {{ background: rgba(0,0,0,0.4); border-radius: 10px; padding: 15px; margin: 20px 0; max-height: 150px; overflow-y: auto; }}
        .log-entry {{ padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .log-entry:last-child {{ border-bottom: none; }}
        .log-action {{ color: #ffd700; }}
        .log-info {{ color: #4ecdc4; }}
        
        .modal {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); display: flex; align-items: center; justify-content: center; z-index: 100; }}
        
        .modal-content {{ background: linear-gradient(145deg, #1a1a2e, #2a2a4e); border-radius: 20px; padding: 40px; text-align: center; max-width: 500px; }}
        
        .start-btn {{ padding: 20px 40px; font-size: 1.5em; background: linear-gradient(145deg, #6bcb77, #4a9a57); border: none; border-radius: 15px; color: #fff; cursor: pointer; margin-top: 20px; }}
        .start-btn:hover {{ transform: scale(1.05); box-shadow: 0 10px 30px rgba(107,203,119,0.4); }}
        
        footer {{ text-align: center; padding: 20px; color: #666; }}
    </style>
</head>
<body>
    <div class="modal" id="startModal">
        <div class="modal-content">
            <h1>🎪 {title} 🎪</h1>
            <p class="subtitle" style="margin: 20px 0;">{setting}</p>
            <h3 style="color: #ffd700;">🎯 Objective:</h3>
            <p style="color: #ccc; margin: 10px 0;">{win_condition}</p>
            <h3 style="color: #4ecdc4; margin-top: 20px;">🎮 Controls:</h3>
            <p style="color: #aaa; margin: 10px 0;">Move with buttons, click items to pick up, click NPCs to talk</p>
            <button class="start-btn" onclick="startGame()">🎮 START!</button>
        </div>
    </div>
    
    <div class="container">
        <header>
            <h1>🎪 {title} 🎪</h1>
            <p class="subtitle">{setting}</p>
        </header>
        
        <div class="viewport">
            <div class="room-header">
                <div class="room-name" id="roomName">Loading...</div>
            </div>
            
            <div class="room-3d">
                <div class="room-box">
                    <div class="room-face floor"></div>
                    <div class="room-face ceiling"></div>
                    <div class="room-face wall-front" id="wallFront">🚪</div>
                    <div class="room-face wall-back">🧱</div>
                    <div class="room-face wall-left">🧱</div>
                    <div class="room-face wall-right">🧱</div>
                </div>
            </div>
            
            <div class="room-desc" id="roomDesc">...</div>
            
            <div class="exits" id="exits"></div>
            <div class="entities" id="entities"></div>
            
            <div class="controls">
                <div></div>
                <button class="btn move" onclick="move('north')">⬆️</button>
                <div></div>
                <button class="btn move" onclick="move('west')">⬅️</button>
                <button class="btn move" onclick="move('south')">⬇️</button>
                <button class="btn move" onclick="move('east')">➡️</button>
            </div>
        </div>
        
        <div class="status-bar">
            <div class="status-box">
                <div class="status-title">📍 Room</div>
                <div class="status-value" id="currentRoom">-</div>
            </div>
            <div class="status-box">
                <div class="status-title">🎒 Inventory</div>
                <div class="status-value" id="inventory">Empty</div>
            </div>
            <div class="status-box">
                <div class="status-title">👟 Steps</div>
                <div class="status-value" id="steps">0</div>
            </div>
        </div>
        
        <div class="log" id="gameLog">
            <div class="log-entry log-info">🎮 Adventure started!</div>
        </div>
    </div>
    
    <footer>🎪 Circus Arena | You ARE the performer!</footer>

    <script>
        const gameData = {{
            world: {{
                title: "{title}",
                startRoom: "{start_room}",
                rooms: {rooms_json},
                items: {items_json},
                npcs: {npcs_json}
            }},
            winCondition: "{win_condition}"
        }};
        
        let currentRoom = "{start_room}";
        let inventory = [];
        let steps = 0;
        let gameStarted = false;
        
        function startGame() {{
            document.getElementById('startModal').style.display = 'none';
            gameStarted = true;
            renderRoom();
            addLog("You begin your adventure!");
        }}
        
        function renderRoom() {{
            const room = gameData.world.rooms.find(r => r.id === currentRoom);
            if (!room) return;
            
            document.getElementById('roomName').textContent = room.name;
            document.getElementById('roomDesc').textContent = room.description;
            document.getElementById('currentRoom').textContent = room.name;
            
            // Render exits
            const exitsDiv = document.getElementById('exits');
            let exitsHtml = '';
            const directions = ['north', 'south', 'east', 'west'];
            directions.forEach(dir => {{
                if (room[dir]) {{
                    const targetRoom = gameData.world.rooms.find(r => r.id === room[dir]);
                    const roomName = targetRoom ? targetRoom.name : 'room';
                    exitsHtml += '<button class="exit-btn" onclick="move(\\'' + dir + '\\')">Go ' + dir + ' to ' + roomName + '</button>';
                }}
            }});
            if (!exitsHtml) exitsHtml = '<p style="color: #888;">No obvious exits</p>';
            exitsDiv.innerHTML = exitsHtml;
            
            // Render entities
            const entitiesDiv = document.getElementById('entities');
            let entitiesHtml = '';
            
            room.items?.forEach(itemId => {{
                const item = gameData.world.items.find(i => i.id === itemId);
                if (item) {{
                    entitiesHtml += '<div class="entity-card" onclick="takeItem(\\'' + itemId + '\\')"><div class="entity-icon">📦</div><div class="entity-name">' + item.name + '</div><div class="entity-desc">' + item.description + '</div><div style="color: #6bcb77;">Click to take!</div></div>';
                }}
            }});
            
            room.npcs?.forEach(npcId => {{
                const npc = gameData.world.npcs.find(n => n.id === npcId);
                if (npc) {{
                    const icons = {{'merchant': '🏪', 'guard': '🛡️', 'quest_giver': '📋', 'wizard': '🧙', 'guardian': '👹'}};
                    const icon = icons[npc.role] || '👤';
                    entitiesHtml += '<div class="entity-card" onclick="talk(\\'' + npcId + '\\')"><div class="entity-icon">' + icon + '</div><div class="entity-name">' + npc.name + '</div><div class="entity-desc">Click to talk</div></div>';
                }}
            }});
            
            if (!entitiesHtml) entitiesHtml = '<p style="color: #888;">Nothing special here</p>';
            entitiesDiv.innerHTML = entitiesHtml;
        }}
        
        function move(direction) {{
            const room = gameData.world.rooms.find(r => r.id === currentRoom);
            const nextRoomId = room && room[direction];
            
            if (nextRoomId) {{
                currentRoom = nextRoomId;
                steps++;
                document.getElementById('steps').textContent = steps;
                const nextRoom = gameData.world.rooms.find(r => r.id === nextRoomId);
                addLog('Moved ' + direction + ' to ' + (nextRoom ? nextRoom.name : 'unknown'));
                renderRoom();
            }} else {{
                addLog('Cannot go ' + direction + ' from here', 'info');
            }}
        }}
        
        function takeItem(itemId) {{
            const room = gameData.world.rooms.find(r => r.id === currentRoom);
            const idx = room && room.items ? room.items.indexOf(itemId) : -1;
            
            if (idx > -1) {{
                room.items.splice(idx, 1);
                inventory.push(itemId);
                document.getElementById('inventory').textContent = inventory.length > 0 ? inventory.join(', ') : 'Empty';
                const item = gameData.world.items.find(i => i.id === itemId);
                addLog('Took ' + (item ? item.name : itemId));
                renderRoom();
            }}
        }}
        
        function talk(npcId) {{
            const npc = gameData.world.npcs.find(n => n.id === npcId);
            if (npc) {{
                addLog(npc.name + ' says: "' + npc.dialogue + '"', 'info');
                if (npc.quest) addLog('Quest: ' + npc.quest, 'action');
            }}
        }}
        
        function addLog(message, type = 'action') {{
            const log = document.getElementById('gameLog');
            const entry = document.createElement('div');
            entry.className = 'log-entry log-' + type;
            entry.textContent = message;
            log.insertBefore(entry, log.firstChild);
        }}
        
        renderRoom();
    </script>
</body>
</html>'''
    
    return html


def save_html_game(world_data: dict, filename: str = "play_adventure.html") -> str:
    html = generate_html_game(world_data)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    return filename
