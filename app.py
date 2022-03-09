import os

from flask import Flask, render_template
from flask_cors import CORS

from utils import api_result as api_result

from controllers import file_controller

import env

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
CORS(app)
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/')
def index():
    return render_template("index.html")
# -------------- #
@app.errorhandler(401)
def method_401(e):
	return api_result.status_result(401)

def method_403(e):
	return api_result.status_result(403)

@app.errorhandler(404)
def method_404(e):
	return api_result.status_result(404, description='requested URL was not found on the server')

@app.errorhandler(405)
def method_405(e):
	return api_result.status_result(405, description='http method is not allowed for the requested URL')

# ------ Registering Blueprints ------ #
app.register_blueprint(file_controller, url_prefix='/file')

# ------------ #
if __name__ == '__main__':
    app.run(host=env.SERVER_HOST, port=env.SERVER_PORT, debug=env.SERVER_DEBUG)