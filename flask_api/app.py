from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/get_topic_names', methods=['GET'])
def get_topic_names():
    try:
        n = request.form["n"]
    except:
        n = 3
    response = jsonify({
        'topic_names': utils.get_topic_names(n)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_top_by_count', methods=['GET', 'POST'])
def get_top_by_count():
    try:
        n = int(request.form["n"])
    except:
        n = 3
    response = jsonify({
        'top_topics': utils.get_top_by_count(n)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_top_by_citation', methods=['GET', 'POST'])
def get_top_by_citation():
    try:
        n = int(request.form["n"])
    except:
        n = 3
    response = jsonify({
        'top_topics': utils.get_top_by_citation(n)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_top_rising', methods=['GET', 'POST'])
def get_top_rising():
    try:
        n = int(request.form["n"])
    except:
        n = 3
    response = jsonify({
        'top_topics': utils.get_top_rising(n)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_relevant_papers', methods=['GET', 'POST'])
def get_relevant_papers():
    input_text = request.form['input_text']

    response = jsonify({
        'relevant_papers': utils.get_relevant_papers(input_text)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    utils.init_model()
    app.run(debug=True)