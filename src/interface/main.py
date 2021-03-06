import curses
from curses.textpad import Textbox, rectangle
from src.core.knowledge_repository import KnowledgeRepository
from src.core.parser import Parser
from src.interface.editor_callout import get_text_from_editor
from src.interface.list_navigator import ListNavigator
from src.interface.text import Text
from src.interface.model import Model, ScreenState


class Display:
    def __init__(self):
        self.__setup()

        # members
        self.model = Model()

        self.knowledge_repo = KnowledgeRepository()
        self.k = 0
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

        # commands
        # TODO switch these out for enums and classes
        command_objects = {
            'toggle_view': {
                'command': self.model.toggle_view,
                'hint': 'Toggle'
            },
            'delete_item': {
                'command': self.delete_item,
                'hint': 'Delete'
            },
            'restore_item': {
                'command': self.restore_item,
                'hint': 'Restore'
            },
            'add_item': {
                'command': self.add_item,
                'hint': 'Add'
            },
            'edit_item': {
                'command': self.edit_item,
                'hint': 'Edit'
            },
            'next_item': {
                'command': self.next_item
            },
            'prev_item': {
                'command': self.prev_item
            },
            'next_page': {
                'command': self.next_page
            },
            'prev_page': {
                'command': self.prev_page
            },
            'confirm': {
                'command': self.confirm
            },
            'backspace': {
                'command': self.backspace
            },
            'go_back': {
                'command': self.model.go_back,
                'hint': 'back'
            }
        }

        self.commands = {
            ScreenState.LIST_ACTIVE: {
                20: command_objects['toggle_view'],
                4: command_objects['delete_item'],
                18: command_objects['restore_item'],
                1: command_objects['add_item'],
                5: command_objects['edit_item'],
                259: command_objects['prev_item'],
                258: command_objects['next_item'],
                260: command_objects['prev_page'],
                261: command_objects['next_page'],
                10: command_objects['confirm'],
                127: command_objects['backspace']
            },
            ScreenState.LIST_ARCHIVED: {
                20: command_objects['toggle_view'],
                4: command_objects['delete_item'],
                18: command_objects['restore_item'],
                1: command_objects['add_item'],
                5: command_objects['edit_item'],
                259: command_objects['prev_item'],
                258: command_objects['next_item'],
                260: command_objects['prev_page'],
                261: command_objects['next_page'],
                10: command_objects['confirm'],
                127: command_objects['backspace']
            },
            ScreenState.ITEM: {
                5: command_objects['edit_item'],
                2: command_objects['go_back']
            }
        }

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
        if self.model.screen_state == ScreenState.LIST_ARCHIVED:
            selected_item = self.data[self.navigator.selected]
            self.knowledge_repo.restore(selected_item.id)

    def delete_item(self):
        if len(self.data) == 0:
            pass
        else:
            selected_item = self.data[self.navigator.selected]
            if self.model.screen_state == ScreenState.LIST_ACTIVE:
                self.knowledge_repo.archive(selected_item.id)
            elif self.model.screen_state == ScreenState.LIST_ARCHIVED:
                self.knowledge_repo.delete(selected_item.id)

    def confirm(self):
        if len(self.data) > 0:
            self.model.screen_state = ScreenState.ITEM

    def next_item(self):
        self.navigator.next()

    def prev_item(self):
        self.navigator.prev()

    def next_page(self):
        self.navigator.next_page()

    def prev_page(self):
        self.navigator.prev_page()

    def backspace(self):
        self.search_term = self.search_term[:-1]

    def get_active_commands(self):
        return self.commands[self.model.screen_state]

    def draw_screen(self):
        """This one screams for refactoring,
        but I'm going to play around just for a bit longer"""

        # main loop
        while (True):
            commands = self.get_active_commands()
            if self.k in commands:
                commands[self.k]['command']()

            # key listeners for list screen state
            if self.model.screen_state == ScreenState.LIST_ACTIVE or self.model.screen_state == ScreenState.LIST_ARCHIVED:
                if self.k and curses.ascii.isprint(chr(self.k)):
                    self.search_term = self.search_term + chr(self.k)

            # ask for data
            if self.model.screen_state == ScreenState.LIST_ACTIVE:
                self.data = self.knowledge_repo.list(self.search_term)
            elif self.model.screen_state == ScreenState.LIST_ARCHIVED:
                self.data = self.knowledge_repo.list_archived()

            # update navigator
            self.navigator.set_size(len(self.data))

            # clear screen
            self.stdscr.clear()

            # render functions
            if self.model.screen_state == ScreenState.LIST_ACTIVE or self.model.screen_state == ScreenState.LIST_ARCHIVED:
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
            elif self.model.screen_state == ScreenState.ITEM:
                # render item content
                item = self.data[self.navigator.selected]
                self.stdscr.addstr(0, 0, Text.format(
                    item.content, self.WIN_WIDTH))

            # render status bar
            status_text = ''
            status_text += f'Page {self.navigator.current_page} / {self.navigator.total_pages}'
            if self.model.screen_state == ScreenState.LIST_ARCHIVED:
                status_text = f'{status_text} (Archived)'

            # add command hints
            commands = self.get_active_commands()
            for key, value in commands.items():
                if 'hint' in value:
                    status_text += f'  ({(curses.keyname(key)).decode("utf-8")}){value["hint"][1:]}'

            wrapped_status_text = Text.format(status_text, self.WIN_WIDTH - 1)

            line_count = wrapped_status_text.count('\n') + 1

            self.stdscr.addstr(self.WIN_HEIGHT - line_count, 0,
                               wrapped_status_text)

            # paint
            self.stdscr.refresh()

            # wait for input
            self.k = self.stdscr.getch()


def main():
    display = Display()
    display.draw_screen()


if __name__ == '__main__':
    main()
