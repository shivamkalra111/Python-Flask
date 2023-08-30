import json
import flask
from flask import request, jsonify,g
import  logging
import time
from datetime import datetime


app = flask.Flask(__name__)
#app.config["DEBUG"] = True

logging.basicConfig(filename=r"C:\Users\ealihks\Desktop\Projects\logs\\" + str((datetime.now()).strftime("%Y%m%d%H")) + ".log", filemode='a+')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.before_request
def start_timer():
    g.start = time.time()
    #logger.info("Request::::")
    

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    now = time.time()
    duration = round(now - g.start, 6)  # to the microsecond
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    host = request.host.split(":", 1)[0]
    if request.method == "GET":
        params = request.args.to_dict(flat=False)
    elif request.method == "POST":
        params = request.form.to_dict(flat=False)
        if not bool(params):
            params = request.get_json(force=True)
        
        
    request_id = request.headers.get("X-Request-ID", "")
    log_params = {
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "request_time":(datetime.now()).strftime("%Y-%m/%d %H:%M:%S"),
        "duration": duration,
        "ip": ip_address,
        "host": host,
        "params": params,
        "request_id": request_id,
    }
    #print(log_params)
    app.logger.info(log_params)
    return response

@app.route('/', methods=['GET'])
def home():
    return "<h1>Flask is working for you</p>"


@app.route('/get', methods=['GET','POST'])
def Unified():
    #print('in function')
    resp=processRequest(request)
    return jsonify(resp)
  

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


# if __name__ == "__ main__":
#     app.run()

#local
#app.run()

#live
app.run(host='127.0.0.1', port=5000,threaded=True)
