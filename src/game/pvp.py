"""
PvP Game - Legacy Compatibility File

⚠️  DEPRECATED: This file is for backward compatibility only.
    Please use the new modular imports:
    
    from src.game.pvp.pvp_command import Pvp
    from src.game.pvp.player import Player
    from src.game.pvp.views import GameView, ChallengeView
    from src.game.pvp.game_logic import GameLogic
    from src.game.pvp.constants import GameConstants, DamageType

New modular structure:
- pvp/constants.py: Game constants, enums, balance values
- pvp/player.py: Player model and stats
- pvp/game_logic.py: Combat calculations and game logic  
- pvp/views.py: Discord UI components
- pvp/pvp_command.py: Main command handler

Original code backup: pvp_original.py
"""

import warnings

# Show deprecation warning
warnings.warn(
    "Importing from src.game.pvp is deprecated. "
    "Use modular imports: from src.game.pvp.pvp_command import Pvp",
    DeprecationWarning,
    stacklevel=2
)

# Import the modular PvP system for backward compatibility
try:
    from .pvp.pvp_command import Pvp
    from .pvp.player import Player
    from .pvp.game_logic import GameLogic
    from .pvp.views import GameView, ChallengeView
    from .pvp.constants import GameConstants, DamageType, ActionType, EmbedColors, Emojis
    
    # Keep the legacy import structure
    __all__ = [
        'Pvp', 'Player', 'GameLogic', 'GameView', 'ChallengeView',
        'GameConstants', 'DamageType', 'ActionType', 'EmbedColors', 'Emojis'
    ]
    
except ImportError as e:
    raise ImportError(
        f"Failed to import PvP modules: {e}\n"
        "Please ensure all PvP modules are properly installed."
    ) from e
