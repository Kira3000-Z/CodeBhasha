import re
from keywords import KEYWORDS

def translate_to_python(hinglish_code):
    # STEP 1: Global Sanitization
    # Replaces Non-Breaking Spaces (\xA0) and Tabs with standard ASCII spaces
    clean_code = hinglish_code.replace('\xA0', ' ').replace('\t', '    ')
    
    # Prefix for terminal clearing support
    prefix = "import os\n"
    
    lines = clean_code.splitlines()
    translated_lines = []
    
    # Sort keywords by length descending to prevent partial matches 
    # (e.g., matching 'agar' before 'agar-agar')
    sorted_keys = sorted(KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for line in lines:
        if not line.strip():
            translated_lines.append("")
            continue

        # STEP 2: Extract original indentation
        indent_match = re.match(r"^\s*", line)
        indent = indent_match.group() if indent_match else ""
        content = line.strip()

        # STEP 3: Smart Replacement
        for hinglish, python in sorted_keys:
            # Check if the keyword is a regex pattern (like mano\s+)
            if "\\" in hinglish or "+" in hinglish:
                content = re.sub(hinglish, python, content)
            else:
                # Use word boundaries (\b) for standard keywords to avoid 
                # replacing 'saaf' inside a word like 'saaf-safai'
                content = re.sub(r'\b' + hinglish + r'\b', python, content)

        # STEP 4: Indentation Normalization
        # If the line is NOT part of a block (doesn't follow a colon),
        # we strip the leading space left over by keywords like 'mano'
        if not (translated_lines and translated_lines[-1].strip().endswith(':')):
            # If the user didn't manually indent 4 spaces, force it to the margin
            if len(indent) < 4:
                indent = ""

        translated_lines.append(indent + content)
        
    # Combine prefix and translated body
    return prefix + "\n".join(translated_lines)