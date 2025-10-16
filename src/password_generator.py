#!/usr/bin/env python3
"""
Enterprise Password Generation Engine
====================================

A cryptographically secure, enterprise-grade password generation system
designed for high-security environments and professional applications.

Author: Gen-Spider Security Systems
Version: 3.2.1
License: MIT
Copyright: 2024 Gen-Spider Security Systems
"""

import secrets
import string
import hashlib
import hmac
import base64
import json
import os
import time
import math
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor

# Cryptographic imports
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
except ImportError:
    # Fallback to standard library
    hashes = None
    PBKDF2HMAC = None


class PasswordComplexity(Enum):
    """Password complexity levels for enterprise requirements."""
    MINIMUM = "minimum"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"
    MILITARY = "military"


class CharacterSet(Enum):
    """Predefined character sets for different security requirements."""
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS_BASIC = "!@#$%^&*()"
    SYMBOLS_EXTENDED = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    SYMBOLS_FULL = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`'\""
    AMBIGUOUS = "0O1lI"
    SIMILAR = "il1Lo0O"
    

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
    """
    Enterprise-grade password generation system with advanced security features.
    
    Features:
    - Cryptographically secure random generation
    - Multiple complexity levels and policies
    - Advanced entropy calculations
    - Dictionary attack resistance
    - Pattern analysis and prevention
    - Multi-threaded batch generation
    - Comprehensive strength analysis
    - Hash generation and verification
    """
    
    # Common password patterns to avoid
    COMMON_PATTERNS = [
        r'(.)\1{2,}',  # Repeated characters
        r'(abc|123|qwe|asd|zxc)',  # Sequential patterns
        r'(password|admin|user|login|test)',  # Common words
        r'(19|20)\d{2}',  # Years
        r'\d{4,}',  # Long number sequences
    ]
    
    # Common weak passwords (subset for performance)
    WEAK_PASSWORDS = {
        'password', '123456', 'password123', 'admin', 'qwerty',
        'letmein', 'welcome', 'monkey', '1234567890', 'abc123',
        'password1', '123456789', 'welcome123', 'admin123'
    }
    
    # Word list for passphrase generation (cryptographic quality)
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
        "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset", "assist",
        "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract",
        "auction", "audit", "august", "aunt", "author", "auto", "autumn", "average",
        "avocado", "avoid", "awake", "aware", "away", "awesome", "awful", "awkward",
        "axis", "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony",
        "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel",
        "base", "basic", "basket", "battle", "beach", "bean", "beauty", "because",
        "become", "beef", "before", "begin", "behave", "behind", "believe", "below",
        "belt", "bench", "benefit", "best", "betray", "better", "between", "beyond",
        "bicycle", "bid", "bike", "bind", "biology", "bird", "birth", "bitter",
        "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind",
        "blood", "blossom", "blow", "blue", "blur", "blush", "board", "boat",
        "body", "boil", "bomb", "bone", "bonus", "book", "boost", "border",
        "boring", "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket",
        "brain", "brand", "brass", "brave", "bread", "breeze", "brick", "bridge",
        "brief", "bright", "bring", "brisk", "broccoli", "broken", "bronze", "broom",
        "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo", "build",
        "bulb", "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst",
        "bus", "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin",
        "cable", "cactus", "cage", "cake", "call", "calm", "camera", "camp",
        "can", "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon",
        "capable", "capital", "captain", "car", "carbon", "card", "care", "career",
        "careful", "careless", "cargo", "carpet", "carry", "cart", "case", "cash",
        "casino", "cast", "casual", "cat", "catalog", "catch", "category", "cattle",
        "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census",
        "century", "cereal", "certain", "chair", "chalk", "champion", "change", "chaos",
        "chapter", "charge", "chase", "chat", "cheap", "check", "cheese", "chef",
        "cherry", "chest", "chicken", "chief", "child", "chimney", "choice", "choose",
        "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon", "circle", "citizen",
        "city", "civil", "claim", "clamp", "clarify", "claw", "clay", "clean",
        "clerk", "clever", "click", "client", "cliff", "climb", "clinic", "clip",
        "clock", "clog", "close", "cloth", "cloud", "clown", "club", "clump",
        "cluster", "clutch", "coach", "coast", "coconut", "code", "coffee", "coil",
        "coin", "collect", "color", "column", "combine", "come", "comfort", "comic",
        "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider",
        "control", "convince", "cook", "cool", "copper", "copy", "coral", "core",
        "corn", "correct", "cost", "cotton", "couch", "country", "couple", "course",
        "cousin", "cover", "coyote", "crack", "cradle", "craft", "cram", "crane",
        "crash", "crater", "crawl", "crazy", "cream", "credit", "creek", "crew",
        "cricket", "crime", "crisp", "critic", "crop", "cross", "crouch", "crowd",
        "crucial", "cruel", "cruise", "crumble", "crunch", "crush", "cry", "crystal",
        "cube", "culture", "cup", "cupboard", "curious", "current", "curtain", "curve",
        "cushion", "custom", "cute", "cycle", "dad", "damage", "damp", "dance",
        "danger", "daring", "dash", "daughter", "dawn", "day", "deal", "debate",
        "debris", "decade", "december", "decide", "decline", "decorate", "decrease", "deer",
        "defense", "define", "defy", "degree", "delay", "deliver", "demand", "demise",
        "denial", "dentist", "deny", "depart", "depend", "deposit", "depth", "deputy",
        "derive", "describe", "desert", "design", "desk", "despair", "destroy", "detail",
        "detect", "device", "devote", "diagram", "dial", "diamond", "diary", "dice",
        "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur",
        "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss", "disorder",
        "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document",
        "dog", "doll", "dolphin", "domain", "donate", "donkey", "donor", "door",
        "dose", "double", "dove", "draft", "dragon", "drama", "drape", "draw",
        "dream", "dress", "drift", "drill", "drink", "drip", "drive", "drop",
        "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch",
        "duty", "dwarf", "dynamic", "eager", "eagle", "early", "earn", "earth",
        "easily", "east", "easy", "echo", "ecology", "economy", "edge", "edit",
        "educate", "effort", "egg", "eight", "either", "elbow", "elder", "electric",
        "elegant", "element", "elephant", "elevator", "elite", "else", "embark", "embody",
        "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact",
        "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine",
        "enhance", "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter",
        "entire", "entry", "envelope", "episode", "equal", "equip", "era", "erase",
        "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate",
        "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example",
        "excess", "exchange", "excite", "exclude", "excuse", "execute", "exercise", "exhale",
        "exhibit", "exile", "exist", "exit", "exotic", "expand", "expect", "expire",
        "explain", "expose", "express", "extend", "extra", "eye", "eyebrow", "fabric",
        "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame",
        "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat",
        "fatal", "father", "fatigue", "fault", "favorite", "feature", "february", "federal",
        "fee", "feed", "feel", "female", "fence", "festival", "fetch", "fever",
        "few", "fiber", "fiction", "field", "figure", "file", "fill", "film",
        "filter", "final", "find", "fine", "finger", "finish", "fire", "firm",
        "first", "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame",
        "flash", "flat", "flavor", "flee", "flight", "flip", "float", "flock",
        "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog",
        "foil", "fold", "follow", "food", "foot", "force", "forest", "forget",
        "fork", "fortune", "forum", "forward", "fossil", "foster", "found", "fox",
        "frame", "frequent", "fresh", "friend", "fringe", "frog", "front", "frost",
        "frown", "frozen", "fruit", "fuel", "fun", "funny", "furnace", "fury",
        "future", "gadget", "gain", "galaxy", "gallery", "game", "gap", "garage",
        "garbage", "garden", "garlic", "garment", "gas", "gasp", "gate", "gather",
        "gauge", "gaze", "general", "genius", "genre", "gentle", "genuine", "gesture",
        "ghost", "giant", "gift", "giggle", "ginger", "giraffe", "girl", "give",
        "glad", "glance", "glare", "glass", "glide", "glimpse", "globe", "gloom",
        "glory", "glove", "glow", "glue", "goat", "goddess", "gold", "good",
        "goose", "gorilla", "gospel", "gossip", "govern", "gown", "grab", "grace",
        "grain", "grant", "grape", "grass", "gravity", "great", "green", "grid",
        "grief", "grit", "grocery", "group", "grow", "grunt", "guard", "guess",
        "guide", "guilt", "guitar", "gun", "gym", "hair", "half", "hammer",
        "hamster", "hand", "happy", "harbor", "hard", "harsh", "harvest", "hat",
        "have", "hawk", "hazard", "head", "health", "heart", "heavy", "hedgehog",
        "height", "hello", "helmet", "help", "hen", "hero", "hidden", "high",
        "hill", "hint", "hip", "hire", "history", "hobby", "hockey", "hold",
        "hole", "holiday", "hollow", "home", "honey", "hood", "hope", "horn",
        "horror", "horse", "hospital", "host", "hotel", "hour", "hover", "hub",
        "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle",
        "hurry", "hurt", "husband", "hybrid", "ice", "icon", "idea", "identify",
        "idle", "ignore", "ill", "illegal", "illness", "image", "imitate", "immense",
        "immune", "impact", "impose", "improve", "impulse", "inch", "include", "income",
        "increase", "index", "indicate", "indoor", "industry", "infant", "inflict", "inform",
        "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner", "innocent",
        "input", "inquiry", "insane", "insect", "inside", "inspire", "install", "intact",
        "interest", "into", "invest", "invite", "involve", "iron", "island", "isolate",
        "issue", "item", "ivory", "jacket", "jaguar", "jar", "jazz", "jealous",
        "jeans", "jelly", "jewel", "job", "join", "joke", "journey", "joy",
        "judge", "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo",
        "keen", "keep", "ketchup", "key", "kick", "kid", "kidney", "kind",
        "kingdom", "kiss", "kit", "kitchen", "kite", "kitten", "kiwi", "knee",
        "knife", "knock", "know", "lab", "label", "labor", "ladder", "lady",
        "lake", "lamp", "language", "laptop", "large", "later", "latin", "laugh",
        "laundry", "lava", "law", "lawn", "lawsuit", "layer", "lazy", "leader",
        "leaf", "learn", "leave", "lecture", "left", "leg", "legal", "legend",
        "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter",
        "level", "liar", "liberty", "library", "license", "life", "lift", "light",
        "like", "limb", "limit", "link", "lion", "liquid", "list", "little",
        "live", "lizard", "load", "loan", "lobster", "local", "lock", "logic",
        "lonely", "long", "loop", "lottery", "loud", "lounge", "love", "loyal",
        "lucky", "luggage", "lumber", "lunar", "lunch", "luxury", "lying", "machine",
        "mad", "magic", "magnet", "maid", "mail", "main", "major", "make",
        "mammal", "man", "manage", "mandate", "mango", "mansion", "manual", "maple",
        "marble", "march", "margin", "marine", "market", "marriage", "mask", "mass",
        "master", "match", "material", "math", "matrix", "matter", "maximum", "maze",
        "meadow", "mean", "measure", "meat", "mechanic", "medal", "media", "melody",
        "melt", "member", "memory", "mention", "menu", "mercy", "merge", "merit",
        "merry", "mesh", "message", "metal", "method", "middle", "midnight", "milk",
        "million", "mimic", "mind", "minimum", "minor", "minute", "miracle", "mirror",
        "misery", "miss", "mistake", "mix", "mixed", "mixture", "mobile", "model",
        "modify", "mom", "moment", "monitor", "monkey", "monster", "month", "moon",
        "moral", "more", "morning", "mosquito", "mother", "motion", "motor", "mountain",
        "mouse", "move", "movie", "much", "muffin", "mule", "multiply", "muscle",
        "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth",
        "naive", "name", "napkin", "narrow", "nasty", "nation", "nature", "near",
        "neck", "need", "needle", "neglect", "neighbor", "neither", "nephew", "nerve",
        "nest", "net", "network", "neutral", "never", "news", "next", "nice",
        "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose",
        "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number",
        "nurse", "nut", "oak", "obey", "object", "oblige", "obscure", "observe",
        "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer",
        "office", "often", "oil", "okay", "old", "olive", "olympic", "omit",
        "once", "one", "onion", "online", "only", "open", "opera", "opinion",
        "oppose", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ",
        "orient", "original", "orphan", "ostrich", "other", "outdoor", "outer", "output",
        "outside", "oval", "oven", "over", "own", "owner", "oxygen", "oyster",
        "ozone", "pact", "paddle", "page", "pair", "palace", "palm", "panda",
        "panel", "panic", "panther", "paper", "parade", "parent", "park", "parrot",
        "part", "party", "pass", "patch", "path", "patient", "patrol", "pattern",
        "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican",
        "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person",
        "pet", "phone", "photo", "phrase", "physical", "piano", "picnic", "picture",
        "piece", "pig", "pigeon", "pill", "pilot", "pink", "pioneer", "pipe",
        "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate", "play",
        "please", "pledge", "pluck", "plug", "plunge", "poem", "poet", "point",
        "polar", "pole", "police", "pond", "pony", "pool", "popular", "portion",
        "position", "possible", "post", "potato", "pottery", "poverty", "powder", "power",
        "practice", "praise", "predict", "prefer", "prepare", "present", "pretty", "prevent",
        "price", "pride", "primary", "print", "priority", "prison", "private", "prize",
        "problem", "process", "produce", "profit", "program", "project", "promote", "proof",
        "property", "prosper", "protect", "proud", "provide", "public", "pudding", "pull",
        "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy", "purchase", "purity",
        "purpose", "purse", "push", "put", "puzzle", "pyramid", "quality", "quantum",
        "quarter", "question", "quick", "quiet", "quilt", "quit", "quiz", "quote",
        "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail", "rain",
        "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare",
        "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason",
        "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce",
        "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax",
        "release", "relief", "rely", "remain", "remember", "remind", "remove", "render",
        "renew", "rent", "reopen", "repair", "repeat", "replace", "report", "require",
        "rescue", "resemble", "resist", "resource", "response", "result", "retire", "retreat",
        "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon",
        "rice", "rich", "ride", "ridge", "rifle", "right", "rigid", "ring",
        "riot", "ripple", "rise", "risk", "ritual", "rival", "river", "road",
        "roast", "rob", "robot", "robust", "rocket", "romance", "roof", "rookie",
        "room", "rose", "rotate", "rough", "round", "route", "royal", "rubber",
        "rude", "rug", "rule", "run", "runway", "rural", "sad", "saddle",
        "sadness", "safe", "sail", "salad", "salmon", "salon", "salt", "salute",
        "same", "sample", "sand", "satisfy", "satoshi", "sauce", "sausage", "save",
        "say", "scale", "scan", "scare", "scatter", "scene", "scheme", "school",
        "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub",
        "sea", "search", "season", "seat", "second", "secret", "section", "security",
        "seed", "seek", "segment", "select", "sell", "seminar", "senior", "sense",
        "sentence", "series", "service", "session", "settle", "setup", "seven", "shadow",
        "shaft", "shallow", "share", "shed", "shell", "sheriff", "shield", "shift",
        "shine", "ship", "shirt", "shock", "shoe", "shoot", "shop", "short",
        "shoulder", "shove", "shrimp", "shrug", "shuffle", "shy", "sibling", "sick",
        "side", "siege", "sight", "sign", "silent", "silk", "silly", "silver",
        "similar", "simple", "since", "sing", "siren", "sister", "situate", "six",
        "size", "skate", "sketch", "ski", "skill", "skin", "skirt", "skull",
        "slab", "slam", "sleep", "slender", "slice", "slide", "slight", "slim",
        "slogan", "slot", "slow", "slush", "small", "smart", "smile", "smoke",
        "smooth", "snack", "snake", "snap", "sniff", "snow", "soap", "soccer",
        "social", "sock", "soda", "soft", "solar", "soldier", "solid", "solution",
        "solve", "someone", "song", "soon", "sorry", "sort", "soul", "sound",
        "soup", "source", "south", "space", "spare", "spatial", "spawn", "speak",
        "special", "speed", "spell", "spend", "sphere", "spice", "spider", "spike",
        "spin", "spirit", "split", "spoil", "sponsor", "spoon", "sport", "spot",
        "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable",
        "stadium", "staff", "stage", "stairs", "stamp", "stand", "start", "state",
        "stay", "steak", "steel", "stem", "step", "stereo", "stick", "still",
        "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy",
        "street", "strike", "strong", "struggle", "student", "stuff", "stumble", "style",
        "subject", "submit", "subway", "success", "such", "sudden", "suffer", "sugar",
        "suggest", "suit", "summer", "sun", "sunny", "sunset", "super", "supply",
        "supreme", "sure", "surface", "surge", "surprise", "surround", "survey", "suspect",
        "sustain", "swallow", "swamp", "swap", "swear", "sweet", "swift", "swim",
        "swing", "switch", "sword", "symbol", "symptom", "syrup", "system", "table",
        "tackle", "tag", "tail", "talent", "talk", "tank", "tape", "target",
        "task", "taste", "tattoo", "taxi", "teach", "team", "tell", "ten",
        "tenant", "tennis", "tent", "term", "test", "text", "thank", "that",
        "theme", "then", "theory", "there", "they", "thing", "this", "thought",
        "three", "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger",
        "tilt", "timber", "time", "tiny", "tip", "tired", "tissue", "title",
        "toast", "tobacco", "today", "toddler", "toe", "together", "toilet", "token",
        "tomato", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top",
        "topic", "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist",
        "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic",
        "train", "transfer", "trap", "trash", "travel", "tray", "treat", "tree",
        "trend", "trial", "tribe", "trick", "trigger", "trim", "trip", "trophy",
        "trouble", "truck", "true", "truly", "trumpet", "trust", "truth", "try",
        "tube", "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle",
        "twelve", "twenty", "twice", "twin", "twist", "two", "type", "typical",
        "ugly", "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo",
        "unfair", "unfold", "unhappy", "uniform", "unique", "unit", "universe", "unknown",
        "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold", "upon",
        "upper", "upset", "urban", "urge", "usage", "use", "used", "useful",
        "useless", "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley",
        "valve", "van", "vanish", "vapor", "various", "vast", "vault", "vehicle",
        "velvet", "vendor", "venture", "venue", "verb", "verify", "version", "very",
        "vessel", "veteran", "viable", "vibrant", "vicious", "victory", "video", "view",
        "village", "vintage", "violin", "virtual", "virus", "visa", "visit", "visual",
        "vital", "vivid", "vocal", "voice", "void", "volcano", "volume", "vote",
        "voyage", "wage", "wagon", "wait", "walk", "wall", "walnut", "want",
        "warfare", "warm", "warrior", "wash", "wasp", "waste", "water", "wave",
        "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding",
        "weekend", "weird", "welcome", "west", "wet", "what", "wheat", "wheel",
        "when", "where", "whip", "whisper", "wide", "width", "wife", "wild",
        "will", "win", "window", "wine", "wing", "wink", "winner", "winter",
        "wire", "wisdom", "wise", "wish", "witness", "wolf", "woman", "wonder",
        "wood", "wool", "word", "work", "world", "worry", "worth", "wrap",
        "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow",
        "you", "young", "youth", "zebra", "zero", "zone", "zoo"
    ]
    
    def __init__(self):
        """Initialize the enterprise password generator."""
        self._entropy_cache = {}
        self._pattern_cache = {}
        
    def generate_password(self, 
                         policy: PasswordPolicy = None,
                         length: int = None,
                         complexity: PasswordComplexity = PasswordComplexity.STANDARD) -> str:
        """
        Generate a cryptographically secure password based on policy requirements.
        
        Args:
            policy: Custom password policy (uses default if None)
            length: Override length from policy
            complexity: Complexity level for automatic policy selection
            
        Returns:
            Generated password string
            
        Raises:
            ValueError: If policy requirements cannot be satisfied
        """
        if policy is None:
            policy = self._get_default_policy(complexity)
            
        if length is not None:
            policy.min_length = length
            policy.max_length = max(length, policy.max_length)
            
        # Validate policy feasibility
        self._validate_policy(policy)
        
        max_attempts = 1000
        for attempt in range(max_attempts):
            password = self._generate_candidate_password(policy)
            
            if self._validate_password(password, policy):
                return password
                
        raise ValueError(f"Unable to generate password meeting policy requirements after {max_attempts} attempts")
    
    def generate_passphrase(self, 
                           word_count: int = 6,
                           separator: str = "-",
                           capitalize: bool = True,
                           add_numbers: bool = True,
                           add_symbols: bool = False,
                           min_entropy: float = 50.0) -> str:
        """
        Generate a cryptographically secure passphrase using the wordlist.
        
        Args:
            word_count: Number of words in the passphrase
            separator: Character(s) to separate words
            capitalize: Whether to capitalize first letter of each word
            add_numbers: Whether to add random numbers
            add_symbols: Whether to add random symbols
            min_entropy: Minimum entropy requirement in bits
            
        Returns:
            Generated passphrase string
        """
        if word_count < 2:
            raise ValueError("Word count must be at least 2")
            
        words = []
        for _ in range(word_count):
            word = secrets.choice(self.WORDLIST)
            if capitalize:
                word = word.capitalize()
            words.append(word)
            
        passphrase = separator.join(words)
        
        if add_numbers:
            num_digits = secrets.randbelow(3) + 2  # 2-4 digits
            numbers = ''.join([str(secrets.randbelow(10)) for _ in range(num_digits)])
            passphrase += separator + numbers
            
        if add_symbols:
            symbol_count = secrets.randbelow(2) + 1  # 1-2 symbols
            symbols = ''.join([secrets.choice(CharacterSet.SYMBOLS_BASIC.value) 
                             for _ in range(symbol_count)])
            passphrase += separator + symbols
            
        # Check entropy requirement
        entropy = self.calculate_entropy(passphrase)
        if entropy < min_entropy:
            # Recursively generate with more complexity
            return self.generate_passphrase(
                word_count=word_count + 1,
                separator=separator,
                capitalize=capitalize,
                add_numbers=add_numbers,
                add_symbols=True,
                min_entropy=min_entropy
            )
            
        return passphrase
    
    def batch_generate(self, 
                      count: int,
                      generator_func: callable,
                      **kwargs) -> List[str]:
        """
        Generate multiple passwords/passphrases using multi-threading for performance.
        
        Args:
            count: Number of passwords to generate
            generator_func: Function to use for generation (generate_password or generate_passphrase)
            **kwargs: Arguments to pass to the generator function
            
        Returns:
            List of generated passwords/passphrases
        """
        if count <= 0:
            raise ValueError("Count must be positive")
            
        if count <= 10:
            # Use single-threaded for small batches
            return [generator_func(**kwargs) for _ in range(count)]
            
        # Use multi-threading for larger batches
        with ThreadPoolExecutor(max_workers=min(count, os.cpu_count() or 4)) as executor:
            futures = [executor.submit(generator_func, **kwargs) for _ in range(count)]
            return [future.result() for future in futures]
    
    def analyze_password(self, password: str, policy: PasswordPolicy = None) -> PasswordAnalysis:
        """
        Perform comprehensive security analysis of a password.
        
        Args:
            password: Password to analyze
            policy: Policy to check compliance against
            
        Returns:
            Detailed password analysis results
        """
        if policy is None:
            policy = self._get_default_policy(PasswordComplexity.STANDARD)
            
        # Calculate entropy
        entropy = self.calculate_entropy(password)
        
        # Calculate strength score (0-100)
        strength_score = self._calculate_strength_score(password, entropy)
        
        # Determine strength level
        strength_level = self._get_strength_level(strength_score)
        
        # Estimate crack time
        crack_time = self._estimate_crack_time(entropy)
        
        # Analyze character composition
        char_analysis = self._analyze_characters(password)
        
        # Check policy compliance
        policy_compliance = self._check_policy_compliance(password, policy)
        
        # Identify vulnerabilities
        vulnerabilities = self._identify_vulnerabilities(password)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(password, policy_compliance, vulnerabilities)
        
        # Generate password hashes
        hash_analysis = self._generate_hash_analysis(password)
        
        return PasswordAnalysis(
            password=password,
            strength_score=strength_score,
            strength_level=strength_level,
            entropy=entropy,
            time_to_crack=crack_time,
            character_analysis=char_analysis,
            policy_compliance=policy_compliance,
            vulnerabilities=vulnerabilities,
            recommendations=recommendations,
            hash_analysis=hash_analysis,
            created_at=time.time()
        )
    
    def calculate_entropy(self, password: str) -> float:
        """
        Calculate the entropy of a password in bits.
        
        Args:
            password: Password to analyze
            
        Returns:
            Entropy value in bits
        """
        if password in self._entropy_cache:
            return self._entropy_cache[password]
            
        if not password:
            return 0.0
            
        # Determine character space
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in CharacterSet.SYMBOLS_EXTENDED.value for c in password):
            charset_size += len(CharacterSet.SYMBOLS_EXTENDED.value)
            
        # Calculate base entropy
        if charset_size == 0:
            entropy = 0.0
        else:
            entropy = len(password) * math.log2(charset_size)
            
        # Apply pattern penalties
        entropy *= self._calculate_pattern_penalty(password)
        
        # Cache result
        self._entropy_cache[password] = entropy
        
        return entropy
    
    def generate_hash(self, password: str, algorithm: str = "sha256", salt: str = None) -> Dict[str, str]:
        """
        Generate cryptographic hashes of the password.
        
        Args:
            password: Password to hash
            algorithm: Hash algorithm to use
            salt: Optional salt (auto-generated if None)
            
        Returns:
            Dictionary containing hash information
        """
        if salt is None:
            salt = secrets.token_hex(16)
            
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8') if isinstance(salt, str) else salt
        
        result = {
            'algorithm': algorithm,
            'salt': salt,
            'timestamp': time.time()
        }
        
        if algorithm.lower() in ['md5', 'sha1', 'sha256', 'sha512', 'sha3_256', 'sha3_512']:
            hasher = hashlib.new(algorithm.lower())
            hasher.update(salt_bytes + password_bytes)
            result['hash'] = hasher.hexdigest()
            
        elif algorithm.lower() == 'pbkdf2':
            if PBKDF2HMAC is not None:
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt_bytes,
                    iterations=100000,
                    backend=default_backend()
                )
                key = kdf.derive(password_bytes)
                result['hash'] = base64.b64encode(key).decode('ascii')
                result['iterations'] = 100000
            else:
                # Fallback implementation
                result['hash'] = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000).hex()
                result['iterations'] = 100000
                
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            
        return result
    
    def verify_hash(self, password: str, hash_info: Dict[str, str]) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: Password to verify
            hash_info: Hash information dictionary
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            new_hash = self.generate_hash(
                password,
                hash_info['algorithm'],
                hash_info['salt']
            )
            return hmac.compare_digest(new_hash['hash'], hash_info['hash'])
        except Exception:
            return False
    
    def _get_default_policy(self, complexity: PasswordComplexity) -> PasswordPolicy:
        """Get default policy for complexity level."""
        if complexity == PasswordComplexity.MINIMUM:
            return PasswordPolicy(
                min_length=8,
                require_symbols=False,
                min_symbols=0,
                entropy_threshold=30.0
            )
        elif complexity == PasswordComplexity.STANDARD:
            return PasswordPolicy(
                min_length=12,
                entropy_threshold=50.0
            )
        elif complexity == PasswordComplexity.HIGH:
            return PasswordPolicy(
                min_length=16,
                min_uppercase=2,
                min_lowercase=2,
                min_digits=2,
                min_symbols=2,
                exclude_ambiguous=True,
                entropy_threshold=70.0
            )
        elif complexity == PasswordComplexity.MAXIMUM:
            return PasswordPolicy(
                min_length=20,
                min_uppercase=3,
                min_lowercase=3,
                min_digits=3,
                min_symbols=3,
                exclude_ambiguous=True,
                exclude_similar=True,
                max_consecutive=1,
                entropy_threshold=90.0
            )
        elif complexity == PasswordComplexity.MILITARY:
            return PasswordPolicy(
                min_length=24,
                min_uppercase=4,
                min_lowercase=4,
                min_digits=4,
                min_symbols=4,
                exclude_ambiguous=True,
                exclude_similar=True,
                exclude_sequential=True,
                exclude_repetitive=True,
                max_consecutive=1,
                entropy_threshold=110.0
            )
        else:
            return PasswordPolicy()
    
    def _validate_policy(self, policy: PasswordPolicy):
        """Validate that policy requirements are feasible."""
        min_required = (policy.min_uppercase + policy.min_lowercase + 
                       policy.min_digits + policy.min_symbols)
        
        if min_required > policy.min_length:
            raise ValueError(
                f"Policy requires minimum {min_required} characters but "
                f"minimum length is only {policy.min_length}"
            )
    
    def _generate_candidate_password(self, policy: PasswordPolicy) -> str:
        """Generate a candidate password based on policy."""
        length = secrets.randbelow(policy.max_length - policy.min_length + 1) + policy.min_length
        
        # Build character set
        charset = ""
        required_chars = []
        
        if policy.require_lowercase:
            charset += CharacterSet.LOWERCASE.value
            for _ in range(policy.min_lowercase):
                required_chars.append(secrets.choice(CharacterSet.LOWERCASE.value))
                
        if policy.require_uppercase:
            charset += CharacterSet.UPPERCASE.value
            for _ in range(policy.min_uppercase):
                required_chars.append(secrets.choice(CharacterSet.UPPERCASE.value))
                
        if policy.require_digits:
            charset += CharacterSet.DIGITS.value
            for _ in range(policy.min_digits):
                required_chars.append(secrets.choice(CharacterSet.DIGITS.value))
                
        if policy.require_symbols:
            charset += CharacterSet.SYMBOLS_EXTENDED.value
            for _ in range(policy.min_symbols):
                required_chars.append(secrets.choice(CharacterSet.SYMBOLS_EXTENDED.value))
        
        # Remove excluded characters
        if policy.exclude_ambiguous:
            charset = ''.join(c for c in charset if c not in CharacterSet.AMBIGUOUS.value)
            
        if policy.exclude_similar:
            charset = ''.join(c for c in charset if c not in CharacterSet.SIMILAR.value)
            
        for exclusion in policy.custom_exclusions:
            charset = charset.replace(exclusion, '')
        
        if not charset:
            raise ValueError("No valid characters remain after applying exclusions")
        
        # Generate password
        password_chars = required_chars[:]
        
        while len(password_chars) < length:
            password_chars.append(secrets.choice(charset))
        
        # Shuffle to avoid predictable positions
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def _validate_password(self, password: str, policy: PasswordPolicy) -> bool:
        """Validate password against policy requirements."""
        # Basic length check
        if not (policy.min_length <= len(password) <= policy.max_length):
            return False
        
        # Character type checks
        uppercase_count = sum(1 for c in password if c.isupper())
        lowercase_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        symbol_count = sum(1 for c in password if c in CharacterSet.SYMBOLS_EXTENDED.value)
        
        if (uppercase_count < policy.min_uppercase or
            lowercase_count < policy.min_lowercase or
            digit_count < policy.min_digits or
            symbol_count < policy.min_symbols):
            return False
        
        # Pattern checks
        if policy.exclude_sequential and self._has_sequential_pattern(password):
            return False
            
        if policy.exclude_repetitive and self._has_repetitive_pattern(password, policy.max_consecutive):
            return False
        
        # Dictionary check
        if policy.exclude_dictionary and self._contains_dictionary_word(password):
            return False
        
        # Entropy check
        if self.calculate_entropy(password) < policy.entropy_threshold:
            return False
        
        return True
    
    def _has_sequential_pattern(self, password: str) -> bool:
        """Check for sequential character patterns."""
        password_lower = password.lower()
        
        # Check for common sequences
        sequences = ['abc', '123', 'qwe', 'asd', 'zxc', 'wer', 'ert', 'rty']
        for seq in sequences:
            if seq in password_lower:
                return True
                
        # Check for ascending/descending sequences
        for i in range(len(password) - 2):
            if (ord(password[i]) + 1 == ord(password[i+1]) and
                ord(password[i+1]) + 1 == ord(password[i+2])):
                return True
            if (ord(password[i]) - 1 == ord(password[i+1]) and
                ord(password[i+1]) - 1 == ord(password[i+2])):
                return True
                
        return False
    
    def _has_repetitive_pattern(self, password: str, max_consecutive: int) -> bool:
        """Check for repetitive character patterns."""
        count = 1
        for i in range(1, len(password)):
            if password[i] == password[i-1]:
                count += 1
                if count > max_consecutive:
                    return True
            else:
                count = 1
        return False
    
    def _contains_dictionary_word(self, password: str) -> bool:
        """Check if password contains common dictionary words."""
        password_lower = password.lower()
        
        # Check against weak passwords
        if password_lower in self.WEAK_PASSWORDS:
            return True
        
        # Check for embedded dictionary words (4+ characters)
        for word in self.WORDLIST:
            if len(word) >= 4 and word in password_lower:
                return True
                
        return False
    
    def _calculate_pattern_penalty(self, password: str) -> float:
        """Calculate penalty multiplier for common patterns."""
        penalty = 1.0
        
        # Check for patterns and reduce entropy accordingly
        for pattern in self.COMMON_PATTERNS:
            if re.search(pattern, password, re.IGNORECASE):
                penalty *= 0.8
        
        # Additional penalties for common weaknesses
        if password.lower() in self.WEAK_PASSWORDS:
            penalty *= 0.1
        
        # Keyboard pattern penalty
        if self._has_keyboard_pattern(password):
            penalty *= 0.7
        
        return max(penalty, 0.1)  # Minimum penalty of 0.1
    
    def _has_keyboard_pattern(self, password: str) -> bool:
        """Check for keyboard patterns."""
        keyboard_patterns = [
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
            '1234567890', '!@#$%^&*()',
            'qwerty', 'asdf', 'zxcv'
        ]
        
        password_lower = password.lower()
        for pattern in keyboard_patterns:
            if pattern in password_lower or pattern[::-1] in password_lower:
                return True
        return False
    
    def _calculate_strength_score(self, password: str, entropy: float) -> float:
        """Calculate overall strength score (0-100)."""
        score = 0
        
        # Length score (0-25 points)
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
        
        # Character variety score (0-25 points)
        varieties = 0
        if any(c.islower() for c in password):
            varieties += 1
        if any(c.isupper() for c in password):
            varieties += 1
        if any(c.isdigit() for c in password):
            varieties += 1
        if any(c in CharacterSet.SYMBOLS_EXTENDED.value for c in password):
            varieties += 1
        
        score += varieties * 6.25
        
        # Entropy score (0-40 points)
        entropy_score = min(40, (entropy / 100) * 40)
        score += entropy_score
        
        # Pattern penalty (0-10 points)
        pattern_penalty = self._calculate_pattern_penalty(password)
        score += pattern_penalty * 10
        
        return min(100, max(0, score))
    
    def _get_strength_level(self, score: float) -> str:
        """Get strength level description from score."""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 80:
            return "VERY_STRONG"
        elif score >= 70:
            return "STRONG"
        elif score >= 60:
            return "GOOD"
        elif score >= 40:
            return "MODERATE"
        elif score >= 20:
            return "WEAK"
        else:
            return "VERY_WEAK"
    
    def _estimate_crack_time(self, entropy: float) -> Dict[str, str]:
        """Estimate time to crack password using different attack methods."""
        if entropy <= 0:
            return {"instant": "0 seconds"}
        
        # Assumptions for different attack scenarios
        scenarios = {
            "online_throttled": 1e3,      # 1K attempts per second
            "online_unthrottled": 1e6,   # 1M attempts per second  
            "offline_slow": 1e9,         # 1B attempts per second
            "offline_fast": 1e12,        # 1T attempts per second
            "massive_cracking": 1e15     # 1P attempts per second
        }
        
        def format_time(seconds: float) -> str:
            if seconds < 60:
                return f"{seconds:.0f} seconds"
            elif seconds < 3600:
                return f"{seconds/60:.0f} minutes"
            elif seconds < 86400:
                return f"{seconds/3600:.1f} hours"
            elif seconds < 31536000:
                return f"{seconds/86400:.0f} days"
            elif seconds < 31536000000:
                return f"{seconds/31536000:.0f} years"
            else:
                return "centuries"
        
        results = {}
        combinations = 2 ** entropy
        
        for scenario, rate in scenarios.items():
            # Average time is half of worst case
            avg_time = (combinations / 2) / rate
            results[scenario] = format_time(avg_time)
            
        return results
    
    def _analyze_characters(self, password: str) -> Dict[str, bool]:
        """Analyze character composition of password."""
        return {
            "has_lowercase": any(c.islower() for c in password),
            "has_uppercase": any(c.isupper() for c in password),
            "has_digits": any(c.isdigit() for c in password),
            "has_symbols": any(c in CharacterSet.SYMBOLS_EXTENDED.value for c in password),
            "has_ambiguous": any(c in CharacterSet.AMBIGUOUS.value for c in password),
            "has_similar": any(c in CharacterSet.SIMILAR.value for c in password),
            "only_ascii": all(ord(c) < 128 for c in password),
            "has_unicode": any(ord(c) >= 128 for c in password)
        }
    
    def _check_policy_compliance(self, password: str, policy: PasswordPolicy) -> Dict[str, bool]:
        """Check password compliance against policy."""
        char_counts = {
            "uppercase": sum(1 for c in password if c.isupper()),
            "lowercase": sum(1 for c in password if c.islower()),
            "digits": sum(1 for c in password if c.isdigit()),
            "symbols": sum(1 for c in password if c in CharacterSet.SYMBOLS_EXTENDED.value)
        }
        
        return {
            "length_ok": policy.min_length <= len(password) <= policy.max_length,
            "uppercase_ok": char_counts["uppercase"] >= policy.min_uppercase,
            "lowercase_ok": char_counts["lowercase"] >= policy.min_lowercase,
            "digits_ok": char_counts["digits"] >= policy.min_digits,
            "symbols_ok": char_counts["symbols"] >= policy.min_symbols,
            "no_ambiguous": not policy.exclude_ambiguous or not any(c in CharacterSet.AMBIGUOUS.value for c in password),
            "no_similar": not policy.exclude_similar or not any(c in CharacterSet.SIMILAR.value for c in password),
            "no_sequential": not policy.exclude_sequential or not self._has_sequential_pattern(password),
            "no_repetitive": not policy.exclude_repetitive or not self._has_repetitive_pattern(password, policy.max_consecutive),
            "no_dictionary": not policy.exclude_dictionary or not self._contains_dictionary_word(password),
            "entropy_ok": self.calculate_entropy(password) >= policy.entropy_threshold
        }
    
    def _identify_vulnerabilities(self, password: str) -> List[str]:
        """Identify security vulnerabilities in password."""
        vulnerabilities = []
        
        if len(password) < 8:
            vulnerabilities.append("Password too short (less than 8 characters)")
        
        if len(set(password)) < len(password) * 0.5:
            vulnerabilities.append("Low character diversity (many repeated characters)")
        
        if password.lower() in self.WEAK_PASSWORDS:
            vulnerabilities.append("Password found in common password lists")
        
        if re.match(r'^[a-z]+$', password):
            vulnerabilities.append("Only lowercase letters used")
        elif re.match(r'^[A-Z]+$', password):
            vulnerabilities.append("Only uppercase letters used")
        elif re.match(r'^[0-9]+$', password):
            vulnerabilities.append("Only digits used")
        
        if self._has_keyboard_pattern(password):
            vulnerabilities.append("Contains keyboard patterns")
        
        if re.search(r'(19|20)\d{2}', password):
            vulnerabilities.append("Contains year pattern")
        
        if re.search(r'(.)\1{2,}', password):
            vulnerabilities.append("Contains repeated character sequences")
        
        if any(word in password.lower() for word in ['password', 'admin', 'user', 'login']):
            vulnerabilities.append("Contains common password terms")
        
        return vulnerabilities
    
    def _generate_recommendations(self, password: str, compliance: Dict[str, bool], vulnerabilities: List[str]) -> List[str]:
        """Generate improvement recommendations for password."""
        recommendations = []
        
        if not compliance.get("length_ok", True):
            recommendations.append("Increase password length to at least 12 characters")
        
        if not compliance.get("uppercase_ok", True):
            recommendations.append("Add uppercase letters (A-Z)")
        
        if not compliance.get("lowercase_ok", True):
            recommendations.append("Add lowercase letters (a-z)")
        
        if not compliance.get("digits_ok", True):
            recommendations.append("Add numeric digits (0-9)")
        
        if not compliance.get("symbols_ok", True):
            recommendations.append("Add special symbols (!@#$%^&*)")
        
        if vulnerabilities:
            if "Low character diversity" in str(vulnerabilities):
                recommendations.append("Use more unique characters")
            
            if "keyboard patterns" in str(vulnerabilities):
                recommendations.append("Avoid keyboard patterns (qwerty, 123456, etc.)")
            
            if "repeated character" in str(vulnerabilities):
                recommendations.append("Avoid repeating the same character multiple times")
        
        entropy = self.calculate_entropy(password)
        if entropy < 50:
            recommendations.append("Increase overall complexity for better security")
        
        if len(recommendations) == 0:
            recommendations.append("Password meets security requirements")
        
        return recommendations
    
    def _generate_hash_analysis(self, password: str) -> Dict[str, str]:
        """Generate hash analysis for password."""
        try:
            return {
                "md5": hashlib.md5(password.encode()).hexdigest(),
                "sha1": hashlib.sha1(password.encode()).hexdigest(),
                "sha256": hashlib.sha256(password.encode()).hexdigest(),
                "sha512": hashlib.sha512(password.encode())[:32].hex()  # Truncated for display
            }
        except Exception:
            return {"error": "Hash generation failed"}


# Convenience functions for backward compatibility
def generate_password(length: int = 12, **kwargs) -> str:
    """Generate a single password with specified length."""
    generator = EnterprisePasswordGenerator()
    return generator.generate_password(length=length, **kwargs)


def generate_passphrase(word_count: int = 6, **kwargs) -> str:
    """Generate a single passphrase with specified word count."""
    generator = EnterprisePasswordGenerator()
    return generator.generate_passphrase(word_count=word_count, **kwargs)


def analyze_password(password: str) -> PasswordAnalysis:
    """Analyze a password and return detailed results."""
    generator = EnterprisePasswordGenerator()
    return generator.analyze_password(password)
