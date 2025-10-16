#!/usr/bin/env python3
"""
Enterprise Password Generator CLI
================================

Advanced command-line interface for the Gen-Pass enterprise password
generation system. Provides comprehensive password management capabilities
for security professionals and developers.

Author: Gen-Spider Security Systems
Version: 3.2.1
License: MIT
"""

import argparse
import sys
import json
import csv
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import getpass
from dataclasses import asdict

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    
from password_generator import (
    EnterprisePasswordGenerator,
    PasswordPolicy,
    PasswordComplexity,
    PasswordAnalysis
)


class PasswordGeneratorCLI:
    """
    Advanced CLI interface for enterprise password generation.
    
    Features:
    - Multiple output formats (JSON, CSV, plain text)
    - Batch operations with progress tracking
    - Interactive policy configuration
    - Comprehensive password analysis
    - Secure password input/verification
    - Export/import capabilities
    """
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.generator = EnterprisePasswordGenerator()
        
    def run(self, args: List[str] = None) -> int:
        """Main entry point for CLI application."""
        parser = self._create_parser()
        
        if args is None:
            args = sys.argv[1:]
            
        try:
            parsed_args = parser.parse_args(args)
            return self._execute_command(parsed_args)
        except KeyboardInterrupt:
            self._print_error("\nOperation cancelled by user")
            return 1
        except Exception as e:
            self._print_error(f"Error: {e}")
            return 1
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with all subcommands."""
        parser = argparse.ArgumentParser(
            prog='gen-pass',
            description='Enterprise Password Generator - Professional security tool for generating and analyzing passwords',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
EXAMPLES:
  gen-pass generate --length 16 --count 5
  gen-pass generate --complexity maximum --output passwords.json
  gen-pass passphrase --words 6 --separator "-"
  gen-pass analyze --password "MyPassword123!"
  gen-pass batch --count 100 --format csv --output batch.csv
  gen-pass policy --create --name "corporate" --min-length 14
  gen-pass interactive
  
SECURITY LEVELS:
  minimum    - Basic 8+ character passwords
  standard   - 12+ characters with mixed case, numbers, symbols
  high       - 16+ characters with strict requirements
  maximum    - 20+ characters with advanced security features
  military   - 24+ characters with maximum security

For more information, visit: https://github.com/Gen-Spider/Gen-pass
"""
        )
        
        parser.add_argument('--version', action='version', version='Gen-Pass v3.2.1')
        parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
        parser.add_argument('--quiet', '-q', action='store_true', help='Suppress non-essential output')
        parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text', help='Output format')
        parser.add_argument('--output', '-o', help='Output file path')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Generate password command
        gen_parser = subparsers.add_parser('generate', help='Generate passwords', aliases=['gen'])
        self._add_generation_args(gen_parser)
        
        # Generate passphrase command
        phrase_parser = subparsers.add_parser('passphrase', help='Generate passphrases', aliases=['phrase'])
        self._add_passphrase_args(phrase_parser)
        
        # Analyze password command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze password strength', aliases=['check'])
        self._add_analysis_args(analyze_parser)
        
        # Batch operations command
        batch_parser = subparsers.add_parser('batch', help='Batch password generation')
        self._add_batch_args(batch_parser)
        
        # Policy management command
        policy_parser = subparsers.add_parser('policy', help='Manage password policies')
        self._add_policy_args(policy_parser)
        
        # Interactive mode command
        interactive_parser = subparsers.add_parser('interactive', help='Interactive mode', aliases=['ui'])
        
        # Hash generation command
        hash_parser = subparsers.add_parser('hash', help='Generate password hashes')
        self._add_hash_args(hash_parser)
        
        return parser
    
    def _add_generation_args(self, parser: argparse.ArgumentParser):
        """Add arguments for password generation."""
        parser.add_argument('--length', '-l', type=int, default=12, help='Password length (default: 12)')
        parser.add_argument('--count', '-c', type=int, default=1, help='Number of passwords to generate')
        parser.add_argument('--complexity', choices=['minimum', 'standard', 'high', 'maximum', 'military'], 
                          default='standard', help='Password complexity level')
        parser.add_argument('--no-uppercase', action='store_true', help='Exclude uppercase letters')
        parser.add_argument('--no-lowercase', action='store_true', help='Exclude lowercase letters')
        parser.add_argument('--no-digits', action='store_true', help='Exclude digits')
        parser.add_argument('--no-symbols', action='store_true', help='Exclude symbols')
        parser.add_argument('--exclude-ambiguous', action='store_true', help='Exclude ambiguous characters (0, O, 1, l, I)')
        parser.add_argument('--exclude-similar', action='store_true', help='Exclude similar characters')
        parser.add_argument('--custom-chars', help='Additional custom characters to include')
        parser.add_argument('--min-entropy', type=float, help='Minimum entropy requirement in bits')
        parser.add_argument('--policy-file', help='Load password policy from JSON file')
    
    def _add_passphrase_args(self, parser: argparse.ArgumentParser):
        """Add arguments for passphrase generation."""
        parser.add_argument('--words', '-w', type=int, default=6, help='Number of words (default: 6)')
        parser.add_argument('--count', '-c', type=int, default=1, help='Number of passphrases to generate')
        parser.add_argument('--separator', '-s', default='-', help='Word separator (default: -)')
        parser.add_argument('--no-capitalize', action='store_true', help='Do not capitalize words')
        parser.add_argument('--no-numbers', action='store_true', help='Do not add numbers')
        parser.add_argument('--add-symbols', action='store_true', help='Add symbols')
        parser.add_argument('--min-entropy', type=float, default=50.0, help='Minimum entropy in bits')
    
    def _add_analysis_args(self, parser: argparse.ArgumentParser):
        """Add arguments for password analysis."""
        parser.add_argument('--password', help='Password to analyze (leave empty for secure input)')
        parser.add_argument('--file', help='File containing passwords to analyze (one per line)')
        parser.add_argument('--policy-file', help='Policy file for compliance checking')
        parser.add_argument('--detailed', action='store_true', help='Show detailed analysis')
        parser.add_argument('--include-hashes', action='store_true', help='Include password hashes')
    
    def _add_batch_args(self, parser: argparse.ArgumentParser):
        """Add arguments for batch operations."""
        parser.add_argument('--count', '-c', type=int, required=True, help='Number of passwords to generate')
        parser.add_argument('--type', choices=['password', 'passphrase'], default='password', help='Type of generation')
        parser.add_argument('--length', '-l', type=int, default=12, help='Password length')
        parser.add_argument('--words', '-w', type=int, default=6, help='Words for passphrases')
        parser.add_argument('--complexity', choices=['minimum', 'standard', 'high', 'maximum', 'military'], 
                          default='standard', help='Complexity level')
        parser.add_argument('--threads', type=int, help='Number of threads (auto-detected if not specified)')
        parser.add_argument('--chunk-size', type=int, default=1000, help='Processing chunk size')
    
    def _add_policy_args(self, parser: argparse.ArgumentParser):
        """Add arguments for policy management."""
        parser.add_argument('--create', action='store_true', help='Create new policy interactively')
        parser.add_argument('--list', action='store_true', help='List available policies')
        parser.add_argument('--export', help='Export policy to file')
        parser.add_argument('--import', dest='import_file', help='Import policy from file')
        parser.add_argument('--validate', help='Validate policy file')
        parser.add_argument('--name', help='Policy name')
        parser.add_argument('--min-length', type=int, help='Minimum length')
        parser.add_argument('--max-length', type=int, help='Maximum length')
    
    def _add_hash_args(self, parser: argparse.ArgumentParser):
        """Add arguments for hash generation."""
        parser.add_argument('--password', help='Password to hash (leave empty for secure input)')
        parser.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256', 'sha512', 'pbkdf2'], 
                          default='sha256', help='Hash algorithm')
        parser.add_argument('--salt', help='Salt for hashing (auto-generated if not provided)')
        parser.add_argument('--verify', help='Verify password against hash info JSON file')
    
    def _execute_command(self, args: argparse.Namespace) -> int:
        """Execute the appropriate command based on parsed arguments."""
        if not args.command:
            # Default to interactive mode
            return self._interactive_mode()
        
        command_map = {
            'generate': self._generate_passwords,
            'gen': self._generate_passwords,
            'passphrase': self._generate_passphrases,
            'phrase': self._generate_passphrases,
            'analyze': self._analyze_passwords,
            'check': self._analyze_passwords,
            'batch': self._batch_operations,
            'policy': self._policy_management,
            'interactive': self._interactive_mode,
            'ui': self._interactive_mode,
            'hash': self._hash_operations
        }
        
        handler = command_map.get(args.command)
        if handler:
            return handler(args)
        else:
            self._print_error(f"Unknown command: {args.command}")
            return 1
    
    def _generate_passwords(self, args: argparse.Namespace) -> int:
        """Generate passwords based on arguments."""
        try:
            # Create policy from arguments
            policy = self._create_policy_from_args(args)
            complexity = PasswordComplexity(args.complexity)
            
            passwords = []
            
            if args.count == 1:
                password = self.generator.generate_password(
                    policy=policy,
                    length=args.length,
                    complexity=complexity
                )
                passwords.append(password)
                
                if not args.quiet:
                    self._print_success(f"Generated password: {password}")
                    
            else:
                if not args.quiet and RICH_AVAILABLE:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TaskProgressColumn(),
                        console=self.console
                    ) as progress:
                        task = progress.add_task("Generating passwords...", total=args.count)
                        
                        passwords = self.generator.batch_generate(
                            count=args.count,
                            generator_func=self.generator.generate_password,
                            policy=policy,
                            length=args.length,
                            complexity=complexity
                        )
                        
                        progress.update(task, completed=args.count)
                else:
                    passwords = self.generator.batch_generate(
                        count=args.count,
                        generator_func=self.generator.generate_password,
                        policy=policy,
                        length=args.length,
                        complexity=complexity
                    )
            
            self._output_results(passwords, args)
            return 0
            
        except Exception as e:
            self._print_error(f"Password generation failed: {e}")
            return 1
    
    def _generate_passphrases(self, args: argparse.Namespace) -> int:
        """Generate passphrases based on arguments."""
        try:
            passphrases = []
            
            if args.count == 1:
                passphrase = self.generator.generate_passphrase(
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=not args.no_capitalize,
                    add_numbers=not args.no_numbers,
                    add_symbols=args.add_symbols,
                    min_entropy=args.min_entropy
                )
                passphrases.append(passphrase)
                
                if not args.quiet:
                    self._print_success(f"Generated passphrase: {passphrase}")
                    
            else:
                if not args.quiet and RICH_AVAILABLE:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TaskProgressColumn(),
                        console=self.console
                    ) as progress:
                        task = progress.add_task("Generating passphrases...", total=args.count)
                        
                        passphrases = self.generator.batch_generate(
                            count=args.count,
                            generator_func=self.generator.generate_passphrase,
                            word_count=args.words,
                            separator=args.separator,
                            capitalize=not args.no_capitalize,
                            add_numbers=not args.no_numbers,
                            add_symbols=args.add_symbols,
                            min_entropy=args.min_entropy
                        )
                        
                        progress.update(task, completed=args.count)
                else:
                    passphrases = self.generator.batch_generate(
                        count=args.count,
                        generator_func=self.generator.generate_passphrase,
                        word_count=args.words,
                        separator=args.separator,
                        capitalize=not args.no_capitalize,
                        add_numbers=not args.no_numbers,
                        add_symbols=args.add_symbols,
                        min_entropy=args.min_entropy
                    )
            
            self._output_results(passphrases, args)
            return 0
            
        except Exception as e:
            self._print_error(f"Passphrase generation failed: {e}")
            return 1
    
    def _analyze_passwords(self, args: argparse.Namespace) -> int:
        """Analyze password strength."""
        try:
            passwords = []
            
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    passwords = [line.strip() for line in f if line.strip()]
            else:
                if args.password:
                    passwords = [args.password]
                else:
                    password = getpass.getpass("Enter password to analyze: ")
                    passwords = [password]
            
            policy = None
            if args.policy_file:
                policy = self._load_policy_from_file(args.policy_file)
            
            results = []
            for password in passwords:
                analysis = self.generator.analyze_password(password, policy)
                results.append(analysis)
                
                if not args.quiet:
                    self._display_analysis(analysis, args.detailed)
            
            if args.output:
                self._save_analysis_results(results, args)
            
            return 0
            
        except Exception as e:
            self._print_error(f"Password analysis failed: {e}")
            return 1
    
    def _batch_operations(self, args: argparse.Namespace) -> int:
        """Perform batch password generation operations."""
        try:
            if not args.quiet:
                self._print_info(f"Starting batch generation of {args.count} {args.type}s...")
            
            start_time = time.time()
            
            if args.type == 'password':
                complexity = PasswordComplexity(args.complexity)
                results = self.generator.batch_generate(
                    count=args.count,
                    generator_func=self.generator.generate_password,
                    length=args.length,
                    complexity=complexity
                )
            else:  # passphrase
                results = self.generator.batch_generate(
                    count=args.count,
                    generator_func=self.generator.generate_passphrase,
                    word_count=args.words
                )
            
            end_time = time.time()
            
            if not args.quiet:
                duration = end_time - start_time
                rate = args.count / duration if duration > 0 else 0
                self._print_success(f"Generated {args.count} {args.type}s in {duration:.2f}s ({rate:.0f}/sec)")
            
            self._output_results(results, args)
            return 0
            
        except Exception as e:
            self._print_error(f"Batch operation failed: {e}")
            return 1
    
    def _policy_management(self, args: argparse.Namespace) -> int:
        """Manage password policies."""
        try:
            if args.create:
                return self._create_policy_interactive(args)
            elif args.list:
                return self._list_policies()
            elif args.export:
                return self._export_policy(args)
            elif args.import_file:
                return self._import_policy(args)
            elif args.validate:
                return self._validate_policy(args)
            else:
                self._print_error("No policy operation specified. Use --create, --list, --export, --import, or --validate")
                return 1
                
        except Exception as e:
            self._print_error(f"Policy management failed: {e}")
            return 1
    
    def _hash_operations(self, args: argparse.Namespace) -> int:
        """Perform password hashing operations."""
        try:
            if args.verify:
                return self._verify_hash(args)
            
            password = args.password
            if not password:
                password = getpass.getpass("Enter password to hash: ")
            
            hash_info = self.generator.generate_hash(
                password=password,
                algorithm=args.algorithm,
                salt=args.salt
            )
            
            if args.format == 'json':
                output = json.dumps(hash_info, indent=2)
            else:
                output = f"""Password Hash Information:
  Algorithm: {hash_info['algorithm']}
  Salt: {hash_info['salt']}
  Hash: {hash_info['hash']}
  Timestamp: {hash_info['timestamp']}"""
                
                if 'iterations' in hash_info:
                    output += f"\n  Iterations: {hash_info['iterations']}"
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                self._print_success(f"Hash information saved to {args.output}")
            else:
                print(output)
            
            return 0
            
        except Exception as e:
            self._print_error(f"Hash operation failed: {e}")
            return 1
    
    def _verify_hash(self, args: argparse.Namespace) -> int:
        """Verify password against stored hash."""
        try:
            with open(args.verify, 'r') as f:
                hash_info = json.load(f)
            
            password = getpass.getpass("Enter password to verify: ")
            
            is_valid = self.generator.verify_hash(password, hash_info)
            
            if is_valid:
                self._print_success("Password verification: VALID")
                return 0
            else:
                self._print_error("Password verification: INVALID")
                return 1
                
        except Exception as e:
            self._print_error(f"Hash verification failed: {e}")
            return 1
    
    def _interactive_mode(self, args: argparse.Namespace = None) -> int:
        """Enter interactive mode for password generation."""
        if not RICH_AVAILABLE:
            self._print_error("Interactive mode requires the 'rich' library. Install with: pip install rich")
            return 1
        
        self._display_banner()
        
        while True:
            try:
                self._display_main_menu()
                choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
                
                if choice == "1":
                    self._interactive_generate_password()
                elif choice == "2":
                    self._interactive_generate_passphrase()
                elif choice == "3":
                    self._interactive_analyze_password()
                elif choice == "4":
                    self._interactive_batch_generate()
                elif choice == "5":
                    self._interactive_policy_manager()
                elif choice == "6":
                    self._interactive_hash_generator()
                elif choice == "7":
                    self._display_help()
                elif choice == "8":
                    self._display_about()
                elif choice == "9":
                    self._print_info("Goodbye from Gen-Spider Security Systems!")
                    break
                    
            except KeyboardInterrupt:
                self._print_info("\nGoodbye from Gen-Spider Security Systems!")
                break
            except Exception as e:
                self._print_error(f"An error occurred: {e}")
        
        return 0
    
    def _display_banner(self):
        """Display the application banner."""
        if RICH_AVAILABLE:
            banner = Text("""
 ██████╗ ███████╗███╗   ██╗      ██████╗  █████╗ ███████╗███████╗
██╔════╝ ██╔════╝████╗  ██║      ██╔══██╗██╔══██╗██╔════╝██╔════╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗██████╔╝███████║███████╗███████╗
██║   ██║██╔══╝  ██║╚██╗██║╚════╝██╔═══╝ ██╔══██║╚════██║╚════██║
╚██████╔╝███████╗██║ ╚████║      ██║     ██║  ██║███████║███████║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝      ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                  
      Enterprise Password Generator v3.2.1 - Security Systems
""", style="bold green")
            
            panel = Panel(
                Align.center(banner),
                title="[bold red]🕷️ GEN-SPIDER SECURITY SYSTEMS 🕷️[/bold red]",
                border_style="red"
            )
            
            self.console.print(panel)
        else:
            print("GEN-PASS - Enterprise Password Generator v3.2.1")
            print("Gen-Spider Security Systems")
            print("=" * 50)
    
    def _display_main_menu(self):
        """Display the main menu options."""
        if RICH_AVAILABLE:
            menu = Table(show_header=False, box=None, padding=(0, 2))
            menu.add_column("Option", style="bold cyan")
            menu.add_column("Description", style="white")
            
            options = [
                ("1.", "🔐 Generate Password"),
                ("2.", "📝 Generate Passphrase"),
                ("3.", "🔍 Analyze Password"),
                ("4.", "⚡ Batch Generation"),
                ("5.", "📋 Policy Manager"),
                ("6.", "🔗 Hash Generator"),
                ("7.", "❓ Help"),
                ("8.", "ℹ️  About"),
                ("9.", "🚪 Exit")
            ]
            
            for option, description in options:
                menu.add_row(option, description)
            
            panel = Panel(
                menu,
                title="[bold green]Main Menu[/bold green]",
                border_style="green"
            )
            
            self.console.print(panel)
        else:
            print("\nMain Menu:")
            print("1. Generate Password")
            print("2. Generate Passphrase")
            print("3. Analyze Password")
            print("4. Batch Generation")
            print("5. Policy Manager")
            print("6. Hash Generator")
            print("7. Help")
            print("8. About")
            print("9. Exit")
    
    def _create_policy_from_args(self, args: argparse.Namespace) -> Optional[PasswordPolicy]:
        """Create a password policy from command line arguments."""
        if hasattr(args, 'policy_file') and args.policy_file:
            return self._load_policy_from_file(args.policy_file)
        
        # Create policy from individual arguments
        policy = PasswordPolicy()
        
        if hasattr(args, 'min_entropy') and args.min_entropy:
            policy.entropy_threshold = args.min_entropy
        
        if hasattr(args, 'no_uppercase') and args.no_uppercase:
            policy.require_uppercase = False
            policy.min_uppercase = 0
        
        if hasattr(args, 'no_lowercase') and args.no_lowercase:
            policy.require_lowercase = False
            policy.min_lowercase = 0
        
        if hasattr(args, 'no_digits') and args.no_digits:
            policy.require_digits = False
            policy.min_digits = 0
        
        if hasattr(args, 'no_symbols') and args.no_symbols:
            policy.require_symbols = False
            policy.min_symbols = 0
        
        if hasattr(args, 'exclude_ambiguous') and args.exclude_ambiguous:
            policy.exclude_ambiguous = True
        
        if hasattr(args, 'exclude_similar') and args.exclude_similar:
            policy.exclude_similar = True
        
        return policy
    
    def _load_policy_from_file(self, filepath: str) -> PasswordPolicy:
        """Load password policy from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert dict to PasswordPolicy object
        return PasswordPolicy(**data)
    
    def _display_analysis(self, analysis: PasswordAnalysis, detailed: bool = False):
        """Display password analysis results."""
        if not RICH_AVAILABLE:
            # Fallback to plain text
            print(f"\nPassword Analysis:")
            print(f"Strength: {analysis.strength_level} ({analysis.strength_score:.1f}/100)")
            print(f"Entropy: {analysis.entropy:.1f} bits")
            if detailed:
                print(f"Vulnerabilities: {', '.join(analysis.vulnerabilities) or 'None'}")
                print(f"Recommendations: {', '.join(analysis.recommendations)}")
            return
        
        # Rich display
        table = Table(title="Password Analysis Results")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Status", justify="center")
        
        # Strength level with color coding
        strength_color = {
            "EXCELLENT": "bright_green",
            "VERY_STRONG": "green",
            "STRONG": "yellow",
            "GOOD": "yellow",
            "MODERATE": "orange1",
            "WEAK": "red",
            "VERY_WEAK": "bright_red"
        }.get(analysis.strength_level, "white")
        
        table.add_row(
            "Strength Level",
            f"[{strength_color}]{analysis.strength_level}[/{strength_color}]",
            f"[{strength_color}]{analysis.strength_score:.1f}/100[/{strength_color}]"
        )
        
        table.add_row("Entropy", f"{analysis.entropy:.1f} bits", "✓" if analysis.entropy >= 50 else "⚠️")
        table.add_row("Length", str(len(analysis.password)), "✓" if len(analysis.password) >= 12 else "⚠️")
        
        # Character analysis
        char_symbols = {
            "has_lowercase": ("Lowercase", "✓" if analysis.character_analysis["has_lowercase"] else "✗"),
            "has_uppercase": ("Uppercase", "✓" if analysis.character_analysis["has_uppercase"] else "✗"),
            "has_digits": ("Digits", "✓" if analysis.character_analysis["has_digits"] else "✗"),
            "has_symbols": ("Symbols", "✓" if analysis.character_analysis["has_symbols"] else "✗")
        }
        
        for key, (label, symbol) in char_symbols.items():
            table.add_row(label, "Present" if analysis.character_analysis[key] else "Missing", symbol)
        
        self.console.print(table)
        
        if detailed:
            # Vulnerabilities
            if analysis.vulnerabilities:
                vuln_panel = Panel(
                    "\n".join(f"• {vuln}" for vuln in analysis.vulnerabilities),
                    title="[bold red]Vulnerabilities[/bold red]",
                    border_style="red"
                )
                self.console.print(vuln_panel)
            
            # Recommendations
            if analysis.recommendations:
                rec_panel = Panel(
                    "\n".join(f"• {rec}" for rec in analysis.recommendations),
                    title="[bold yellow]Recommendations[/bold yellow]",
                    border_style="yellow"
                )
                self.console.print(rec_panel)
            
            # Crack time estimates
            if analysis.time_to_crack:
                crack_table = Table(title="Estimated Crack Time")
                crack_table.add_column("Attack Scenario", style="cyan")
                crack_table.add_column("Time to Crack", style="white")
                
                for scenario, time_str in analysis.time_to_crack.items():
                    crack_table.add_row(scenario.replace('_', ' ').title(), time_str)
                
                self.console.print(crack_table)
    
    def _output_results(self, results: List[str], args: argparse.Namespace):
        """Output results in the specified format."""
        if args.format == 'json':
            output_data = {
                "results": results,
                "count": len(results),
                "timestamp": time.time(),
                "generator": "Gen-Pass v3.2.1"
            }
            output = json.dumps(output_data, indent=2)
        elif args.format == 'csv':
            output = "password\n"
            output += "\n".join(results)
        else:
            output = "\n".join(results)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            if not args.quiet:
                self._print_success(f"Results saved to {args.output}")
        else:
            print(output)
    
    def _save_analysis_results(self, results: List[PasswordAnalysis], args: argparse.Namespace):
        """Save password analysis results to file."""
        if args.format == 'json':
            output_data = [asdict(result) for result in results]
            output = json.dumps(output_data, indent=2)
        elif args.format == 'csv':
            # CSV output for analysis
            import io
            output_buffer = io.StringIO()
            writer = csv.writer(output_buffer)
            
            # Header
            writer.writerow([
                'password', 'strength_level', 'strength_score', 'entropy',
                'has_lowercase', 'has_uppercase', 'has_digits', 'has_symbols',
                'vulnerabilities', 'recommendations'
            ])
            
            # Data
            for result in results:
                writer.writerow([
                    result.password,
                    result.strength_level,
                    result.strength_score,
                    result.entropy,
                    result.character_analysis['has_lowercase'],
                    result.character_analysis['has_uppercase'],
                    result.character_analysis['has_digits'],
                    result.character_analysis['has_symbols'],
                    '; '.join(result.vulnerabilities),
                    '; '.join(result.recommendations)
                ])
            
            output = output_buffer.getvalue()
        else:
            # Plain text output
            output_parts = []
            for i, result in enumerate(results, 1):
                output_parts.append(f"Password {i}: {result.password}")
                output_parts.append(f"Strength: {result.strength_level} ({result.strength_score:.1f}/100)")
                output_parts.append(f"Entropy: {result.entropy:.1f} bits")
                output_parts.append("---")
            
            output = "\n".join(output_parts)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    
    def _print_success(self, message: str):
        """Print success message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold green]✓[/bold green] {message}")
        else:
            print(f"✓ {message}")
    
    def _print_error(self, message: str):
        """Print error message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold red]✗[/bold red] {message}")
        else:
            print(f"✗ {message}", file=sys.stderr)
    
    def _print_info(self, message: str):
        """Print info message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold blue]ℹ[/bold blue] {message}")
        else:
            print(f"ℹ {message}")
    
    def _print_warning(self, message: str):
        """Print warning message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold yellow]⚠[/bold yellow] {message}")
        else:
            print(f"⚠ {message}")
    
    # Placeholder methods for interactive mode (to be implemented)
    def _interactive_generate_password(self):
        """Interactive password generation."""
        self._print_info("Interactive password generation - Feature coming soon!")
    
    def _interactive_generate_passphrase(self):
        """Interactive passphrase generation."""
        self._print_info("Interactive passphrase generation - Feature coming soon!")
    
    def _interactive_analyze_password(self):
        """Interactive password analysis."""
        self._print_info("Interactive password analysis - Feature coming soon!")
    
    def _interactive_batch_generate(self):
        """Interactive batch generation."""
        self._print_info("Interactive batch generation - Feature coming soon!")
    
    def _interactive_policy_manager(self):
        """Interactive policy management."""
        self._print_info("Interactive policy management - Feature coming soon!")
    
    def _interactive_hash_generator(self):
        """Interactive hash generation."""
        self._print_info("Interactive hash generation - Feature coming soon!")
    
    def _display_help(self):
        """Display help information."""
        self._print_info("Help system - Feature coming soon!")
    
    def _display_about(self):
        """Display about information."""
        if RICH_AVAILABLE:
            about_text = Text("""
Gen-Pass Enterprise Password Generator v3.2.1

Developed by Gen-Spider Security Systems
Copyright © 2024 Gen-Spider Security Systems

Features:
• Cryptographically secure password generation
• Advanced entropy calculation and analysis
• Multiple complexity levels and policies
• Batch processing with multi-threading
• Comprehensive security analysis
• Hash generation and verification
• Enterprise-grade security standards

License: MIT License
Repository: https://github.com/Gen-Spider/Gen-pass

For support and documentation:
https://github.com/Gen-Spider/Gen-pass/wiki
""", style="cyan")
            
            panel = Panel(
                about_text,
                title="[bold green]About Gen-Pass[/bold green]",
                border_style="green"
            )
            
            self.console.print(panel)
        else:
            print("""
Gen-Pass Enterprise Password Generator v3.2.1
Developed by Gen-Spider Security Systems

Features: Cryptographically secure generation, advanced analysis,
batch processing, enterprise policies, and more.

Repository: https://github.com/Gen-Spider/Gen-pass
License: MIT License
""")
    
    # Additional placeholder methods for policy management
    def _create_policy_interactive(self, args):
        """Create policy interactively."""
        self._print_info("Interactive policy creation - Feature coming soon!")
        return 0
    
    def _list_policies(self):
        """List available policies."""
        self._print_info("Policy listing - Feature coming soon!")
        return 0
    
    def _export_policy(self, args):
        """Export policy to file."""
        self._print_info("Policy export - Feature coming soon!")
        return 0
    
    def _import_policy(self, args):
        """Import policy from file."""
        self._print_info("Policy import - Feature coming soon!")
        return 0
    
    def _validate_policy(self, args):
        """Validate policy file."""
        self._print_info("Policy validation - Feature coming soon!")
        return 0


def main():
    """Main entry point for the CLI application."""
    cli = PasswordGeneratorCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
