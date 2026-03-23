import re

# We use r"" (raw strings) for keys that contain regex patterns like \s+
KEYWORDS = {
    # Variable assignment (Consumes 'mano' and the spaces after it)
    r"mano\s+": "", 

    # Control Flow
    "agar": "if",
    "warna": "else",
    "nahito": "elif",
    "jabtak": "while",
    "phir": "for",
    "mein": "in",
    "ruk": "break",
    "chalo": "continue",
    
    # Functions & Definitions
    "kaam": "def",
    "vapas": "return",
    
    # Input/Output
    "dikhao": "print",
    "pucho": "input",
    
    # Logic & Constants
    "sahi": "True",
    "galat": "False",
    "aur": "and",
    "ya": "or",
    "nahi": "not",
    "khali": "None",
    
    # Built-ins
    "range_tak": "range",
    "lambai": "len",

    # Math & Logic
    "jodo": "+",
    "ghatao": "-",
    "guna": "*",
    "bhag": "/",
    "barabar": "==",

    # Others
    "saaf": "os.system('cls' if os.name == 'nt' else 'clear')",

    # Comments
    "socho": "#",
}