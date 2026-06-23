"""
World Generator - Ringmaster creates complete adventure worlds
"""
import json
import ollama


SYSTEM_PROMPT = """You are the Ringmaster of Circus Arena. You create complete, unique adventure worlds for AI performers to play.

IMPORTANT: Make the adventure TAKE A DECENT AMOUNT OF TIME to finish! This means:
- Multiple layers/levels to explore
- Several rooms (8-15 rooms minimum)
- Multiple objectives that must be completed in sequence
- Items that must be collected before proceeding
- NPCs with quests/challenges
- 3+ distinct areas with different themes
- A final challenge that requires completing earlier tasks

Think of it like a mini RPG - the performers should need 15-25 steps to complete it!

Your job:
1. Create an interesting world with a clear setting/backstory
2. Define rooms/locations with connections (8-15 rooms)
3. Add NPCs, items, and atmosphere
4. Set a WIN condition and FAIL condition
5. Create 3-5 rounds/challenges of increasing difficulty

Output ONLY valid JSON - no markdown, no extra text. Keep it interesting and unique!

JSON structure:
{
  "title": "Adventure Name",
  "setting": "2-3 sentences about the world - make it interesting!",
  "rounds": [
    {"id": 1, "name": "Round Name", "objective": "What to do", "hint": "Optional hint"},
    {"id": 2, "name": "Round Name", "objective": "What to do"},
    {"id": 3, "name": "Round Name", "objective": "What to do"},
    {"id": 4, "name": "Round Name", "objective": "What to do"}
  ],
  "world": {
    "rooms": [
      {"id": "room_id", "name": "Name", "description": "desc", 
       "north": "room_id or null", "south": null, "east": null, "west": null,
       "items": ["item_id"], "npcs": ["npc_id"], "theme": "cave/tower/garden/etc"}
    ],
    "items": [{"id": "item_id", "name": "Name", "description": "desc", "effect": "what it does"}],
    "npcs": [{"id": "npc_id", "name": "Name", "dialogue": "What they say", "role": "type", "quest": "optional quest"}]
  },
  "start_room": "room_id",
  "win_condition": "How to win - make it require completing multiple steps!",
  "fail_condition": "What causes failure",
  "difficulty": "easy/medium/hard",
  "estimated_time": "15-25 steps"
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
            "Create a haunted mansion adventure with hidden secrets, multiple floors, secret passages, and a mystery to solve!",
            "Create a sci-fi space station survival scenario with multiple decks, airlocks, and dangerous areas!",
            "Create a fantasy dungeon escape with traps, puzzles, multiple levels, and treasure!",
            "Create a pirate treasure hunt on a mysterious island with caves, jungles, and buried treasure!",
            "Create a cyberpunk hacker infiltration mission through multiple systems and security layers!",
            "Create a post-apocalyptic wasteland survival story with multiple locations and resources to find!",
        ]
        
        import time
        prompt = prompts[int(time.time()) % len(prompts)]
        
        response = ollama.chat(
            model=self.ringmaster_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Create a unique, CREATIVE adventure that takes time to complete! Minimum 10 rooms, multiple objectives, interesting story. {prompt}"}
            ],
            options={"temperature": 1.0, "num_predict": 800}
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
            "title": "The Lost Temple of Azurath",
            "setting": "An ancient temple has appeared in the mountains. Legends speak of a treasure that requires solving multiple puzzles to obtain.",
            "rounds": [
                {"id": 1, "name": "Enter the Temple", "objective": "Find the entrance and explore the first chamber"},
                {"id": 2, "name": "Collect the Keys", "objective": "Find the three elemental keys hidden in different areas"},
                {"id": 3, "name": "Solve the Riddle", "objective": "Speak to the Oracle and solve the ancient riddle"},
                {"id": 4, "name": "Claim the Treasure", "objective": "Use the keys to open the treasure vault and escape"}
            ],
            "world": {
                "rooms": [
                    {"id": "entrance", "name": "Temple Entrance", "description": "Massive stone pillars flank an ancient doorway. Torchlight flickers.", 
                     "north": "main_hall", "items": ["torch"], "npcs": [], "theme": "temple"},
                    {"id": "main_hall", "name": "Main Hall", "description": "A grand hall with columns. Ancient symbols glow on the floor.", 
                     "south": "entrance", "east": "fire_chamber", "west": "water_chamber", "north": "oracle_room", "items": [], "npcs": ["guardian"], "theme": "hall"},
                    {"id": "fire_chamber", "name": "Fire Chamber", "description": "The room is warm, with flames along the walls.", 
                     "west": "main_hall", "items": ["fire_key"], "npcs": [], "theme": "fire"},
                    {"id": "water_chamber", "name": "Water Chamber", "description": "Water drips from stalactites. A pool glows in the center.", 
                     "east": "main_hall", "items": ["water_key"], "npcs": [], "theme": "water"},
                    {"id": "oracle_room", "name": "Oracle Chamber", "description": "A mysterious figure sits on a stone throne.", 
                     "south": "main_hall", "north": "locked_vault", "items": ["riddle_answer"], "npcs": ["oracle"], "theme": "mystic"},
                    {"id": "locked_vault", "name": "Sealed Vault", "description": "Three keyholes gleam in the massive door.", 
                     "south": "oracle_room", "east": "treasure_room", "items": [], "npcs": [], "theme": "vault"},
                    {"id": "treasure_room", "name": "Treasure Chamber", "description": "Gold and jewels glitter in the torchlight!", 
                     "west": "locked_vault", "items": ["treasure"], "npcs": [], "theme": "treasure"}
                ],
                "items": [
                    {"id": "torch", "name": "Ancient Torch", "description": "Illuminates dark areas", "effect": "reveals_secrets"},
                    {"id": "fire_key", "name": "Fire Key", "description": "A key made of obsidian", "effect": "unlocks_fire"},
                    {"id": "water_key", "name": "Water Key", "description": "A key made of pearl", "effect": "unlocks_water"},
                    {"id": "riddle_answer", "name": "Ancient Wisdom", "description": "The answer to the Oracle's riddle", "effect": "opens_vault"},
                    {"id": "treasure", "name": "Azurath's Treasure", "description": "The legendary artifact!", "effect": "win_game"}
                ],
                "npcs": [
                    {"id": "guardian", "name": "Stone Guardian", "dialogue": "Only the worthy may proceed.", "role": "guardian", "quest": "Prove your worth"},
                    {"id": "oracle", "name": "The Oracle", "dialogue": "Answer my riddle to proceed.", "role": "quest_giver", "quest": "Solve the riddle of time"}
                ]
            },
            "start_room": "entrance",
            "win_condition": "Collect all three keys, solve the Oracle's riddle, unlock the vault, and claim the treasure!",
            "fail_condition": "Get lost or take too long (30+ turns)",
            "difficulty": "medium",
            "estimated_time": "20-25 steps"
        }
