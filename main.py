from anki_object_detection.anki_camera import AnkiCamera
import argparse
from anki_object_detection.line import Line


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
    #loop = asyncio.get_event_loop()
    #messageGateway = Websocket(loop)

    max_left_lane = Line(542, 332, 472, 898)
    max_right_lane = Line(789, 906, 470, 880)
    max_horizontal_upper_lane = Line(260, 1062, 579, 535)
    max_horizontal_lower_lane = Line(132, 1163, 718, 653)

    ankiCamera = AnkiCamera()
    try:
        ankiCamera.run(max_left_lane, max_right_lane, max_horizontal_upper_lane, max_horizontal_lower_lane)
    except KeyboardInterrupt:
        ankiCamera.terminate()

if __name__ == "__main__":
    main()
