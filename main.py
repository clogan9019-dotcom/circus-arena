#!/usr/bin/env python3
"""
Circus Arena - Ringmaster Edition!
"""
import time
import os

from circus import GameEngine
from circus.html_generator import save_html_game


def main():
    print("\n" + "=" * 50)
    print("🎪 CIRCUS ARENA - Ringmaster Edition! 🎪")
    print("=" * 50)
    print("""
    LOOP:
    🧠 Ringmaster (14B) creates world
       ↓
    🎭 Performers (0.5B) play
       ↓
    💬 Feedback -> RINGMASTER
       ↓
    🧠 Ringmaster improves world
       ↓
    🔄 Repeat!
    """)
    
    engine = GameEngine(
        ringmaster_model="Qwen2.5-Coder-14B-Instruct-abliterated:latest",
        performer_model="qwen2.5:0.5b",
        num_performers=2
    )
    
    engine.start_game()
    num_rounds = 2  # Fewer rounds for faster generation
    
    print("\n" + "=" * 60)
    print(f"🎮 PLAYING {num_rounds} ROUNDS WITH FEEDBACK LOOP")
    print("=" * 60)
    
    for round_num in range(num_rounds):
        print("\n" + "=" * 50)
        print(f"🔄 ITERATION {round_num + 1}")
        print("=" * 50)
        
        engine.play_round(round_num)
        feedback = engine.collect_feedback(round_num)
        improvement = engine.ringmaster_improves(feedback, round_num)
        
        if improvement.get('improved'):
            print("\n   📖 New adventure version:")
            print(f"   {engine.world.get('title', 'Unknown')}")
        
        time.sleep(0.5)
    
    # Generate PLAYABLE HTML game
    print("\n" + "=" * 60)
    print("🎮 GENERATING PLAYABLE ADVENTURE!")
    print("=" * 60)
    
    output_file = save_html_game(engine.get_render_data(), "play_adventure.html")
    
    full_path = os.path.abspath(output_file)
    print(f"\n✅ PLAYABLE GAME SAVED: {full_path}")
    print("\n🌐 Open the file in your browser to PLAY!")
    print("   You control the performer, move around, collect items, talk to NPCs!")
    
    # Try to open browser
    try:
        import webbrowser
        webbrowser.open(f'file://{full_path}')
        print("\n🌐 Opening in your browser...")
    except:
        pass


if __name__ == "__main__":
    main()
