from anki_sensor.tile import Tile
from anki_sensor.track_generator import TrackGenerator


class Game:
    tiles = []
    cars = []

    def __init__(self):
        super()

        tiles = TrackGenerator.generate_oval()

    def update_state(self, raw_data):
        pass
