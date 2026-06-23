#!/usr/bin/env python3
"""
Circus Arena - Ringmaster Edition!

🧠 Ringmaster (14B) creates world
🎭 Performers (0.5B) play the game  
💬 Performers give FEEDBACK to Ringmaster
🧠 Ringmaster IMPROVES based on feedback
🔄 Repeat!
"""
import time
import os

from circus import GameEngine
from circus.html_generator import save_html_game
from circus.viewer import save_viewer


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
    num_rounds = 2
    
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
    
    # Generate both outputs
    print("\n" + "=" * 60)
    print("🎮 GENERATING OUTPUTS")
    print("=" * 60)
    
    # 1. PLAYABLE GAME - YOU can play it
    play_file = save_html_game(engine.get_render_data(), "play_adventure.html")
    
    # 2. SPECTATOR VIEW - WATCH the AI play!
    spectate_file = save_viewer(engine, "spectate.html")
    
    print(f"\n✅ PLAYABLE GAME (YOU play): {os.path.abspath(play_file)}")
    print(f"✅ SPECTATOR VIEW (WATCH AI): {os.path.abspath(spectate_file)}")
    print("\n🌐 Opening SPECTATOR VIEW...")
    
    # Open spectator view by default
    try:
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(spectate_file)}')
    except:
        pass


if __name__ == "__main__":
    main()
