import curses
from curses.textpad import Textbox, rectangle
from src.core.knowledge_repository import KnowledgeRepository
from src.core.parser import Parser
from src.interface.editor_callout import get_text_from_editor
from src.interface.list_navigator import ListNavigator
from src.interface.text import Text
from enum import Enum


class ScreenState(Enum):
    LIST_ACTIVE = 1
    LIST_ARCHIVED = 2
    ITEM = 3


class Display:
    def __init__(self):
        self.__setup()

        # members
        self.knowledge_repo = KnowledgeRepository()
        self.k = 0
        self.screen_state = ScreenState.LIST_ACTIVE
        self.search_term = ''
        self.data = []

        # constants
        self.LIST_TOP_MARGIN = 1
        self.WIN_HEIGHT, self.WIN_WIDTH = self.stdscr.getmaxyx()
        self.STATUS_BAR_HEIGHT = 1
        self.LIST_START = self.LIST_TOP_MARGIN
        self.LIST_END = self.WIN_HEIGHT - 1 - self.STATUS_BAR_HEIGHT
        self.PAGE_LENGTH = self.WIN_HEIGHT - self.LIST_TOP_MARGIN - self.STATUS_BAR_HEIGHT

        self.navigator = ListNavigator(0, self.PAGE_LENGTH)

    def __del__(self):
        self.__teardown()

    def __setup(self):
        # sets up curses stuff
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # inital blank screen
        curses.curs_set(0)
        self.stdscr.clear()
        self.stdscr.refresh()

    def __teardown(self):
        # tears down curses stuff
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()

        curses.endwin()

    def add_item(self):
        self.__teardown()
        text = get_text_from_editor()
        self.__setup()
        new_item = Parser.text_to_knowledge_item(text)
        self.knowledge_repo.add(new_item)

    def edit_item(self):
        if len(self.data) == 0:
            pass
        else:
            selected_item = self.data[self.navigator.selected]
            self.__teardown()
            text = get_text_from_editor(
                Parser.knowledge_item_to_text(selected_item))
            self.__setup()
            new_item = Parser.text_to_knowledge_item(text)
            selected_item.title = new_item.title
            selected_item.category = new_item.category
            selected_item.content = new_item.content
            self.knowledge_repo.update(selected_item)

    def restore_item(self):
        if self.screen_state == ScreenState.LIST_ARCHIVED:
            selected_item = self.data[self.navigator.selected]
            self.knowledge_repo.restore(selected_item.id)

    def delete_item(self):
        if len(self.data) == 0:
            pass
        else:
            selected_item = self.data[self.navigator.selected]
            if self.screen_state == ScreenState.LIST_ACTIVE:
                self.knowledge_repo.archive(selected_item.id)
            elif self.screen_state == ScreenState.LIST_ARCHIVED:
                self.knowledge_repo.delete(selected_item.id)

    def confirm(self):
        if len(self.data) > 0:
            self.screen_state = ScreenState.ITEM

    def toggle_view(self):
        if self.screen_state == ScreenState.LIST_ACTIVE:
            self.screen_state = ScreenState.LIST_ARCHIVED
        elif self.screen_state == ScreenState.LIST_ARCHIVED:
            self.screen_state = ScreenState.LIST_ACTIVE

    def draw_screen(self):
        """This one screams for refactoring,
        but I'm going to play around just for a bit longer"""

        commands = {
            ScreenState.LIST_ACTIVE: {
                b'^T': self.toggle_view,
                b'^D': self.delete_item,
                b'^R': self.restore_item,
                b'^A': self.add_item,
                b'^E': self.edit_item
            },
            ScreenState.LIST_ARCHIVED: {
                b'^T': self.toggle_view,
                b'^D': self.delete_item,
                b'^R': self.restore_item,
                b'^A': self.add_item,
                b'^E': self.edit_item,
            },
        }

        # main loop
        while (True):
            command_name = curses.keyname(self.k)
            screen_commands = commands[self.screen_state]
            if command_name in screen_commands:
                screen_commands[command_name]()

            # key listeners for list screen state
            if self.screen_state == ScreenState.LIST_ACTIVE or self.screen_state == ScreenState.LIST_ARCHIVED:
                if self.k == curses.KEY_UP:
                    self.navigator.prev()
                if self.k == curses.KEY_DOWN:
                    self.navigator.next()
                if self.k == curses.KEY_RIGHT:
                    self.navigator.next_page()
                if self.k == curses.KEY_LEFT:
                    self.navigator.prev_page()
                if self.k in (curses.KEY_ENTER, 10, 13):
                    self.confirm()
                if self.k and curses.ascii.isprint(chr(self.k)):
                    self.search_term = self.search_term + chr(self.k)
                if self.k in (curses.KEY_BACKSPACE, 127):
                    self.search_term = self.search_term[:-1]

            # key listeners for item screen state
            if self.screen_state == ScreenState.ITEM:
                if self.k == ord('b'):
                    self.screen_state = ScreenState.LIST_ACTIVE

            # ask for data
            if self.screen_state == ScreenState.LIST_ACTIVE:
                self.data = self.knowledge_repo.list(self.search_term)
            elif self.screen_state == ScreenState.LIST_ARCHIVED:
                self.data = self.knowledge_repo.list_archived()

            # update navigator
            self.navigator.set_size(len(self.data))

            # clear screen
            self.stdscr.clear()

            # render functions
            if self.screen_state == ScreenState.LIST_ACTIVE or self.screen_state == ScreenState.LIST_ARCHIVED:
                # render list
                if self.navigator.selected != -1:
                    for i, item in enumerate(self.data[self.navigator.start:self.navigator.stop + 1]):
                        attribute = curses.A_NORMAL
                        if self.navigator.selected % self.PAGE_LENGTH == i:
                            attribute = curses.A_REVERSE
                        y_position = i + self.LIST_TOP_MARGIN
                        if y_position >= self.LIST_START and y_position <= self.LIST_END:
                            self.stdscr.addstr(self.LIST_TOP_MARGIN + i, 0,
                                               f'{item.category and item.category.upper() or "N/A"} - {item.title} ({item.created})', attribute)
                # render prompt
                self.stdscr.addstr(0, 0, f'> {self.search_term}')
            elif self.screen_state == ScreenState.ITEM:
                # render item content
                item = self.data[self.navigator.selected]
                self.stdscr.addstr(0, 0, Text.format(
                    item.content, self.WIN_WIDTH))

            # render status bar
            status_text = f'Page {self.navigator.current_page} / {self.navigator.total_pages}'
            if self.screen_state == ScreenState.LIST_ARCHIVED:
                status_text = f'{status_text} (Archived)'
            self.stdscr.addstr(self.WIN_HEIGHT - 1, 0,
                               status_text)

            # paint
            self.stdscr.refresh()

            # wait for input
            self.k = self.stdscr.getch()


def main():
    display = Display()
    display.draw_screen()


if __name__ == '__main__':
    main()
