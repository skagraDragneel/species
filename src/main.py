import os
import argparse
from utils.detect.image_recognition import ImageRecognition


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
    print(image_recognition.get_classes('utils/detect/sample.jpg'))
    print(image_recognition.get_classes('utils/detect/sample.jpg'))
    image_recognition.close()


if __name__ == '__main__':
    main()
