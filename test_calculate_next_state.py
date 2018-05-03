import unittest
from main import calculate_next_state, JsonState

class TestCalculateNextState(unittest.TestCase):

    def test_display_pressed_number_when_state_is_null(self):
        self.assertEqual('1', calculate_next_state(None, '1').display)

    def test_display_when_operator_is_pressed_after_a_number(self):
        state = JsonState(['1'])
        self.assertEqual('1', calculate_next_state(state, '+').display)

    def test_display_when_dividing_by_zero(self):
        state = JsonState(['1', '/', '0'])
        self.assertEqual('can not divide by zero', calculate_next_state(state, '=').display)