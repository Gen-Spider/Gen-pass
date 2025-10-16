#!/usr/bin/env python3
"""
Gen-Pass: A Professional Password Generator with Matrix UI
========================================================

A secure, customizable password generator with full-screen terminal interface,
3D Gen-Spider banner, and red matrix theme with delayed animations.

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
    Full-screen Matrix-style terminal interface with Gen-Spider branding.
    """
    
    def __init__(self):
        self.console = Console()
        self.width = self.console.size.width
        self.height = self.console.size.height
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def typewriter_effect(self, text: str, delay: float = 0.03, color: str = "red"):
        """Print text with typewriter effect."""
        for char in text:
            print(f"\033[91m{char}\033[0m", end='', flush=True)
            time.sleep(delay)
        print()
        
    def show_gen_spider_banner(self):
        """Display the epic Gen-Spider banner with 3D effect."""
        self.clear_screen()
        
        banner = """
██████████████████████████████████████████████████████████████████████████████
██                                                                            ██
██    ██████╗ ███████╗███╗   ██╗      ███████╗██████╗ ██╗██████╗ ███████╗██████╗     ██
██    ██╔══██╗██╔════╝████╗  ██║      ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗    ██
██    ██║  ██║█████╗  ██╔██╗ ██║█████╗███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝    ██
██    ██║  ██║██╔══╝  ██║╚██╗██║╚════╝╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗    ██
██    ██████╔╝███████╗██║ ╚████║      ███████║██║     ██║██████╔╝███████╗██║  ██║    ██
██    ╚═════╝ ╚══════╝╚═╝  ╚═══╝      ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ██
██                                                                            ██
██                           🕷️  PROFESSIONAL PASSWORD GENERATOR  🕷️                        ██
██                                                                            ██
██████████████████████████████████████████████████████████████████████████████
"""
        # Set red background for entire screen
        print(f"\033[41m\033[2J\033[H", end='')
        
        # Print banner with red background and white text
        lines = banner.split('\n')
        for i, line in enumerate(lines):
            if i < 3:  # Top border with delay
                time.sleep(0.1)
            print(f"\033[91m\033[1m{line}\033[0m")
            if i > len(lines) - 4:  # Bottom border with delay
                time.sleep(0.1)
                
    def show_matrix_rain(self, duration: int = 3):
        """Show matrix digital rain effect."""
        chars = "0123456789ABCDEF!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Clear line and print falling characters
            for _ in range(self.width // 2):
                char = random.choice(chars)
                col = random.randint(0, self.width - 1)
                print(f"\033[{random.randint(1, self.height)};{col}H\033[91m{char}\033[0m", end='')
            time.sleep(0.05)
            
    def show_loading_animation(self, text: str = "Initializing Gen-Spider Matrix"):
        """Show loading animation with progress bar."""
        with Progress(
            SpinnerColumn("dots", style="red"),
            TextColumn("[red]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(text, total=100)
            
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.02)
                
    def show_menu(self):
        """Display the main menu with 3D effects."""
        menu_panel = Panel(
            Text("""
🔐 PASSWORD GENERATION OPTIONS 🔐

1. 🎯 Generate Standard Password
2. 🌌 Generate Secure Passphrase  
3. 📊 Analyze Password Strength
4. 🎰 Batch Password Generation
5. ⚙️  Advanced Settings
6. 🚪 Exit Matrix

🔴 Enter your choice (1-6): """, style="bold red"),
            title="[bold red]🕷️ GEN-SPIDER MATRIX 🕷️[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(Align.center(menu_panel))
        
    def animated_text(self, text: str, delay: float = 0.05):
        """Display text with animation effect."""
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
        """Launch the full Matrix experience."""
        if not self.ui:
            return
            
        # Clear screen and show banner
        self.ui.show_gen_spider_banner()
        time.sleep(2)
        
        # Show loading animation
        print("\n\n")
        self.ui.show_loading_animation("Loading Gen-Spider Security Matrix...")
        time.sleep(1)
        
        # Show matrix rain effect
        self.ui.show_matrix_rain(2)
        
        # Clear and show menu
        self.ui.clear_screen()
        self.ui.show_gen_spider_banner()
        print("\n")
        self.ui.show_menu()
        
    def generate_password(self, 
                         length: int = 12,
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_symbols: bool = True,
                         exclude_ambiguous: bool = False,
                         custom_chars: str = "",
                         animated: bool = False) -> str:
        """
        Generate a secure password with specified criteria.
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character set
        chars = ""
        required_chars = []
        
        if use_lowercase:
            chars += self.lowercase
            required_chars.append(secrets.choice(self.lowercase))
            
        if use_uppercase:
            chars += self.uppercase
            required_chars.append(secrets.choice(self.uppercase))
            
        if use_digits:
            chars += self.digits
            required_chars.append(secrets.choice(self.digits))
            
        if use_symbols:
            chars += self.symbols
            required_chars.append(secrets.choice(self.symbols))
            
        if custom_chars:
            chars += custom_chars
            
        if not chars:
            raise ValueError("At least one character type must be selected")
        
        # Remove ambiguous characters if requested
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in self.ambiguous)
            required_chars = [c for c in required_chars if c not in self.ambiguous]
        
        # Generate password ensuring at least one character from each selected type
        password = required_chars.copy()
        
        # Fill remaining length with random characters
        for _ in range(length - len(required_chars)):
            password.append(secrets.choice(chars))
        
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        generated_password = ''.join(password)
        
        # Show with animation if UI mode
        if animated and self.ui:
            print("\n\033[91m█████ GENERATING QUANTUM PASSWORD █████\033[0m")
            self.ui.animated_text(f"Password: {generated_password}", 0.1)
            
        return generated_password
    
    def generate_passphrase(self, 
                          word_count: int = 4,
                          separator: str = "-",
                          capitalize: bool = True,
                          add_numbers: bool = False,
                          animated: bool = False) -> str:
        """
        Generate a memorable passphrase using common words.
        """
        # Common word list for passphrases
        words = [
            "apple", "beach", "chair", "dance", "eagle", "flame", "grape", "house",
            "island", "jungle", "kite", "lemon", "moon", "night", "ocean", "peace",
            "quiet", "river", "storm", "tiger", "under", "voice", "water", "zebra",
            "bright", "cloud", "dream", "earth", "forest", "golden", "happy", "light",
            "magic", "nature", "power", "quick", "shine", "thunder", "wind", "wonder",
            "matrix", "cipher", "spider", "quantum", "secure", "digital", "crypto", "shield"
        ]
        
        selected_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            if capitalize:
                word = word.capitalize()
            selected_words.append(word)
        
        passphrase = separator.join(selected_words)
        
        if add_numbers:
            numbers = ''.join([str(secrets.randbelow(10)) for _ in range(2)])
            passphrase += separator + numbers
        
        # Show with animation if UI mode
        if animated and self.ui:
            print("\n\033[91m█████ GENERATING QUANTUM PASSPHRASE █████\033[0m")
            self.ui.animated_text(f"Passphrase: {passphrase}", 0.08)
            
        return passphrase
    
    def check_strength(self, password: str, animated: bool = False) -> Dict[str, Any]:
        """
        Analyze password strength and provide feedback.
        """
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
            feedback.append("Consider using at least 12 characters")
        else:
            feedback.append("Password too short - use at least 8 characters")
        
        # Character variety checks
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        score += variety_count * 15
        
        if variety_count < 3:
            feedback.append("Use a mix of uppercase, lowercase, numbers, and symbols")
        
        # Common pattern checks
        if password.lower() in ['password', '123456', 'qwerty', 'admin']:
            score = 0
            feedback.append("Avoid common passwords")
        
        # Determine strength level
        if score >= 80:
            strength = "MAXIMUM SECURITY"
            strength_bar = "█" * 20
        elif score >= 60:
            strength = "STRONG"
            strength_bar = "█" * 15 + "░" * 5
        elif score >= 40:
            strength = "MODERATE"
            strength_bar = "█" * 10 + "░" * 10
        elif score >= 20:
            strength = "WEAK"
            strength_bar = "█" * 5 + "░" * 15
        else:
            strength = "CRITICAL"
            strength_bar = "░" * 20
        
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
        
        # Show animated analysis if UI mode
        if animated and self.ui:
            print("\n\033[91m█████ QUANTUM ANALYSIS COMPLETE █████\033[0m")
            self.ui.animated_text(f"Strength: {strength}", 0.05)
            self.ui.animated_text(f"Security Level: [{strength_bar}] {score}%", 0.02)
            
        return analysis

def main():
    """Main function with Matrix UI support."""
    parser = argparse.ArgumentParser(
        description="Gen-Pass: Professional Password Generator with Matrix UI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-l', '--length', type=int, default=12,
                       help='Password length (default: 12)')
    parser.add_argument('-c', '--count', type=int, default=1,
                       help='Number of passwords to generate (default: 1)')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='Exclude uppercase letters')
    parser.add_argument('--no-lowercase', action='store_true',
                       help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true',
                       help='Exclude digits')
    parser.add_argument('--no-symbols', action='store_true',
                       help='Exclude symbols')
    parser.add_argument('--exclude-ambiguous', action='store_true',
                       help='Exclude ambiguous characters (0, O, 1, l, I)')
    parser.add_argument('--passphrase', action='store_true',
                       help='Generate passphrase instead of password')
    parser.add_argument('--words', type=int, default=4,
                       help='Number of words in passphrase (default: 4)')
    parser.add_argument('--separator', default='-',
                       help='Passphrase word separator (default: -)')
    parser.add_argument('--check', type=str,
                       help='Check strength of provided password')
    parser.add_argument('--save', type=str,
                       help='Save generated passwords to file')
    parser.add_argument('--matrix', action='store_true',
                       help='Launch full Matrix UI experience')
    parser.add_argument('--no-ui', action='store_true',
                       help='Disable Matrix UI (CLI only mode)')
    parser.add_argument('--animate', action='store_true',
                       help='Enable text animations')
    
    args = parser.parse_args()
    
    # Initialize generator with UI mode
    ui_enabled = not args.no_ui
    generator = PasswordGenerator(ui_mode=ui_enabled)
    
    # Launch Matrix mode if requested or no arguments provided
    if args.matrix or (len(sys.argv) == 1 and ui_enabled):
        try:
            generator.launch_matrix_mode()
            
            while True:
                try:
                    choice = input("\n\033[91mMatrix Command: \033[0m").strip()
                    
                    if choice == '1':
                        length = int(input("\033[91mPassword Length (12): \033[0m") or "12")
                        password = generator.generate_password(length=length, animated=True)
                        generator.check_strength(password, animated=True)
                        
                    elif choice == '2':
                        words = int(input("\033[91mNumber of Words (4): \033[0m") or "4")
                        passphrase = generator.generate_passphrase(word_count=words, animated=True)
                        generator.check_strength(passphrase, animated=True)
                        
                    elif choice == '3':
                        pwd = input("\033[91mEnter Password to Analyze: \033[0m")
                        generator.check_strength(pwd, animated=True)
                        
                    elif choice == '4':
                        count = int(input("\033[91mNumber of Passwords (5): \033[0m") or "5")
                        print("\n\033[91m█████ BATCH GENERATION █████\033[0m")
                        for i in range(count):
                            password = generator.generate_password(animated=True)
                            time.sleep(0.5)
                            
                    elif choice == '6' or choice.lower() in ['exit', 'quit', 'q']:
                        generator.ui.animated_text("\n🔴 Exiting Matrix... Stay Secure! 🔴", 0.05)
                        break
                        
                    else:
                        print("\033[91mInvalid choice. Please select 1-6.\033[0m")
                        
                except KeyboardInterrupt:
                    generator.ui.animated_text("\n\n🔴 Matrix Interrupted. Goodbye! 🔴", 0.05)
                    break
                except Exception as e:
                    print(f"\033[91mError: {e}\033[0m")
                    
        except KeyboardInterrupt:
            print("\n\033[91m🔴 Matrix Session Terminated \033[0m")
        return
    
    # Check password strength if requested
    if args.check:
        analysis = generator.check_strength(args.check, animated=args.animate)
        print(f"\nPassword Strength Analysis:")
        print(f"Password: {args.check}")
        print(f"Strength: {analysis['strength']}")
        print(f"Score: {analysis['score']}/100")
        print(f"Security Level: [{analysis['strength_bar']}]")
        print(f"Length: {analysis['length']}")
        print(f"Character Types:")
        print(f"  - Lowercase: {'✓' if analysis['has_lowercase'] else '✗'}")
        print(f"  - Uppercase: {'✓' if analysis['has_uppercase'] else '✗'}")
        print(f"  - Digits: {'✓' if analysis['has_digits'] else '✗'}")
        print(f"  - Symbols: {'✓' if analysis['has_symbols'] else '✗'}")
        if analysis['feedback']:
            print(f"\nRecommendations:")
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
        
        # Save to file if requested
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