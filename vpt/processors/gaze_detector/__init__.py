"""Human facial landmark detector based on Convolutional Neural Network."""
import math
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # To disable TF's warnings

import cv2
import numpy as np
import tensorflow as tf
from rx import Observable
from rx.subject import Subject
from tensorflow import keras

from vpt.data_structures import VideoFrame
from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase

tf.get_logger().setLevel('ERROR')


class FaceDetector:
    """Detect human face from image"""

    def __init__(self,
                 dnn_proto_text='models/deploy.prototxt',
                 dnn_model='models/res10_300x300_ssd_iter_140000.caffemodel'):
        """Initialization"""
        self.face_net = cv2.dnn.readNetFromCaffe(dnn_proto_text, dnn_model)
        self.detection_result = None

    def get_faceboxes(self, image, threshold=0.5):
        """
        Get the bounding box of faces in image using dnn.
        """
        rows, cols, _ = image.shape

        confidences = []
        faceboxes = []

        self.face_net.setInput(cv2.dnn.blobFromImage(
            image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False))
        detections = self.face_net.forward()

        for result in detections[0, 0, :, :]:
            confidence = result[2]
            if confidence > threshold:
                x_left_bottom = int(result[3] * cols)
                y_left_bottom = int(result[4] * rows)
                x_right_top = int(result[5] * cols)
                y_right_top = int(result[6] * rows)
                confidences.append(confidence)
                faceboxes.append(
                    [x_left_bottom, y_left_bottom, x_right_top, y_right_top])

        self.detection_result = [faceboxes, confidences]

        return confidences, faceboxes


class MarkDetector:
    """Facial landmark detector by Convolutional Neural Network"""

    def __init__(self, saved_model='models/pose_model'):
        """Initialization"""
        # A face detector is required for mark detection.
        self.face_detector = FaceDetector()

        self.cnn_input_size = 128
        self.marks = None

        # Restore model from the saved_model file.
        self.model = keras.models.load_model(saved_model)

    @staticmethod
    def move_box(box, offset):
        """Move the box to direction specified by vector offset"""
        left_x = box[0] + offset[0]
        top_y = box[1] + offset[1]
        right_x = box[2] + offset[0]
        bottom_y = box[3] + offset[1]
        return [left_x, top_y, right_x, bottom_y]

    @staticmethod
    def get_square_box(box):
        """Get a square box out of the given box, by expanding it."""
        left_x = box[0]
        top_y = box[1]
        right_x = box[2]
        bottom_y = box[3]

        box_width = right_x - left_x
        box_height = bottom_y - top_y

        # Check if box is already a square. If not, make it a square.
        diff = box_height - box_width
        delta = int(abs(diff) / 2)

        if diff == 0:  # Already a square.
            return box
        if diff > 0:  # Height > width, a slim box.
            left_x -= delta
            right_x += delta
            if diff % 2 == 1:
                right_x += 1
        else:  # Width > height, a short box.
            top_y -= delta
            bottom_y += delta
            if diff % 2 == 1:
                bottom_y += 1

        # Make sure box is always square.
        assert ((right_x - left_x) == (bottom_y - top_y)), 'Box is not square.'

        return [left_x, top_y, right_x, bottom_y]

    @staticmethod
    def box_in_image(box, image):
        """Check if the box is in image"""
        rows = image.shape[0]
        cols = image.shape[1]
        return box[0] >= 0 and box[1] >= 0 and box[2] <= cols and box[3] <= rows

    def extract_cnn_facebox(self, image):
        """Extract face area from image."""
        _, raw_boxes = self.face_detector.get_faceboxes(
            image=image, threshold=0.5)
        res = []
        for box in raw_boxes:
            # Move box down.
            # diff_height_width = (box[3] - box[1]) - (box[2] - box[0])
            offset_y = int(abs((box[3] - box[1]) * 0.1))
            box_moved = self.move_box(box, [0, offset_y])

            # Make box square.
            facebox = self.get_square_box(box_moved)

            if self.box_in_image(facebox, image):
                res.append(facebox)

        return res

    def detect_marks(self, image_np):
        """Detect marks from image"""

        # # Actual detection.
        predictions = self.model.signatures["predict"](
            tf.constant(image_np, dtype=tf.uint8))

        # Convert predictions to landmarks.
        marks = np.array(predictions['output']).flatten()[:136]
        marks = np.reshape(marks, (-1, 2))

        return marks


mark_detector = MarkDetector()
font = cv2.FONT_HERSHEY_SIMPLEX
# 3D model points.
model_points = np.array([
    (0.0, 0.0, 0.0),  # Nose tip
    (0.0, -330.0, -65.0),  # Chin
    (-225.0, 170.0, -135.0),  # Left eye left corner
    (225.0, 170.0, -135.0),  # Right eye right corner
    (-150.0, -150.0, -125.0),  # Left Mouth corner
    (150.0, -150.0, -125.0)  # Right mouth corner
])


class GazeDetector(ProcessorBase[np.ndarray]):
    """Detects if the user is looking at the screen or not"""
    _subj: Subject

    def __init__(self, video_source: SourceBase[VideoFrame]):
        self._subj = Subject()
        self.stopped = True
        self.sources = [video_source]
        video_source.output.subscribe(self.process_frame)

    def process_frame(self, frame: VideoFrame):
        """Processes each incoming frame to detect gaze"""
        size = frame.frame.shape
        # Camera internals
        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )

        faceboxes = mark_detector.extract_cnn_facebox(frame.frame)

        if len(faceboxes) == 0:
            self._subj.on_next(None)

        # For each facebox found in the picture, extract 128x128 region
        #   and pass it to PnP solve method
        for facebox in faceboxes:
            face_img = frame.frame[facebox[1]: facebox[3],
                       facebox[0]: facebox[2]]
            face_img = cv2.resize(face_img, (128, 128))
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

            # Find facial marks on the picture
            marks = mark_detector.detect_marks([face_img])
            marks *= (facebox[2] - facebox[0])
            marks[:, 0] += facebox[0]
            marks[:, 1] += facebox[1]
            shape = marks.astype(np.uint)

            image_points = np.array([
                shape[30],  # Nose tip
                shape[8],  # Chin
                shape[36],  # Left eye left corner
                shape[45],  # Right eye right corne
                shape[48],  # Left Mouth corner
                shape[54]  # Right mouth corner
            ], dtype="double")

            # Solve PnP
            dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
            (_success, rotation_vector, _translation_vector) = cv2.solvePnP(
                model_points, image_points, camera_matrix,
                dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

            # Normalize x axis values
            if rotation_vector[0] < 0:
                rotation_vector[0] += math.pi + math.pi
            rotation_vector[0] -= math.pi

            rot_arr = np.array(rotation_vector).reshape(1, 3)

            # Append the current rotation vector to the data
            # data = np.empty(shape=(0, 3))

            # data = np.concatenate((data, rot_arr), axis=0)
            # debug.draw_rotation_values()

            self._subj.on_next(rot_arr)

    @property
    def output(self) -> Observable:
        '''The getter for the gaze codes observable.'''
        return self._subj
