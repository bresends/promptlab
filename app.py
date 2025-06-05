import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.j2')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)