from elasticsearch import Elasticsearch, VERSION

from rich import print
from rich.table import Table
import time

from ..parsers.log_parser import LogParser
from ..parsers.query_parser import QueryParser
from ..utils.spinner import ElkSpinner


class Elastic:
    """
    This class is used to connect to the elastic search and query the data
    """

    def __init__(
        self, url="", port=9200, username="elastic", password="", insecure=False
    ) -> None:
        self._elk = None
        self._index = ""

        self._url = url
        self._port = port
        self._useSSL = True
        self._insecure = insecure

        self._username = username
        self._password = password
        self._refresh_rate = 1
        self._index_list = []
        self._columns = {}

        self._excluded_indexes = []

        self._logParser = LogParser()
        self._queryParser = QueryParser()
        self.__connected = self._connect()
        self.spinner = ElkSpinner()

    def connected(self) -> bool:
        """
        Check if the elastic search is connected

        Args:
            None

        Returns:
            True if connected, False otherwise
        """
        return self.__connected

    @property
    def _create_url(self) -> str:
        """
        Create the url for the elastic search

        Args:
            None

        Returns:
            The url for the elastic search
        """
        url = "http://"
        if self._useSSL:
            url = "https://"

        url = url + self._url
        if self._port:
            url = url + ":" + str(self._port)

        return url

    def __getsuggest(self):
        """
        Get the suggest for the elastic search

        Args:
            None

        Returns:
            Nothing
        """

        self.__indexes()
        self.__columns()

    def connect(
        self, url: str, port: int, username: str, password: str, insecure: bool
    ) -> bool:
        """
        Connect to the elastic search

        Args:
            url: The url of the elastic search
            port: The port of the elastic search
            username: The username of the elastic search
            password: The password of the elastic search
            insecure: The insecure option of the elastic search

        Returns:
            Nothing
        """
        self._url = url
        self._port = port
        self._username = username
        self._password = password
        self._insecure = insecure

        connected = self._connect()
        if not connected:
            return False
        return True

    def _connect(self) -> bool:
        """
        Connect to the elastic search

        Args:
            None

        Returns:
            Nothing
        """
        if not self._url or not self._username or not self._password:
            return False

        auth = {}

        if VERSION[0] >= 8:
            auth["basic_auth"] = (self._username, self._password)
        else:
            auth["http_auth"] = (self._username, self._password)

        # Connect to the elastic search and try to get information for user validation
        self._elk = Elasticsearch(
            self._create_url,
            verify_certs=not self._insecure,
            ssl_show_warn=False,
            **auth,
        )
        self.info()

        self.__getsuggest()
        return False

    def info(self):
        """
        Get the info for the elastic search

        Returns:
            The info for the elastic search
        """

        if not self._elk:
            return None

        return self._elk.info()

    @property
    def url(self):
        """
        The url of the elastic search

        Returns:
            The url of the elastic search
        """
        return self._url

    @property
    def password(self):
        """
        The password of the elastic search

        Returns:
            The password of the elastic search
        """

        return self._password

    @property
    def username(self):
        """
        The username of the elastic search

        Returns:
            The username of the elastic search
        """

        return self._username

    @property
    def index(self):
        """
        The index of the elastic search

        Returns:
            The index of the elastic search
        """

        return self._index

    def __indexes(self):
        """
        The indexes of the elastic search

        Returns:
            The indexes of the elastic search
        """
        if not self._elk:
            return

        if not self._index_list:
            includes = self._elk.cat.indices(
                include_unloaded_segments=False,
                pretty=False,
                human=True,
                help=False,
                format="json",
            )
            for include in includes:
                index = include["index"]
                if not index or index in self._excluded_indexes:
                    continue

                self._index_list.append(index)

            self._index_list = sorted(self._index_list, reverse=True)

    def get_RefreshRate(self) -> str:
        """
        Get the refresh rate of the elastic search

        Returns:
            The refresh rate of the elastic search
        """
        if self._refresh_rate == 0:
            return "Disabled"

        return "{} Seconds".format(self._refresh_rate)

    def printOptions(self, option=""):
        """
        Print the options for the elastic search

        Args:
            option: The option to print

        Returns:
            Nothing
        """

        if option.lower() in ["", "all", "auth"]:
            self.printAuth()

        if option.lower() in ["", "all", "elastic"]:
            self.printElasicOptions()

        if option.lower() in ["", "all", "log"]:
            self._logParser.printOptions()

    def printElasicOptions(self):
        """
        Print the options for the elastic search

        Args:
            None

        Returns:
            Nothing
        """

        elasticOptions = Table(
            show_header=True,
            min_width=20,
            title="Elastic search Options",
            header_style="magenta",
        )
        elasticOptions.add_column("Option")
        elasticOptions.add_column("Type")
        elasticOptions.add_column("")

        elasticOptions.add_row("Index", "String", self.index)
        elasticOptions.add_row("Tail Refresh Rate", "Integer", self.get_RefreshRate())
        elasticOptions.add_row("Batch Size", "Integer", self._queryParser.get_size())

        # FIXME: Add the excluded indexes
        # elasticOptions.add_row("Excluded Indexes", "Array","\n".join(self._excluded_indexes))

        print(elasticOptions)

    def printAuth(self):
        """
        Print the auth options for the elastic search

        Args:
            None

        Returns:
            Nothing
        """

        insecure = "False"
        if self._insecure:
            insecure = "True"

        useSSL = "False"
        if self._useSSL:
            useSSL = "True"

        reqOptions = Table(
            show_header=False, min_width=50, title="Server Info", header_style="magenta"
        )
        reqOptions.add_column("")
        reqOptions.add_column("")
        reqOptions.add_row("Use SSL", useSSL)
        reqOptions.add_row("Url", self._url)
        reqOptions.add_row("Port", str(self._port))
        reqOptions.add_row("Insecure", insecure)
        reqOptions.add_row("Username", self._username)
        reqOptions.add_row("Password", "*" * len(self._password))

        print(reqOptions)

    def setOption(self, key: str, value) -> str:
        """
        Set the option for the elastic search

        Args:
            key: The key to set
            value: The value to set

        Returns:
            Error message if the option is not found
        """
        if key.lower() == "pattern":
            self._logParser.setPattern(value)
        elif key.lower() == "color":
            s = value.split(" ")
            if len(s) < 2:
                print("Missing Color")
                return "Missing Color"

            logType = s[0]
            value = s[1]
            self._logParser.setLogColor(logType, value)

        elif key.lower() == "refresh":
            if value == "":
                print("Refresh rate is required")
                return "Refresh rate is required"
            elif int(value) <= 0:
                print("Refresh rate must be greater than 0")
                return "Refresh rate must be greater than 0"

            self._refresh_rate = int(value)

        elif key.lower() == "size":
            if value == "":
                print("Size is required")
                return "Size is required"
            elif int(value) <= 0:
                print("Size must be greater than 0")
                return "Size must be greater than 0"

            self._queryParser.set_size(int(value))

        elif key.lower() == "index":
            if value == "":
                print("Index is required")
                return "Index is required"

            self._index = value.replace(" ", ",")

        else:
            print("Option not found")
            return "Option not found"

        return ""

    def tables_suggestions(self, text: str) -> list[str]:
        """
        Get the suggestions for the elastic search

        Args:
            text: The text to search

        Returns:
            The suggestions for the elastic search
        """

        self.__indexes()
        if not self._elk or not self._index_list:
            return []

        return [
            e
            for e in self._index_list
            if e not in self._excluded_indexes and e.startswith(text.lower())
        ]

    def __columns(self):
        """
        Get the columns for the elastic search

        Args:
            index: The index to search

        Returns:
            The columns for the elastic search
        """

        if not self._elk:
            return

        if not self._columns:
            fields = self._elk.indices.get_field_mapping(index="*", fields="*")
            if not fields:
                return

            for index in list(fields.keys()):
                self._columns[index] = list(fields[index]["mappings"].keys())

            # self._columns = sorted(self._columns)

    def columns_suggestions(self, text: str) -> list[str]:
        """
        Get the suggestions for the elastic search

        Args:
            text: The text to search

        Returns:
            The suggestions for the elastic search
        """

        if not self._elk:
            return []

        self.__columns()
        suggestions = []

        for index in self.index.split(","):
            cols = []
            for index_cols in list(self._columns.keys()):
                if index in index_cols:
                    cols = self._columns[index_cols]
                    break

            if not cols:
                continue

            suggestion = list(cols)
            suggestion = list(set(suggestion) - set(suggestions))

            suggestions = suggestions + suggestion

        return [e for e in suggestions if e.startswith(text.lower())]

    def get_snapshots(self):
        """
        Get the snapshots for the elastic search

        Returns:
            The snapshots for the elastic search
        """

        if not self._elk:
            return

        snapshots = self._elk.snapshot.get(repository="backup", snapshot="_all")
        print(snapshots)

    def take_snapshot(self, snapshot_name: str, index: str):
        """
        Take the snapshot for the elastic search

        Args:
            snapshot_name: The snapshot name to take
            index: The index to take

        Returns:
            Nothing
        """

        if not self._elk:
            return

        self._elk.snapshot.create(
            repository="backup",
            snapshot=snapshot_name,
            body={"indices": index, "ignore_unavailable": True},
        )

    def commit_snapshot(self, snapshot_name: str, index: str):
        """
        Commit the snapshot for the elastic search

        Args:
            snapshot_name: The snapshot name to commit
            index: The index to commit

        Returns:
            Nothing
        """

        if not self._elk:
            return

        self._elk.snapshot.create(
            repository="backup", snapshot=snapshot_name, body={"indices": index}
        )

    def search(self, query: str, is_tail=False):
        """
        splite the query to commands, fields and message using regex

        Args:
            query: The query to search
            is_tail: The tail option to search

        Returns:
            Nothing
        """
        if not self._elk:
            return

        es_query = self._queryParser.query_builder(query)
        if is_tail:
            self._tail(es_query)
        else:

            def func():
                self._search(es_query)

            self.spinner.start([func], "Searching...", "Done", "Failed!")

    def _search(self, query) -> bool:
        """
        Search the elastic search

        Args:
            query: The query to search

        Returns:
            Nothing
        """

        if not self._elk:
            return False

        try:
            result = self._elk.search(index=self.index, body=query)
            hits = result["hits"]["hits"]
            hasData = False
            last_printed_index = ""
            for hit in hits:
                hasData = True
                # if last_printed_index != hit["_index"]:
                #     print(f"Index: {hit['_index']}")
                #     last_printed_index = hit["_index"]
                log = ""
                source = hit["_source"]
                if "event" not in source:
                    log = f"level=\"{source['status']}\" msg=\"{source['message']}\""
                    if "ansible_result" in source:
                        log += f" ansible_result=\"{source['ansible_result']}\""
                else:
                    log = source["event"]["original"]

                self._logParser.printColoredLog(log)

            return hasData
        except Exception as e:
            print(f"Error: {e}")
            return False

    def _tail(self, query):
        """
        Tail the elastic search

        Args:
            query: The query to search

        Returns:
            Nothing
        """

        if not self._elk:
            return

        self._search(query)

        timestemp = time.time()
        date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestemp))

        filter = {"filter": [{"range": {"@timestamp": {"gte": f"{date}"}}}]}
        query["query"]["bool"]["filter"] = filter["filter"]

        while True:
            hasData = self._search(query)
            if hasData:
                timestemp = time.time()
                date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestemp))
                query["query"]["bool"]["filter"][0]["range"]["@timestamp"][
                    "gte"
                ] = f"{date}"
            time.sleep(self._refresh_rate)


def connect(username: str, password: str, url: str, port: int, insecure: bool):
    """
    Connect to the elastic search

    Args:
        None

    Returns:
        Nothing
    """
    import elkcli.globals as globals

    globals.ELK = Elastic(url, port, username, password, insecure)
