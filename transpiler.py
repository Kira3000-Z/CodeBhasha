import re
from keywords import KEYWORDS

def translate_to_python(hinglish_code):
    # 1. Boilerplate imports for the generated environment
    prefix = "import os\n"
    
    # 2. Cleanup: Standardize spaces and remove "Ghost Spaces" (\xA0)
    clean_code = hinglish_code.replace('\xA0', ' ').replace('\t', '    ')
    
    lines = clean_code.splitlines()
    translated_lines = []
    
    # Sort keywords by length to avoid partial matching (e.g., matching 'agar' before 'agar-agar')
    sorted_keys = sorted(KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for line in lines:
        if not line.strip():
            translated_lines.append("")
            continue

        # 3. Extract original indentation
        indent_match = re.match(r"^\s*", line)
        indent = indent_match.group() if indent_match else ""
        content = line.strip()

        # 4. Handle Comments (socho) First
        # If the line is a comment, we swap 'socho' for '#' and skip the rest
        if content.startswith("socho"):
            content = content.replace("socho", "#", 1)
            translated_lines.append(indent + content)
            continue

        # 5. Smart Keyword Replacement (String-Aware)
        for hinglish, python in sorted_keys:
            # Check if keyword is a regex pattern like mano\s+
            if "\\" in hinglish or "+" in hinglish:
                content = re.sub(hinglish, python, content)
            else:
                # String Shield: Only replace if NOT inside double quotes
                pattern = r'\b' + hinglish + r'\b(?=(?:[^"]*"[^"]*")*[^"]*$)'
                content = re.sub(pattern, python, content)

        # 6. Indentation Normalization
        # Ensures that lines like 'mano name = "Kira"' don't have leftover leading spaces
        if not (translated_lines and translated_lines[-1].strip().endswith(':')):
            if len(indent) < 4:
                indent = ""

        translated_lines.append(indent + content)
        
    return prefix + "\n".join(translated_lines)