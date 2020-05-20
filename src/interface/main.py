import curses
from curses.textpad import Textbox, rectangle
from src.core.knowledge_repository import KnowledgeRepository
from src.core.parser import Parser
from src.interface.editor_callout import get_text_from_editor
from src.interface.list_navigator import ListNavigator
from enum import Enum


class ScreenState(Enum):
    LIST = 1
    ITEM = 2


class Display:
    def __init__(self):
        self.__setup()

    def __del__(self):
        self.__teardown()

    def __setup(self):
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # inital blank screen
        curses.curs_set(0)
        self.stdscr.clear()
        self.stdscr.refresh()

    def __teardown(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()

        curses.endwin()

    def draw_screen(self):
        """This one screams for refactoring,
        but I'm going to play around just for a bit longer"""

        # members
        knowledge_repo = KnowledgeRepository()
        k = 0
        screen_state = ScreenState.LIST
        search_term = ''
        data = []

        # constants
        LIST_TOP_MARGIN = 1
        WIN_HEIGHT, WIN_WIDTH = self.stdscr.getmaxyx()
        STATUS_BAR_HEIGHT = 1
        LIST_START = LIST_TOP_MARGIN
        LIST_END = WIN_HEIGHT - 1 - STATUS_BAR_HEIGHT
        PAGE_LENGTH = WIN_HEIGHT - LIST_TOP_MARGIN - STATUS_BAR_HEIGHT

        navigator = ListNavigator(0, PAGE_LENGTH)

        # main loop
        while (True):
            # key listeners for list screen state
            if screen_state == ScreenState.LIST:
                if k == curses.KEY_UP:
                    navigator.prev()
                if k == curses.KEY_DOWN:
                    navigator.next()
                if k in (curses.KEY_ENTER, 10, 13):
                    if len(data) > 0:
                        screen_state = ScreenState.ITEM
                if k and curses.ascii.isprint(chr(k)):
                    search_term = search_term + chr(k)
                if k in (curses.KEY_BACKSPACE, 127):
                    search_term = search_term[:-1]
                if curses.keyname(k) == b'^D':
                    if len(data) == 0:
                        pass
                    else:
                        selected_item = data[navigator.selected]
                        knowledge_repo.delete(selected_item.id)
                if curses.keyname(k) == b'^A':
                    self.__teardown()
                    text = get_text_from_editor()
                    self.__setup()
                    new_item = Parser.text_to_knowledge_item(text)
                    knowledge_repo.add(new_item)
                if curses.keyname(k) == b'^E':
                    if len(data) == 0:
                        pass
                    else:
                        selected_item = data[navigator.selected]
                        self.__teardown()
                        text = get_text_from_editor(
                            Parser.knowledge_item_to_text(selected_item))
                        self.__setup()
                        new_item = Parser.text_to_knowledge_item(text)
                        selected_item.title = new_item.title
                        selected_item.category = new_item.category
                        selected_item.content = new_item.content
                        knowledge_repo.update(selected_item)

            # key listeners for item screen state
            if screen_state == ScreenState.ITEM:
                if k == ord('b'):
                    screen_state = ScreenState.LIST

            # ask for data
            data = knowledge_repo.list(search_term)

            # update navigator
            navigator.set_size(len(data))

            # clear screen
            self.stdscr.clear()

            # render functions
            if (screen_state == ScreenState.LIST):
                # render list
                if navigator.selected != -1:
                    for i, item in enumerate(data[navigator.start:navigator.stop + 1]):
                        attribute = curses.A_NORMAL
                        if navigator.selected % PAGE_LENGTH == i:
                            attribute = curses.A_REVERSE
                        y_position = i + LIST_TOP_MARGIN
                        if y_position >= LIST_START and y_position <= LIST_END:
                            self.stdscr.addstr(LIST_TOP_MARGIN + i, 0,
                                               f'{item.category and item.category.upper() or "N/A"} - {item.title} ({item.created})', attribute)
                # render prompt
                self.stdscr.addstr(0, 0, f'> {search_term}')
            elif (screen_state == ScreenState.ITEM):
                # render item content
                item = data[navigator.selected]
                lines = item.content.splitlines()
                for i, line in enumerate(lines):
                    self.stdscr.addstr(i, 0, line)

            # render status bar
            self.stdscr.addstr(WIN_HEIGHT - 1, 0,
                               f'Page {navigator.current_page} / {navigator.total_pages}')

            # paint
            self.stdscr.refresh()

            # wait for input
            k = self.stdscr.getch()


def main():
    display = Display()
    display.draw_screen()


if __name__ == '__main__':
    main()
