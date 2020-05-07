import curses
from curses.textpad import Textbox, rectangle
from src.core.knowledge_service import KnowledgeService
from enum import Enum

class ScreenState(Enum):
    LIST = 1
    ITEM = 2

def draw_screen(stdscr):
    """This one screams for refactoring,
    but I'm going to play around just for a bit longer""" 

    # members
    knowledge_service = KnowledgeService()
    k = 0
    menu_index = 0
    screen_state = ScreenState.LIST
    edit_window = curses.newwin(1, 30, 0, 2)
    search_term = ''
    current_page = 0
    pages = 1

    # inital blank screen
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()
    
    # constants
    LIST_TOP_MARGIN = 1
    WIN_HEIGHT, WIN_WIDTH = stdscr.getmaxyx()
    STATUS_BAR_HEIGHT = 1
    LIST_START = LIST_TOP_MARGIN
    LIST_END = WIN_HEIGHT - 1 - STATUS_BAR_HEIGHT
    PAGE_LENGTH = WIN_HEIGHT - LIST_TOP_MARGIN - STATUS_BAR_HEIGHT

    # main loop
    while (k != ord('q')):
        # key listeners for list screen state
        if screen_state == ScreenState.LIST:
            if k == curses.KEY_UP and menu_index > 0:
                menu_index = menu_index - 1
            if k == curses.KEY_DOWN and menu_index < len(data) - 1:
                menu_index = menu_index + 1
            if k in (curses.KEY_ENTER, 10, 13):
                screen_state = ScreenState.ITEM
            if k and curses.ascii.isprint(chr(k)):
                search_term = search_term + chr(k)
            if k in (curses.KEY_BACKSPACE, 127):
                search_term = search_term[:-1]

        # key listeners for item screen state
        if screen_state == ScreenState.ITEM:
            if k == ord('b'):
                screen_state = ScreenState.LIST

        # ask for data
        data = knowledge_service.list_knowledge(search_term)
        pages = (len(data) // PAGE_LENGTH) + 1
        if len(data) == 0:
            menu_index = 0
        elif menu_index > len(data) - 1:
            menu_index = len(data) - 1

        current_page = (menu_index) // PAGE_LENGTH
        list_start = current_page * PAGE_LENGTH
        list_end = list_start + PAGE_LENGTH

        # clear screen
        stdscr.clear()

        # render functions
        if (screen_state == ScreenState.LIST):
            # render list
            for i, item in enumerate(data[list_start:list_end + 1]):
                attribute = curses.A_NORMAL
                if menu_index % PAGE_LENGTH == i:
                    attribute = curses.A_REVERSE
                y_position = i + LIST_TOP_MARGIN
                if y_position >= LIST_START and y_position <= LIST_END:
                    stdscr.addstr(LIST_TOP_MARGIN + i, 0,
                        f'{item.category and item.category.upper() or "N/A"} - {item.title} ({item.created})', attribute)
            # render prompt
            stdscr.addstr(0, 0, f'> {search_term}')
        elif (screen_state == ScreenState.ITEM):
            # render item content
            item = data[menu_index]
            lines = item.content.splitlines()
            for i, line in enumerate(lines):
                stdscr.addstr(i, 0, line)

        # render status bar
        stdscr.addstr(WIN_HEIGHT - 1, 0, f'Page {current_page + 1} / {pages}')

        # paint
        stdscr.refresh()

        # wait for input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

if __name__ == '__main__':
  main()
