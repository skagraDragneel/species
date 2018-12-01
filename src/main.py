import os
import argparse
from utils.detect.image_recognition import ImageRecognition
from flask import Flask, request, render_template, jsonify
from configparser import ConfigParser

app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
default_model = os.path.join(current_dir, 'model/frozen_inference_graph.pb')
default_labels = os.path.join(current_dir, 'model/mscoco_label_map.pbtxt')
image_recognition = ImageRecognition(default_model, default_labels)
default_config = os.path.join(current_dir, 'care.ini')
config = ConfigParser()
config.read(default_config)


def get_care_url(names):
    print(names)
    for name in names:
        name.lower().replace(' ', '_')
        if name in config['animal_links']:
            return config['animal_links'][name]
    return ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main_page')
def main_route():
    return render_template('main.html')


@app.route('/get_care', methods=['POST'])
def name():
    image_b64 = request.json['image_data'].split(',')[1]
    care_url = get_care_url(image_recognition.get_classes(image_b64))
    return jsonify({'url': care_url}), 200, {'ContentType': 'application/json'}


def main():
    # Default Values
    current_dir = os.path.abspath(os.path.dirname(__file__))
    default_model = os.path.join(current_dir, 'model/frozen_inference_graph.pb')
    default_labels = os.path.join(current_dir, 'model/mscoco_label_map.pbtxt')

    # Argument Parsing
    parser = argparse.ArgumentParser(description='Run the species specific app')
    parser.add_argument('--frozen_model', default=default_model,
                        help='location of the frozen tensorflow model')
    parser.add_argument('--labels', default=default_labels,
                        help='location of the tensorflow labels')

    args = parser.parse_args()

    image_recognition = ImageRecognition(args.frozen_model, args.labels)
    print(image_recognition.get_classes('model/zebra.jpg'))
    image_recognition.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
