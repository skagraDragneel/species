import os
import argparse
from utils.detect.image_recognition import ImageRecognition
from flask import Flask, request, render_template, jsonify
from configparser import ConfigParser

app = Flask(__name__)
image_recognition = None
config = None


def get_care_url(names: str) -> str:
    '''
    Goes through the list of recognized objects from the object detection and returns
    the url for the first recognized object that has a corresponding url. If none
    are found, returns empty string
    '''
    print(names)
    for name in names:
        name.lower().replace(' ', '_')
        if name in config['animal_links']:
            return config['animal_links'][name]
    return ""


@app.route('/')
def index():
    '''
    Main page where user send photo and views the corresponding instructions
    '''
    return render_template('main.html')


@app.route('/get_care', methods=['POST'])
def get_care():
    '''
    Used to get the care url.
    Expects the request to contain a base64 encoded string containing the image to 
    analyze.
    Returns json with the url to the instructions
    '''
    image_b64 = request.json['image_data'].split(',')[1]
    care_url = get_care_url(image_recognition.get_classes(image_b64))
    return jsonify({'url': care_url}), 200, {'ContentType': 'application/json'}


def main():
    '''
    Handles running the app including initializing image detection with values passed
    in from the user
    '''
    global image_recognition
    global config
    # Default Values
    current_dir = os.path.abspath(os.path.dirname(__file__))
    default_model = os.path.join(current_dir, 'model/frozen_inference_graph.pb')
    default_labels = os.path.join(current_dir, 'model/mscoco_label_map.pbtxt')
    default_config = os.path.join(current_dir, 'care.ini')

    # Argument Parsing
    parser = argparse.ArgumentParser(description='Run the species specific app')
    parser.add_argument('--frozen_model', default=default_model,
                        help='location of the frozen tensorflow model')
    parser.add_argument('--labels', default=default_labels,
                        help='location of the tensorflow labels')
    parser.add_argument('--config', default=default_config)

    args = parser.parse_args()

    image_recognition = ImageRecognition(args.frozen_model, args.labels)
    config = ConfigParser()
    config.read(default_config)

    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    main()
