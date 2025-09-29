"""
TexasSolver GTO Poker API Integration
This module provides GTO (Game Theory Optimal) poker analysis functionality for research purposes.
"""

import requests
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class PokerAction(Enum):
    FOLD = "fold"
    CALL = "call"
    CHECK = "check"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"

class Position(Enum):
    BTN = "BTN"  # Button
    SB = "SB"    # Small Blind
    BB = "BB"    # Big Blind
    UTG = "UTG"  # Under the Gun
    MP = "MP"    # Middle Position
    CO = "CO"    # Cutoff

@dataclass
class HandRange:
    """Represents a poker hand range with associated frequencies"""
    hands: Dict[str, float]  # hand -> frequency
    position: Position
    action: PokerAction

@dataclass
class PokerHand:
    """Represents a specific poker hand"""
    cards: str  # e.g., "AhKs" for Ace of hearts, King of spades
    strength: float
    equity: float

@dataclass
class BetSizingPlan:
    """Represents equilibrium bet sizing recommendations across streets"""
    stack_size: int
    pot_size: float
    street_recommendations: Dict[str, Dict[str, float]]
    notes: str

@dataclass
class PostflopStrategy:
    """Summarizes equilibrium-inspired postflop guidance"""
    board: str
    category: str
    hero_range_advantage: str
    recommended_actions: Dict[str, str]
    blocker_applications: List[str]

@dataclass
class GTOSolution:
    """Represents a GTO solution for a specific situation"""
    ranges: Dict[Position, HandRange]
    ev: float  # Expected Value
    exploitability: float
    bet_sizing_plan: Optional[BetSizingPlan] = None
    postflop_strategy: Optional[PostflopStrategy] = None
    blocker_explanation: Optional[str] = None

class TexasSolverAPI:
    """
    TexasSolver GTO Poker API Client
    This class provides methods to analyze poker hands and situations using GTO principles.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.texassolver.com/v1"  # Hypothetical API endpoint
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _determine_stack_bucket(self, stack_size: int) -> str:
        if stack_size >= 80:
            return "deep"
        if stack_size >= 40:
            return "mid"
        return "short"

    def analyze_preflop_range(self, position: Position, stack_size: int = 100) -> HandRange:
        """
        Analyze optimal preflop hand range for a given position

        Args:
            position: Player position at the table
            stack_size: Stack size in big blinds

        Returns:
            HandRange: Optimal hand range with frequencies
        """
        stack_profile = self._determine_stack_bucket(stack_size)

        # Stack-aware preflop ranges approximating equilibrium adjustments
        ranges = {
            Position.UTG: {
                "deep": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 0.8,
                    'AJs': 1.0, 'AJo': 0.6, 'ATs': 1.0, 'KQs': 1.0,
                    '99': 1.0, '88': 0.8, '77': 0.6
                },
                "mid": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 0.7,
                    'AJs': 1.0, 'ATs': 0.9, 'KQs': 0.9,
                    '99': 0.9, '88': 0.7, '77': 0.5
                },
                "short": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 0.9,
                    'TT': 0.9, '99': 0.8, 'AQo': 0.5
                }
            },
            Position.MP: {
                "deep": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0,
                    'AJo': 0.8, 'ATs': 1.0, 'ATo': 0.6, 'KQs': 1.0, 'KQo': 0.7,
                    'KJs': 1.0, 'KJo': 0.5, '88': 1.0, '77': 0.8, '66': 0.6
                },
                "mid": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 0.9,
                    'AJs': 1.0, 'ATs': 0.9, 'KQs': 0.9, 'KJs': 0.9,
                    '99': 0.9, '88': 0.8, '77': 0.6, '66': 0.5, '55': 0.4
                },
                "short": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 0.9, 'AQo': 0.7,
                    'TT': 1.0, '99': 0.9, '88': 0.7, '77': 0.5
                }
            },
            Position.CO: {
                "deep": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0, '88': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                    'ATs': 1.0, 'ATo': 0.8, 'A9s': 1.0, 'A8s': 0.8, 'A7s': 0.6,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 0.8, 'KTs': 1.0,
                    '77': 1.0, '66': 0.8, '55': 0.6, '44': 0.4
                },
                "mid": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0,
                    'AJo': 0.9, 'ATs': 0.9, 'A9s': 0.9, 'A8s': 0.7,
                    'KQs': 1.0, 'KQo': 0.9, 'KJs': 0.9, 'KJo': 0.7, 'KTs': 0.9,
                    '88': 1.0, '77': 0.9, '66': 0.7, '55': 0.5
                },
                "short": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 0.9, 'AJs': 1.0,
                    'KQs': 0.9, 'KJs': 0.8, 'TT': 1.0, '99': 0.9, '88': 0.8,
                    'ATs': 0.8, 'A9s': 0.7
                }
            },
            Position.BTN: {
                "deep": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0, '88': 1.0, '77': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                    'ATs': 1.0, 'ATo': 1.0, 'A9s': 1.0, 'A9o': 0.8, 'A8s': 1.0, 'A7s': 1.0,
                    'A6s': 0.8, 'A5s': 1.0, 'A4s': 1.0, 'A3s': 0.8, 'A2s': 0.8,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 1.0, 'KTs': 1.0, 'KTo': 0.8,
                    '66': 1.0, '55': 1.0, '44': 1.0, '33': 0.8, '22': 0.8,
                    'QJs': 1.0, 'QJo': 0.8, 'QTs': 1.0, 'Q9s': 0.8, 'JTs': 1.0, 'J9s': 0.8,
                    'T9s': 1.0, '98s': 1.0, '87s': 1.0
                },
                "mid": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                    'ATs': 1.0, 'ATo': 0.9, 'A9s': 1.0, 'A8s': 0.9, 'A7s': 0.9,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 0.9, 'KTs': 1.0,
                    '66': 1.0, '55': 1.0, '44': 0.9, '33': 0.7, '22': 0.7,
                    'QJs': 1.0, 'QTs': 1.0, 'JTs': 1.0, 'T9s': 1.0, '98s': 0.9
                },
                "short": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0,
                    'ATs': 0.9, 'A9s': 0.9, 'KQs': 1.0, 'KJs': 0.9,
                    '99': 0.9, '88': 0.8, '77': 0.7, '66': 0.6,
                    'QJs': 0.9, 'JTs': 0.9, 'T9s': 0.9
                }
            },
            Position.SB: {
                "deep": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0, '88': 1.0, '77': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                    'ATs': 1.0, 'ATo': 1.0, 'A9s': 1.0, 'A8s': 1.0, 'A7s': 1.0, 'A6s': 1.0,
                    'A5s': 1.0, 'A4s': 1.0, 'A3s': 1.0, 'A2s': 1.0,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 1.0, 'KTs': 1.0, 'KTo': 1.0,
                    'K9s': 1.0, 'K8s': 0.8, 'K7s': 0.6, 'K6s': 0.4,
                    '66': 1.0, '55': 1.0, '44': 1.0, '33': 1.0, '22': 1.0,
                    'QJs': 1.0, 'QTs': 1.0, 'Q9s': 1.0, 'Q8s': 0.8,
                    'JTs': 1.0, 'J9s': 1.0, 'J8s': 0.8, 'T9s': 1.0, 'T8s': 0.8
                },
                "mid": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                    'ATs': 1.0, 'ATo': 1.0, 'A9s': 1.0, 'A8s': 1.0, 'A7s': 1.0,
                    'A6s': 1.0, 'A5s': 1.0, 'A4s': 1.0, 'A3s': 0.9, 'A2s': 0.9,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 0.9, 'KTs': 1.0,
                    'K9s': 0.9, 'K8s': 0.7, 'K7s': 0.5,
                    '66': 1.0, '55': 1.0, '44': 1.0, '33': 0.9, '22': 0.9,
                    'QJs': 1.0, 'QTs': 1.0, 'Q9s': 0.9,
                    'JTs': 1.0, 'J9s': 0.9, 'T9s': 0.9
                },
                "short": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0,
                    'ATs': 1.0, 'A9s': 1.0, 'KQs': 1.0, 'KJs': 0.9,
                    '99': 1.0, '88': 0.9, '77': 0.8, '66': 0.7,
                    'A5s': 0.9, 'A4s': 0.9, 'QJs': 0.9, 'JTs': 0.9
                }
            },
            Position.BB: {
                "deep": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0, '88': 1.0, '77': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                    'ATs': 1.0, 'ATo': 1.0, 'A9s': 1.0, 'A9o': 0.8, 'A8s': 1.0, 'A8o': 0.6,
                    'A7s': 1.0, 'A6s': 1.0, 'A5s': 1.0, 'A4s': 1.0, 'A3s': 1.0, 'A2s': 1.0,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 1.0, 'KTs': 1.0, 'KTo': 0.8,
                    'K9s': 1.0, 'K8s': 1.0, 'K7s': 1.0, 'K6s': 0.8, 'K5s': 0.6,
                    '66': 1.0, '55': 1.0, '44': 1.0, '33': 1.0, '22': 1.0,
                    'QJs': 1.0, 'QTs': 1.0, 'Q9s': 1.0, 'Q8s': 1.0, 'Q7s': 0.8,
                    'JTs': 1.0, 'J9s': 1.0, 'J8s': 1.0, 'J7s': 0.8,
                    'T9s': 1.0, 'T8s': 1.0, 'T7s': 0.8, '98s': 1.0, '97s': 0.8, '87s': 1.0
                },
                "mid": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0,
                    'ATs': 1.0, 'ATo': 0.9, 'A9s': 1.0, 'A8s': 1.0, 'A8o': 0.7,
                    'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KTs': 1.0, 'KTo': 0.7,
                    'K9s': 1.0, 'K8s': 0.9, 'K7s': 0.9, 'K6s': 0.7,
                    'QJs': 1.0, 'QTs': 1.0, 'Q9s': 1.0, 'Q8s': 0.9,
                    'JTs': 1.0, 'J9s': 1.0, 'J8s': 0.9,
                    'T9s': 1.0, 'T8s': 0.9, '98s': 1.0, '87s': 0.9
                },
                "short": {
                    'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                    'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 0.9,
                    'AJs': 1.0, 'ATs': 0.9, 'KQs': 1.0, 'KJs': 0.9,
                    '99': 1.0, '88': 0.9, '77': 0.8, '66': 0.7,
                    'QJs': 0.9, 'JTs': 0.9, 'T9s': 0.9, '98s': 0.9
                }
            }
        }

        position_ranges = ranges.get(position, {})
        hand_range = position_ranges.get(stack_profile, position_ranges.get("deep", {}))
        recommended_action = PokerAction.RAISE if stack_size >= 20 else PokerAction.ALL_IN

        return HandRange(hands=hand_range, position=position, action=recommended_action)

    def get_bet_sizing_plan(self, position: Position, stack_size: int, pot_size: float) -> BetSizingPlan:
        """Generate a stack-aware bet sizing plan across all streets"""

        stack_profile = self._determine_stack_bucket(stack_size)

        preflop_open_sizes = {
            "deep": {
                Position.UTG: 2.5,
                Position.MP: 2.3,
                Position.CO: 2.2,
                Position.BTN: 2.1,
                Position.SB: 3.0
            },
            "mid": {
                Position.UTG: 2.3,
                Position.MP: 2.2,
                Position.CO: 2.1,
                Position.BTN: 2.0,
                Position.SB: 2.8
            },
            "short": {
                Position.UTG: 2.2,
                Position.MP: 2.1,
                Position.CO: 2.0,
                Position.BTN: 2.0,
                Position.SB: 2.5
            }
        }

        three_bet_sizes = {"deep": 3.2, "mid": 3.0, "short": 2.6}
        four_bet_sizes = {"deep": 2.5, "mid": 2.2, "short": 2.0}
        shove_threshold = {"deep": 0, "mid": 30, "short": 22}

        flop_sizing = {
            "deep": {"small": 0.33, "big": 0.75, "raise": 2.8, "shove": 2.5},
            "mid": {"small": 0.40, "big": 0.70, "raise": 2.5, "shove": 2.2},
            "short": {"small": 0.45, "big": 0.60, "raise": 2.2, "shove": 1.8}
        }

        turn_sizing = {
            "deep": {"small": 0.60, "big": 1.10, "raise": 2.4, "shove": 2.2},
            "mid": {"small": 0.65, "big": 1.00, "raise": 2.1, "shove": 1.8},
            "short": {"small": 0.70, "big": 0.90, "raise": 1.8, "shove": 1.6}
        }

        river_sizing = {
            "deep": {"small": 0.70, "big": 1.35, "raise": 2.2, "shove": 2.0},
            "mid": {"small": 0.75, "big": 1.20, "raise": 2.0, "shove": 1.7},
            "short": {"small": 0.80, "big": 1.10, "raise": 1.7, "shove": 1.5}
        }

        open_size = preflop_open_sizes[stack_profile].get(position, 2.3)
        shove_cap = shove_threshold[stack_profile]

        notes = (
            f"{stack_size}bb effective stack ({stack_profile}) -> open {open_size:.1f}bb, "
            f"3-bet {three_bet_sizes[stack_profile]:.1f}x, 4-bet {four_bet_sizes[stack_profile]:.1f}x. "
            "Postflop sizings expand when deep to pressure condensed ranges and contract when shallow to preserve stack leverage."
        )

        street_recommendations = {
            "preflop": {
                "open": open_size,
                "three_bet": three_bet_sizes[stack_profile],
                "four_bet": four_bet_sizes[stack_profile],
                "shove": shove_cap if shove_cap else stack_size
            },
            "flop": flop_sizing[stack_profile],
            "turn": turn_sizing[stack_profile],
            "river": river_sizing[stack_profile]
        }

        return BetSizingPlan(
            stack_size=stack_size,
            pot_size=pot_size,
            street_recommendations=street_recommendations,
            notes=notes
        )

    def calculate_hand_equity(self, hand: str, board: str = "", opponents: int = 1) -> float:
        """
        Calculate equity of a hand against random opponents
        
        Args:
            hand: Hand in format "AhKs" 
            board: Board cards in format "AhKsQd"
            opponents: Number of opponents
            
        Returns:
            float: Equity percentage (0.0 to 1.0)
        """
        # Simplified equity calculation based on hand strength
        hand_strength_map = {
            'AA': 0.85, 'KK': 0.82, 'QQ': 0.80, 'JJ': 0.77, 'TT': 0.75,
            'AKs': 0.67, 'AKo': 0.65, 'AQs': 0.66, 'AQo': 0.64,
            'AJs': 0.65, 'AJo': 0.63, 'ATs': 0.64, 'ATo': 0.62,
            'KQs': 0.63, 'KQo': 0.61, 'KJs': 0.62, 'KJo': 0.60,
            '99': 0.72, '88': 0.69, '77': 0.66, '66': 0.63,
            '55': 0.60, '44': 0.57, '33': 0.54, '22': 0.51
        }
        
        # Get base equity
        base_equity = hand_strength_map.get(hand, 0.50)
        
        # Adjust for number of opponents
        adjusted_equity = base_equity * (0.85 ** (opponents - 1))
        
        return min(adjusted_equity, 1.0)
    
    def analyze_spot(self, position: Position, action_history: List[str],
                    stack_sizes: Dict[Position, int], board: str = "",
                    pot_size: float = 0.0, villain_position: Optional[Position] = None) -> GTOSolution:
        """
        Analyze a specific poker spot and provide GTO solution

        Args:
            position: Hero's position
            action_history: Sequence of actions taken
            stack_sizes: Stack sizes for each position
            board: Current board cards if postflop
            pot_size: Current pot size
            villain_position: Opponent position when heads-up

        Returns:
            GTOSolution: Optimal strategy for the spot
        """
        effective_stack = stack_sizes.get(position, 100)
        preflop_range = self.analyze_preflop_range(position, stack_size=effective_stack)

        if villain_position is None:
            villain_position = next((pos for pos in stack_sizes.keys() if pos != position), Position.BB)
        villain_stack = stack_sizes.get(villain_position, effective_stack)
        effective_stack = min(effective_stack, villain_stack)

        if pot_size <= 0:
            pot_size = 3.0 if position in {Position.CO, Position.BTN} else 2.5

        bet_plan = self.get_bet_sizing_plan(position, effective_stack, pot_size)

        postflop_strategy = None
        blocker_explanation = None
        if board:
            postflop_strategy = self.analyze_postflop_spot(board, pot_size, effective_stack, position, villain_position)
            blocker_explanation = self.explain_blocker_importance(postflop_strategy)

        ranges = {position: preflop_range}

        return GTOSolution(
            ranges=ranges,
            ev=0.15,  # Example EV placeholder
            exploitability=0.05,  # Example exploitability placeholder
            bet_sizing_plan=bet_plan,
            postflop_strategy=postflop_strategy,
            blocker_explanation=blocker_explanation
        )
    
    def get_optimal_sizing(self, pot_size: float, position: Position,
                          action: PokerAction, stack_size: int = 100,
                          street: str = "flop") -> float:
        """
        Get optimal bet sizing for given situation

        Args:
            pot_size: Current pot size
            position: Player position
            action: Type of action (bet/raise)
            stack_size: Effective stack size in big blinds
            street: Street of play (preflop, flop, turn, river)

        Returns:
            float: Optimal bet size as fraction of pot
        """
        plan = self.get_bet_sizing_plan(position, stack_size, pot_size)

        if street == "preflop":
            preflop_plan = plan.street_recommendations["preflop"]
            if action == PokerAction.RAISE:
                return preflop_plan["three_bet"] * pot_size
            if action == PokerAction.ALL_IN:
                shove_size = min(stack_size, preflop_plan["shove"])
                return shove_size * pot_size
            return preflop_plan["open"] * pot_size

        street_plan = plan.street_recommendations.get(street, {})

        if action == PokerAction.BET:
            return street_plan.get("small", 0.6) * pot_size
        if action == PokerAction.RAISE:
            return street_plan.get("raise", street_plan.get("big", 0.9)) * pot_size
        if action == PokerAction.ALL_IN:
            shove_multiplier = street_plan.get("shove", 1.0)
            return min(stack_size, shove_multiplier * pot_size)

        return street_plan.get("small", 0.5) * pot_size

    def _parse_board(self, board: str) -> Tuple[List[str], List[str]]:
        ranks = [board[i] for i in range(0, len(board), 2)]
        suits = [board[i + 1] for i in range(0, len(board), 2) if i + 1 < len(board)]
        return ranks, suits

    def _categorize_board(self, ranks: List[str], suits: List[str]) -> str:
        rank_order = "23456789TJQKA"
        indices = [rank_order.index(r) for r in ranks if r in rank_order]
        if not indices:
            indices = [0]
        spread = max(indices) - min(indices)
        unique_suits = set(suits)
        is_monotone = len(unique_suits) == 1
        is_two_tone = len(unique_suits) == 2
        is_paired = len(ranks) != len(set(ranks))
        high_cards = sum(1 for r in ranks if r in "TJQKA")
        top_rank = ranks[0] if ranks else ""

        if is_monotone:
            return "monotone"
        if is_paired and high_cards >= 1:
            return "paired_high"
        if is_paired:
            return "paired_low"
        if is_two_tone and spread <= 4:
            return "dynamic"
        if high_cards >= 2:
            return "dry_high"
        if high_cards >= 1 and top_rank in "AKQ" and spread >= 4:
            return "dry_high"
        if spread <= 4:
            return "low_connected"
        return "dry_low"

    def analyze_postflop_spot(self, board: str, pot_size: float, stack_size: int,
                              position: Position, villain_position: Position) -> PostflopStrategy:
        ranks, suits = self._parse_board(board)
        category = self._categorize_board(ranks, suits)
        stack_profile = self._determine_stack_bucket(stack_size)

        hero_advantage = "balanced"
        if position in {Position.UTG, Position.MP, Position.CO} and villain_position in {Position.SB, Position.BB}:
            if category in {"dry_high", "paired_high"}:
                hero_advantage = "significant"
            elif category in {"monotone", "dynamic"}:
                hero_advantage = "slight"
        elif position in {Position.BTN, Position.SB} and villain_position == Position.BB:
            if category in {"dynamic", "monotone"}:
                hero_advantage = "slight"
            else:
                hero_advantage = "neutral"

        recommended_actions = {}
        if category == "dry_high":
            recommended_actions["flop"] = (
                "C-bet ~33% with entire range, checking only slowplays and the weakest backdoor hands."
            )
            recommended_actions["turn"] = (
                "On bricks, polarize between 65% and 110% pot; slow down when overcards help villain."
            )
            recommended_actions["river"] = (
                "Use 130% overbets with nut advantage, mix 70% value bets when ranges condense."
            )
        elif category == "dynamic":
            recommended_actions["flop"] = (
                "Mix 45% checks with 60-70% pot bets using top pair+ and strong draws; bet small with gutters plus backdoors."
            )
            recommended_actions["turn"] = (
                "Accelerate on favorable turns with 75-100% pot; mix in check-raises holding combo draws."
            )
            recommended_actions["river"] = (
                "Arrive polarized; bluff missed draws that block straights while value-betting big with two pair+."
            )
        elif category == "monotone":
            recommended_actions["flop"] = (
                "Check range ~55%; bet 50% pot with nut advantage and strong blockers to deny equity."
            )
            recommended_actions["turn"] = (
                "When suit pairs, attack with 80% pot leveraging nut flush advantage; otherwise keep sizing to 60%."
            )
            recommended_actions["river"] = (
                "Select polarized 120% bets with nut blockers, check medium strength to bluff catch."
            )
        elif category.startswith("paired"):
            recommended_actions["flop"] = (
                "Range stab 33% to deny equity; mix in checks with underpairs to protect checking range."
            )
            recommended_actions["turn"] = (
                "Double barrel 65% when unpaired overcards fall; slow down on coordinated cards."
            )
            recommended_actions["river"] = (
                "Shove or bet 120% with quads/full houses; thin value 55% with overpairs blocking boats."
            )
        elif category == "low_connected":
            recommended_actions["flop"] = (
                "Check 50%+; bet 45% pot with overpairs and strong draws, mixing some large bets with sets."
            )
            recommended_actions["turn"] = (
                "Pressure with 70% pot on bricks; overbet when straight advantage persists."
            )
            recommended_actions["river"] = (
                "Bluff missed overcards blocking straights; value bet 65% with overpairs."
            )
        else:
            recommended_actions["flop"] = (
                "Adopt balanced 40% frequency bets (~50% pot) to probe; check-call marginal made hands."
            )
            recommended_actions["turn"] = (
                "Select 70% pot barrels when range retains nut advantage, otherwise check with medium pairs."
            )
            recommended_actions["river"] = (
                "Use 75% pot value bets for straights+; choose bluff combos that block villain's top pairs."
            )

        blocker_applications: List[str] = []
        dominant_suit = suits[0] if suits else None
        top_rank = ranks[0] if ranks else ""

        if dominant_suit and category in {"monotone", "dynamic"}:
            blocker_applications.append(
                f"Holding the {dominant_suit}-suit Ace/King blocks villain's nut flushes, enabling high-frequency barrels."
            )
        if category.startswith("paired"):
            paired_rank = next((r for r in ranks if ranks.count(r) > 1), top_rank)
            blocker_applications.append(
                f"Having a {paired_rank} reduces villain's full house combos, letting you overbet rivers confidently."
            )
        if top_rank in {"A", "K"}:
            blocker_applications.append(
                f"Ace and King blockers remove top-pair holdings from villain, boosting bluff success on {board}."
            )
        if category in {"dynamic", "low_connected"}:
            blocker_applications.append(
                "Straight blockers (e.g., holding the key middle ranks) cut villain's nutted combos when bluffing."
            )
        if not blocker_applications:
            blocker_applications.append(
                "Prioritize blockers that remove villain's strongest continues to maintain proper bluff:value ratios."
            )

        if stack_profile == "short":
            recommended_actions["turn"] += " Adjust frequencies downward to avoid stack-commitment without equity."
            recommended_actions["river"] += " Choose shove-or-fold decisions based on nut blockers."

        return PostflopStrategy(
            board=board,
            category=category,
            hero_range_advantage=hero_advantage,
            recommended_actions=recommended_actions,
            blocker_applications=blocker_applications
        )

    def explain_blocker_importance(self, postflop_strategy: PostflopStrategy) -> str:
        explanation_lines = [
            f"On board {postflop_strategy.board}, blockers dictate combo availability and therefore bluffing frequency.",
            "Key blocker applications:"
        ]
        for note in postflop_strategy.blocker_applications:
            explanation_lines.append(f"- {note}")
        explanation_lines.append(
            "Balancing these blockers with value combos keeps betting ranges within solver-approved bluff:value ratios."
        )
        return "\n".join(explanation_lines)

class PokerResearchTool:
    """
    High-level interface for poker research using GTO principles
    """
    
    def __init__(self):
        self.solver = TexasSolverAPI()
        self.hand_history = []
    
    def simulate_tournament_spots(self, num_simulations: int = 1000) -> Dict[str, float]:
        """
        Simulate various tournament spots to analyze optimal play
        
        Args:
            num_simulations: Number of simulations to run
            
        Returns:
            Dict with analysis results
        """
        results = {
            'avg_ev': 0.0,
            'win_rate': 0.0,
            'optimal_frequencies': {}
        }
        
        total_ev = 0.0
        wins = 0
        
        for _ in range(num_simulations):
            # Simulate random spot
            position = Position.BTN  # Default position
            solution = self.solver.analyze_spot(position, [], {position: 100})
            total_ev += solution.ev
            if solution.ev > 0:
                wins += 1
        
        results['avg_ev'] = total_ev / num_simulations
        results['win_rate'] = wins / num_simulations
        
        return results
    
    def analyze_hand_vs_range(self, hero_hand: str, villain_range: HandRange) -> Dict[str, float]:
        """
        Analyze hero's hand equity against villain's range
        
        Args:
            hero_hand: Hero's hand (e.g., "AhKs")
            villain_range: Villain's hand range
            
        Returns:
            Dict with equity analysis
        """
        hero_equity = self.solver.calculate_hand_equity(hero_hand)
        
        # Calculate average equity against range
        total_equity = 0.0
        total_frequency = 0.0
        
        for hand, frequency in villain_range.hands.items():
            if frequency > 0:
                equity_vs_hand = self.solver.calculate_hand_equity(hero_hand, opponents=1)
                total_equity += equity_vs_hand * frequency
                total_frequency += frequency
        
        avg_equity = total_equity / total_frequency if total_frequency > 0 else 0.5
        
        return {
            'hero_hand': hero_hand,
            'equity_vs_range': avg_equity,
            'raw_equity': hero_equity,
            'range_size': len([h for h, f in villain_range.hands.items() if f > 0])
        }
    
    def export_ranges_to_file(self, ranges: Dict[Position, HandRange], filename: str):
        """
        Export hand ranges to a file for further analysis
        
        Args:
            ranges: Dictionary of position -> HandRange
            filename: Output filename
        """
        data = {}
        for position, hand_range in ranges.items():
            data[position.value] = {
                'hands': hand_range.hands,
                'action': hand_range.action.value
            }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Ranges exported to {filename}")

# Example usage and research functions
def demonstrate_gto_analysis():
    """
    Demonstrate the GTO poker analysis capabilities
    """
    print("=== TexasSolver GTO Poker Analysis Demo ===")
    
    # Initialize research tool
    research_tool = PokerResearchTool()
    
    # Analyze preflop ranges for different stack depths
    print("\n1. Preflop Range Analysis by Stack Depth:")
    for stack in [100, 40, 20]:
        range_analysis = research_tool.solver.analyze_preflop_range(Position.CO, stack_size=stack)
        range_size = len([h for h, f in range_analysis.hands.items() if f > 0])
        print(f"   CO {stack}bb: {range_size} combos, action = {range_analysis.action.value}")

    # Show equilibrium bet sizing plan
    print("\n2. Bet Sizing Equilibrium Plan (BTN vs BB, 60bb):")
    bet_plan = research_tool.solver.get_bet_sizing_plan(Position.BTN, 60, pot_size=4.5)
    print(f"   Notes: {bet_plan.notes}")
    for street, recs in bet_plan.street_recommendations.items():
        print(f"   {street.capitalize()} sizings: {recs}")

    # Postflop spot analysis with blocker insights
    print("\n3. Postflop Strategy Snapshot (BTN vs BB on As7s4d, pot 6.5bb):")
    postflop = research_tool.solver.analyze_postflop_spot("As7s4d", 6.5, 50, Position.BTN, Position.BB)
    print(f"   Board category: {postflop.category}, hero advantage: {postflop.hero_range_advantage}")
    for street, advice in postflop.recommended_actions.items():
        print(f"   {street.capitalize()} plan: {advice}")

    print("\n4. Blocker Importance:")
    print(research_tool.solver.explain_blocker_importance(postflop))

    # Analyze specific hands
    print("\n5. Hand Equity Analysis:")
    test_hands = ['AA', 'AKs', 'QQ', 'JTs', '76s']
    for hand in test_hands:
        equity = research_tool.solver.calculate_hand_equity(hand)
        print(f"   {hand}: {equity:.1%} equity vs random hand")

    # Simulate tournament spots
    print("\n6. Tournament Simulation (100 spots):")
    simulation_results = research_tool.simulate_tournament_spots(100)
    print(f"   Average EV: {simulation_results['avg_ev']:.3f}")
    print(f"   Win Rate: {simulation_results['win_rate']:.1%}")

    # Hand vs Range analysis
    print("\n7. Hand vs Range Analysis:")
    btn_range = research_tool.solver.analyze_preflop_range(Position.BTN)
    analysis = research_tool.analyze_hand_vs_range('AKo', btn_range)
    print(f"   AKo vs BTN range: {analysis['equity_vs_range']:.1%} equity")
    print(f"   Range contains {analysis['range_size']} hands")

if __name__ == "__main__":
    demonstrate_gto_analysis()