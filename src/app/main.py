#USER LOGIN
#USER SELECT PLAYLIST
#click spot it
#CREATE MODEL USING SCRIPT
#LOAD MODEL
#click find new songs
#ASSIGN REDDIT SONGS TO CLUSTERS

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    input_data = request.form['input_data']
    # Do some processing with the input data here
    processed_data = [f"{input_data}_{num}" for num in range(8)]
    # Render a new page with the processed data
    return render_template('result.html', list_of_playlists=processed_data)

@app.route('/recommend', methods=['POST'])
def transform_fruit():
    # Get the selected fruit from the request data
    selected_fruit = request.json.get('playlist')

    # Do some data transformation
    transformed_playlist = [f"{selected_fruit}_{num}" for num in range(8)]

    # Return the transformed data as JSON
    return jsonify({'result': transformed_playlist})

if __name__ == "__main__":
    app.run(debug = True)