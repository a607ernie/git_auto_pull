from flask import jsonify,request,Flask
import subprocess
from pathlib import Path,PurePath
app = Flask(__name__)

@app.route('/')
def api_root():
    return "welcome to github auto deploy"

@app.route('/webhook',methods=['POST'])
def webhook():
    data = request.json
    repository_name = data['repository']['name']
    p = subprocess.run("cd %s && git pull"%repository_name, shell=True,cwd=Path(__file__).parent.absolute())
    return ""

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)