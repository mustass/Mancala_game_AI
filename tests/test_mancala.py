from unittest import TestCase
from game.mancala import Game

class TestGame(TestCase, Game):
    def test_main(self):
        Game.main(self)

        self.fail()
