import cv2 as cv2
from anki_object_detection.cube_detector import CubeDetector
from anki_object_detection.lane_detector import LaneDetector
from anki_object_detection.cube import Cube

def main():
    video_capture = cv2.VideoCapture(0)
    cube_detector = CubeDetector()
    lane_detector = LaneDetector()

    while(True):
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cube = cube_detector.detect(frame)
        max_left_lane, max_right_lane = lane_detector.detect(frame)

        cv2.rectangle(frame, (cube.x, cube.y), (cube.width, cube.height), (255, 0, 0), 2)
        if max_left_lane is not None and max_right_lane is not None:
            # print lanes
            cv2.line(image, (max_left_lane.x1, max_left_lane.y1), (max_left_lane.x2, max_left_lane.y2), (255, 0, 0), 5)
            cv2.line(image, (max_right_lane.x1, max_right_lane.y1), (max_right_lane.x2, max_right_lane.y2), (255, 0, 0), 5)

        cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        cv2.imshow('test', frame)
        cv2.waitKey(10)

    # When everything done, release the capture
    video_capture.release()
    video_capture.destroyAllWindows()

if __name__ == "__main__":
    main()