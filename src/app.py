from flask import Flask, request

app = Flask(__name__)

@app.route('/repoName', methods=['GET','POST'])
def getRepoData() :
	repo = request.args.get('repoName')
	return repo

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=5000)