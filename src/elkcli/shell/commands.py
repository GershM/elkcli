import elkcli.globals as g


class command:
    def __init__(self, name: str, help: str):
        self.name = name
        self.help = help
        self.options = []

    def get_options(self, cmds: str, word_before_cursor: str) -> list[str]:
        return []

    def execute(self, cmds: str):
        pass

    def print_help(self):
        print(self.help)


class SnapshotCommand(command):
    def __init__(self):
        super().__init__("snapshot", "Take a snapshot of the logs")
        self.options = ["help"]

    def get_options(self, cmds: str, word_before_cursor: str) -> list[str]:
        if g.ELK is None:
            print("Not connected")
            return []

        options = g.ELK.columns_suggestions(word_before_cursor)
        return self.options + options

    def execute(self, cmds):
        if g.ELK is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        g.ELK.get_snapshots()


class SearchCommand(command):
    def __init__(self):
        super().__init__("search", "Search for a pattern in the logs")
        self.options = ["help"]

    def get_options(self, cmds: str, word_before_cursor: str) -> list[str]:
        if g.ELK is None:
            print("Not connected")
            return []

        options = g.ELK.columns_suggestions(word_before_cursor)
        return self.options + options

    def execute(self, cmds):
        if g.ELK is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        g.ELK.search(cmds, False)


class TailCommand(command):
    def __init__(self):
        super().__init__("tail", "Tail the logs with a pattern")
        self.options = ["help"]

    def get_options(self, cmds: str, word_before_cursor: str) -> list[str]:
        if g.ELK is None:
            print("Not connected")
            return []

        options = g.ELK.columns_suggestions(word_before_cursor)
        return self.options + options

    def execute(self, cmds):
        if g.ELK is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        g.ELK.search(cmds, True)


class OptionsCommand(command):
    def __init__(self):
        super().__init__("options", "Show all the options")
        self.options = ["auth", "elastic", "log", "all", "help"]

    def get_options(self, cmds: str, word_before_cursor: str) -> list[str]:
        return self.options

    def execute(self, cmds: str):
        if g.ELK is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        g.ELK.printOptions(cmds)


class SetCommand(command):
    def __init__(self):
        super().__init__("set", "Set the options")
        self.options = ["index", "pattern", "color", "refresh", "size", "help"]

    def execute(self, cmds):
        if g.ELK is None:
            print("Not connected")
            return

        if cmds == "":
            print("Missing option")
            return

        c = cmds.split()
        if c[0] not in self.options:
            print("Invalid option")
            return

        elif c[0] == "help":
            self.print_help()
            return

        cmd = " ".join(c[1:]) if len(c) > 1 else ""
        g.ELK.setOption(c[0], cmd)

    def get_options(self, cmds: str, word_before_cursor: str) -> list[str]:
        if g.ELK is None:
            return []

        c = cmds.split()
        cmd = c[0] if len(c) > 0 else ""
        if cmd == "index":
            cmd = c[1] if len(c) > 1 else ""
            return g.ELK.tables_suggestions(cmd)

        elif cmd in self.options:
            return []

            # elif cmds[0] in ["pattern", "color"]:
            #     return g.ELK.get_suggestions("set", cmds[1])

        return self.options


class HelpCommand(command):
    def __init__(self, commands: dict[str, command]):
        super().__init__("help", "Get help")
        self.commands = commands

    def execute(self, cmds):
        print("Commands:")
        for c in self.commands:
            cmd = self.commands[c]
            print(f"\t{cmd.name}\t\t{cmd.help}")


class ExitCommand(command):
    def __init__(self):
        super().__init__("exit", "Exit the program")
        self.options = None

    def execute(self, cmds):
        print("Exiting...")
        exit(0)
