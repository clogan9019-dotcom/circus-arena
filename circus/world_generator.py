"""
World Generator - Ringmaster creates complete adventure worlds
"""
import json
import ollama


SYSTEM_PROMPT = """You are the Ringmaster of Circus Arena. You create complete, unique adventure worlds for AI performers to play.

Your job:
1. Create an interesting world with a clear setting/backstory
2. Define rooms/locations with connections
3. Add NPCs, items, and atmosphere
4. Set a WIN condition and FAIL condition
5. Create 3 rounds/challenges of increasing difficulty

Output ONLY valid JSON - no markdown, no extra text. Keep it interesting and unique!

JSON structure:
{
  "title": "Adventure Name",
  "setting": "2-3 sentences about the world",
  "rounds": [
    {"id": 1, "name": "Round Name", "objective": "What to do", "hint": "Optional hint"},
    {"id": 2, "name": "Round Name", "objective": "What to do"},
    {"id": 3, "name": "Round Name", "objective": "What to do"}
  ],
  "world": {
    "rooms": [
      {"id": "room_id", "name": "Name", "description": "desc", 
       "north": "room_id or null", "south": null, "east": null, "west": null,
       "items": ["item_id"], "npcs": ["npc_id"]}
    ],
    "items": [{"id": "item_id", "name": "Name", "description": "desc", "effect": "what it does"}],
    "npcs": [{"id": "npc_id", "name": "Name", "dialogue": "What they say", "role": "type"}]
  },
  "start_room": "room_id",
  "win_condition": "How to win",
  "fail_condition": "What causes failure",
  "difficulty": "easy/medium/hard"
}
"""


class WorldGenerator:
    """Ringmaster AI generates complete adventure worlds"""
    
    def __init__(self, ringmaster_model: str = "Qwen2.5-Coder-14B-Instruct-abliterated:latest"):
        self.ringmaster_model = ringmaster_model
    
    def generate(self) -> dict:
        """Generate a complete adventure world"""
        print("🧠 Ringmaster is creating an adventure...")
        
        prompts = [
            "Create a haunted mansion adventure with hidden secrets",
            "Create a sci-fi space station survival scenario",
            "Create a fantasy dungeon escape with traps and puzzles",
            "Create a pirate treasure hunt on a mysterious island",
            "Create a cyberpunk hacker infiltration mission",
            "Create a post-apocalyptic wasteland survival story",
        ]
        
        import time
        prompt = prompts[int(time.time()) % len(prompts)]
        
        response = ollama.chat(
            model=self.ringmaster_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Create a unique, creative adventure. {prompt}"}
            ],
            options={"temperature": 1.0, "num_predict": 600}
        )
        
        content = response['message']['content']
        print(f"   Ringmaster created: {content[:80]}...")
        
        try:
            json_str = content
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0]
            
            world = json.loads(json_str.strip())
            return self._validate_world(world)
        except json.JSONDecodeError as e:
            print(f"⚠️ Parse error: {e}")
            return self._fallback_world()
    
    def _validate_world(self, world: dict) -> dict:
        """Ensure world has required structure"""
        required = ['title', 'world', 'start_room', 'win_condition']
        for field in required:
            if field not in world:
                if field == 'world':
                    world['world'] = {'rooms': [], 'items': [], 'npcs': []}
                else:
                    raise ValueError(f"Missing: {field}")
        
        room_ids = [r['id'] for r in world['world'].get('rooms', [])]
        if world['start_room'] not in room_ids:
            world['start_room'] = room_ids[0] if room_ids else 'room_1'
        
        return world
    
    def _fallback_world(self) -> dict:
        """Fallback adventure"""
        return {
            "title": "The Lost Temple",
            "setting": "An ancient temple has appeared in the mountains. Strange lights glow from within.",
            "rounds": [
                {"id": 1, "name": "Enter the Temple", "objective": "Find the entrance and enter safely"},
                {"id": 2, "name": "Navigate the Chambers", "objective": "Find the golden key hidden in the chambers"},
                {"id": 3, "name": "Escape with Treasure", "objective": "Use the key to open the treasure room and escape"}
            ],
            "world": {
                "rooms": [
                    {"id": "entrance", "name": "Temple Entrance", "description": "Stone pillars flank a dark doorway", 
                     "north": "hallway", "items": ["torch"], "npcs": []},
                    {"id": "hallway", "name": "Main Hall", "description": "A long corridor with glowing runes", 
                     "south": "entrance", "east": "chamber1", "west": "chamber2", "north": "locked_door", "items": [], "npcs": ["guardian"]},
                    {"id": "chamber1", "name": "East Chamber", "description": "Dusty room with old artifacts", 
                     "west": "hallway", "items": ["key"], "npcs": []},
                    {"id": "chamber2", "name": "West Chamber", "description": "Collapsed room, not safe", 
                     "east": "hallway", "items": [], "npcs": []},
                    {"id": "locked_door", "name": "Locked Door", "description": "A heavy door with a golden lock", 
                     "south": "hallway", "items": [], "npcs": []},
                    {"id": "treasure", "name": "Treasure Room", "description": "Glittering gold everywhere!", 
                     "south": "locked_door", "items": ["treasure"], "npcs": []}
                ],
                "items": [
                    {"id": "torch", "name": "Ancient Torch", "description": "Lights up dark areas", "effect": "reveals_secrets"},
                    {"id": "key", "name": "Golden Key", "description": "Opens the treasure room", "effect": "unlocks_door"},
                    {"id": "treasure", "name": "Ancient Treasure", "description": "The legendary artifact", "effect": "win_game"}
                ],
                "npcs": [
                    {"id": "guardian", "name": "Stone Guardian", "dialogue": "Only the worthy may pass", "role": "guardian"}
                ]
            },
            "start_room": "entrance",
            "win_condition": "Collect the golden key, open the locked door, and claim the treasure",
            "fail_condition": "Get trapped or take too long (15+ turns)",
            "difficulty": "medium"
        }
