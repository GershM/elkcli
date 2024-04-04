from prompt_toolkit.completion import Completer, Completion
from parsers.query_parser import QueryParser

class elkcliCompleater(Completer):
    def __init__(self, commands):
        super().__init__()
        self.commands = commands

    @staticmethod
    def find_matches(text, collection):
        t = text.lower()
        return (Completion(z,  -len(text)) for z in collection if z.lower().startswith(t))

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        sLine = QueryParser.tokenizer(document.current_line)
        cmds = list(self.commands.keys())
        if len(sLine) > 0 and sLine[0] in self.commands and self.commands[sLine[0]] is not None:
            cmds = self.commands[sLine[0]].get_options(" ".join(sLine[1:]), word_before_cursor)

        return self.find_matches(word_before_cursor, cmds)
