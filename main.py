#!/usr/bin/env python3
"""
Gen-Pass: A Professional Password Generator with Matrix UI
========================================================

A secure, customizable password generator with full-screen terminal interface,
3D Git Spider banner, and red themed text animations.

Author: Gen-Spider
License: MIT
"""

import random
import string
import secrets
import argparse
import json
import os
import sys
import time
from typing import List, Dict, Any
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn
    import colorama
    from colorama import Fore, Back, Style, init
except ImportError:
    print("Installing required dependencies...")
    os.system("pip install rich colorama")
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn
    import colorama
    from colorama import Fore, Back, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

class MatrixUI:
    """
    Terminal interface with Git Spider branding and red text animations.
    """
    
    def __init__(self):
        self.console = Console()
        self.width = self.console.size.width
        self.height = self.console.size.height
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def typewriter_effect(self, text: str, delay: float = 0.03, color: str = "red"):
        """Print text with typewriter effect in red."""
        color_code = "\033[91m" if color == "red" else ""
        for char in text:
            print(f"{color_code}{char}\033[0m", end='', flush=True)
            time.sleep(delay)
        print()
        
    def show_git_spider_banner(self):
        """Display the Git Spider banner (red text only)."""
        self.clear_screen()
        
        banner = """
██████████████████████████████████████████████████████████████████████████████
██                                                                            ██
██    ██████╗ ██╗████████╗       ███████╗██████╗ ██╗██████╗ ███████╗██████╗    ██
██    ██╔══██╗██║╚══██╔══╝       ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗   ██
██    ██║  ██║██║   ██║          ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝   ██
██    ██║  ██║██║   ██║          ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗   ██
██    ██████╔╝██║   ██║          ███████║██║     ██║██████╔╝███████╗██║  ██║   ██
██    ╚═════╝ ╚═╝   ╚═╝          ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝   ██
██                                                                            ██
██                            🕷️   GIT SPIDER SECURITY   🕷️                          ██
██                                                                            ██
██████████████████████████████████████████████████████████████████████████████
"""
        # Only red text (no full-screen red background)
        for line in banner.split('\n'):
            print(f"\033[91m\033[1m{line}\033[0m")
        
    def show_matrix_rain(self, duration: int = 2):
        """Show subtle matrix-style tickers with red glyphs (no background fill)."""
        chars = "0123456789ABCDEF!@#$%^&*()_+-=[]{}|;:,.<>?"
        start_time = time.time()
        while time.time() - start_time < duration:
            col = random.randint(1, max(1, self.width - 2))
            row = random.randint(1, max(1, self.height - 2))
            char = random.choice(chars)
            print(f"\033[{row};{col}H\033[91m{char}\033[0m", end='', flush=True)
            time.sleep(0.01)
        print("\033[0m", end='')
        
    def show_loading_animation(self, text: str = "Initializing Git Spider"):
        """Show loading animation with red spinner text."""
        with Progress(
            SpinnerColumn("dots", style="red"),
            TextColumn("[red]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(text, total=100)
            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.015)
        
    def show_menu(self):
        """Display the main menu with red-styled text."""
        menu_panel = Panel(
            Text("""
🔐 PASSWORD GENERATION OPTIONS 🔐

1. 🎯 Generate Standard Password
2. 🌌 Generate Secure Passphrase  
3. 📊 Analyze Password Strength
4. 🎰 Batch Password Generation
5. ⚙️  Advanced Settings
6. 🚪 Exit

Enter your choice (1-6): """, style="bold red"),
            title="[bold red]🕷️ GIT SPIDER MATRIX 🕷️[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        self.console.print(Align.center(menu_panel))
        
    def animated_text(self, text: str, delay: float = 0.05):
        """Display red animated text."""
        for char in text:
            print(f"\033[91m{char}\033[0m", end='', flush=True)
            time.sleep(delay)
        print()

class PasswordGenerator:
    """
    Enhanced password generator with Matrix UI integration.
    """
    
    def __init__(self, ui_mode: bool = True):
        self.ui = MatrixUI() if ui_mode else None
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1lI"
        
    def launch_matrix_mode(self):
        """Launch the experience with Git Spider banner and red text only."""
        if not self.ui:
            return
        self.ui.show_git_spider_banner()
        time.sleep(1.2)
        print("\n")
        self.ui.show_loading_animation("Loading Git Spider Security Console...")
        time.sleep(0.5)
        self.ui.show_matrix_rain(1)
        print("\n")
        self.ui.show_menu()
        
    # ... the rest of the class remains unchanged from previous version ...

    def generate_password(self, 
                         length: int = 12,
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_symbols: bool = True,
                         exclude_ambiguous: bool = False,
                         custom_chars: str = "",
                         animated: bool = False) -> str:
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        chars = ""; required_chars = []
        if use_lowercase:
            chars += self.lowercase; required_chars.append(secrets.choice(self.lowercase))
        if use_uppercase:
            chars += self.uppercase; required_chars.append(secrets.choice(self.uppercase))
        if use_digits:
            chars += self.digits; required_chars.append(secrets.choice(self.digits))
        if use_symbols:
            chars += self.symbols; required_chars.append(secrets.choice(self.symbols))
        if custom_chars:
            chars += custom_chars
        if not chars:
            raise ValueError("At least one character type must be selected")
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in self.ambiguous)
            required_chars = [c for c in required_chars if c not in self.ambiguous]
        password = required_chars.copy()
        for _ in range(length - len(required_chars)):
            password.append(secrets.choice(chars))
        secrets.SystemRandom().shuffle(password)
        generated_password = ''.join(password)
        if animated and self.ui:
            print("\n\033[91m█████ GENERATING SECURE PASSWORD █████\033[0m")
            self.ui.animated_text(f"Password: {generated_password}")
        return generated_password

    def generate_passphrase(self, 
                          word_count: int = 4,
                          separator: str = "-",
                          capitalize: bool = True,
                          add_numbers: bool = False,
                          animated: bool = False) -> str:
        words = [
            "apple","beach","chair","dance","eagle","flame","grape","house",
            "island","jungle","kite","lemon","moon","night","ocean","peace",
            "quiet","river","storm","tiger","under","voice","water","zebra",
            "bright","cloud","dream","earth","forest","golden","happy","light",
            "magic","nature","power","quick","shine","thunder","wind","wonder",
            "matrix","cipher","spider","quantum","secure","digital","crypto","shield"
        ]
        selected_words = []
        for _ in range(word_count):
            w = secrets.choice(words)
            if capitalize:
                w = w.capitalize()
            selected_words.append(w)
        passphrase = separator.join(selected_words)
        if add_numbers:
            numbers = ''.join([str(secrets.randbelow(10)) for _ in range(2)])
            passphrase += separator + numbers
        if animated and self.ui:
            print("\n\033[91m█████ GENERATING SECURE PASSPHRASE █████\033[0m")
            self.ui.animated_text(f"Passphrase: {passphrase}")
        return passphrase

    def check_strength(self, password: str, animated: bool = False) -> Dict[str, Any]:
        score = 0; feedback = []
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15; feedback.append("Consider using at least 12 characters")
        else:
            feedback.append("Password too short - use at least 8 characters")
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbols for c in password)
        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        score += variety_count * 15
        if variety_count < 3:
            feedback.append("Use a mix of uppercase, lowercase, numbers, and symbols")
        if password.lower() in ['password', '123456', 'qwerty', 'admin']:
            score = 0; feedback.append("Avoid common passwords")
        if score >= 80:
            strength = "MAXIMUM SECURITY"; strength_bar = "█" * 20
        elif score >= 60:
            strength = "STRONG"; strength_bar = "█" * 15 + "░" * 5
        elif score >= 40:
            strength = "MODERATE"; strength_bar = "█" * 10 + "░" * 10
        elif score >= 20:
            strength = "WEAK"; strength_bar = "█" * 5 + "░" * 15
        else:
            strength = "CRITICAL"; strength_bar = "░" * 20
        analysis = {
            "strength": strength,
            "score": score,
            "feedback": feedback,
            "length": len(password),
            "has_lowercase": has_lower,
            "has_uppercase": has_upper,
            "has_digits": has_digit,
            "has_symbols": has_symbol,
            "strength_bar": strength_bar
        }
        if animated and self.ui:
            print("\n\033[91m█████ ANALYSIS COMPLETE █████\033[0m")
            self.ui.animated_text(f"Strength: {strength}")
            self.ui.animated_text(f"Security Level: [{strength_bar}] {score}%", 0.02)
        return analysis

def main():
    parser = argparse.ArgumentParser(
        description="Gen-Pass: Professional Password Generator with Git Spider UI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-l','--length', type=int, default=12)
    parser.add_argument('-c','--count', type=int, default=1)
    parser.add_argument('--no-uppercase', action='store_true')
    parser.add_argument('--no-lowercase', action='store_true')
    parser.add_argument('--no-digits', action='store_true')
    parser.add_argument('--no-symbols', action='store_true')
    parser.add_argument('--exclude-ambiguous', action='store_true')
    parser.add_argument('--passphrase', action='store_true')
    parser.add_argument('--words', type=int, default=4)
    parser.add_argument('--separator', default='-')
    parser.add_argument('--check', type=str)
    parser.add_argument('--save', type=str)
    parser.add_argument('--matrix', action='store_true')
    parser.add_argument('--no-ui', action='store_true')
    parser.add_argument('--animate', action='store_true')
    args = parser.parse_args()

    ui_enabled = not args.no_ui
    generator = PasswordGenerator(ui_mode=ui_enabled)

    if args.matrix or (len(sys.argv) == 1 and ui_enabled):
        try:
            generator.launch_matrix_mode()
            while True:
                try:
                    choice = input("\n\033[91mCommand: \033[0m").strip()
                    if choice == '1':
                        length = int(input("\033[91mPassword Length (12): \033[0m") or "12")
                        pwd = generator.generate_password(length=length, animated=True)
                        generator.check_strength(pwd, animated=True)
                    elif choice == '2':
                        words = int(input("\033[91mWords (4): \033[0m") or "4")
                        phrase = generator.generate_passphrase(word_count=words, animated=True)
                        generator.check_strength(phrase, animated=True)
                    elif choice == '3':
                        to_check = input("\033[91mEnter Password: \033[0m")
                        generator.check_strength(to_check, animated=True)
                    elif choice == '4':
                        count = int(input("\033[91mHow many (5): \033[0m") or "5")
                        print("\n\033[91m█████ BATCH █████\033[0m")
                        for _ in range(count):
                            generator.generate_password(animated=True)
                            time.sleep(0.3)
                    elif choice == '6' or choice.lower() in ['exit','quit','q']:
                        generator.ui.animated_text("\n🔴 Goodbye from Git Spider! 🔴", 0.05)
                        break
                    else:
                        print("\033[91mPick 1-6.\033[0m")
                except KeyboardInterrupt:
                    generator.ui.animated_text("\n\n🔴 Session Interrupted. 🔴", 0.05)
                    break
                except Exception as e:
                    print(f"\033[91mError: {e}\033[0m")
        except KeyboardInterrupt:
            print("\n\033[91m🔴 Session Terminated \033[0m")
        return

    if args.check:
        analysis = generator.check_strength(args.check, animated=args.animate)
        print(f"\nPassword Strength Analysis:")
        print(f"Password: {args.check}")
        print(f"Strength: {analysis['strength']}")
        print(f"Score: {analysis['score']}/100")
        print(f"Security Level: [{analysis['strength_bar']}]")
        print(f"Length: {analysis['length']}")
        print("Character Types:")
        print(f"  - Lowercase: {'✓' if analysis['has_lowercase'] else '✗'}")
        print(f"  - Uppercase: {'✓' if analysis['has_uppercase'] else '✗'}")
        print(f"  - Digits: {'✓' if analysis['has_digits'] else '✗'}")
        print(f"  - Symbols: {'✓' if analysis['has_symbols'] else '✗'}")
        if analysis['feedback']:
            print("\nRecommendations:")
            for tip in analysis['feedback']:
                print(f"  - {tip}")
        return

    results = []
    try:
        for i in range(args.count):
            if args.passphrase:
                password = generator.generate_passphrase(
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=True,
                    add_numbers=True,
                    animated=args.animate
                )
                print(f"Passphrase {i+1}: {password}")
            else:
                password = generator.generate_password(
                    length=args.length,
                    use_uppercase=not args.no_uppercase,
                    use_lowercase=not args.no_lowercase,
                    use_digits=not args.no_digits,
                    use_symbols=not args.no_symbols,
                    exclude_ambiguous=args.exclude_ambiguous,
                    animated=args.animate
                )
                print(f"Password {i+1}: {password}")
            results.append(password)
        if args.save:
            with open(args.save, 'w') as f:
                for password in results:
                    f.write(password + '\n')
            print(f"\nPasswords saved to: {args.save}")
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())