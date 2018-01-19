from anki_object_detection.anki_camera import AnkiCamera
from anki_object_detection.line import Line
import argparse
import json
import numpy as np
import settings


def main():
    settings.init()

    parser = argparse.ArgumentParser(description='Detect a blue cube')
    parser.add_argument('configFile', nargs='?',  default='config.json')

    #parser.add_argument('verticalRightLane', type=int, nargs=4,
    #                    help='the vertical right lane x1 y1 x2 y2')

    #parser.add_argument('horizontalTopLane', type=int, nargs=4,
    #                    help='the horizontal top lane x1 y1 x2 y2')

    #parser.add_argument('horizontalBottomLane', type=int, nargs=4,
    #                    help='the horizontal bottom lane x1 y1 x2 y2')

    args = parser.parse_args()

    with open(args.configFile) as json_data:
        config = json.load(json_data)
    print(config)

    #kafka = Kafka()
    #loop = asyncio.get_event_loop()
    #messageGateway = Websocket(loop)

    max_left_lane = Line(config['maxLeftLane']['x1'], config['maxLeftLane']['x2'], config['maxLeftLane']['y1'], config['maxLeftLane']['y2'])
    max_right_lane = Line(config['maxRightLane']['x1'], config['maxRightLane']['x2'], config['maxRightLane']['y1'], config['maxRightLane']['y2'])
    max_horizontal_upper_lane = Line(config['maxHorizontalUpperLane']['x1'], config['maxHorizontalUpperLane']['x2'], config['maxHorizontalUpperLane']['y1'],
                                     config['maxHorizontalUpperLane']['y2'])
    max_horizontal_lower_lane = Line(config['maxHorizontalLowerLane']['x1'], config['maxHorizontalLowerLane']['x2'], config['maxHorizontalLowerLane']['y1'],
                                     config['maxHorizontalLowerLane']['y2'])

    lower_color_range = np.array([config['lowerColorRange']['hue'], config['lowerColorRange']['saturation'], config['lowerColorRange']['luminance']])
    upper_color_range = np.array([config['upperColorRange']['hue'], config['upperColorRange']['saturation'], config['upperColorRange']['luminance']])

    ankiCamera = AnkiCamera(config["cameraDeviceId"])
    ankiCamera.run(max_left_lane, max_right_lane, max_horizontal_upper_lane, max_horizontal_lower_lane, lower_color_range, upper_color_range)

if __name__ == "__main__":
    main()
