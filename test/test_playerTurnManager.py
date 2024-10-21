import unittest

from playerTurnManager import PlayerTurnManager, TurnPhase


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = PlayerTurnManager()

    def test_init(self):
        self.assertEqual(self.manager.get_current_phase(), TurnPhase.ROLL)



if __name__ == '__main__':
    unittest.main()
