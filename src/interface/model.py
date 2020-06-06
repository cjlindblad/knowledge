from enum import Enum


class ScreenState(Enum):
    LIST_ACTIVE = 1
    LIST_ARCHIVED = 2
    ITEM = 3


class Model:
    def __init__(self):
        self.__screen_state = ScreenState.LIST_ACTIVE

    def toggle_view(self):
        if self.__screen_state == ScreenState.LIST_ACTIVE:
            self.__screen_state = ScreenState.LIST_ARCHIVED
        elif self.__screen_state == ScreenState.LIST_ARCHIVED:
            self.__screen_state = ScreenState.LIST_ACTIVE

    def go_back(self):
        if self.screen_state == ScreenState.ITEM:
            self.screen_state = ScreenState.LIST_ACTIVE

    @property
    def screen_state(self):
        return self.__screen_state

    @screen_state.setter
    def screen_state(self, value):
        self.__screen_state = value
