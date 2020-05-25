from textwrap import wrap


class Text:
    @staticmethod
    def format(text, width):
        result = '\n'.join(wrap(text, width=width, replace_whitespace=False))
        return result
