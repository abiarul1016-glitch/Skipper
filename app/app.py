import subprocess

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/run-skipper', methods=['POST'])
def run_skipper():

    result = subprocess.check_output(['uv', 'run', 'apple.py']).decode('utf-8')
    return jsonify(output=result)

if __name__ == '__main__':
    app.run(debug=True)