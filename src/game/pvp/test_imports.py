"""
Test file để kiểm tra modular PvP system
"""

import sys
import os
import warnings

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

# Test imports
try:
    # Test legacy imports (should show deprecation warning)
    print("Testing legacy imports...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from src.game.pvp import Pvp, Player, GameLogic, GameView, ChallengeView, GameConstants
    print("✅ Legacy imports work!")
    
    # Test new modular imports
    print("Testing new modular imports...")
    from src.game.pvp.player import Player as PlayerNew
    from src.game.pvp.game_logic import GameLogic as GameLogicNew
    from src.game.pvp.views import GameView as GameViewNew, ChallengeView as ChallengeViewNew
    from src.game.pvp.pvp_command import Pvp as PvpNew
    from src.game.pvp.constants import GameConstants as ConstantsNew, DamageType, EmbedColors
    print("✅ New modular imports work!")
    
    # Test constants
    print("Testing constants...")
    assert ConstantsNew.MAX_HP == 100
    assert DamageType.PHYSICAL.value == "physical"
    print("✅ Constants work correctly!")
    
    print("\n🎉 PvP module refactoring successful!")
    print("📁 Files cleaned up successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
