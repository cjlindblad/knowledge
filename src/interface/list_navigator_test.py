import unittest
from src.interface.list_navigator import ListNavigator


class ListNavigatorTest(unittest.TestCase):
    def __shorthand(self, navigator):
        return (
            f'{navigator.selected},' +
            f'{navigator.start},' +
            f'{navigator.stop},' +
            f'{navigator.current_page},' +
            f'{navigator.total_pages}'
        )

    def test_empty_list_properties(self):
        navigator = ListNavigator(0, 10)

        self.assertEqual('-1,-1,-1,0,0', self.__shorthand(navigator))

    def test_half_page_list_properties(self):
        navigator = ListNavigator(5, 10)

        self.assertEqual('0,0,4,1,1', self.__shorthand(navigator))

    def test_two_pages_list_properties(self):
        navigator = ListNavigator(20, 10)

        self.assertEqual('0,0,9,1,2', self.__shorthand(navigator))

    def test_valid_navigation(self):
        navigator = ListNavigator(10, 10)

        navigator.next()
        navigator.next()
        navigator.prev()

        self.assertEqual('1,0,9,1,1', self.__shorthand(navigator))

    def test_invalid_backward_navigation(self):
        navigator = ListNavigator(10, 10)

        navigator.prev()

        self.assertEqual('0,0,9,1,1', self.__shorthand(navigator))

    def test_invalid_forward_navigation(self):
        navigator = ListNavigator(2, 10)

        navigator.next()
        navigator.next()

        self.assertEqual('1,0,1,1,1', self.__shorthand(navigator))

    def test_valid_page_change(self):
        navigator = ListNavigator(9, 3)

        navigator.next_page()
        navigator.next_page()
        navigator.prev_page()

        self.assertEqual('3,3,5,2,3', self.__shorthand(navigator))

    def test_invalid_forward_page_change(self):
        navigator = ListNavigator(3, 3)

        navigator.next_page()

        self.assertEqual('2,0,2,1,1', self.__shorthand(navigator))

    def test_invalid_backward_page_change(self):
        navigator = ListNavigator(3, 3)

        navigator.prev_page()

        self.assertEqual('0,0,2,1,1', self.__shorthand(navigator))

    def test_page_change_remembers_selection_offset(self):
        navigator = ListNavigator(10, 5)

        # first we offset the selection
        navigator.next()
        navigator.next()

        # then we switch page
        navigator.next_page()

        self.assertEqual('7,5,9,2,2', self.__shorthand(navigator))

    def test_forward_page_change_adjusts_offset(self):
        navigator = ListNavigator(12, 5)

        # offset selection
        for _ in range(3):
            navigator.next()

        # change page
        for _ in range(2):
            navigator.next_page()

        self.assertEqual('11,10,11,3,3', self.__shorthand(navigator))

    def test_backward_page_change_adjusts_offset(self):
        navigator = ListNavigator(10, 10)

        navigator.next()

        navigator.prev_page()

        self.assertEqual('0,0,9,1,1', self.__shorthand(navigator))

    def test_increase_size(self):
        navigator = ListNavigator(10, 10)

        navigator.next()
        navigator.next()

        navigator.set_size(20)

        self.assertEqual('2,0,9,1,2', self.__shorthand(navigator))

    def test_decrease_size(self):
        navigator = ListNavigator(20, 10)

        navigator.next()
        navigator.next_page()

        navigator.set_size(10)

        self.assertEqual('9,0,9,1,1', self.__shorthand(navigator))

    def test_reduce_size_to_zero_and_back_again(self):
        navigator = ListNavigator(10, 10)

        navigator.set_size(0)
        navigator.set_size(10)

        self.assertEqual('0,0,9,1,1', self.__shorthand(navigator))
