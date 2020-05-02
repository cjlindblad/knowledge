import curses
from knowledge_service import KnowledgeService

def draw_screen(stdscr):
    # members
    knowledge_service = KnowledgeService()
    k = 0
    menu_index = 0

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
        if k == curses.KEY_UP and menu_index > 0:
            menu_index = menu_index - 1
        elif k == curses.KEY_DOWN and menu_index < len(data) - 1:
            menu_index = menu_index + 1

        stdscr.clear()

        for i, item in enumerate(data):
            attribute = curses.A_NORMAL
            if menu_index == i:
                attribute = curses.A_REVERSE

            stdscr.addstr(i, 0, f'{item.created} {item.title}', attribute)

        stdscr.refresh()

        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

if __name__ == '__main__':
  main()
