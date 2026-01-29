"""
Simple Flask web application for Selenium testing demonstration
"""
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for demo purposes
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append({'id': len(tasks) + 1, 'task': task, 'completed': False})
        return jsonify({'success': True, 'task': task})
    return jsonify({'success': False, 'error': 'No task provided'})

@app.route('/clear_tasks', methods=['POST'])
def clear_tasks():
    tasks.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    # Use host='0.0.0.0' to make it accessible from browser and tests
    # This is safe for local development
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)