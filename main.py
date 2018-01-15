import cv2 as cv2
from anki_object_detection.cube_detector import CubeDetector
from anki_object_detection.lane_detector import LaneDetector
from anki_object_detection.lane_calculator import LaneCalculator
from anki_object_detection.line import Line
from anki_object_detection.kafka import Kafka
from anki_object_detection.position_update_message import PositionUpdateMessage
from anki_object_detection.websocket import Websocket
import argparse
import json
import asyncio


def main():

    parser = argparse.ArgumentParser(description='Detect a blue cube')
    #parser.add_argument('verticalLeftLane', type=int, nargs=4,
    #                    help='the vertical left lane x1 y1 x2 y2')

    #parser.add_argument('verticalRightLane', type=int, nargs=4,
    #                    help='the vertical right lane x1 y1 x2 y2')

    #parser.add_argument('horizontalTopLane', type=int, nargs=4,
    #                    help='the horizontal top lane x1 y1 x2 y2')

    #parser.add_argument('horizontalBottomLane', type=int, nargs=4,
    #                    help='the horizontal bottom lane x1 y1 x2 y2')

    args = parser.parse_args()

    #kafka = Kafka()
    loop = asyncio.get_event_loop()
    messageGateway = Websocket(loop)

    loop.run_until_complete(messageGateway.coroutine)
    loop.run_until_complete(ioloop.create_task(video_loop))
    loop.run_forever()
    loop.close()


async def video_loop():
    video_capture = cv2.VideoCapture(1)
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

        max_left_lane = Line(542, 332, 472, 898)
        max_right_lane = Line(789, 906, 470, 880)
        max_horizontal_upper_lane = Line(260, 1062, 579, 535)
        max_horizontal_lower_lane = Line(132, 1163, 718, 653)

        cube = cube_detector.detect(frame)

        if cube.x != 0 and cube.y != 0:
            horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                              max_horizontal_upper_lane, max_horizontal_lower_lane)

            if horizontal_lane != last_horizontal_lane:
                positionMessage = json.dumps(PositionUpdateMessage(-1, horizontal_lane).__dict__)
                print("INFO: Sending message " + positionMessage)
                messageGateway.send(positionMessage)
                last_horizontal_lane = horizontal_lane

            if vertical_lane != last_vertical_lane:
                positionMessage = json.dumps(PositionUpdateMessage(-2, vertical_lane).__dict__)
                print("INFO: Sending message " + positionMessage)
                messageGateway.send(positionMessage)
                last_vertical_lane = vertical_lane

        cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        cv2.imshow('test', frame)
        cv2.waitKey(10)

    # When everything done, release the capture
    video_capture.release()
    video_capture.destroyAllWindows()


if __name__ == "__main__":
    main()
