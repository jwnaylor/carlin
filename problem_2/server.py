from flask import Flask, request, render_template, send_from_directory, jsonify
from pprint import pprint, pformat
from cleaner import clean_data
from utils import read_json_from_file, dumpsutf8
import json

app = Flask(__name__, static_url_path='')
app.debug=False

sample_json=read_json_from_file('./sample.json')
pprint(sample_json)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('js', path)

@app.route('/hello')
def hello():
    return "Hello\n"

@app.route('/try', methods=['GET'])
def enter():
    return render_template('cleaned.html', cleaned_json=None, cleaning_report=None)

@app.route('/send', methods=['POST'])
def handle_send_post():
    if 'Content-Type' not in request.headers:
        message="No Content-Type request header"
        app.logger.error(message)
        return render_error(message)
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        message = "Unsupported Content-Type: {}".format(content_type)
        app.logger.error(message)
        return render_error(message)

    accept = 'text/html'
    if 'Accept' in request.headers:
        accept = request.headers.get('Accept')
    if accept.find('application/json') == -1 and accept.find('text/html') == -1:
        message = "Unsupported MIME type requested {}".format(accept)
        app.logger.error(message)
        return render_error(message)
    app.logger.info("Trying")
    payload=None
    try:
        payload = request.get_json()
        app.logger.info("GOT JSON")
    except Exception as e:
        return render_error("Failed to parse JSON")

    report=[]
    cleaned_data=clean_data(payload, sample_json, report)
    if accept.find('application/json') != -1:
        return render_cleaned_json(cleaned_data, report)
    else:
        return render_cleaned_content(cleaned_data, report)

# root of json document must be an object/dictionary not an array/list
# e.g., {[]} not [{}]

def render_cleaned_json(cleaned_data, report):
    result={"result":"success", "cleaned_data" : dumpsutf8(cleaned_data), "cleaning_report" : report}
    return jsonify(result), 200, {'Content-Type' : 'application/json'}

def render_cleaned_report(cleaned_data, report):
    return render_template('cleaned.html', cleaned_json=dumpsutf8(cleaned_data), cleaning_report=report)

def render_cleaned_content(cleaned_data, report):
    return render_template('content.html', cleaned_json=dumpsutf8(cleaned_data), cleaning_report=report)

def render_error(message):
    return render_template('error.html', message=message), 500



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)



