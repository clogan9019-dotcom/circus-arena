#!/usr/bin/env python3
"""
Circus Arena - Ringmaster Edition!

🧠 Ringmaster (14B) creates world - takes DECENT TIME to finish!
🎭 Performers (0.5B) play the game  
💬 Performers give FEEDBACK to Ringmaster
🧠 Ringmaster IMPROVES based on feedback
🔄 Repeat!
"""
import time
import os
import threading
import http.server
import socketserver


# Simple HTTP server for the HTML file
def start_server(port=8080, filename="spectate.html"):
    """Start a simple HTTP server to serve the HTML file"""
    os.chdir(os.path.dirname(os.path.abspath(filename)) or '.')
    
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\n🌐 Local server running!")
        print(f"   Open: http://localhost:{port}/{filename}")
        print(f"   Or just: http://localhost:{port}")
        print(f"\n   Press Ctrl+C to stop the server")
        httpd.serve_forever()


def main():
    from circus import GameEngine
    from circus.viewer import save_viewer
    
    print("\n" + "=" * 50)
    print("🎪 CIRCUS ARENA - Ringmaster Edition! 🎪")
    print("=" * 50)
    print("""
    🧠 Ringmaster (14B) creates WORLD
       Takes DECENT TIME to finish! (15-25 steps)
    
    🎭 Performers (0.5B) PLAY the game
       ↓
    💬 Feedback -> RINGMASTER
       ↓
    🧠 Ringmaster IMPROVES
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
            print("\n   📖 Ringmaster improved the adventure!")
        
        time.sleep(0.5)
    
    # Generate spectate HTML
    print("\n" + "=" * 60)
    print("🎮 GENERATING 3D SPECTATE VIEWER")
    print("=" * 60)
    
    filename = "spectate.html"
    save_viewer(engine, filename)
    
    full_path = os.path.abspath(filename)
    print(f"\n✅ Saved: {full_path}")
    
    # Start local server in background
    print("\n" + "=" * 60)
    print("🌐 STARTING LOCAL SERVER")
    print("=" * 60)
    
    # Run server in thread
    server_thread = threading.Thread(target=start_server, args=(8080, filename), daemon=True)
    server_thread.start()
    
    # Give it a moment to start
    time.sleep(1)
    
    print(f"\n🎉 Open your browser and go to:")
    print(f"   http://localhost:8080")
    print(f"\n   You'll see 3D rooms, performers moving around,")
    print(f"   action logs, and feedback to the Ringmaster!")
    print(f"\n   Press Ctrl+C in this window to stop the server")
    
    # Keep running so user can view
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped!")


if __name__ == "__main__":
    main()
