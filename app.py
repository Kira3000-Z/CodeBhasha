from flask import Flask, render_template, request, jsonify
import sys
import io
from transpiler import translate_to_python

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    hinglish_code = request.json.get('code', '')
    
    # 1. Transpile
    try:
        python_code = translate_to_python(hinglish_code)
        
        # 2. Capture Output
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        # 3. Execute
        exec(python_code, {"__name__": "__main__"})
        
        sys.stdout = sys.__stdout__
        result = output_buffer.getvalue()
    except Exception as e:
        result = f"Error: {str(e)}"
    
    return jsonify({"output": result, "python": python_code})

if __name__ == '__main__':
    app.run(debug=True)