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
class GTOSolution:
    """Represents a GTO solution for a specific situation"""
    ranges: Dict[Position, HandRange]
    ev: float  # Expected Value
    exploitability: float

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
    
    def analyze_preflop_range(self, position: Position, stack_size: int = 100) -> HandRange:
        """
        Analyze optimal preflop hand range for a given position
        
        Args:
            position: Player position at the table
            stack_size: Stack size in big blinds
            
        Returns:
            HandRange: Optimal hand range with frequencies
        """
        # Simplified GTO preflop ranges based on position
        ranges = {
            Position.UTG: {
                'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
                'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 0.8,
                'AJs': 1.0, 'AJo': 0.6, 'ATs': 1.0, 'KQs': 1.0,
                '99': 1.0, '88': 0.8, '77': 0.6
            },
            Position.MP: {
                'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0,
                'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0,
                'AJo': 0.8, 'ATs': 1.0, 'ATo': 0.6, 'KQs': 1.0, 'KQo': 0.7,
                'KJs': 1.0, 'KJo': 0.5, '88': 1.0, '77': 0.8, '66': 0.6
            },
            Position.CO: {
                'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0, '88': 1.0,
                'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                'ATs': 1.0, 'ATo': 0.8, 'A9s': 1.0, 'A8s': 0.8, 'A7s': 0.6,
                'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 0.8, 'KTs': 1.0,
                '77': 1.0, '66': 0.8, '55': 0.6, '44': 0.4
            },
            Position.BTN: {
                'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0, '99': 1.0, '88': 1.0, '77': 1.0,
                'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0, 'AJs': 1.0, 'AJo': 1.0,
                'ATs': 1.0, 'ATo': 1.0, 'A9s': 1.0, 'A9o': 0.8, 'A8s': 1.0, 'A7s': 1.0,
                'A6s': 0.8, 'A5s': 1.0, 'A4s': 1.0, 'A3s': 0.8, 'A2s': 0.8,
                'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KJo': 1.0, 'KTs': 1.0, 'KTo': 0.8,
                '66': 1.0, '55': 1.0, '44': 1.0, '33': 0.8, '22': 0.8,
                'QJs': 1.0, 'QJo': 0.8, 'QTs': 1.0, 'Q9s': 0.8, 'JTs': 1.0, 'J9s': 0.8
            },
            Position.SB: {
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
            Position.BB: {
                # BB calling range vs BTN open
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
            }
        }
        
        hand_range = ranges.get(position, {})
        return HandRange(hands=hand_range, position=position, action=PokerAction.RAISE)
    
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
                    stack_sizes: Dict[Position, int]) -> GTOSolution:
        """
        Analyze a specific poker spot and provide GTO solution
        
        Args:
            position: Hero's position
            action_history: Sequence of actions taken
            stack_sizes: Stack sizes for each position
            
        Returns:
            GTOSolution: Optimal strategy for the spot
        """
        # Simplified GTO analysis
        preflop_range = self.analyze_preflop_range(position)
        
        ranges = {position: preflop_range}
        
        return GTOSolution(
            ranges=ranges,
            ev=0.15,  # Example EV
            exploitability=0.05  # Example exploitability
        )
    
    def get_optimal_sizing(self, pot_size: float, position: Position, 
                          action: PokerAction) -> float:
        """
        Get optimal bet sizing for given situation
        
        Args:
            pot_size: Current pot size
            position: Player position
            action: Type of action (bet/raise)
            
        Returns:
            float: Optimal bet size as fraction of pot
        """
        sizing_map = {
            PokerAction.BET: {
                Position.BTN: 0.75,
                Position.CO: 0.70,
                Position.MP: 0.65,
                Position.UTG: 0.60
            },
            PokerAction.RAISE: {
                Position.BTN: 3.0,  # 3x raise
                Position.CO: 2.8,
                Position.MP: 2.5,
                Position.UTG: 2.2
            }
        }
        
        return sizing_map.get(action, {}).get(position, 0.67) * pot_size

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
    
    # Analyze preflop ranges for different positions
    print("\n1. Preflop Range Analysis:")
    for position in [Position.UTG, Position.MP, Position.CO, Position.BTN]:
        range_analysis = research_tool.solver.analyze_preflop_range(position)
        range_size = len([h for h, f in range_analysis.hands.items() if f > 0])
        print(f"   {position.value}: {range_size} hands in opening range")
    
    # Analyze specific hands
    print("\n2. Hand Equity Analysis:")
    test_hands = ['AA', 'AKs', 'QQ', 'JTs', '76s']
    for hand in test_hands:
        equity = research_tool.solver.calculate_hand_equity(hand)
        print(f"   {hand}: {equity:.1%} equity vs random hand")
    
    # Simulate tournament spots
    print("\n3. Tournament Simulation (100 spots):")
    simulation_results = research_tool.simulate_tournament_spots(100)
    print(f"   Average EV: {simulation_results['avg_ev']:.3f}")
    print(f"   Win Rate: {simulation_results['win_rate']:.1%}")
    
    # Hand vs Range analysis
    print("\n4. Hand vs Range Analysis:")
    btn_range = research_tool.solver.analyze_preflop_range(Position.BTN)
    analysis = research_tool.analyze_hand_vs_range('AKo', btn_range)
    print(f"   AKo vs BTN range: {analysis['equity_vs_range']:.1%} equity")
    print(f"   Range contains {analysis['range_size']} hands")

if __name__ == "__main__":
    demonstrate_gto_analysis()