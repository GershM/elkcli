from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich import print as rprint

import re


class LogParser:
    def __init__(self) -> None:
        self.logPattern = 'level="(.*?)"'
        self.logColorMap = {
            "emergency": "black on red",
            "alert": "black on orange3",
            "critical": "red",
            "fatal": "red",
            "error": "red",
            "notice": "orange3",
            "warning": "yellow",
            "info": "blue",
            "debug": "green",
            "trace": "magenta",
            "ok": "green",
            "failed": "red",
            "changed": "yellow",
            "unreachable": "green",
            "skipped": "blue",
            "rescued": "green",
            "ignored": "blue",
            "default": "white",
        }

    def setPattern(self, pattern: str):
        self.logPattern = pattern

    def setLogColor(self, logType: str, color: str):
        logType = logType.lower()
        color = color.lower()
        self.logColorMap[logType] = color

    def printOptions(self):
        """
        Print the options for the log parser
        """
        elasticOptions = Table(
            show_header=True, min_width=20, title="Log Parser", header_style="magenta"
        )
        elasticOptions.add_column("Option")
        elasticOptions.add_column("Type")
        elasticOptions.add_column("", min_width=20)

        elasticOptions.add_row("Pattern", "String", self.logPattern)
        colorMap = "\n".join(
            [f"{key}: {value}" for key, value in self.logColorMap.items()]
        )
        elasticOptions.add_row("Error Code Style", "Array", colorMap)

        rprint(elasticOptions)

    def printColoredLog(self, log: str):
        """
        Print the log with the color based on the log level
        """
        rg = re.search(self.logPattern, log)
        logLevel = "default"
        if rg:
            logLevel = rg.group(1).lower()

        console = Console(theme=Theme(self.logColorMap))
        text = Text(log, style=logLevel)
        console.print(text)
