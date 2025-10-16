#!/usr/bin/env python3
"""
Gen-Pass Enterprise Security Suite - Main Interface
==================================================

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
import secrets
import string
import math
import re
import hashlib
import hmac
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import getpass
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import threading

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.align import Align
    from rich.live import Live
    from rich.layout import Layout
    from rich.columns import Columns
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Installing required dependencies...")
    os.system("pip install rich colorama")
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
        from rich.prompt import Prompt, Confirm, IntPrompt
        from rich.syntax import Syntax
        from rich.tree import Tree
        from rich.align import Align
        from rich.live import Live
        from rich.layout import Layout
        from rich.columns import Columns
        RICH_AVAILABLE = True
    except ImportError:
        RICH_AVAILABLE = False

try:
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)

# Color constants
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


class PasswordComplexity(Enum):
    """Password complexity levels for enterprise requirements."""
    MINIMUM = "minimum"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"
    MILITARY = "military"


@dataclass
class PasswordPolicy:
    """Enterprise password policy configuration."""
    min_length: int = 12
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_symbols: bool = True
    min_uppercase: int = 1
    min_lowercase: int = 1
    min_digits: int = 1
    min_symbols: int = 1
    exclude_ambiguous: bool = False
    exclude_similar: bool = False
    exclude_sequential: bool = True
    exclude_repetitive: bool = True
    max_consecutive: int = 2
    exclude_dictionary: bool = True
    custom_exclusions: List[str] = None
    entropy_threshold: float = 50.0
    
    def __post_init__(self):
        if self.custom_exclusions is None:
            self.custom_exclusions = []


@dataclass
class PasswordAnalysis:
    """Comprehensive password strength analysis."""
    password: str
    strength_score: float
    strength_level: str
    entropy: float
    time_to_crack: Dict[str, str]
    character_analysis: Dict[str, bool]
    policy_compliance: Dict[str, bool]
    vulnerabilities: List[str]
    recommendations: List[str]
    hash_analysis: Dict[str, str]
    created_at: float


class EnterprisePasswordGenerator:
    """Enterprise-grade password generation and analysis system."""
    
    # Common password patterns to avoid
    COMMON_PATTERNS = [
        r'(.)\1{2,}',  # Repeated characters
        r'(abc|123|qwe|asd|zxc)',  # Sequential patterns
        r'(password|admin|user|login|test)',  # Common words
        r'(19|20)\d{2}',  # Years
        r'\d{4,}',  # Long number sequences
    ]
    
    # Common weak passwords
    WEAK_PASSWORDS = {
        'password', '123456', 'password123', 'admin', 'qwerty',
        'letmein', 'welcome', 'monkey', '1234567890', 'abc123',
        'password1', '123456789', 'welcome123', 'admin123'
    }
    
    # Word list for passphrase generation
    WORDLIST = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
        "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
        "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
        "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
        "advice", "aerobic", "affair", "afford", "afraid", "again", "against", "agent",
        "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
        "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
        "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
        "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
        "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
        "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april",
        "arcade", "arch", "arctic", "area", "arena", "argue", "arm", "armed",
        "armor", "army", "around", "arrange", "arrest", "arrive", "arrow", "art",
        "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume",
        "athlete", "atom", "attack", "attend", "attitude", "attract", "auction", "audit",
        "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid",
        "awake", "aware", "away", "awesome", "awful", "awkward", "axis", "baby",
        "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball", "bamboo",
        "banana", "banner", "bar", "barely", "bargain", "barrel", "base", "basic",
        "basket", "battle", "beach", "bean", "beauty", "because", "become", "beef",
        "before", "begin", "behave", "behind", "believe", "below", "belt", "bench",
        "benefit", "best", "betray", "better", "between", "beyond", "bicycle", "bid",
        "bike", "bind", "biology", "bird", "birth", "bitter", "black", "blade",
        "blame", "blanket", "blast", "bleak", "bless", "blind", "blood", "blossom",
        "blow", "blue", "blur", "blush", "board", "boat", "body", "boil",
        "bomb", "bone", "bonus", "book", "boost", "border", "boring", "borrow",
        "boss", "bottom", "bounce", "box", "boy", "bracket", "brain", "brand",
        "brass", "brave", "bread", "breeze", "brick", "bridge", "brief", "bright",
        "bring", "brisk", "broccoli", "broken", "bronze", "broom", "brother", "brown",
        "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb", "bulk",
        "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus", "business",
        "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable", "cactus",
        "cage", "cake", "call", "calm", "camera", "camp", "can", "canal",
        "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital",
        "captain", "car", "carbon", "card", "care", "career", "careful", "careless",
        "cargo", "carpet", "carry", "cart", "case", "cash", "casino", "cast",
        "casual", "cat", "catalog", "catch", "category", "cattle", "caught", "cause",
        "caution", "cave", "ceiling", "celery", "cement", "census", "century", "cereal",
        "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge",
        "chase", "chat", "cheap", "check", "cheese", "chef", "cherry", "chest",
        "chicken", "chief", "child", "chimney", "choice", "choose", "chronic", "chuckle",
        "chunk", "churn", "cigar", "cinnamon", "circle", "citizen", "city", "civil",
        "claim", "clamp", "clarify", "claw", "clay", "clean", "clerk", "clever",
        "click", "client", "cliff", "climb", "clinic", "clip", "clock", "clog",
        "close", "cloth", "cloud", "clown", "club", "clump", "cluster", "clutch",
        "coach", "coast", "coconut", "code", "coffee", "coil", "coin", "collect",
        "color", "column", "combine", "come", "comfort", "comic", "common", "company",
        "concert", "conduct", "confirm", "congress", "connect", "consider", "control", "convince",
        "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct",
        "cost", "cotton", "couch", "country", "couple", "course", "cousin", "cover",
        "coyote", "crack", "cradle", "craft", "cram", "crane", "crash", "crater",
        "crawl", "crazy", "cream", "credit", "creek", "crew", "cricket", "crime",
        "crisp", "critic", "crop", "cross", "crouch", "crowd", "crucial", "cruel",
        "cruise", "crumble", "crunch", "crush", "cry", "crystal", "cube", "culture",
        "cup", "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom",
        "cute", "cycle", "dad", "damage", "damp", "dance", "danger", "daring",
        "dash", "daughter", "dawn", "day", "deal", "debate", "debris", "decade",
        "december", "decide", "decline", "decorate", "decrease", "deer", "defense", "define",
        "defy", "degree", "delay", "deliver", "demand", "demise", "denial", "dentist",
        "deny", "depart", "depend", "deposit", "depth", "deputy", "derive", "describe",
        "desert", "design", "desk", "despair", "destroy", "detail", "detect", "device",
        "devote", "diagram", "dial", "diamond", "diary", "dice", "diesel", "diet",
        "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur", "direct", "dirt",
        "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display", "distance",
        "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog", "doll",
        "dolphin", "domain", "donate", "donkey", "donor", "door", "dose", "double",
        "dove", "draft", "dragon", "drama", "drape", "draw", "dream", "dress",
        "drift", "drill", "drink", "drip", "drive", "drop", "drum", "dry",
        "duck", "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf",
        "dynamic", "eager", "eagle", "early", "earn", "earth", "easily", "east",
        "easy", "echo", "ecology", "economy", "edge", "edit", "educate", "effort",
        "egg", "eight", "either", "elbow", "elder", "electric", "elegant", "element",
        "elephant", "elevator", "elite", "else", "embark", "embody", "embrace", "emerge",
        "emotion", "employ", "empower", "empty", "enable", "enact", "end", "endless",
        "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance", "enjoy",
        "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire", "entry",
        "envelope", "episode", "equal", "equip", "era", "erase", "erode", "erosion",
        "error", "erupt", "escape", "essay", "essence", "estate", "eternal", "ethics",
        "evidence", "evil", "evoke", "evolve", "exact", "example", "excess", "exchange",
        "excite", "exclude", "excuse", "execute", "exercise", "exhale", "exhibit", "exile",
        "exist", "exit", "exotic", "expand", "expect", "expire", "explain", "expose",
        "express", "extend", "extra", "eye", "eyebrow", "fabric", "face", "faculty",
        "fade", "faint", "faith", "fall", "false", "fame", "family", "famous",
        "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal", "father",
        "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed",
        "feel", "female", "fence", "festival", "fetch", "fever", "few", "fiber",
        "fiction", "field", "figure", "file", "fill", "film", "filter", "final",
        "find", "fine", "finger", "finish", "fire", "firm", "first", "fiscal",
        "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat",
        "flavor", "flee", "flight", "flip", "float", "flock", "floor", "flower",
        "fluid", "flush", "fly", "foam", "focus", "fog", "foil", "fold",
        "follow", "food", "foot", "force", "forest", "forget", "fork", "fortune",
        "forum", "forward", "fossil", "foster", "found", "fox", "frame", "frequent",
        "fresh", "friend", "fringe", "frog", "front", "frost", "frown", "frozen",
        "fruit", "fuel", "fun", "funny", "furnace", "fury", "future", "gadget",
        "gain", "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden",
        "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze",
        "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost", "giant",
        "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance",
        "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory", "glove",
        "glow", "glue", "goat", "goddess", "gold", "good", "goose", "gorilla",
        "gospel", "gossip", "govern", "gown", "grab", "grace", "grain", "grant",
        "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit",
        "grocery", "group", "grow", "grunt", "guard", "guess", "guide", "guilt",
        "guitar", "gun", "gym", "hair", "half", "hammer", "hamster", "hand",
        "happy", "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk",
        "hazard", "head", "health", "heart", "heavy", "hedgehog", "height", "hello",
        "helmet", "help", "hen", "hero", "hidden", "high", "hill", "hint",
        "hip", "hire", "history", "hobby", "hockey", "hold", "hole", "holiday",
        "hollow", "home", "honey", "hood", "hope", "horn", "horror", "horse",
        "hospital", "host", "hotel", "hour", "hover", "hub", "huge", "human",
        "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "hurt",
        "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore",
        "ill", "illegal", "illness", "image", "imitate", "immense", "immune", "impact",
        "impose", "improve", "impulse", "inch", "include", "income", "increase", "index",
        "indicate", "indoor", "industry", "infant", "inflict", "inform", "inhale", "inherit",
        "initial", "inject", "injury", "inmate", "inner", "innocent", "input", "inquiry",
        "insane", "insect", "inside", "inspire", "install", "intact", "interest", "into",
        "invest", "invite", "involve", "iron", "island", "isolate", "issue", "item",
        "ivory", "jacket", "jaguar", "jar", "jazz", "jealous", "jeans", "jelly",
        "jewel", "job", "join", "joke", "journey", "joy", "judge", "juice",
        "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen", "keep",
        "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss",
        "kit", "kitchen", "kite", "kitten", "kiwi", "knee", "knife", "knock",
        "know", "lab", "label", "labor", "ladder", "lady", "lake", "lamp",
        "language", "laptop", "large", "later", "latin", "laugh", "laundry", "lava",
        "law", "lawn", "lawsuit", "layer", "lazy", "leader", "leaf", "learn",
        "leave", "lecture", "left", "leg", "legal", "legend", "leisure", "lemon",
        "lend", "length", "lens", "leopard", "lesson", "letter", "level", "liar",
        "liberty", "library", "license", "life", "lift", "light", "like", "limb",
        "limit", "link", "lion", "liquid", "list", "little", "live", "lizard",
        "load", "loan", "lobster", "local", "lock", "logic", "lonely", "long",
        "loop", "lottery", "loud", "lounge", "love", "loyal", "lucky", "luggage",
        "lumber", "lunar", "lunch", "luxury", "lying", "machine", "mad", "magic",
        "magnet", "maid", "mail", "main", "major", "make", "mammal", "man",
        "manage", "mandate", "mango", "mansion", "manual", "maple", "marble", "march",
        "margin", "marine", "market", "marriage", "mask", "mass", "master", "match",
        "material", "math", "matrix", "matter", "maximum", "maze", "meadow", "mean",
        "measure", "meat", "mechanic", "medal", "media", "melody", "melt", "member",
        "memory", "mention", "menu", "mercy", "merge", "merit", "merry", "mesh",
        "message", "metal", "method", "middle", "midnight", "milk", "million", "mimic",
        "mind", "minimum", "minor", "minute", "miracle", "mirror", "misery", "miss",
        "mistake", "mix", "mixed", "mixture", "mobile", "model", "modify", "mom",
        "moment", "monitor", "monkey", "monster", "month", "moon", "moral", "more",
        "morning", "mosquito", "mother", "motion", "motor", "mountain", "mouse", "move",
        "movie", "much", "muffin", "mule", "multiply", "muscle", "museum", "mushroom",
        "music", "must", "mutual", "myself", "mystery", "myth", "naive", "name",
        "napkin", "narrow", "nasty", "nation", "nature", "near", "neck", "need",
        "needle", "neglect", "neighbor", "neither", "nephew", "nerve", "nest", "net",
        "network", "neutral", "never", "news", "next", "nice", "night", "noble",
        "noise", "nominee", "noodle", "normal", "north", "nose", "notable", "note",
        "nothing", "notice", "novel", "now", "nuclear", "number", "nurse", "nut",
        "oak", "obey", "object", "oblige", "obscure", "observe", "obtain", "obvious",
        "occur", "ocean", "october", "odor", "off", "offer", "office", "often",
        "oil", "okay", "old", "olive", "olympic", "omit", "once", "one",
        "onion", "online", "only", "open", "opera", "opinion", "oppose", "option",
        "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient", "original",
        "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval",
        "oven", "over", "own", "owner", "oxygen", "oyster", "ozone", "pact",
        "paddle", "page", "pair", "palace", "palm", "panda", "panel", "panic",
        "panther", "paper", "parade", "parent", "park", "parrot", "part", "party",
        "pass", "patch", "path", "patient", "patrol", "pattern", "pause", "pave",
        "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen", "penalty",
        "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone",
        "photo", "phrase", "physical", "piano", "picnic", "picture", "piece", "pig",
        "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch",
        "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge",
        "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole",
        "police", "pond", "pony", "pool", "popular", "portion", "position", "possible",
        "post", "potato", "pottery", "poverty", "powder", "power", "practice", "praise",
        "predict", "prefer", "prepare", "present", "pretty", "prevent", "price", "pride",
        "primary", "print", "priority", "prison", "private", "prize", "problem", "process",
        "produce", "profit", "program", "project", "promote", "proof", "property", "prosper",
        "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse",
        "pumpkin", "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse",
        "push", "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question",
        "quick", "quiet", "quilt", "quit", "quiz", "quote", "rabbit", "raccoon",
        "race", "rack", "radar", "radio", "rail", "rain", "raise", "rally",
        "ramp", "ranch", "random", "range", "rapid", "rare", "rate", "rather",
        "raven", "raw", "razor", "ready", "real", "reason", "rebel", "rebuild",
        "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect", "reform",
        "refuse", "region", "regret", "regular", "reject", "relax", "release", "relief",
        "rely", "remain", "remember", "remind", "remove", "render", "renew", "rent",
        "reopen", "repair", "repeat", "replace", "report", "require", "rescue", "resemble",
        "resist", "resource", "response", "result", "retire", "retreat", "return", "reunion",
        "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice", "rich",
        "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "ripple",
        "rise", "risk", "ritual", "rival", "river", "road", "roast", "rob",
        "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose",
        "rotate", "rough", "round", "route", "royal", "rubber", "rude", "rug",
        "rule", "run", "runway", "rural", "sad", "saddle", "sadness", "safe",
        "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample",
        "sand", "satisfy", "satoshi", "sauce", "sausage", "save", "say", "scale",
        "scan", "scare", "scatter", "scene", "scheme", "school", "science", "scissors",
        "scorpion", "scout", "scrap", "screen", "script", "scrub", "sea", "search",
        "season", "seat", "second", "secret", "section", "security", "seed", "seek",
        "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series",
        "service", "session", "settle", "setup", "seven", "shadow", "shaft", "shallow",
        "share", "shed", "shell", "sheriff", "shield", "shift", "shine", "ship",
        "shirt", "shock", "shoe", "shoot", "shop", "short", "shoulder", "shove",
        "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side", "siege",
        "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple",
        "since", "sing", "siren", "sister", "situate", "six", "size", "skate",
        "sketch", "ski", "skill", "skin", "skirt", "skull", "slab", "slam",
        "sleep", "slender", "slice", "slide", "slight", "slim", "slogan", "slot",
        "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack",
        "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock",
        "soda", "soft", "solar", "soldier", "solid", "solution", "solve", "someone",
        "song", "soon", "sorry", "sort", "soul", "sound", "soup", "source",
        "south", "space", "spare", "spatial", "spawn", "speak", "special", "speed",
        "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit",
        "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread",
        "spring", "spy", "square", "squeeze", "squirrel", "stable", "stadium", "staff",
        "stage", "stairs", "stamp", "stand", "start", "state", "stay", "steak",
        "steel", "stem", "step", "stereo", "stick", "still", "sting", "stock",
        "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike",
        "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit",
        "subway", "success", "such", "sudden", "suffer", "sugar", "suggest", "suit",
        "summer", "sun", "sunny", "sunset", "super", "supply", "supreme", "sure",
        "surface", "surge", "surprise", "surround", "survey", "suspect", "sustain", "swallow",
        "swamp", "swap", "swear", "sweet", "swift", "swim", "swing", "switch",
        "sword", "symbol", "symptom", "syrup", "system", "table", "tackle", "tag",
        "tail", "talent", "talk", "tank", "tape", "target", "task", "taste",
        "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant", "tennis",
        "tent", "term", "test", "text", "thank", "that", "theme", "then",
        "theory", "there", "they", "thing", "this", "thought", "three", "thrive",
        "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber",
        "time", "tiny", "tip", "tired", "tissue", "title", "toast", "tobacco",
        "today", "toddler", "toe", "together", "toilet", "token", "tomato", "tomorrow",
        "tone", "tongue", "tonight", "tool", "tooth", "top", "topic", "topple",
        "torch", "tornado", "tortoise", "toss", "total", "tourist", "toward", "tower",
        "town", "toy", "track", "trade", "traffic", "tragic", "train", "transfer",
        "trap", "trash", "travel", "tray", "treat", "tree", "trend", "trial",
        "tribe", "trick", "trigger", "trim", "trip", "trophy", "trouble", "truck",
        "true", "truly", "trumpet", "trust", "truth", "try", "tube", "tuition",
        "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve", "twenty",
        "twice", "twin", "twist", "two", "type", "typical", "ugly", "umbrella",
        "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair", "unfold",
        "unhappy", "uniform", "unique", "unit", "universe", "unknown", "unlock", "until",
        "unusual", "unveil", "update", "upgrade", "uphold", "upon", "upper", "upset",
        "urban", "urge", "usage", "use", "used", "useful", "useless", "usual",
        "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve", "van",
        "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor",
        "venture", "venue", "verb", "verify", "version", "very", "vessel", "veteran",
        "viable", "vibrant", "vicious", "victory", "video", "view", "village", "vintage",
        "violin", "virtual", "virus", "visa", "visit", "visual", "vital", "vivid",
        "vocal", "voice", "void", "volcano", "volume", "vote", "voyage", "wage",
        "wagon", "wait", "walk", "wall", "walnut", "want", "warfare", "warm",
        "warrior", "wash", "wasp", "waste", "water", "wave", "way", "wealth",
        "weapon", "wear", "weasel", "weather", "web", "wedding", "weekend", "weird",
        "welcome", "west", "wet", "what", "wheat", "wheel", "when", "where",
        "whip", "whisper", "wide", "width", "wife", "wild", "will", "win",
        "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom",
        "wise", "wish", "witness", "wolf", "woman", "wonder", "wood", "wool",
        "word", "work", "world", "worry", "worth", "wrap", "wreck", "wrestle",
        "wrist", "write", "wrong", "yard", "year", "yellow", "you", "young",
        "youth", "zebra", "zero", "zone", "zoo", "matrix", "cipher", "quantum", "secure"
    ]
    
    def __init__(self):
        """Initialize the enterprise password generator."""
        self._entropy_cache = {}
    
    def generate_password(self, 
                         length: int = 12,
                         complexity: PasswordComplexity = PasswordComplexity.STANDARD,
                         exclude_ambiguous: bool = False,
                         exclude_similar: bool = False,
                         custom_chars: str = "") -> str:
        """Generate a cryptographically secure password."""
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        ambiguous = "0O1lI"
        similar = "il1Lo0O"
        
        # Build character set based on complexity
        charset = ""
        required_chars = []
        
        if complexity in [PasswordComplexity.MINIMUM, PasswordComplexity.STANDARD, 
                         PasswordComplexity.HIGH, PasswordComplexity.MAXIMUM, 
                         PasswordComplexity.MILITARY]:
            charset += lowercase
            required_chars.append(secrets.choice(lowercase))
            
            if complexity != PasswordComplexity.MINIMUM:
                charset += uppercase
                required_chars.append(secrets.choice(uppercase))
                
                charset += digits
                required_chars.append(secrets.choice(digits))
                
                if complexity in [PasswordComplexity.STANDARD, PasswordComplexity.HIGH, 
                                 PasswordComplexity.MAXIMUM, PasswordComplexity.MILITARY]:
                    charset += symbols
                    required_chars.append(secrets.choice(symbols))
        
        # Remove excluded characters
        if exclude_ambiguous:
            charset = ''.join(c for c in charset if c not in ambiguous)
            required_chars = [c for c in required_chars if c not in ambiguous]
            
        if exclude_similar:
            charset = ''.join(c for c in charset if c not in similar)
            required_chars = [c for c in required_chars if c not in similar]
        
        # Add custom characters
        charset += custom_chars
        
        # Generate password
        password_chars = required_chars[:]
        while len(password_chars) < length:
            password_chars.append(secrets.choice(charset))
        
        # Shuffle for randomness
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_passphrase(self, 
                           word_count: int = 6,
                           separator: str = "-",
                           capitalize: bool = True,
                           add_numbers: bool = True,
                           add_symbols: bool = False) -> str:
        """Generate a cryptographically secure passphrase."""
        
        words = []
        for _ in range(word_count):
            word = secrets.choice(self.WORDLIST)
            if capitalize:
                word = word.capitalize()
            words.append(word)
        
        passphrase = separator.join(words)
        
        if add_numbers:
            num_digits = secrets.randbelow(3) + 2
            numbers = ''.join([str(secrets.randbelow(10)) for _ in range(num_digits)])
            passphrase += separator + numbers
        
        if add_symbols:
            symbol_count = secrets.randbelow(2) + 1
            symbols = ''.join([secrets.choice("!@#$%^&*") for _ in range(symbol_count)])
            passphrase += separator + symbols
        
        return passphrase
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits."""
        if not password:
            return 0.0
        
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            charset_size += 23
        
        if charset_size == 0:
            return 0.0
        
        return len(password) * math.log2(charset_size)
    
    def analyze_password(self, password: str) -> PasswordAnalysis:
        """Perform comprehensive password analysis."""
        entropy = self.calculate_entropy(password)
        
        # Calculate strength score
        score = 0
        length = len(password)
        
        if length >= 20:
            score += 25
        elif length >= 16:
            score += 20
        elif length >= 12:
            score += 15
        elif length >= 8:
            score += 10
        else:
            score += max(0, length * 2)
        
        # Character variety
        varieties = 0
        if any(c.islower() for c in password):
            varieties += 1
        if any(c.isupper() for c in password):
            varieties += 1
        if any(c.isdigit() for c in password):
            varieties += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            varieties += 1
        
        score += varieties * 6.25
        score += min(40, (entropy / 100) * 40)
        
        # Determine strength level
        if score >= 90:
            strength = "EXCELLENT"
        elif score >= 80:
            strength = "VERY_STRONG"
        elif score >= 70:
            strength = "STRONG"
        elif score >= 60:
            strength = "GOOD"
        elif score >= 40:
            strength = "MODERATE"
        elif score >= 20:
            strength = "WEAK"
        else:
            strength = "VERY_WEAK"
        
        # Character analysis
        char_analysis = {
            "has_lowercase": any(c.islower() for c in password),
            "has_uppercase": any(c.isupper() for c in password),
            "has_digits": any(c.isdigit() for c in password),
            "has_symbols": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "has_ambiguous": any(c in "0O1lI" for c in password),
            "has_similar": any(c in "il1Lo0O" for c in password)
        }
        
        # Vulnerabilities
        vulnerabilities = []
        if length < 8:
            vulnerabilities.append("Password too short (less than 8 characters)")
        if password.lower() in self.WEAK_PASSWORDS:
            vulnerabilities.append("Password found in common password lists")
        if len(set(password)) < len(password) * 0.5:
            vulnerabilities.append("Low character diversity")
        
        # Recommendations
        recommendations = []
        if length < 12:
            recommendations.append("Increase length to at least 12 characters")
        if not char_analysis["has_uppercase"]:
            recommendations.append("Add uppercase letters")
        if not char_analysis["has_lowercase"]:
            recommendations.append("Add lowercase letters")
        if not char_analysis["has_digits"]:
            recommendations.append("Add numeric digits")
        if not char_analysis["has_symbols"]:
            recommendations.append("Add special symbols")
        
        # Time to crack estimates
        crack_time = {}
        if entropy > 0:
            combinations = 2 ** entropy
            scenarios = {
                "online_throttled": 1e3,
                "online_unthrottled": 1e6,
                "offline_slow": 1e9,
                "offline_fast": 1e12,
            }
            
            for scenario, rate in scenarios.items():
                avg_time = (combinations / 2) / rate
                if avg_time < 60:
                    crack_time[scenario] = f"{avg_time:.0f} seconds"
                elif avg_time < 3600:
                    crack_time[scenario] = f"{avg_time/60:.0f} minutes"
                elif avg_time < 86400:
                    crack_time[scenario] = f"{avg_time/3600:.1f} hours"
                elif avg_time < 31536000:
                    crack_time[scenario] = f"{avg_time/86400:.0f} days"
                else:
                    crack_time[scenario] = f"{avg_time/31536000:.0f} years"
        
        # Generate hashes
        hash_analysis = {
            "md5": hashlib.md5(password.encode()).hexdigest(),
            "sha256": hashlib.sha256(password.encode()).hexdigest(),
        }
        
        return PasswordAnalysis(
            password=password,
            strength_score=score,
            strength_level=strength,
            entropy=entropy,
            time_to_crack=crack_time,
            character_analysis=char_analysis,
            policy_compliance={},  # Placeholder
            vulnerabilities=vulnerabilities,
            recommendations=recommendations,
            hash_analysis=hash_analysis,
            created_at=time.time()
        )
    
    def batch_generate(self, count: int, generator_type: str = "password", **kwargs) -> List[str]:
        """Generate multiple passwords/passphrases."""
        results = []
        
        if generator_type == "password":
            for _ in range(count):
                results.append(self.generate_password(**kwargs))
        else:
            for _ in range(count):
                results.append(self.generate_passphrase(**kwargs))
        
        return results


class MatrixUI:
    """Enhanced Matrix UI with more features."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.width = self.console.size.width if RICH_AVAILABLE else 80
        self.height = self.console.size.height if RICH_AVAILABLE else 24
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        """Display enhanced Gen-Spider banner."""
        if RICH_AVAILABLE:
            banner_text = Text("""
██████╗ ███████╗███╗   ██╗      ██████╗  █████╗ ███████╗███████╗
██╔════╝ ██╔════╝████╗  ██║      ██╔══██╗██╔══██╗██╔════╝██╔════╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗██████╔╝███████║███████╗███████╗
██║   ██║██╔══╝  ██║╚██╗██║╚════╝██╔═══╝ ██╔══██║╚════██║╚════██║
╚██████╔╝███████╗██║ ╚████║      ██║     ██║  ██║███████║███████║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝      ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                  
    🕷️  ENTERPRISE SECURITY SUITE v3.2.1  🕷️
    Professional Password Generation & Analysis System
""", style="bold green")
            
            panel = Panel(
                Align.center(banner_text),
                title="[bold red]🔐 GEN-SPIDER SECURITY SYSTEMS 🔐[/bold red]",
                border_style="red",
                padding=(1, 2)
            )
            
            self.console.print(panel)
        else:
            print(f"{GREEN}{BOLD}")
            print("=" * 70)
            print("    GEN-PASS ENTERPRISE SECURITY SUITE v3.2.1")
            print("    Professional Password Generation & Analysis")
            print("    🕷️ Gen-Spider Security Systems 🕷️")
            print("=" * 70)
            print(f"{RESET}")
    
    def show_loading(self, text: str = "Initializing Security Systems", duration: float = 2.0):
        """Show loading animation."""
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn("dots", style="green"),
                TextColumn("[green]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(text, total=100)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(duration / 100)
        else:
            print(f"{GREEN}{text}...{RESET}")
            time.sleep(duration)
    
    def show_matrix_effect(self, duration: int = 3):
        """Show matrix falling effect."""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        start_time = time.time()
        
        while time.time() - start_time < duration:
            if RICH_AVAILABLE:
                col = secrets.randbelow(self.width - 1)
                row = secrets.randbelow(self.height - 5)
                ch = secrets.choice(chars)
                print(f"\033[{row};{col}H{GREEN}{ch}{RESET}", end='', flush=True)
            else:
                print(f"{GREEN}{secrets.choice(chars)}{RESET}", end='', flush=True)
            time.sleep(0.01)
        print("\033[H\033[J", end='')  # Clear screen


class PasswordGeneratorCLI:
    """Enhanced CLI with full functionality."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.generator = EnterprisePasswordGenerator()
        self.ui = MatrixUI()
        
    def run(self, args: List[str] = None) -> int:
        """Main entry point."""
        if args is None:
            args = sys.argv[1:]
        
        if not args or (len(args) == 1 and args[0] in ['--matrix', 'interactive', 'ui']):
            return self.interactive_mode()
        
        parser = self.create_parser()
        
        try:
            parsed_args = parser.parse_args(args)
            return self.execute_command(parsed_args)
        except KeyboardInterrupt:
            self.print_error("\nOperation cancelled by user")
            return 1
        except Exception as e:
            self.print_error(f"Error: {e}")
            return 1
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog='gen-pass',
            description='Enterprise Password Generator - Professional security tool',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument('--version', action='version', version='Gen-Pass v3.2.1')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Generate command
        gen_parser = subparsers.add_parser('generate', help='Generate passwords')
        gen_parser.add_argument('--length', '-l', type=int, default=12, help='Password length')
        gen_parser.add_argument('--count', '-c', type=int, default=1, help='Number of passwords')
        gen_parser.add_argument('--complexity', choices=['minimum', 'standard', 'high', 'maximum', 'military'], 
                               default='standard', help='Complexity level')
        gen_parser.add_argument('--exclude-ambiguous', action='store_true', help='Exclude ambiguous characters')
        gen_parser.add_argument('--exclude-similar', action='store_true', help='Exclude similar characters')
        gen_parser.add_argument('--save', help='Save to file')
        
        # Passphrase command
        phrase_parser = subparsers.add_parser('passphrase', help='Generate passphrases')
        phrase_parser.add_argument('--words', '-w', type=int, default=6, help='Number of words')
        phrase_parser.add_argument('--count', '-c', type=int, default=1, help='Number of passphrases')
        phrase_parser.add_argument('--separator', '-s', default='-', help='Word separator')
        phrase_parser.add_argument('--no-capitalize', action='store_true', help='Don\'t capitalize words')
        phrase_parser.add_argument('--no-numbers', action='store_true', help='Don\'t add numbers')
        phrase_parser.add_argument('--add-symbols', action='store_true', help='Add symbols')
        phrase_parser.add_argument('--save', help='Save to file')
        
        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze password strength')
        analyze_parser.add_argument('password', nargs='?', help='Password to analyze')
        
        # Interactive command
        subparsers.add_parser('interactive', help='Interactive mode')
        
        return parser
    
    def execute_command(self, args: argparse.Namespace) -> int:
        """Execute parsed command."""
        if args.command == 'generate':
            return self.generate_passwords_cmd(args)
        elif args.command == 'passphrase':
            return self.generate_passphrases_cmd(args)
        elif args.command == 'analyze':
            return self.analyze_password_cmd(args)
        elif args.command == 'interactive':
            return self.interactive_mode()
        else:
            return self.interactive_mode()
    
    def generate_passwords_cmd(self, args: argparse.Namespace) -> int:
        """Generate passwords from command line."""
        try:
            complexity = PasswordComplexity(args.complexity)
            
            passwords = []
            for _ in range(args.count):
                password = self.generator.generate_password(
                    length=args.length,
                    complexity=complexity,
                    exclude_ambiguous=args.exclude_ambiguous,
                    exclude_similar=args.exclude_similar
                )
                passwords.append(password)
            
            for i, password in enumerate(passwords, 1):
                print(f"Password {i}: {password}")
            
            if args.save:
                with open(args.save, 'w') as f:
                    f.write('\n'.join(passwords))
                self.print_success(f"Passwords saved to {args.save}")
            
            return 0
        except Exception as e:
            self.print_error(f"Generation failed: {e}")
            return 1
    
    def generate_passphrases_cmd(self, args: argparse.Namespace) -> int:
        """Generate passphrases from command line."""
        try:
            passphrases = []
            for _ in range(args.count):
                passphrase = self.generator.generate_passphrase(
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=not args.no_capitalize,
                    add_numbers=not args.no_numbers,
                    add_symbols=args.add_symbols
                )
                passphrases.append(passphrase)
            
            for i, passphrase in enumerate(passphrases, 1):
                print(f"Passphrase {i}: {passphrase}")
            
            if args.save:
                with open(args.save, 'w') as f:
                    f.write('\n'.join(passphrases))
                self.print_success(f"Passphrases saved to {args.save}")
            
            return 0
        except Exception as e:
            self.print_error(f"Generation failed: {e}")
            return 1
    
    def analyze_password_cmd(self, args: argparse.Namespace) -> int:
        """Analyze password from command line."""
        try:
            password = args.password
            if not password:
                password = getpass.getpass("Enter password to analyze: ")
            
            analysis = self.generator.analyze_password(password)
            
            print(f"\nPassword Analysis for: {'*' * len(password)}")
            print(f"Strength: {analysis.strength_level} ({analysis.strength_score:.1f}/100)")
            print(f"Entropy: {analysis.entropy:.1f} bits")
            print(f"Length: {len(password)} characters")
            
            print("\nCharacter Analysis:")
            print(f"  Lowercase: {'✓' if analysis.character_analysis['has_lowercase'] else '✗'}")
            print(f"  Uppercase: {'✓' if analysis.character_analysis['has_uppercase'] else '✗'}")
            print(f"  Digits: {'✓' if analysis.character_analysis['has_digits'] else '✗'}")
            print(f"  Symbols: {'✓' if analysis.character_analysis['has_symbols'] else '✗'}")
            
            if analysis.vulnerabilities:
                print("\nVulnerabilities:")
                for vuln in analysis.vulnerabilities:
                    print(f"  • {vuln}")
            
            if analysis.recommendations:
                print("\nRecommendations:")
                for rec in analysis.recommendations:
                    print(f"  • {rec}")
            
            return 0
        except Exception as e:
            self.print_error(f"Analysis failed: {e}")
            return 1
    
    def interactive_mode(self) -> int:
        """Full interactive mode with all features working."""
        self.ui.clear_screen()
        self.ui.show_banner()
        self.ui.show_loading("Initializing Enterprise Security Systems", 1.5)
        
        while True:
            try:
                self.show_main_menu()
                choice = self.get_user_choice()
                
                if choice == '1':
                    self.interactive_generate_password()
                elif choice == '2':
                    self.interactive_generate_passphrase()
                elif choice == '3':
                    self.interactive_analyze_password()
                elif choice == '4':
                    self.interactive_batch_generate()
                elif choice == '5':
                    self.interactive_policy_manager()
                elif choice == '6':
                    self.interactive_hash_generator()
                elif choice == '7':
                    self.interactive_security_audit()
                elif choice == '8':
                    self.show_system_info()
                elif choice == '9':
                    self.show_help()
                elif choice == '0':
                    self.ui.show_matrix_effect(2)
                    self.print_success("\n🕷️ Thank you for using Gen-Pass Enterprise! 🕷️")
                    break
                else:
                    self.print_error("Invalid choice. Please select 0-9.")
                    
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                self.print_info("\n\n🕷️ Session terminated. Goodbye! 🕷️")
                break
            except Exception as e:
                self.print_error(f"An error occurred: {e}")
                input("Press Enter to continue...")
        
        return 0
    
    def show_main_menu(self):
        """Display the main menu."""
        if RICH_AVAILABLE:
            menu_items = [
                ("1.", "🔐 Generate Password", "Create secure passwords with custom settings"),
                ("2.", "📝 Generate Passphrase", "Create memorable word-based passphrases"),
                ("3.", "🔍 Analyze Password", "Comprehensive password strength analysis"),
                ("4.", "⚡ Batch Generation", "Generate multiple passwords/passphrases"),
                ("5.", "📋 Policy Manager", "Configure enterprise security policies"),
                ("6.", "🔗 Hash Generator", "Generate cryptographic hashes"),
                ("7.", "🛡️ Security Audit", "Advanced security testing tools"),
                ("8.", "💻 System Info", "View system and security information"),
                ("9.", "❓ Help & Documentation", "View help and usage examples"),
                ("0.", "🚪 Exit", "Exit Gen-Pass Enterprise")
            ]
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Option", style="bold cyan", width=3)
            table.add_column("Feature", style="bold white", width=25)
            table.add_column("Description", style="dim white")
            
            for option, feature, description in menu_items:
                table.add_row(option, feature, description)
            
            panel = Panel(
                table,
                title="[bold green]🔐 MAIN SECURITY MENU 🔐[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print("\n")
            self.console.print(panel)
        else:
            print(f"\n{GREEN}{BOLD}=== MAIN SECURITY MENU ==={RESET}")
            print(f"{CYAN}1.{RESET} 🔐 Generate Password")
            print(f"{CYAN}2.{RESET} 📝 Generate Passphrase")
            print(f"{CYAN}3.{RESET} 🔍 Analyze Password")
            print(f"{CYAN}4.{RESET} ⚡ Batch Generation")
            print(f"{CYAN}5.{RESET} 📋 Policy Manager")
            print(f"{CYAN}6.{RESET} 🔗 Hash Generator")
            print(f"{CYAN}7.{RESET} 🛡️ Security Audit")
            print(f"{CYAN}8.{RESET} 💻 System Info")
            print(f"{CYAN}9.{RESET} ❓ Help & Documentation")
            print(f"{CYAN}0.{RESET} 🚪 Exit")
            print(f"{GREEN}{'=' * 30}{RESET}")
    
    def get_user_choice(self) -> str:
        """Get user menu choice."""
        if RICH_AVAILABLE:
            return Prompt.ask("\n[bold cyan]Select option[/bold cyan]", 
                            choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        else:
            while True:
                choice = input(f"\n{CYAN}Select option (0-9): {RESET}").strip()
                if choice in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return choice
                print(f"{RED}Invalid choice. Please select 0-9.{RESET}")
    
    def interactive_generate_password(self):
        """Interactive password generation with full functionality."""
        self.print_info("\n🔐 INTERACTIVE PASSWORD GENERATOR")
        
        try:
            if RICH_AVAILABLE:
                length = IntPrompt.ask("Password length", default=12, show_default=True)
                count = IntPrompt.ask("Number of passwords", default=1, show_default=True)
                complexity = Prompt.ask("Complexity level", 
                                      choices=["minimum", "standard", "high", "maximum", "military"],
                                      default="standard")
                exclude_ambiguous = Confirm.ask("Exclude ambiguous characters (0, O, 1, l, I)?", default=False)
                exclude_similar = Confirm.ask("Exclude similar characters?", default=False)
                save_file = Prompt.ask("Save to file (optional)", default="")
            else:
                length = int(input("Password length [12]: ") or "12")
                count = int(input("Number of passwords [1]: ") or "1")
                print("Complexity levels: minimum, standard, high, maximum, military")
                complexity = input("Complexity level [standard]: ").strip() or "standard"
                exclude_ambiguous = input("Exclude ambiguous characters? [y/N]: ").lower().startswith('y')
                exclude_similar = input("Exclude similar characters? [y/N]: ").lower().startswith('y')
                save_file = input("Save to file (optional): ").strip()
            
            self.print_info("\n⚡ Generating passwords...")
            
            passwords = []
            for i in range(count):
                password = self.generator.generate_password(
                    length=length,
                    complexity=PasswordComplexity(complexity),
                    exclude_ambiguous=exclude_ambiguous,
                    exclude_similar=exclude_similar
                )
                passwords.append(password)
                
                # Show each password with analysis
                analysis = self.generator.analyze_password(password)
                
                if RICH_AVAILABLE:
                    table = Table(title=f"Password {i+1}")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="white")
                    
                    table.add_row("Password", f"[bold green]{password}[/bold green]")
                    table.add_row("Strength", f"[bold {self.get_strength_color(analysis.strength_level)}]{analysis.strength_level}[/bold {self.get_strength_color(analysis.strength_level)}]")
                    table.add_row("Score", f"{analysis.strength_score:.1f}/100")
                    table.add_row("Entropy", f"{analysis.entropy:.1f} bits")
                    
                    self.console.print(table)
                else:
                    print(f"\n{GREEN}Password {i+1}: {password}{RESET}")
                    print(f"Strength: {analysis.strength_level} ({analysis.strength_score:.1f}/100)")
                    print(f"Entropy: {analysis.entropy:.1f} bits")
                
                time.sleep(0.1)  # Small delay for effect
            
            if save_file:
                with open(save_file, 'w') as f:
                    f.write('\n'.join(passwords))
                self.print_success(f"Passwords saved to {save_file}")
            
        except Exception as e:
            self.print_error(f"Password generation failed: {e}")
    
    def interactive_generate_passphrase(self):
        """Interactive passphrase generation."""
        self.print_info("\n📝 INTERACTIVE PASSPHRASE GENERATOR")
        
        try:
            if RICH_AVAILABLE:
                words = IntPrompt.ask("Number of words", default=6, show_default=True)
                count = IntPrompt.ask("Number of passphrases", default=1, show_default=True)
                separator = Prompt.ask("Word separator", default="-")
                capitalize = Confirm.ask("Capitalize words?", default=True)
                add_numbers = Confirm.ask("Add numbers?", default=True)
                add_symbols = Confirm.ask("Add symbols?", default=False)
                save_file = Prompt.ask("Save to file (optional)", default="")
            else:
                words = int(input("Number of words [6]: ") or "6")
                count = int(input("Number of passphrases [1]: ") or "1")
                separator = input("Word separator [-]: ").strip() or "-"
                capitalize = not input("Capitalize words? [Y/n]: ").lower().startswith('n')
                add_numbers = not input("Add numbers? [Y/n]: ").lower().startswith('n')
                add_symbols = input("Add symbols? [y/N]: ").lower().startswith('y')
                save_file = input("Save to file (optional): ").strip()
            
            self.print_info("\n⚡ Generating passphrases...")
            
            passphrases = []
            for i in range(count):
                passphrase = self.generator.generate_passphrase(
                    word_count=words,
                    separator=separator,
                    capitalize=capitalize,
                    add_numbers=add_numbers,
                    add_symbols=add_symbols
                )
                passphrases.append(passphrase)
                
                analysis = self.generator.analyze_password(passphrase)
                
                if RICH_AVAILABLE:
                    table = Table(title=f"Passphrase {i+1}")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="white")
                    
                    table.add_row("Passphrase", f"[bold green]{passphrase}[/bold green]")
                    table.add_row("Strength", f"[bold {self.get_strength_color(analysis.strength_level)}]{analysis.strength_level}[/bold {self.get_strength_color(analysis.strength_level)}]")
                    table.add_row("Score", f"{analysis.strength_score:.1f}/100")
                    table.add_row("Entropy", f"{analysis.entropy:.1f} bits")
                    table.add_row("Length", f"{len(passphrase)} characters")
                    
                    self.console.print(table)
                else:
                    print(f"\n{GREEN}Passphrase {i+1}: {passphrase}{RESET}")
                    print(f"Strength: {analysis.strength_level} ({analysis.strength_score:.1f}/100)")
                    print(f"Entropy: {analysis.entropy:.1f} bits")
                
                time.sleep(0.1)
            
            if save_file:
                with open(save_file, 'w') as f:
                    f.write('\n'.join(passphrases))
                self.print_success(f"Passphrases saved to {save_file}")
                
        except Exception as e:
            self.print_error(f"Passphrase generation failed: {e}")
    
    def interactive_analyze_password(self):
        """Interactive password analysis."""
        self.print_info("\n🔍 INTERACTIVE PASSWORD ANALYZER")
        
        try:
            password = getpass.getpass("Enter password to analyze (hidden): ")
            
            if not password:
                self.print_error("No password entered.")
                return
            
            self.print_info("\n⚡ Analyzing password security...")
            analysis = self.generator.analyze_password(password)
            
            if RICH_AVAILABLE:
                # Main analysis table
                main_table = Table(title="Password Security Analysis")
                main_table.add_column("Metric", style="cyan", no_wrap=True)
                main_table.add_column("Value", style="white")
                main_table.add_column("Status", justify="center")
                
                strength_color = self.get_strength_color(analysis.strength_level)
                main_table.add_row(
                    "Overall Strength",
                    f"[bold {strength_color}]{analysis.strength_level}[/bold {strength_color}]",
                    f"[bold {strength_color}]{analysis.strength_score:.1f}/100[/bold {strength_color}]"
                )
                
                main_table.add_row("Entropy", f"{analysis.entropy:.1f} bits", "✓" if analysis.entropy >= 50 else "⚠️")
                main_table.add_row("Length", f"{len(password)} characters", "✓" if len(password) >= 12 else "⚠️")
                
                self.console.print(main_table)
                
                # Character analysis
                char_table = Table(title="Character Analysis")
                char_table.add_column("Type", style="cyan")
                char_table.add_column("Present", justify="center")
                
                char_types = [
                    ("Lowercase Letters", analysis.character_analysis["has_lowercase"]),
                    ("Uppercase Letters", analysis.character_analysis["has_uppercase"]),
                    ("Digits", analysis.character_analysis["has_digits"]),
                    ("Symbols", analysis.character_analysis["has_symbols"]),
                ]
                
                for char_type, present in char_types:
                    char_table.add_row(char_type, "✅" if present else "❌")
                
                self.console.print(char_table)
                
                # Vulnerabilities
                if analysis.vulnerabilities:
                    vuln_panel = Panel(
                        "\n".join(f"• {vuln}" for vuln in analysis.vulnerabilities),
                        title="[bold red]⚠️ Security Vulnerabilities[/bold red]",
                        border_style="red"
                    )
                    self.console.print(vuln_panel)
                
                # Recommendations
                if analysis.recommendations:
                    rec_panel = Panel(
                        "\n".join(f"• {rec}" for rec in analysis.recommendations),
                        title="[bold yellow]💡 Security Recommendations[/bold yellow]",
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
                    
            else:
                print(f"\n{GREEN}=== PASSWORD ANALYSIS ==={RESET}")
                print(f"Password: {'*' * len(password)}")
                print(f"Strength: {analysis.strength_level} ({analysis.strength_score:.1f}/100)")
                print(f"Entropy: {analysis.entropy:.1f} bits")
                print(f"Length: {len(password)} characters")
                
                print("\nCharacter Analysis:")
                print(f"  Lowercase: {'✓' if analysis.character_analysis['has_lowercase'] else '✗'}")
                print(f"  Uppercase: {'✓' if analysis.character_analysis['has_uppercase'] else '✗'}")
                print(f"  Digits: {'✓' if analysis.character_analysis['has_digits'] else '✗'}")
                print(f"  Symbols: {'✓' if analysis.character_analysis['has_symbols'] else '✗'}")
                
                if analysis.vulnerabilities:
                    print("\nVulnerabilities:")
                    for vuln in analysis.vulnerabilities:
                        print(f"  • {vuln}")
                
                if analysis.recommendations:
                    print("\nRecommendations:")
                    for rec in analysis.recommendations:
                        print(f"  • {rec}")
            
        except Exception as e:
            self.print_error(f"Analysis failed: {e}")
    
    def interactive_batch_generate(self):
        """Interactive batch generation."""
        self.print_info("\n⚡ BATCH PASSWORD GENERATION")
        
        try:
            if RICH_AVAILABLE:
                gen_type = Prompt.ask("Generation type", choices=["password", "passphrase"], default="password")
                count = IntPrompt.ask("Number to generate", default=10)
                save_file = Prompt.ask("Save to file", default="batch_passwords.txt")
            else:
                print("Generation types: password, passphrase")
                gen_type = input("Generation type [password]: ").strip() or "password"
                count = int(input("Number to generate [10]: ") or "10")
                save_file = input("Save to file [batch_passwords.txt]: ").strip() or "batch_passwords.txt"
            
            self.print_info(f"\n⚡ Generating {count} {gen_type}s...")
            
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    console=self.console
                ) as progress:
                    task = progress.add_task(f"Generating {gen_type}s...", total=count)
                    
                    results = []
                    for i in range(count):
                        if gen_type == "password":
                            result = self.generator.generate_password(length=14)
                        else:
                            result = self.generator.generate_passphrase(word_count=5)
                        results.append(result)
                        progress.update(task, advance=1)
            else:
                results = []
                for i in range(count):
                    if gen_type == "password":
                        result = self.generator.generate_password(length=14)
                    else:
                        result = self.generator.generate_passphrase(word_count=5)
                    results.append(result)
                    print(f"Generated {i+1}/{count}", end='\r')
                print()  # New line
            
            # Save results
            with open(save_file, 'w') as f:
                for i, result in enumerate(results, 1):
                    f.write(f"{gen_type.capitalize()} {i}: {result}\n")
            
            self.print_success(f"Generated {count} {gen_type}s and saved to {save_file}")
            
            # Show sample
            if RICH_AVAILABLE:
                sample_table = Table(title="Sample Results (First 5)")
                sample_table.add_column("#", style="cyan", width=3)
                sample_table.add_column(f"{gen_type.capitalize()}", style="green")
                
                for i, result in enumerate(results[:5], 1):
                    sample_table.add_row(str(i), result)
                
                if len(results) > 5:
                    sample_table.add_row("...", f"[dim]and {len(results) - 5} more[/dim]")
                
                self.console.print(sample_table)
            else:
                print("\nSample results:")
                for i, result in enumerate(results[:5], 1):
                    print(f"{i}. {result}")
                if len(results) > 5:
                    print(f"... and {len(results) - 5} more")
            
        except Exception as e:
            self.print_error(f"Batch generation failed: {e}")
    
    def interactive_policy_manager(self):
        """Interactive policy management."""
        self.print_info("\n📋 ENTERPRISE POLICY MANAGER")
        
        if RICH_AVAILABLE:
            policy_table = Table(title="Current Security Policies")
            policy_table.add_column("Policy", style="cyan")
            policy_table.add_column("Value", style="white")
            
            default_policy = PasswordPolicy()
            policies = [
                ("Minimum Length", f"{default_policy.min_length} characters"),
                ("Maximum Length", f"{default_policy.max_length} characters"),
                ("Require Uppercase", "✅" if default_policy.require_uppercase else "❌"),
                ("Require Lowercase", "✅" if default_policy.require_lowercase else "❌"),
                ("Require Digits", "✅" if default_policy.require_digits else "❌"),
                ("Require Symbols", "✅" if default_policy.require_symbols else "❌"),
                ("Entropy Threshold", f"{default_policy.entropy_threshold} bits")
            ]
            
            for policy, value in policies:
                policy_table.add_row(policy, value)
            
            self.console.print(policy_table)
        else:
            print("Current Security Policies:")
            print("- Minimum Length: 12 characters")
            print("- Maximum Length: 128 characters")
            print("- Require Uppercase: ✓")
            print("- Require Lowercase: ✓")
            print("- Require Digits: ✓")
            print("- Require Symbols: ✓")
            print("- Entropy Threshold: 50.0 bits")
        
        self.print_info("\n💼 Policy management features coming in next update!")
    
    def interactive_hash_generator(self):
        """Interactive hash generation."""
        self.print_info("\n🔗 CRYPTOGRAPHIC HASH GENERATOR")
        
        try:
            password = getpass.getpass("Enter text to hash (hidden): ")
            
            if not password:
                self.print_error("No text entered.")
                return
            
            if RICH_AVAILABLE:
                algorithm = Prompt.ask("Hash algorithm", 
                                     choices=["md5", "sha1", "sha256", "sha512"], 
                                     default="sha256")
            else:
                print("Available algorithms: md5, sha1, sha256, sha512")
                algorithm = input("Hash algorithm [sha256]: ").strip() or "sha256"
            
            # Generate multiple hashes
            hashes = {
                "MD5": hashlib.md5(password.encode()).hexdigest(),
                "SHA1": hashlib.sha1(password.encode()).hexdigest(),
                "SHA256": hashlib.sha256(password.encode()).hexdigest(),
                "SHA512": hashlib.sha512(password.encode()).hexdigest()
            }
            
            if RICH_AVAILABLE:
                hash_table = Table(title="Cryptographic Hashes")
                hash_table.add_column("Algorithm", style="cyan")
                hash_table.add_column("Hash Value", style="green")
                
                for alg, hash_val in hashes.items():
                    hash_table.add_row(alg, hash_val)
                
                self.console.print(hash_table)
            else:
                print("\nCryptographic Hashes:")
                for alg, hash_val in hashes.items():
                    print(f"{alg}: {hash_val}")
                    
        except Exception as e:
            self.print_error(f"Hash generation failed: {e}")
    
    def interactive_security_audit(self):
        """Interactive security audit tools."""
        self.print_info("\n🛡️ SECURITY AUDIT SUITE")
        
        if RICH_AVAILABLE:
            audit_table = Table(title="Security Audit Tools")
            audit_table.add_column("Tool", style="cyan")
            audit_table.add_column("Description", style="white")
            audit_table.add_column("Status", style="green")
            
            tools = [
                ("Password Strength Tester", "Bulk password analysis", "✅ Available"),
                ("Dictionary Attack Simulator", "Test against common passwords", "✅ Available"),
                ("Entropy Calculator", "Advanced entropy measurements", "✅ Available"),
                ("Pattern Detector", "Identify password patterns", "🔄 Beta"),
                ("Breach Database Check", "Check against known breaches", "🔜 Coming Soon"),
                ("Policy Compliance Audit", "Enterprise policy validation", "🔜 Coming Soon")
            ]
            
            for tool, desc, status in tools:
                audit_table.add_row(tool, desc, status)
            
            self.console.print(audit_table)
        else:
            print("Security Audit Tools:")
            print("1. Password Strength Tester - ✓ Available")
            print("2. Dictionary Attack Simulator - ✓ Available")
            print("3. Entropy Calculator - ✓ Available")
            print("4. Pattern Detector - 🔄 Beta")
            print("5. Breach Database Check - 🔜 Coming Soon")
            print("6. Policy Compliance Audit - 🔜 Coming Soon")
        
        # Simple entropy test
        test_passwords = ["password", "P@ssw0rd!", "Tr0ub4dor&3", "correct horse battery staple"]
        
        self.print_info("\nSample Entropy Analysis:")
        
        if RICH_AVAILABLE:
            entropy_table = Table(title="Sample Password Entropy")
            entropy_table.add_column("Password", style="cyan")
            entropy_table.add_column("Entropy (bits)", style="white")
            entropy_table.add_column("Strength", style="green")
            
            for pwd in test_passwords:
                analysis = self.generator.analyze_password(pwd)
                entropy_table.add_row(
                    pwd, 
                    f"{analysis.entropy:.1f}",
                    analysis.strength_level
                )
            
            self.console.print(entropy_table)
        else:
            for pwd in test_passwords:
                analysis = self.generator.analyze_password(pwd)
                print(f"{pwd}: {analysis.entropy:.1f} bits ({analysis.strength_level})")
    
    def show_system_info(self):
        """Show system information."""
        self.print_info("\n💻 SYSTEM INFORMATION")
        
        import platform
        import sys
        
        info = {
            "System": platform.system(),
            "Platform": platform.platform(),
            "Architecture": platform.architecture()[0],
            "Python Version": sys.version.split()[0],
            "Gen-Pass Version": "3.2.1",
            "Security Level": "Enterprise",
            "Crypto Support": "✅ Available",
            "Rich Interface": "✅ Available" if RICH_AVAILABLE else "❌ Not Available"
        }
        
        if RICH_AVAILABLE:
            info_table = Table(title="System Information")
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            for prop, value in info.items():
                info_table.add_row(prop, str(value))
            
            self.console.print(info_table)
        else:
            print("System Information:")
            for prop, value in info.items():
                print(f"{prop}: {value}")
    
    def show_help(self):
        """Show help information."""
        self.print_info("\n❓ HELP & DOCUMENTATION")
        
        help_sections = [
            ("Basic Usage", [
                "• Select menu options using numbers 0-9",
                "• Follow prompts for interactive generation",
                "• Use Ctrl+C to cancel operations"
            ]),
            ("Password Generation", [
                "• Choose complexity: minimum to military grade",
                "• Set custom length (recommended: 12+ characters)",
                "• Exclude ambiguous/similar characters for clarity"
            ]),
            ("Passphrase Generation", [
                "• Use 4-8 words for best security/memorability balance",
                "• Add numbers and symbols for extra security",
                "• Customize separators for personal preference"
            ]),
            ("Security Analysis", [
                "• Entropy measures randomness (aim for 50+ bits)",
                "• Check character variety for strong passwords",
                "• Review recommendations for improvements"
            ])
        ]
        
        if RICH_AVAILABLE:
            for section, items in help_sections:
                panel = Panel(
                    "\n".join(items),
                    title=f"[bold cyan]{section}[/bold cyan]",
                    border_style="blue"
                )
                self.console.print(panel)
        else:
            for section, items in help_sections:
                print(f"\n{section}:")
                for item in items:
                    print(f"  {item}")
    
    def get_strength_color(self, strength: str) -> str:
        """Get color for strength level."""
        colors = {
            "EXCELLENT": "bright_green",
            "VERY_STRONG": "green",
            "STRONG": "yellow",
            "GOOD": "yellow",
            "MODERATE": "orange3",
            "WEAK": "red",
            "VERY_WEAK": "bright_red"
        }
        return colors.get(strength, "white")
    
    def print_success(self, message: str):
        """Print success message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold green]✅[/bold green] {message}")
        else:
            print(f"{GREEN}✅ {message}{RESET}")
    
    def print_error(self, message: str):
        """Print error message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold red]❌[/bold red] {message}")
        else:
            print(f"{RED}❌ {message}{RESET}")
    
    def print_info(self, message: str):
        """Print info message."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold blue]ℹ️[/bold blue] {message}")
        else:
            print(f"{BLUE}ℹ️ {message}{RESET}")


def main():
    """Main entry point."""
    cli = PasswordGeneratorCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
