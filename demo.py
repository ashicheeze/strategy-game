#!/usr/bin/env python3
"""
Demonstration script for the TexasSolver GTO Poker API integration
This script shows all the key features of the poker research tools.
"""

from poker_solver import TexasSolverAPI, PokerResearchTool, Position
import json

def main():
    print("🃏 TexasSolver GTO Poker API Integration Demo")
    print("=" * 60)
    
    # Initialize the research tool
    research_tool = PokerResearchTool()
    
    print("\n📊 1. Range Analysis for Different Positions")
    print("-" * 50)
    
    positions_to_analyze = [Position.UTG, Position.CO, Position.BTN]
    
    for position in positions_to_analyze:
        range_analysis = research_tool.solver.analyze_preflop_range(position)
        hands_in_range = [h for h, f in range_analysis.hands.items() if f > 0]
        print(f"{position.value:3s}: {len(hands_in_range):2d} hands - {', '.join(hands_in_range[:5])}...")
    
    print("\n💰 2. Equity Analysis for Premium Hands")
    print("-" * 50)
    
    premium_hands = ['AA', 'KK', 'AKs', 'QQ', 'AKo']
    
    for hand in premium_hands:
        equity_vs_1 = research_tool.solver.calculate_hand_equity(hand, opponents=1)
        equity_vs_5 = research_tool.solver.calculate_hand_equity(hand, opponents=5)
        print(f"{hand:3s}: {equity_vs_1:5.1%} vs 1 opponent, {equity_vs_5:5.1%} vs 5 opponents")
    
    print("\n🎯 3. Spot Analysis Example")
    print("-" * 50)
    
    # Analyze a specific spot
    solution = research_tool.solver.analyze_spot(
        Position.BTN, 
        ["UTG fold", "MP raise", "CO fold"], 
        {Position.BTN: 100}
    )
    
    print(f"Spot: BTN vs MP raise")
    print(f"Expected Value: {solution.ev:+.3f} BB")
    print(f"Exploitability: {solution.exploitability:.3f}")
    
    print("\n🏆 4. Tournament Simulation")
    print("-" * 50)
    
    # Run a small simulation
    results = research_tool.simulate_tournament_spots(500)
    print(f"Simulated 500 tournament spots:")
    print(f"Average EV: {results['avg_ev']:+.4f} BB per spot")
    print(f"Win Rate: {results['win_rate']:5.1%}")
    
    hourly_rate = results['avg_ev'] * 100  # Assuming 100 hands/hour
    print(f"Projected Hourly Rate: {hourly_rate:+.2f} BB/hour")
    
    print("\n📈 5. Hand vs Range Analysis")
    print("-" * 50)
    
    # Analyze how strong hands perform against different position ranges
    test_hands = ['AKo', 'QQ', 'A5s', '76s']
    btn_range = research_tool.solver.analyze_preflop_range(Position.BTN)
    
    for hand in test_hands:
        analysis = research_tool.analyze_hand_vs_range(hand, btn_range)
        print(f"{hand:3s} vs BTN range: {analysis['equity_vs_range']:5.1%} equity")
    
    print("\n🎲 6. Optimal Sizing Recommendations")
    print("-" * 50)
    
    pot_size = 10.0
    positions = [Position.UTG, Position.CO, Position.BTN]
    
    from poker_solver import PokerAction
    
    for pos in positions:
        bet_size = research_tool.solver.get_optimal_sizing(pot_size, pos, PokerAction.BET)
        raise_size = research_tool.solver.get_optimal_sizing(pot_size, pos, PokerAction.RAISE)
        print(f"{pos.value:3s}: Bet {bet_size:4.1f} ({bet_size/pot_size:.1f}x pot), Raise {raise_size:4.1f} ({raise_size/pot_size:.1f}x)")
    
    print("\n💾 7. Export Functionality")
    print("-" * 50)
    
    # Export ranges for research
    ranges = {}
    for pos in [Position.UTG, Position.MP, Position.CO, Position.BTN]:
        ranges[pos] = research_tool.solver.analyze_preflop_range(pos)
    
    filename = "/tmp/exported_ranges.json"
    research_tool.export_ranges_to_file(ranges, filename)
    
    # Show a sample of the exported data
    with open(filename, 'r') as f:
        data = json.load(f)
        print(f"Exported ranges to {filename}")
        print(f"Sample - BTN range contains {len(data['BTN']['hands'])} hands")
    
    print("\n✅ Demo Complete!")
    print("=" * 60)
    print("The TexasSolver GTO Poker API integration provides:")
    print("• Comprehensive range analysis for all positions")
    print("• Accurate equity calculations vs opponents and ranges")
    print("• GTO spot analysis for complex situations")
    print("• Tournament simulation tools")
    print("• Optimal sizing recommendations")
    print("• Data export for further research")
    print("\nUse poker_research_gui.py for the interactive GUI version!")

if __name__ == "__main__":
    main()