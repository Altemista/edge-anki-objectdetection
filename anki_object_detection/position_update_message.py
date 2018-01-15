from datetime import datetime


class PositionUpdateMessage:
    def __init__(self, carNo, laneNo):
        self.msgID = 39
        self.msgName = 'POSITION_UPDATE'
        self.msgTimestamp = datetime.now().isoformat(timespec='milliseconds')+"Z"
        self.carNo = carNo
        self.carID = str(carNo)
        self.posLocation = 0
        self.posTileNo = 10
        self.laneOffset = 0
        self.carSpeed = 0
        # laneNo has to be calculated
        self.laneNo = laneNo
        self.laneLength = 550
        self.posTileType = 'CROSSING'
        # internal position has to be calculated
        self.posOptions = []
        self.maxTileNo = 8