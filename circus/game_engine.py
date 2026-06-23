"""
Game Engine - The main game loop with Ringmaster feedback loop
"""
import ollama
from .world_generator import WorldGenerator
from .performer import Performer


class GameEngine:
    """Ringmaster creates world -> Performers play -> Feedback to Ringmaster -> Improve"""
    
    def __init__(self, 
                 ringmaster_model: str = "Qwen2.5-Coder-14B-Instruct-abliterated:latest",
                 performer_model: str = "qwen2.5:0.5b",
                 num_performers: int = 2):
        
        self.ringmaster_model = ringmaster_model
        self.performer_model = performer_model
        
        self.performers = [
            Performer(f"Performer-{i+1}", performer_model) 
            for i in range(num_performers)
        ]
        
        self.generator = WorldGenerator(ringmaster_model)
        self.world = {}
        self.revisions = []
        self.game_log = []
        
    def start_game(self):
        """Ringmaster creates initial adventure"""
        print("\n" + "=" * 50)
        print("\n🎪 CIRCUS ARENA - Ringmaster Edition! 🎪")
        print("\n" + "=" * 50)
        
        print("\n🧠 Ringmaster (14B) is creating an adventure...")
        self.world = self.generator.generate()
        
        print("\n" + "=" * 60)
        print("📖 THE ADVENTURE:")
        print("=" * 60)
        print(f"🎬 {self.world.get('title', 'Unknown')}")
        print(f"   {self.world.get('setting', '')}")
        print(f"\n🎯 Win: {self.world.get('win_condition', 'Unknown')}")
        
        start_room = self.world.get('start_room', 'room_1')
        for p in self.performers:
            p.current_room = start_room
            p.inventory = []
            p.steps = 0
        
        print(f"\n🎭 {len(self.performers)} performers ready to play!")
    
    def play_round(self, round_num: int) -> dict:
        """Performers play the round"""
        rounds = self.world.get('rounds', [])
        round_obj = rounds[round_num] if round_num < len(rounds) else {
            "name": "Explore", 
            "objective": "Explore and interact"
        }
        
        print("\n" + "=" * 60)
        print(f"🎮 ROUND {round_num + 1}: {round_obj['name']}")
        print(f"📋 {round_obj['objective']}")
        print("=" * 60)
        
        round_results = []
        
        for performer in self.performers:
            print(f"\n🎭 {performer.name} playing:")
            result = performer.play_turn(self.world, round_obj)
            
            print(f"   💭 {result.get('decision', {}).get('thinking', '...')[:60]}...")
            print(f"   ➡️  {result.get('decision', {}).get('action', 'look')}")
            print(f"   📍 Now in: {result.get('room', 'unknown')}")
            
            round_results.append(result)
        
        return {"round": round_num, "results": round_results}
    
    def collect_feedback(self, round_num: int) -> list:
        """Collect feedback from performers TO THE RINGMASTER"""
        print("\n" + "=" * 60)
        print("💬 PERFORMER FEEDBACK -> RINGMASTER")
        print("=" * 60)
        
        feedback_list = []
        
        for performer in self.performers:
            print(f"\n📣 {performer.name}'s feedback to Ringmaster:")
            feedback = performer.give_feedback(self.world, round_num)
            print(f"   {feedback[:200]}...")
            feedback_list.append(feedback)
        
        return feedback_list
    
    def ringmaster_improves(self, feedback_list: list, round_num: int) -> dict:
        """Ringmaster uses feedback to improve the adventure"""
        print("\n" + "=" * 60)
        print("🧠 RINGMASTER RECEIVES FEEDBACK & IMPROVES!")
        print("=" * 60)
        
        feedback_text = "\n\n".join([f"{i+1}. {f}" for i, f in enumerate(feedback_list)])
        
        improvement_prompt = f"""You are the Ringmaster of Circus Arena. Performers just played through your adventure and gave you FEEDBACK.

Adventure: {self.world.get('title', 'Unknown')}
Round {round_num + 1}

Performer Feedback:
{feedback_text}

Based on this feedback, improve the adventure. You can:
- Adjust difficulty
- Add/remove challenges
- Improve descriptions
- Add more interesting elements
- Fix confusing parts

Output ONLY the improved adventure as JSON (same format as before). Keep what worked, fix what didn't.
"""
        
        try:
            response = ollama.chat(
                model=self.ringmaster_model,
                messages=[{"role": "user", "content": improvement_prompt}],
                options={"temperature": 0.7, "num_predict": 500}
            )
            
            content = response['message']['content']
            print(f"\n   🧠 Ringmaster improved the adventure!")
            
            import json
            json_str = content
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0]
            
            improved_world = json.loads(json_str.strip())
            
            self.revisions.append({
                "round": round_num,
                "feedback": feedback_list,
                "improvements": "World updated based on performer feedback"
            })
            
            self.world.update(improved_world)
            
            print(f"   ✅ World improved! Changes tracked.")
            
            return {"improved": True, "world": improved_world}
            
        except Exception as e:
            print(f"   ⚠️ Couldn't improve: {e}")
            return {"improved": False, "error": str(e)}
    
    def get_render_data(self) -> dict:
        """Get data for HTML visualization"""
        return {
            "title": self.world.get('title', 'Circus Arena'),
            "setting": self.world.get('setting', ''),
            "rounds": self.world.get('rounds', []),
            "world": self.world.get('world', {}),
            "performers": [
                {
                    "name": p.name,
                    "room": p.current_room,
                    "inventory": p.inventory,
                    "steps": p.steps
                }
                for p in self.performers
            ],
            "revisions": self.revisions,
            "log": self.game_log,
            "win_condition": self.world.get('win_condition', '')
        }
