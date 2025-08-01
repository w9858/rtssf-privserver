from flask import Flask, g, send_from_directory
import time
from api import api

app = Flask("Spyce")

app.register_blueprint(api)

@app.after_request
def add_headers(response):
    if getattr(g, 'is_api', False):
        response.headers['Content-Type'] = 'application/x-protobuf'
        response.headers['X_SQLITE_VER'] = '99'
        response.headers['X_RES_STATUS'] = '0'
        response.headers['X_TIMESTAMP'] = str(int(time.time()))
        # response.headers['X_ERROR_MSG'] = ''
    return response

# Static files
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('./img/assets', filename)

@app.route('/sqlites/<path:filename>')
def serve_sqlites(filename):
    return send_from_directory('./img/sqlites', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('./img/images', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=21219, debug=True)
