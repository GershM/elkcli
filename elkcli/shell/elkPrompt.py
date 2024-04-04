#!/usr/bin/env python3
from rich import print
from elk.elastic import *
import constants as const
import globals_
import click
from utils.compleater import elkcliCompleater
from utils.keybindings import *
from utils.toolbar import create_toolbar_tokens_func
from utils.spinner import ElkSpinner

from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from pathlib import Path

from shell.commands import *

# INFO:
# https://python-prompt-toolkit.readthedocs.io/
class ElkCliPrompt:
    """
    Elastic Search CLI using prompt_toolkit
    """
    def __init__(self):
        self.__prepare_commands()
        self.key_bindings = EditingMode.EMACS
        self.toolbar_error_message = None
        self.completion_refresher = None
        self.__spinner = ElkSpinner()


    def __prepare_commands(self):
        """
        Prepare the CLI

        Args:
            None

        Returns:
            Nothing
        """
        self.commands = {
            "search": searchCommand(),
            "snapshot": snapshotCommand(),
            "tail": tailCommand(),
            "options": optionsCommand(),
            "set": setCommand(),
            "exit": exitCommand()
        }

        self.commands["help"] = helpCommand(self.commands)

    def connect(self, args):
        """
        Connect to the Elastic Search

        Args:
            None

        Returns:
            Nothing
        """


        print(const.BANNER)

        print("Username:", args.username)

        if args.vi:
            self.key_bindings = EditingMode.VI

        retries = 0
        while True:
            try:
                password = prompt("Password: ", is_password=True)
                if not password:
                    continue

                functions = [lambda: connect(args.username, password, args.host, args.port, args.insecure)]
                self.__spinner.start(functions, "Connecting...", "Connected!", "Failed to connect!")
                if globals_.elk and globals_.elk.connected:
                    break

            except KeyboardInterrupt:
                exit(0)
            except EOFError:
                exit(0)
            except Exception:
                retries += 1
                if retries > 3:
                    print("Too many retries")
                    exit(1)

        path = "{}/.elkcli.{}.history".format(Path.home(), args.host)
        self._session = PromptSession(history=FileHistory(path))

    def prompt(self):
        """
        Prompt the user for input

        Args:
            None

        Returns:
            Nothing
        """
        if not globals_.elk:
            return "Not Connected"

        index = ""
        if globals_.elk.index:
            index = " ({})".format(globals_.elk.index)
        url = "{}".format(globals_.elk.url)

        return f"{url}{index}: "

    def set_commands(self, commands):
        """
        Set the commands

        Args:
            commands: dict

        Returns:
            Nothing
        """
        if not globals_.elk or not commands:
            return

        cmds = commands.split()
        if len(cmds) > 0 and cmds[0] in self.commands:
            self.commands[cmds[0]].execute(" ".join(cmds[1:]))
        else:
            print("Invalid command")

    def __elkInfo(self):
        """
        Get the Elastic Search info
            
        Args:
            None

        Returns:
            Nothing
        """

        if not globals_.elk: return

        info = globals_.elk.info()
        if not info: return  

        header ="Elastic Search Info:"
        version = "Version: {}".format(info["version"]["number"])
        name = "Name: {}".format(info["cluster_name"])

        elkinfo = f"{header.center(80)}\n{version.center(80)}\n{name.center(80)}"
        print(elkinfo)

    
    def run(self):
        """
        Run the CLI

        Args:
            None

        Returns:
            Nothing
        """

        bindings = key_bindings(self)
        self.__elkInfo()
        while True:
            try:
                toolbar = create_toolbar_tokens_func(self)
                text = self._session.prompt(
                        self.prompt,
                        completer=elkcliCompleater(self.commands), 
                        auto_suggest=AutoSuggestFromHistory(),
                        is_password=False,
                        key_bindings=bindings,
                        vi_mode=self.key_bindings == EditingMode.VI,
                        editing_mode=self.key_bindings,
                        bottom_toolbar=toolbar
                        )
                self.set_commands(text)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

