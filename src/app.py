from flask import Flask, request
from flask_cors import CORS

import gatherData
import processData

app = Flask(__name__)
cors = CORS(app)

@app.route('/analyse', methods=['GET','POST'])
def anaylseData() :
	repoName = request.args.get('repoName')
	return gatherData.collectData(repoName)

@app.route('/extract', methods=['GET','POST'])
def extractData() :
	repoName = request.args.get('repoName')
	username = request.args.get('username')
	return processData.extractData(repoName, username)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=5000)