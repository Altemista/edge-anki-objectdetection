# -*- coding: utf-8 -*-
import cv2 as cv2
from anki_object_detection.cube_detector import CubeDetector
from anki_object_detection.lane_detector import LaneDetector
from anki_object_detection.lane_calculator import LaneCalculator
from anki_object_detection.position_update_message import PositionUpdateMessage
from anki_object_detection.anki_websocket_client import AnkiWebSocketClient
import json
import os
from threading import Timer
import sys


class AnkiCamera(object):
    def __init__(self, cameraDeviceId):
        # init the websocket
        self.httpWebsocket = os.environ.get('HTTP_WEBSOCKET')

        if self.httpWebsocket is None:
            print('Using 127.0.0.1 as default websocket server.')
            self.httpWebsocket='127.0.0.1'

        self.cameraDeviceId = cameraDeviceId

        self.timer_started = False
        self.connect()

    def start_connection_timer(self):
        if not self.timer_started:
            self.connectionTimer = Timer(5.0, self.connect)
            self.timer_started = True
            self.connectionTimer.start()

    def connect(self):
        try:
            self.client = AnkiWebSocketClient("ws://" + self.httpWebsocket + ":8003/status")
            self.client.connect()
            self.connectionTimer.cancel()
            self.timer_started = False
            print("Connected to websocket")
        except Exception:
            self.timer_started = False
            self.start_connection_timer()
            print("Could not connect to websocket")

    def run(self, max_left_lane, max_right_lane,
            max_horizontal_upper_lane,
            max_horizontal_lower_lane,
            lower_color_range,
            upper_color_range):
        try:
            print("Running")

            video_capture = cv2.VideoCapture(self.cameraDeviceId)

            cube_detector = CubeDetector(lower_color_range, upper_color_range)
            lane_detector = LaneDetector()

            last_horizontal_lane = None
            last_vertical_lane = None

            count_failed_frames = 0

            while(True):
                # Capture frame-by-frame
                ret, frame = video_capture.read()
                count_failed_frames += 1

                #frame = cv2.imread("anki_object_detection/images/cube_left_lane_1.jpg")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if frame is not None:
                    cube = cube_detector.detect(frame)

                    if cube.x != 0 and cube.y != 0:
                        horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                                          max_horizontal_upper_lane, max_horizontal_lower_lane)

                        if horizontal_lane != last_horizontal_lane:
                            #positionMessage = json.dumps(PositionUpdateMessage(-1, horizontal_lane).__dict__)
                            positionMessage = PositionUpdateMessage(-1, horizontal_lane).toCsv()
                            print("INFO: Sending message " + positionMessage)
                            try:
                                print("INFO: Sending message " + positionMessage)
                                self.client.send(positionMessage)
                            except Exception:
                                print("ERROR: Message could not be sent.")
                                self.start_connection_timer()


                            last_horizontal_lane = horizontal_lane

                        if vertical_lane != last_vertical_lane:
                            #positionMessage = json.dumps(PositionUpdateMessage(-2, vertical_lane).__dict__)
                            positionMessage = PositionUpdateMessage(-2, vertical_lane).toCsv()
                            try:
                                print("INFO: Sending message " + positionMessage)
                                self.client.send(positionMessage)
                            except Exception:
                                self.start_connection_timer()
                                print("ERROR: Message could not be sent.")

                            last_vertical_lane = vertical_lane

                    label = "Lane hor: " + str(last_horizontal_lane) + ", lane vert: " + str(last_vertical_lane)
                    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                    cv2.namedWindow('test', cv2.WINDOW_NORMAL)
                    cv2.imshow('test', frame)
                    cv2.waitKey(10)
                else:
                    # If we could not initialize the camera after 100 frames, simply exit
                    count_failed_frames += 1
                    if count_failed_frames > 100:
                        raise EnvironmentError("Could not init camera")

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
        sys.exit()
