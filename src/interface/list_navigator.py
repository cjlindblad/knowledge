import math


class ListNavigator:
    def __init__(self, size, page_size):
        self.__size = size
        self.__selected = 0
        self.__page_size = page_size

    @property
    def start(self):
        if self.__size == 0:
            return -1

        return (self.current_page - 1) * self.__page_size

    @property
    def stop(self):
        if self.__size == 0:
            return -1

        last_index = self.__size - 1
        proposed_stop = self.start + (self.__page_size - 1)
        if last_index >= proposed_stop:
            return proposed_stop
        else:
            return last_index

    @property
    def selected(self):
        if self.__size == 0:
            return -1

        return self.__selected

    @property
    def current_page(self):
        if self.__size == 0:
            return 0

        return (self.__selected // self.__page_size) + 1

    @property
    def total_pages(self):
        return math.ceil(self.__size / self.__page_size)

    def next(self):
        if self.__selected < self.__size - 1:
            self.__selected += 1

    def prev(self):
        if self.__selected > 0:
            self.__selected -= 1

    def next_page(self):
        if self.__selected + self.__page_size < self.__size:
            self.__selected += self.__page_size
        else:
            self.__selected = self.__size - 1

    def prev_page(self):
        if self.__selected >= self.__page_size:
            self.__selected -= self.__page_size
        else:
            self.__selected = 0

    def set_size(self, size):
        self.__size = size

        if self.__size != 0 and self.__selected >= self.__size:
            self.__selected = self.__size - 1
