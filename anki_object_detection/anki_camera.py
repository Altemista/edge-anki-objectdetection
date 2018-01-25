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
import settings
import signal
import base64
import atexit
import traceback
from datetime import datetime

class AnkiCamera(object):
    def __init__(self, cameraDeviceId):
        self.adasClient = None
        self.twinClient = None
        atexit.register(self.terminate)

        # init the websocket
        self.httpAdasWebsocket = os.environ.get('HTTP_WEBSOCKET')

        if self.httpAdasWebsocket is None:
            print('Using 127.0.0.1:8003 as default websocket adas server.')
            self.httpAdasWebsocket = '127.0.0.1:8003'
        else:
            print("Using ", self.httpAdasWebsocket, "as adas websocket")


        self.httpTwinWebsocket = os.environ.get("HTTP_IMAGE_WEBSOCKET")
        if self.httpTwinWebsocket is None:
            print('Using 127.0.0.1:8001 as default twin server.')
            self.httpTwinWebsocket = '127.0.0.1:8001'
        else:
            print("Using ", self.httpTwinWebsocket, "as twin websocket")

        self.cameraDeviceId = cameraDeviceId

        self.adas_connect_timer_started = False
        self.connectAdas()

        self.twin_connect_timer_started = False
        self.connectTwin()

    def start_adas_connection_timer(self):
        if not self.adas_connect_timer_started:
            self.adasConnectionTimer = Timer(5.0, self.connectAdas)
            self.adas_connect_timer_started = True
            self.adasConnectionTimer.start()

    def connectAdas(self):
        try:
            self.adasClient = AnkiWebSocketClient("ws://" + self.httpAdasWebsocket + "/status")
            self.adasClient.connect()
            self.adasConnectionTimer.cancel()
            self.adas_connect_timer_started = False
            print("Connected to adas websocket")
        except Exception:
            self.adas_connect_timer_started = False
            self.start_adas_connection_timer()
            print("Could not connect to adas websocket")

    def start_twin_connection_timer(self):
        if not self.twin_connect_timer_started:
            self.twinConnectionTimer = Timer(5.0, self.connectTwin)
            self.twin_connect_timer_started = True
            self.twinConnectionTimer.start()

    def connectTwin(self):
        try:
            self.twinClient = AnkiWebSocketClient("ws://" + self.httpTwinWebsocket + "/image")
            self.twinClient.connect()
            self.twinConnectionTimer.cancel()
            self.twin_connect_timer_started = False
            print("Connected to twin websocket")
        except Exception:
            self.twin_connect_timer_started = False
            self.start_twin_connection_timer()
            print("Could not connect to twin websocket")

    def run(self, max_left_lane, max_right_lane,
            max_horizontal_upper_lane,
            max_horizontal_lower_lane,
            lower_color_range,
            upper_color_range):
        try:
            print("Running")

            self.video_capture = cv2.VideoCapture(self.cameraDeviceId)
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

            cv2.waitKey(5000)

            cube_detector = CubeDetector(lower_color_range, upper_color_range)
            lane_detector = LaneDetector()

            last_horizontal_lane = -1
            last_vertical_lane = -1

            count_failed_frames = 0

            while(True):
                # Capture frame-by-frame
                ret, frame = self.video_capture.read()
                count_failed_frames += 1

                #frame = cv2.imread("anki_object_detection/images/cube_left_lane_1.jpg")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if ret:
                    cube = cube_detector.detect(frame, max_left_lane, max_right_lane, max_horizontal_upper_lane, max_horizontal_lower_lane)

                    if cube.x != 0 and cube.y != 0 and cube.width != 0 and cube.height != 0:
                        horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                                          max_horizontal_upper_lane, max_horizontal_lower_lane)

                        if horizontal_lane != last_horizontal_lane:
                            #positionMessage = json.dumps(PositionUpdateMessage(-1, horizontal_lane).__dict__)
                            positionMessage = PositionUpdateMessage(-1, horizontal_lane).toCsv()
                            print("INFO: Sending message " + positionMessage)
                            try:
                                print("INFO: Sending message " + positionMessage)
                                self.adasClient.send(positionMessage)
                            except Exception:
                                print("ERROR: Message could not be sent.")
                                self.start_adas_connection_timer()


                            last_horizontal_lane = horizontal_lane

                        if vertical_lane != last_vertical_lane:
                            #positionMessage = json.dumps(PositionUpdateMessage(-2, vertical_lane).__dict__)
                            positionMessage = PositionUpdateMessage(-2, vertical_lane).toCsv()
                            try:
                                print("INFO: Sending message " + positionMessage)
                                self.adasClient.send(positionMessage)
                            except Exception:
                                self.start_adas_connection_timer()
                                print("ERROR: Message could not be sent.")

                            last_vertical_lane = vertical_lane
                    else:
                        try:
                            horizontal_lane = -1
                            vertical_lane = -1

                            if horizontal_lane != last_horizontal_lane:
                                resetMessage = PositionUpdateMessage(-1, -1);
                                resetMessage.msgTimestamp = datetime.min.isoformat(timespec='milliseconds')+"Z";
                                resetMessageCsv = resetMessage.toCsv()
                                print("INFO: Sending message " + resetMessageCsv)
                                self.adasClient.send(resetMessageCsv)

                            if vertical_lane != last_vertical_lane:
                                resetMessage = PositionUpdateMessage(-2, -1);
                                resetMessage.msgTimestamp = datetime.min.isoformat(timespec='milliseconds')+"Z";
                                resetMessageCsv = resetMessage.toCsv()
                                print("INFO: Sending message " + resetMessageCsv)
                                self.adasClient.send(resetMessageCsv)

                            last_horizontal_lane = horizontal_lane
                            last_vertical_lane = vertical_lane
                        except Exception:
                            self.start_adas_connection_timer()
                            print("ERROR: Message could not be sent.")
                            traceback.print_exc(file=sys.stdout)


                    label = "Lane hor: " + str(last_horizontal_lane) + ", lane vert: " + str(last_vertical_lane)
                    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    print(label)

                    #resize image
                    resized_image = cv2.resize(frame, (800, 600))
                    #write image to disk
                    cv2.imwrite("capture.jpg", resized_image)
                    with open("capture.jpg", "rb") as imageFile:
                        base64Image = base64.b64encode(imageFile.read())
                        try:
                            print("INFO: Sending image as base64")
                            self.twinClient.send(base64Image)
                        except Exception:
                            self.start_twin_connection_timer()
                            print("ERROR: Image could not be sent")


                    if settings.enable_debug_images:
                        cv2.namedWindow('test', cv2.WINDOW_NORMAL)
                        cv2.imshow('test', frame)
                    cv2.waitKey(10)
                else:
                    # If we could not initialize the camera after 100 frames, simply exit
                    count_failed_frames += 1
                    if count_failed_frames > 100:
                        print("ERROR: Could not init camera")
                        os.kill(os.getpid(), signal.SIGKILL)
                        sys.exit(0)
        except:
            print("Exception occurred")
            traceback.print_exc(file=sys.stdout)
        finally:
            # When everything done, release the capture
            self.video_capture.release()
            cv2.destroyAllWindows()

            self.terminate()

    def terminate(self):
        print("Terminate")
        os.kill(os.getpid(), signal.SIGKILL)
        sys.exit(0)
