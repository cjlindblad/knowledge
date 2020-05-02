import curses
from knowledge_service import KnowledgeService
from enum import Enum

class ScreenState(Enum):
    LIST = 1
    ITEM = 2

def draw_screen(stdscr):
    # members
    knowledge_service = KnowledgeService()
    k = 0
    menu_index = 0
    screen_state = ScreenState.LIST

    # inital blank screen
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()

    # main loop
    while (k != ord('q')):
        # ask for data
        data = knowledge_service.list_knowledge()
        if menu_index > len(data) - 1:
            menu_index = len(data) - 1

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

        stdscr.clear()

        # render functions
        if (screen_state == ScreenState.LIST):
            for i, item in enumerate(data):
                attribute = curses.A_NORMAL
                if menu_index == i:
                    attribute = curses.A_REVERSE
                stdscr.addstr(i, 0, f'{item.created} {item.title}', attribute)
        elif (screen_state == ScreenState.ITEM):
            item = data[menu_index]
            lines = item.content.splitlines()
            for i, line in enumerate(lines):
                stdscr.addstr(i, 0, line)

        stdscr.refresh()

        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

if __name__ == '__main__':
  main()
