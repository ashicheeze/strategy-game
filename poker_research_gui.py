"""
Poker Research GUI - Integration with Strategy Game
This module provides a graphical interface for poker GTO analysis and research.
"""

import pygame
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from poker_solver import TexasSolverAPI, PokerResearchTool, Position, PokerAction
import threading
from typing import Dict, Optional

class PokerResearchGUI:
    """
    GUI interface for poker research and GTO analysis
    """
    
    def __init__(self):
        self.research_tool = PokerResearchTool()
        self.current_analysis = None
        self.setup_gui()
    
    def setup_gui(self):
        """Initialize the GUI components"""
        self.root = tk.Tk()
        self.root.title("TexasSolver GTO Poker Research Tool")
        self.root.geometry("1000x700")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_range_analysis_tab()
        self.create_equity_calculator_tab()
        self.create_spot_analyzer_tab()
        self.create_simulation_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready for poker analysis")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_range_analysis_tab(self):
        """Create the range analysis tab"""
        range_frame = ttk.Frame(self.notebook)
        self.notebook.add(range_frame, text="Range Analysis")
        
        # Position selection
        pos_frame = ttk.LabelFrame(range_frame, text="Position Selection", padding="10")
        pos_frame.pack(fill='x', padx=10, pady=5)
        
        self.position_var = tk.StringVar(value="BTN")
        positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        
        for i, pos in enumerate(positions):
            ttk.Radiobutton(pos_frame, text=pos, variable=self.position_var, 
                           value=pos).grid(row=0, column=i, padx=5)
        
        # Analysis button
        ttk.Button(pos_frame, text="Analyze Range", 
                  command=self.analyze_range).grid(row=1, column=0, columnspan=3, pady=10)
        
        # Results display
        results_frame = ttk.LabelFrame(range_frame, text="Range Analysis Results", padding="10")
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.range_text = scrolledtext.ScrolledText(results_frame, height=20, width=80)
        self.range_text.pack(fill='both', expand=True)
    
    def create_equity_calculator_tab(self):
        """Create the equity calculator tab"""
        equity_frame = ttk.Frame(self.notebook)
        self.notebook.add(equity_frame, text="Equity Calculator")
        
        # Input frame
        input_frame = ttk.LabelFrame(equity_frame, text="Hand Analysis", padding="10")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Hand input
        tk.Label(input_frame, text="Hero Hand:").grid(row=0, column=0, sticky='w')
        self.hand_entry = tk.Entry(input_frame, width=10)
        self.hand_entry.grid(row=0, column=1, padx=5)
        self.hand_entry.insert(0, "AKo")
        
        # Board input
        tk.Label(input_frame, text="Board:").grid(row=0, column=2, sticky='w', padx=(20,0))
        self.board_entry = tk.Entry(input_frame, width=15)
        self.board_entry.grid(row=0, column=3, padx=5)
        
        # Opponents
        tk.Label(input_frame, text="Opponents:").grid(row=1, column=0, sticky='w')
        self.opponents_var = tk.IntVar(value=1)
        opponents_spin = tk.Spinbox(input_frame, from_=1, to=9, width=5, 
                                   textvariable=self.opponents_var)
        opponents_spin.grid(row=1, column=1, padx=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate Equity", 
                  command=self.calculate_equity).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(equity_frame, text="Equity Results", padding="10")
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.equity_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.equity_text.pack(fill='both', expand=True)
    
    def create_spot_analyzer_tab(self):
        """Create the spot analyzer tab"""
        spot_frame = ttk.Frame(self.notebook)
        self.notebook.add(spot_frame, text="Spot Analyzer")
        
        # Spot configuration
        config_frame = ttk.LabelFrame(spot_frame, text="Spot Configuration", padding="10")
        config_frame.pack(fill='x', padx=10, pady=5)
        
        # Hero position
        tk.Label(config_frame, text="Hero Position:").grid(row=0, column=0, sticky='w')
        self.hero_pos_var = tk.StringVar(value="BTN")
        hero_pos_combo = ttk.Combobox(config_frame, textvariable=self.hero_pos_var,
                                     values=["UTG", "MP", "CO", "BTN", "SB", "BB"])
        hero_pos_combo.grid(row=0, column=1, padx=5)
        
        # Stack sizes
        tk.Label(config_frame, text="Stack Size (BB):").grid(row=0, column=2, sticky='w', padx=(20,0))
        self.stack_entry = tk.Entry(config_frame, width=10)
        self.stack_entry.grid(row=0, column=3, padx=5)
        self.stack_entry.insert(0, "100")
        
        # Action history
        tk.Label(config_frame, text="Action History:").grid(row=1, column=0, sticky='w')
        self.action_entry = tk.Entry(config_frame, width=30)
        self.action_entry.grid(row=1, column=1, columnspan=2, padx=5)
        self.action_entry.insert(0, "UTG raise, MP fold, CO call")
        
        # Analyze button
        ttk.Button(config_frame, text="Analyze Spot", 
                  command=self.analyze_spot).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Results
        spot_results_frame = ttk.LabelFrame(spot_frame, text="GTO Solution", padding="10")
        spot_results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.spot_text = scrolledtext.ScrolledText(spot_results_frame, height=15, width=80)
        self.spot_text.pack(fill='both', expand=True)
    
    def create_simulation_tab(self):
        """Create the simulation tab"""
        sim_frame = ttk.Frame(self.notebook)
        self.notebook.add(sim_frame, text="Tournament Simulation")
        
        # Simulation controls
        control_frame = ttk.LabelFrame(sim_frame, text="Simulation Parameters", padding="10")
        control_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(control_frame, text="Number of Simulations:").grid(row=0, column=0, sticky='w')
        self.sim_count_entry = tk.Entry(control_frame, width=10)
        self.sim_count_entry.grid(row=0, column=1, padx=5)
        self.sim_count_entry.insert(0, "1000")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky='ew', pady=10)
        
        # Run simulation button
        self.sim_button = ttk.Button(control_frame, text="Run Simulation", 
                                    command=self.run_simulation)
        self.sim_button.grid(row=2, column=0, columnspan=3, pady=5)
        
        # Results
        sim_results_frame = ttk.LabelFrame(sim_frame, text="Simulation Results", padding="10")
        sim_results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.sim_text = scrolledtext.ScrolledText(sim_results_frame, height=15, width=80)
        self.sim_text.pack(fill='both', expand=True)
    
    def analyze_range(self):
        """Analyze hand range for selected position"""
        try:
            position = Position(self.position_var.get())
            self.status_var.set(f"Analyzing {position.value} range...")
            
            range_analysis = self.research_tool.solver.analyze_preflop_range(position)
            
            # Display results
            self.range_text.delete(1.0, tk.END)
            self.range_text.insert(tk.END, f"=== {position.value} Opening Range ===\n\n")
            
            # Sort hands by frequency
            sorted_hands = sorted(range_analysis.hands.items(), 
                                key=lambda x: x[1], reverse=True)
            
            self.range_text.insert(tk.END, f"Range Size: {len([h for h, f in sorted_hands if f > 0])} hands\n\n")
            
            self.range_text.insert(tk.END, "Hand Frequencies:\n")
            for hand, frequency in sorted_hands:
                if frequency > 0:
                    percentage = frequency * 100
                    equity = self.research_tool.solver.calculate_hand_equity(hand)
                    self.range_text.insert(tk.END, 
                                         f"{hand:4s}: {percentage:5.1f}% frequency, {equity:5.1%} equity\n")
            
            # Add range statistics
            total_hands = len([h for h, f in sorted_hands if f > 0])
            avg_frequency = sum(f for h, f in sorted_hands) / len(sorted_hands)
            
            self.range_text.insert(tk.END, f"\n=== Range Statistics ===\n")
            self.range_text.insert(tk.END, f"Total hands in range: {total_hands}\n")
            self.range_text.insert(tk.END, f"Average frequency: {avg_frequency:.3f}\n")
            self.range_text.insert(tk.END, f"Range tightness: {total_hands/169:.1%} of all hands\n")
            
            self.status_var.set("Range analysis complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Range analysis failed: {str(e)}")
            self.status_var.set("Ready")
    
    def calculate_equity(self):
        """Calculate hand equity"""
        try:
            hand = self.hand_entry.get().strip()
            board = self.board_entry.get().strip()
            opponents = self.opponents_var.get()
            
            if not hand:
                messagebox.showwarning("Warning", "Please enter a hand")
                return
            
            self.status_var.set("Calculating equity...")
            
            equity = self.research_tool.solver.calculate_hand_equity(hand, board, opponents)
            
            # Display results
            self.equity_text.delete(1.0, tk.END)
            self.equity_text.insert(tk.END, f"=== Equity Analysis ===\n\n")
            self.equity_text.insert(tk.END, f"Hero Hand: {hand}\n")
            self.equity_text.insert(tk.END, f"Board: {board if board else 'Preflop'}\n")
            self.equity_text.insert(tk.END, f"Opponents: {opponents}\n\n")
            self.equity_text.insert(tk.END, f"Equity: {equity:.1%}\n\n")
            
            # Add hand strength analysis
            if equity >= 0.70:
                strength = "Very Strong"
            elif equity >= 0.60:
                strength = "Strong"
            elif equity >= 0.50:
                strength = "Marginal"
            else:
                strength = "Weak"
            
            self.equity_text.insert(tk.END, f"Hand Strength: {strength}\n")
            
            # Add recommended actions
            self.equity_text.insert(tk.END, f"\n=== Recommended Actions ===\n")
            if equity >= 0.65:
                self.equity_text.insert(tk.END, "• Suitable for value betting\n")
                self.equity_text.insert(tk.END, "• Good for 3-betting preflop\n")
            elif equity >= 0.55:
                self.equity_text.insert(tk.END, "• Can call raises in position\n")
                self.equity_text.insert(tk.END, "• Consider as bluff catcher\n")
            else:
                self.equity_text.insert(tk.END, "• Fold to significant action\n")
                self.equity_text.insert(tk.END, "• Avoid building large pots\n")
            
            self.status_var.set("Equity calculation complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Equity calculation failed: {str(e)}")
            self.status_var.set("Ready")
    
    def analyze_spot(self):
        """Analyze specific poker spot"""
        try:
            hero_pos = Position(self.hero_pos_var.get())
            stack_size = int(self.stack_entry.get())
            action_history = self.action_entry.get().strip().split(', ')
            
            self.status_var.set("Analyzing poker spot...")
            
            solution = self.research_tool.solver.analyze_spot(
                hero_pos, action_history, {hero_pos: stack_size}
            )
            
            # Display results
            self.spot_text.delete(1.0, tk.END)
            self.spot_text.insert(tk.END, f"=== GTO Spot Analysis ===\n\n")
            self.spot_text.insert(tk.END, f"Hero Position: {hero_pos.value}\n")
            self.spot_text.insert(tk.END, f"Stack Size: {stack_size} BB\n")
            self.spot_text.insert(tk.END, f"Action History: {', '.join(action_history)}\n\n")
            
            self.spot_text.insert(tk.END, f"Expected Value: {solution.ev:+.3f} BB\n")
            self.spot_text.insert(tk.END, f"Exploitability: {solution.exploitability:.3f}\n\n")
            
            # Show recommended ranges
            for position, range_data in solution.ranges.items():
                self.spot_text.insert(tk.END, f"=== {position.value} Strategy ===\n")
                hands_in_range = [h for h, f in range_data.hands.items() if f > 0]
                self.spot_text.insert(tk.END, f"Range size: {len(hands_in_range)} hands\n")
                self.spot_text.insert(tk.END, f"Action: {range_data.action.value}\n\n")
                
                # Show top hands
                sorted_hands = sorted(range_data.hands.items(), 
                                    key=lambda x: x[1], reverse=True)[:10]
                self.spot_text.insert(tk.END, "Top hands:\n")
                for hand, freq in sorted_hands:
                    if freq > 0:
                        self.spot_text.insert(tk.END, f"  {hand}: {freq:.1%}\n")
                self.spot_text.insert(tk.END, "\n")
            
            # Add strategic recommendations
            self.spot_text.insert(tk.END, "=== Strategic Recommendations ===\n")
            if solution.ev > 0.1:
                self.spot_text.insert(tk.END, "• This spot shows positive expected value\n")
                self.spot_text.insert(tk.END, "• Continue with aggressive strategy\n")
            elif solution.ev > 0:
                self.spot_text.insert(tk.END, "• Marginally profitable spot\n")
                self.spot_text.insert(tk.END, "• Play carefully, avoid big mistakes\n")
            else:
                self.spot_text.insert(tk.END, "• Losing spot on average\n")
                self.spot_text.insert(tk.END, "• Consider folding or playing defensively\n")
            
            self.status_var.set("Spot analysis complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Spot analysis failed: {str(e)}")
            self.status_var.set("Ready")
    
    def run_simulation(self):
        """Run tournament simulation"""
        def simulation_thread():
            try:
                num_sims = int(self.sim_count_entry.get())
                self.sim_button.config(state='disabled')
                self.progress_var.set(0)
                
                # Run simulation with progress updates
                results = self.research_tool.simulate_tournament_spots(num_sims)
                
                # Display results
                self.sim_text.delete(1.0, tk.END)
                self.sim_text.insert(tk.END, f"=== Tournament Simulation Results ===\n\n")
                self.sim_text.insert(tk.END, f"Simulations Run: {num_sims:,}\n")
                self.sim_text.insert(tk.END, f"Average EV: {results['avg_ev']:+.4f} BB\n")
                self.sim_text.insert(tk.END, f"Win Rate: {results['win_rate']:.1%}\n\n")
                
                # Calculate additional statistics
                hourly_ev = results['avg_ev'] * 100  # Assuming 100 hands per hour
                self.sim_text.insert(tk.END, f"Projected Hourly EV: {hourly_ev:+.2f} BB/hour\n")
                
                if results['win_rate'] > 0.55:
                    performance = "Excellent"
                elif results['win_rate'] > 0.52:
                    performance = "Good"
                elif results['win_rate'] > 0.50:
                    performance = "Break-even"
                else:
                    performance = "Losing"
                
                self.sim_text.insert(tk.END, f"Performance Rating: {performance}\n\n")
                
                # Add recommendations
                self.sim_text.insert(tk.END, "=== Recommendations ===\n")
                if results['avg_ev'] > 0.05:
                    self.sim_text.insert(tk.END, "• Strong positive EV - continue current strategy\n")
                    self.sim_text.insert(tk.END, "• Focus on volume to maximize profits\n")
                elif results['avg_ev'] > 0:
                    self.sim_text.insert(tk.END, "• Slight edge - work on reducing variance\n")
                    self.sim_text.insert(tk.END, "• Study marginal spots for improvement\n")
                else:
                    self.sim_text.insert(tk.END, "• Negative EV - review and adjust strategy\n")
                    self.sim_text.insert(tk.END, "• Focus on fundamental improvements\n")
                
                self.progress_var.set(100)
                self.status_var.set("Simulation complete")
                
            except Exception as e:
                messagebox.showerror("Error", f"Simulation failed: {str(e)}")
                self.status_var.set("Ready")
            finally:
                self.sim_button.config(state='normal')
        
        # Run simulation in background thread
        threading.Thread(target=simulation_thread, daemon=True).start()
        self.status_var.set("Running simulation...")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the poker research GUI"""
    print("Starting TexasSolver GTO Poker Research Tool...")
    app = PokerResearchGUI()
    app.run()

if __name__ == "__main__":
    main()