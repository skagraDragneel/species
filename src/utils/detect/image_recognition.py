import tensorflow as tf
import cv2 as cv
import utils.detect.label_map_util as label_util


class ImageRecognition:
    def __init__(self, graph_location: str, graph_labels):
        with tf.gfile.FastGFile(graph_location, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        self.sess = tf.Session()
        # Restore session
        self.sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        self.labels = label_util.get_label_map_dict(graph_labels)

    def get_classes(self, image_location: str):
        img = cv.imread(image_location)
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

        # Run the model
        out = self.sess.run([self.sess.graph.get_tensor_by_name('num_detections:0'),
                            self.sess.graph.get_tensor_by_name('detection_scores:0'),
                            self.sess.graph.get_tensor_by_name('detection_boxes:0'),
                            self.sess.graph.get_tensor_by_name('detection_classes:0')],
                            feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        detection_names = []
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.3:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
            detection_names.append(self.labels[classId])
        return detection_names

    def close(self):
        self.sess.close()
