from anki_sensor.tile import Tile
from anki_sensor.tile_types import TileTypes


class TrackGenerator:

    @staticmethod
    def generate_oval():
        tiles = list()
        tiles.append(Tile(34, TileTypes.START_1))
        tiles.append(Tile(33, TileTypes.START_2))
        tiles.append(Tile(17, TileTypes.CURVE))
        tiles.append(Tile(18, TileTypes.CURVE))
        tiles.append(Tile(40, TileTypes.STRAIGHT))
        tiles.append(Tile(18, TileTypes.CURVE))
        tiles.append(Tile(23, TileTypes.CURVE))
