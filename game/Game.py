from .Player import Player
from .World import World


class Game:

    def __init__(self):
        self.game_is_on = True
        self.player_name = ''
        self.messages = []

    def create_player(self, player_name):
        return Player(player_name, self)
