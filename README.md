# ELKCLI (Elasticsearch Command Line Interface)
ELKCLI is a command-line tool that provides a user-friendly interface for interacting with Elasticsearch, similar to the popular `mycli` application for MySQL databases. It offers a set of commands to perform various operations on Elasticsearch indices, documents, and clusters.

## Installation
in the project directory execute:
```bash
pip install .
```

## Usage

```bash
elkcli -h

usage: elkcli [-h] [-H HOST] [-P PORT] [-k] [-u USERNAME] [-vi]

Elastic Search CLI

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  host to connect to the Elastic Search [Default: localhost]
  -P PORT, --port PORT  Port number to use for connection [Default: 9200]
  -k, --insecure        Allow insecure server connections
  -u USERNAME, --username USERNAME
                        Username to connect to the Elastic Search [Default: elastic]
  -vi                   Enable Vi Mode
```

## Prompt commands

| Command | Description |
|-----|----|
| search | Search for a pattern in the logs |
| tail | Tail the logs with a pattern |
| options | Show all the options |
| set | Set the options |
| exit | Exit the program |
| help | Get help |


## Log Coloring 
### patterns Examples
| Log types | Pattern |
|-------------|---------|
|php-fpm|.\*: PHP.\*(NOTICE\|error\|Warning\|Notice)|
|nginx| .*\[(error\|warning\|notice\|info)\]|
|Default|level=\"(.*?)\"|



### Colors Template
| Log Level | Color |
| ----------------- | ---------------------|
| emergency | black on red |
| alert | black on orange3 |
| critical | red |
| fatal | red |
| error | red |
| notice | orange3 |
| warning | yellow |
| info | blue |
| debug | green |
| trace | magenta |
| default | white |

Available Colors: https://rich.readthedocs.io/en/stable/appendix/colors.html


## Features

- Query execution: Execute Elasticsearch queries from the command line.
- (In Progress)Index management: Create, delete, and manage Elasticsearch indices.
- (In Progress) Document operations: Add, update, delete, and search for documents in Elasticsearch.
- (In Progress) Cluster information: Get information about the Elasticsearch cluster and nodes.
- (In Progress) Snapshot and restore: Perform snapshot and restore operations on Elasticsearch indices.


