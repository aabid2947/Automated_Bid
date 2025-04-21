from flask import Flask, request, jsonify, render_template
from main import main as run_main
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Extract form data
        url = request.form.get("url")
        username = request.form.get("username")
        password = request.form.get("password")
        security_answer = request.form.get("security_answer", "")

        result = run_main(url, username, password, security_answer)
        return render_template("index.html", error=None, message=result["message"])
    
    except Exception as e:
        return render_template("index.html", error=str(e), message=None)
if __name__ == '__main__':
    app.run(debug=True)