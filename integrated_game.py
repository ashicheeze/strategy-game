"""Integrated Strategy Game launcher.

This module combines the pygame based battle game with the Tkinter poker
research GUI.  In headless environments (like CI containers) there is no X11
display available, which previously caused pygame to abort immediately.  The
new implementation detects such situations and offers a textual fallback so
the script can still be executed for automated smoke tests or demonstrations.
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
from typing import Optional

if not os.environ.get("DISPLAY") and sys.platform != "win32":
    # In CI or other headless environments pygame cannot open a window.  The
    # dummy driver allows pygame to initialise without a display so we can run
    # non-interactive smoke tests.
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import tkinter as tk
from tkinter import messagebox

from battle_game import BattleGame
from poker_research_gui import PokerResearchGUI

class IntegratedStrategyGame:
    """
    Main application that integrates the battle game with poker research tools
    """
    
    def __init__(self):
        self.battle_game = None
        self.poker_gui = None
        self.setup_main_menu()
    
    def setup_main_menu(self):
        """Create the main menu interface"""
        self.root = tk.Tk()
        self.root.title("Strategy Game Hub - Battle Game & Poker Research")
        self.root.geometry("600x400")
        self.root.configure(bg='#2c3e50')
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="Strategy Game Hub",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Battle Game & TexasSolver GTO Poker Research",
            font=('Arial', 14),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack(pady=10)
        
        # Main buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(expand=True)
        
        # Battle Game button
        battle_button = tk.Button(
            buttons_frame,
            text="🏰 Start Battle Game",
            font=('Arial', 16, 'bold'),
            width=25,
            height=2,
            bg='#e74c3c',
            fg='white',
            command=self.start_battle_game,
            relief='raised',
            bd=3
        )
        battle_button.pack(pady=15)
        
        # Poker Research button
        poker_button = tk.Button(
            buttons_frame,
            text="♠️ Poker Research Tool",
            font=('Arial', 16, 'bold'),
            width=25,
            height=2,
            bg='#27ae60',
            fg='white',
            command=self.start_poker_research,
            relief='raised',
            bd=3
        )
        poker_button.pack(pady=15)
        
        # Both button
        both_button = tk.Button(
            buttons_frame,
            text="🎯 Launch Both Applications",
            font=('Arial', 16, 'bold'),
            width=25,
            height=2,
            bg='#3498db',
            fg='white',
            command=self.start_both,
            relief='raised',
            bd=3
        )
        both_button.pack(pady=15)
        
        # Information frame
        info_frame = tk.LabelFrame(
            self.root,
            text="About",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e',
            labelanchor='n'
        )
        info_frame.pack(fill='x', padx=20, pady=20)
        
        info_text = tk.Text(
            info_frame,
            height=6,
            width=70,
            bg='#34495e',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            wrap='word'
        )
        info_text.pack(padx=10, pady=10)
        
        info_content = """
Battle Game: A strategic board game with hidden information elements.
Move soldiers and kings on a 9x9 grid to defeat your opponent.

Poker Research Tool: Advanced GTO (Game Theory Optimal) poker analysis.
Analyze hand ranges, calculate equity, study tournament spots, and run simulations.

This integrated platform allows you to research strategic thinking across
different game types and improve your decision-making skills.
        """.strip()
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select an application to launch")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#34495e',
            fg='white'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_battle_game(self):
        """Start the battle game in a separate thread"""
        def run_battle_game():
            try:
                self.status_var.set("Starting Battle Game...")
                self.battle_game = BattleGame()
                self.battle_game.game_loop()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start Battle Game: {str(e)}")
            finally:
                self.status_var.set("Battle Game closed")
        
        # Run in separate thread to avoid blocking the main GUI
        game_thread = threading.Thread(target=run_battle_game, daemon=True)
        game_thread.start()
        
        messagebox.showinfo(
            "Battle Game", 
            "Battle Game is starting!\n\n"
            "Controls:\n"
            "• Click to select pieces\n"
            "• WASD keys to move selected piece\n"
            "• Find and eliminate enemy king to win!"
        )
    
    def start_poker_research(self):
        """Start the poker research tool"""
        try:
            self.status_var.set("Starting Poker Research Tool...")
            
            if self.poker_gui:
                # If already running, just bring to front
                self.poker_gui.root.lift()
                self.poker_gui.root.focus_force()
            else:
                # Create new poker GUI instance
                self.poker_gui = PokerResearchGUI()
                
                # Override the mainloop to integrate with our main application
                def run_poker_gui():
                    self.poker_gui.run()
                    self.poker_gui = None  # Reset when closed
                    self.status_var.set("Poker Research Tool closed")
                
                poker_thread = threading.Thread(target=run_poker_gui, daemon=True)
                poker_thread.start()
                
                messagebox.showinfo(
                    "Poker Research Tool",
                    "Poker Research Tool is starting!\n\n"
                    "Features:\n"
                    "• Range Analysis for all positions\n"
                    "• Equity Calculator with hand vs range\n"
                    "• Spot Analyzer for complex situations\n"
                    "• Tournament simulation tools"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Poker Research Tool: {str(e)}")
            self.status_var.set("Ready")
    
    def start_both(self):
        """Start both applications"""
        self.start_battle_game()
        # Small delay to avoid overwhelming the system
        self.root.after(1000, self.start_poker_research)
        
        messagebox.showinfo(
            "Both Applications",
            "Starting both Battle Game and Poker Research Tool!\n\n"
            "You can now:\n"
            "• Play the strategic battle game\n"
            "• Research poker GTO strategies\n"
            "• Compare strategic thinking across game types"
        )
    
    def run(self):
        """Start the main application"""
        print("Starting Integrated Strategy Game Hub...")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the Strategy Game Hub?"):
            # Clean up any running games
            if self.battle_game:
                try:
                    pygame.quit()
                except:
                    pass
            
            if self.poker_gui:
                try:
                    self.poker_gui.root.destroy()
                except:
                    pass
            
            self.root.destroy()
            sys.exit()

def is_headless() -> bool:
    """Return True if the environment has no available graphical display."""

    if sys.platform == "win32":
        # Windows always provides a display surface, so we only treat UNIX-like
        # systems without DISPLAY as headless.
        return False

    return not os.environ.get("DISPLAY")


def run_headless_mode(message: Optional[str] = None) -> None:
    """Provide a textual fallback when no GUI can be created."""

    header = "=" * 60
    print(header)
    print("Integrated Strategy Game Hub - Headless Mode")
    print(header)
    if message:
        print(message)
        print()

    print(
        "A graphical display was not detected, so the interactive "
        "Tkinter/Pygame interface cannot be shown.\n"
        "You can still experiment with the analytical tooling from the "
        "command line:"
    )
    print("  • python poker_solver.py --help        # explore solver options")
    print("  • python demo.py                       # text-based walkthrough")
    print()
    print(
        "To launch the full GUI experience, run this program on a machine with "
        "an available desktop session."
    )


def main(argv: Optional[list[str]] = None) -> None:
    """Main entry point supporting a headless fallback."""

    parser = argparse.ArgumentParser(
        description=(
            "Launch the integrated battle game and poker research hub. "
            "Use --headless to force a textual fallback."
        )
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without creating GUI windows (useful in CI environments).",
    )
    args = parser.parse_args(argv)

    if args.headless or is_headless():
        run_headless_mode(
            "Headless execution requested." if args.headless else None
        )
        return

    try:
        app = IntegratedStrategyGame()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as exc:  # pragma: no cover - defensive safeguard
        print(f"Fatal error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
