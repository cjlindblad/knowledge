import curses
from curses.textpad import Textbox, rectangle
from knowledge_service import KnowledgeService
from enum import Enum

class ScreenState(Enum):
    LIST = 1
    ITEM = 2

def draw_screen(stdscr):
    """This one screams for refactoring,
    but I'm going to play around just for a bit longer""" 
    # constants
    LIST_TOP_MARGIN = 2

    # members
    knowledge_service = KnowledgeService()
    k = 0
    menu_index = 0
    screen_state = ScreenState.LIST
    edit_window = curses.newwin(1, 30, 0, 2)
    search_term = ''

    # inital blank screen
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()

    # main loop
    while (k != ord('q')):
        # key listeners
        if k == curses.KEY_UP and menu_index > 0 and screen_state == ScreenState.LIST:
            menu_index = menu_index - 1
        elif k == curses.KEY_DOWN and menu_index < len(data) - 1 and screen_state == ScreenState.LIST:
            menu_index = menu_index + 1
        elif k == curses.KEY_ENTER or k == 10 or k == 13:
            screen_state = ScreenState.ITEM
        elif k ==  ord('b'):
            if screen_state == ScreenState.ITEM:
                screen_state = ScreenState.LIST
        else:
            if screen_state == ScreenState.LIST and k:
                search_term = search_term + chr(k)

        # ask for data
        data = knowledge_service.list_knowledge(search_term)
        if menu_index > len(data) - 1:
            menu_index = len(data) - 1

        # clear screen
        stdscr.clear()

        # render functions
        if (screen_state == ScreenState.LIST):
            # render list
            for i, item in enumerate(data):
                attribute = curses.A_NORMAL
                if menu_index == i:
                    attribute = curses.A_REVERSE
                stdscr.addstr(LIST_TOP_MARGIN + i, 0, f'{item.created} {item.title}', attribute)
            # render prompt
            stdscr.addstr(0, 0, f'> {search_term}')
        elif (screen_state == ScreenState.ITEM):
            # render item content
            item = data[menu_index]
            lines = item.content.splitlines()
            for i, line in enumerate(lines):
                stdscr.addstr(i, 0, line)

        # paint
        stdscr.refresh()

        # wait for input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

if __name__ == '__main__':
  main()
