import globals_

class command:
    def __init__(self, name:str, help:str):
        self.name = name
        self.help = help
        self.options = []

    def get_options(self, cmds: str, word_before_cursor: str)->list[str]:
        return []

    def execute(self, cmds:str):
        pass

    def print_help(self):
        print(self.help)

class snapshotCommand(command):
    def __init__(self):
        super().__init__("snapshot", "Take a snapshot of the logs")
        self.options = ["help"]

    def get_options(self, cmds: str, word_before_cursor:str)->list[str]:
        if globals_.elk is None:
            print("Not connected")
            return []

        options = globals_.elk.columns_suggestions(word_before_cursor)
        return self.options + options

    def execute(self, cmds):
        if globals_.elk is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        globals_.elk.get_snapshots()

class searchCommand(command):
    def __init__(self):
        super().__init__("search", "Search for a pattern in the logs")
        self.options = ["help"]

    def get_options(self, cmds: str, word_before_cursor:str)->list[str]:
        if globals_.elk is None:
            print("Not connected")
            return []

        options = globals_.elk.columns_suggestions(word_before_cursor)
        return self.options + options

    def execute(self, cmds):
        if globals_.elk is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        globals_.elk.search(cmds, False)

class tailCommand(command):
    def __init__(self):
        super().__init__("tail", "Tail the logs with a pattern")
        self.options = ["help"]

    def get_options(self, cmds: str, word_before_cursor:str)->list[str]:
        if globals_.elk is None:
            print("Not connected")
            return []

        options = globals_.elk.columns_suggestions(word_before_cursor)
        return self.options + options

    def execute(self, cmds):
        if globals_.elk is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        globals_.elk.search(cmds, True)

class optionsCommand(command):
    def __init__(self):
        super().__init__("options", "Show all the options")
        self.options = ["auth", "elastic", "log", "all", "help"]

    def get_options(self, cmds: str, word_before_cursor:str)->list[str]:
        return self.options

    def execute(self, cmds:str):
        if globals_.elk is None:
            print("Not connected")
            return

        if cmds.lower() == "help":
            self.print_help()
            return

        globals_.elk.printOptions(cmds)

class setCommand(command):
    def __init__(self):
        super().__init__("set", "Set the options")
        self.options = ["index", "pattern", "color", "refresh", "size", "help"]

    def execute(self, cmds):
        if globals_.elk is None:
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
        globals_.elk.setOption(c[0], cmd)

    def get_options(self, cmds: str, word_before_cursor:str)->list[str]:
        if globals_.elk is None:
            return []

        c = cmds.split()
        cmd = c[0] if len(c) > 0 else ""
        if cmd == "index":
            cmd = c[1] if len(c) > 1 else ""
            return globals_.elk.tables_suggestions(cmd)

        elif cmd in self.options:
            return []

            # elif cmds[0] in ["pattern", "color"]:
            #     return globals_.elk.get_suggestions("set", cmds[1])

        return self.options


class helpCommand(command):
    def __init__(self, commands: dict[str, command]):
        super().__init__("help", "Get help")
        self.commands = commands

    def execute(self, cmds):
        print("Commands:")
        for c in self.commands:
            cmd = self.commands[c]
            print(f"\t{cmd.name}\t\t{cmd.help}")

class exitCommand(command):
    def __init__(self):
        super().__init__("exit", "Exit the program")
        self.options = None

    def execute(self, cmds):
        print("Exiting...")
        exit(0)
