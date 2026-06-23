"""
Performer - AI agents that play and give feedback to Ringmaster
"""
import ollama


class Performer:
    """An AI performer that plays the game and reports back to Ringmaster"""
    
    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model
        self.current_room = None
        self.inventory = []
        self.steps = 0
        self.thoughts = []
    
    def play_turn(self, world: dict, round_obj: dict) -> dict:
        """Actually play the game"""
        room_data = self._get_room(world, self.current_room)
        
        context = f"""You are {self.name}, playing an adventure game!

Round: {round_obj['name']}
Objective: {round_obj['objective']}

Current Room: {room_data['name']}
Description: {room_data['description']}

Exits: {self._get_exits(room_data)}
Items: {room_data.get('items', [])}
NPCs: {room_data.get('npcs', [])}

Inventory: {self.inventory}
Steps: {self.steps}

Choose ONE action:
- move_north / move_south / move_east / move_west
- take [item]
- talk [npc]
- look

Output JSON: {{"action": "action", "target": "target", "thinking": "why"}}
"""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": context}],
                options={"temperature": 0.6, "num_predict": 80}
            )
            
            content = response['message']['content']
            
            decision = {"action": "look", "thinking": content[:50]}
            if '"action"' in content:
                import json
                try:
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0]
                    else:
                        json_str = content
                    decision = json.loads(json_str)
                except:
                    pass
            
            result = self._execute_action(decision, world)
            
            return {
                "performer": self.name,
                "decision": decision,
                "result": result,
                "room": self.current_room,
                "inventory": self.inventory.copy()
            }
            
        except Exception as e:
            return {"performer": self.name, "error": str(e)}
    
    def give_feedback(self, world: dict, round_num: int) -> str:
        """Give FEEDBACK directly to the Ringmaster (14B)"""
        
        context = f"""As {self.name}, you just played through this adventure. 

Adventure: {world.get('title', 'Unknown')}
Round: {round_num + 1}

What you experienced:
- Explored: {self.current_room}
- Found items: {self.inventory}
- Steps taken: {self.steps}
- Thoughts: {self.thoughts[-2:] if self.thoughts else 'Played carefully'}

Now give HONEST FEEDBACK to the Ringmaster (14B AI):
1. What was confusing or frustrating?
2. What was fun or well-designed?
3. What would make it better?
4. Rate 1-10 and explain

This feedback goes DIRECTLY to the Ringmaster to improve the game!
"""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": context}],
                options={"temperature": 0.8, "num_predict": 150}
            )
            return response['message']['content']
        except Exception as e:
            return f"Feedback error: {e}"
    
    def _get_room(self, world: dict, room_id: str) -> dict:
        for room in world.get('world', {}).get('rooms', []):
            if room['id'] == room_id:
                return room
        return {"id": "unknown", "name": "Unknown", "description": "Nothing here", "items": [], "npcs": []}
    
    def _get_exits(self, room: dict) -> list:
        exits = [d for d in ['north', 'south', 'east', 'west'] if room.get(d)]
        return exits if exits else ["blocked"]
    
    def _execute_action(self, decision: dict, world: dict) -> str:
        action = decision.get('action', 'look')
        target = decision.get('target', '')
        room_data = self._get_room(world, self.current_room)
        
        if action == 'look':
            return room_data['description']
        
        elif action.startswith('move_'):
            direction = action.replace('move_', '')
            next_room = room_data.get(direction)
            if next_room:
                self.current_room = next_room
                self.steps += 1
                self.thoughts.append(f"Moved {direction}")
                return f"Moved {direction}"
            return f"Can't go {direction}"
        
        elif action == 'take' and target:
            if target in room_data.get('items', []):
                room_data['items'].remove(target)
                self.inventory.append(target)
                self.thoughts.append(f"Took {target}")
                return f"Took {target}"
            return f"No {target} here"
        
        elif action == 'talk' and target:
            for npc in world.get('world', {}).get('npcs', []):
                if npc['id'] == target:
                    self.thoughts.append(f"Talked to {npc['name']}")
                    return f"{npc['name']}: {npc['dialogue']}"
            return "No one to talk to"
        
        return "Did nothing"
