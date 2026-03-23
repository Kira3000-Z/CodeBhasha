from transpiler import translate_to_python

def run_code_bhasha(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            hinglish_code = f.read()

        # Transpile the code
        python_version = translate_to_python(hinglish_code)

        # CLEANING STEP: Force the first line to have zero indentation
        # We split the lines, strip the whole block, and join them back
        cleaned_python = python_version.strip()

        print(f"--- DEBUG: Generated Code ---\n'{cleaned_python}'\n---")

        print(f"--- Running {file_path} ---")
        # Run the cleaned version
        exec(cleaned_python)

    except Exception as e:
        # This will now show you EXACTLY which line failed
        import traceback
        print(f"Runtime Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run_code_bhasha("game.cb")