#!/usr/bin/env python3
"""
Gen-Pass: A Professional Password Generator
==========================================

A secure, customizable password generator with multiple options for creating
strong passwords tailored to your security needs.

Author: Gen-Spider
License: MIT
"""

import random
import string
import secrets
import argparse
import json
from typing import List, Dict, Any
from pathlib import Path


class PasswordGenerator:
    """
    A comprehensive password generator with customizable options.
    """
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1lI"
        
    def generate_password(self, 
                         length: int = 12,
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_symbols: bool = True,
                         exclude_ambiguous: bool = False,
                         custom_chars: str = "") -> str:
        """
        Generate a secure password with specified criteria.
        
        Args:
            length: Password length (default: 12)
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_digits: Include digits
            use_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters (0, O, 1, l, I)
            custom_chars: Additional custom characters to include
            
        Returns:
            Generated password string
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
        
        return ''.join(password)
    
    def generate_passphrase(self, 
                          word_count: int = 4,
                          separator: str = "-",
                          capitalize: bool = True,
                          add_numbers: bool = False) -> str:
        """
        Generate a memorable passphrase using common words.
        
        Args:
            word_count: Number of words in passphrase
            separator: Character to separate words
            capitalize: Capitalize first letter of each word
            add_numbers: Add random numbers to the passphrase
            
        Returns:
            Generated passphrase string
        """
        # Common word list for passphrases
        words = [
            "apple", "beach", "chair", "dance", "eagle", "flame", "grape", "house",
            "island", "jungle", "kite", "lemon", "moon", "night", "ocean", "peace",
            "quiet", "river", "storm", "tiger", "under", "voice", "water", "zebra",
            "bright", "cloud", "dream", "earth", "forest", "golden", "happy", "light",
            "magic", "nature", "power", "quick", "shine", "thunder", "wind", "wonder"
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
        
        return passphrase
    
    def check_strength(self, password: str) -> Dict[str, Any]:
        """
        Analyze password strength and provide feedback.
        
        Args:
            password: Password to analyze
            
        Returns:
            Dictionary containing strength analysis
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
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Moderate"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return {
            "strength": strength,
            "score": score,
            "feedback": feedback,
            "length": len(password),
            "has_lowercase": has_lower,
            "has_uppercase": has_upper,
            "has_digits": has_digit,
            "has_symbols": has_symbol
        }


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(
        description="Gen-Pass: Professional Password Generator",
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
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # Check password strength if requested
    if args.check:
        analysis = generator.check_strength(args.check)
        print(f"\nPassword Strength Analysis:")
        print(f"Password: {args.check}")
        print(f"Strength: {analysis['strength']}")
        print(f"Score: {analysis['score']}/100")
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
                    add_numbers=True
                )
                print(f"Passphrase {i+1}: {password}")
            else:
                password = generator.generate_password(
                    length=args.length,
                    use_uppercase=not args.no_uppercase,
                    use_lowercase=not args.no_lowercase,
                    use_digits=not args.no_digits,
                    use_symbols=not args.no_symbols,
                    exclude_ambiguous=args.exclude_ambiguous
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