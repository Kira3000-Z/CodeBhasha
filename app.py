import os
import sys
import io
import eventlet

# This 'monkey_patch' is crucial for making the server 
# handle the "pause and wait" logic correctly.
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from transpiler import translate_to_python

app = Flask(__name__)
app.config['SECRET_KEY'] = 'codebhasha_secret_key'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# This is our "Post Office Box" for input
user_input_queue = eventlet.queue.Queue()

def socket_input(prompt):
    """
    This replaces Python's internal input().
    It sends a request to the browser and STOPS execution 
    until data arrives in the queue.
    """
    # 1. Ask the browser for input
    socketio.emit('input_request', {'prompt': prompt})
    
    # 2. WAIT here. The code will not move to the next line 
    # until user_input_queue.put() is called elsewhere.
    user_response = user_input_queue.get() 
    return user_response

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('input_response')
def handle_input_response(data):
    """
    This is triggered when the browser sends the 
    actual typed name back to the server.
    """
    val = data.get('value', '')
    user_input_queue.put(val) # Put the name in the box!

@socketio.on('run_code')
def handle_run(data):
    hinglish_code = data.get('code', '')
    
    try:
        # 1. Transpile
        python_code = translate_to_python(hinglish_code)
        emit('transpiled_python', {'python': python_code})
        
        # 2. Redirect Print (dikhao)
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        # 3. Execution Logic
        # We run this in a 'spawn' thread so the server stays alive while waiting
        def run_task():
            try:
                # Override input with our custom socket_input
                exec(python_code, {"__name__": "__main__", "input": socket_input})
                socketio.emit('output_response', {'output': output_buffer.getvalue()})
            except Exception as e:
                socketio.emit('output_response', {'output': f"Runtime Error: {str(e)}"})
            finally:
                sys.stdout = sys.__stdout__

        eventlet.spawn(run_task)

    except Exception as e:
        emit('output_response', {'output': f"Transpilation Error: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, debug=True)