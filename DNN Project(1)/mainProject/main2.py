from flask import Flask, render_template, jsonify
import subprocess  # To run the Python script

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page with the button

@app.route('/run_script', methods=['POST'])
def run_script():
    # Run the main.py script when the button is clicked
    result = subprocess.run(['python', 'c:/Users/shail sharma/Desktop/DNN Project(1)/mainProject/main.py'], capture_output=True, text=True)
    return jsonify({'output': result.stdout})  # Return the script's output

if __name__ == "__main__":
    app.run(debug=True)
