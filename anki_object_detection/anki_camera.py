# -*- coding: utf-8 -*-
import cv2 as cv2
from anki_object_detection.cube_detector import CubeDetector
from anki_object_detection.lane_detector import LaneDetector
from anki_object_detection.lane_calculator import LaneCalculator
from anki_object_detection.position_update_message import PositionUpdateMessage
from anki_object_detection.anki_websocket_client import AnkiWebSocketClient
import json
import os


class AnkiCamera(object):
    def __init__(self):
        # init the websocket
        self.httpWebsocket = os.environ.get('HTTP_WEBSOCKET')

        if self.httpWebsocket is None:
            print('Using 127.0.0.1 as default websocket server.')
            self.httpWebsocket='127.0.0.1'

        self.client = AnkiWebSocketClient("ws://" + self.httpWebsocket + ":8003/status")
        self.client.connect()

    def run(self, max_left_lane, max_right_lane, max_horizontal_upper_lane, max_horizontal_lower_lane):
        try:
            print("Running")

            video_capture = cv2.VideoCapture(0)
            cube_detector = CubeDetector()
            lane_detector = LaneDetector()

            last_horizontal_lane = None
            last_vertical_lane = None

            while(True):
                # Capture frame-by-frame
                ret, frame = video_capture.read()
                #frame = cv2.imread("anki_object_detection/images/cube_left_lane_1.jpg")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                cube = cube_detector.detect(frame)

                if cube.x != 0 and cube.y != 0:
                    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

                    if horizontal_lane != last_horizontal_lane:
                        positionMessage = json.dumps(PositionUpdateMessage(-1, horizontal_lane).__dict__)
                        print("INFO: Sending message " + positionMessage)
                        self.client.send(positionMessage)
                        last_horizontal_lane = horizontal_lane

                    if vertical_lane != last_vertical_lane:
                        positionMessage = json.dumps(PositionUpdateMessage(-2, vertical_lane).__dict__)
                        print("INFO: Sending message " + positionMessage)
                        self.client.send(positionMessage)
                        last_vertical_lane = vertical_lane

                cv2.namedWindow('test', cv2.WINDOW_NORMAL)
                cv2.imshow('test', frame)
                cv2.waitKey(10)

            # When everything done, release the capture
            video_capture.release()
            video_capture.destroyAllWindows()
        finally:
            self.terminate()

    def terminate(self):
        print("Terminate")

        if not self.client.terminated:
            self.client.close()
            self.client._th.join()
            self.client = None