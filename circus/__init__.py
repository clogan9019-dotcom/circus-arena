"""
Circus Arena - Ringmaster Edition!

🧠 Ringmaster (14B) creates adventure
🎭 Performers (0.5B) play the game  
💬 Performers give FEEDBACK to Ringmaster
🧠 Ringmaster IMPROVES based on feedback
🔄 Repeat!
"""
from .game_engine import GameEngine
from .world_generator import WorldGenerator
from .performer import Performer
from .html_generator import save_html_game, generate_html_game

__version__ = "0.5.0"
__all__ = ["GameEngine", "WorldGenerator", "Performer", "save_html_game", "generate_html_game"]
