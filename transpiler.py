import re
from keywords import KEYWORDS

def translate_to_python(hinglish_code):
    # 1. Add necessary imports for the generated Python environment
    prefix = "import os\n"
    
    # 2. Global Sanitization: Kill Non-Breaking Spaces (\xA0) and Tabs
    clean_code = hinglish_code.replace('\xA0', ' ').replace('\t', '    ')
    
    lines = clean_code.splitlines()
    translated_lines = []
    
    # Sort keywords by length descending to match 'agar-agar' before 'agar'
    sorted_keys = sorted(KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for line in lines:
        if not line.strip():
            translated_lines.append("")
            continue

        # 3. Extract original indentation
        indent_match = re.match(r"^\s*", line)
        indent = indent_match.group() if indent_match else ""
        content = line.strip()

        # 4. Smart Replacement (String-Aware)
        for hinglish, python in sorted_keys:
            # If it's a regex pattern like mano\s+, handle it directly
            if "\\" in hinglish or "+" in hinglish:
                content = re.sub(hinglish, python, content)
            else:
                # Regex magic: Matches 'hinglish' only if followed by an even 
                # number of quotes (meaning it's outside a string literal)
                pattern = r'\b' + hinglish + r'\b(?=(?:[^"]*"[^"]*")*[^"]*$)'
                content = re.sub(pattern, python, content)

        # 5. Indentation Normalization
        # If the line doesn't follow a colon, we ensure no "ghost spaces" remain
        if not (translated_lines and translated_lines[-1].strip().endswith(':')):
            # If the indent is small (likely a leftover from 'mano '), force to margin
            if len(indent) < 4:
                indent = ""

        translated_lines.append(indent + content)
        
    return prefix + "\n".join(translated_lines)