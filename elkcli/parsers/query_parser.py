from tokenize import DEDENT, ENCODING, ENDMARKER, INDENT, NEWLINE, STRING, tokenize
from io import BytesIO

#  constructing an Elasticsearch query from SQL components:   
class QueryParser:
    def __init__(self, size: int = 100):
        self._size = size

    def set_size(self, size: int):
        """
        Set the size of the query

        Args:
            size: size of the query

        Return:
            Nothing
        """
        if size <= 0:
            print("Size must be greater than 0")
            return

        self._size = size

    def get_size(self) -> str:
        """
        Get the size of the query

        Args:
            None

        Return:
            size of the query
        """
        return "{} lines".format(self._size)


    # 1. Split the query into tokens
    @staticmethod
    def tokenizer(s: str)->list[str]:
        """
        Tokenize the input string into a list of tokens

        Args: 
            s: input string

        Return:
            list of tokens
        """

        result = []
        g = tokenize(BytesIO(s.encode('utf-8')).readline)
        for toknum, tokval, _, _, _ in g:
            if toknum in [ENDMARKER, ENCODING, INDENT,NEWLINE,DEDENT]:
                continue
            if toknum == STRING and tokval[0] in ["'", '"'] and tokval[0] == tokval[-1]:
                tokval = tokval[1:-1]
            result.append(tokval)

        return result

    # 2. Parse the tokens into an Elasticsearch query
    def __parse_query(self, tokens: list[str])->dict[str, dict[str, list[dict[str, dict[str, list[dict[str, str]]]]]]]:
        """
        Parse the tokens into an Elasticsearch query

        Args:
            tokens: list of tokens

        Return:
        """

        matches = { "bool": { 'must': [] } }
        matchItem = { "bool":{ "should":[] } }

        tokenLength = len(tokens)
        for i in range(tokenLength):
            if tokens[i].lower() == "and":
               matches["bool"]["must"].append(matchItem)
               matchItem = {
                   "bool":{
                       "should":[

                       ]
                   }
               }

            elif tokens[i] in ["=", ">", "<", "<=", ">="]:
                key = tokens[i-1]
                value = tokens[i+1]

                if tokens[i] == "=":
                    obj ={ key: value }
                    matchItem["bool"]["should"].append({ "match": obj })

                elif tokens[i] in [">", "<", "<=", ">="]:
                    opType = ""

                    if tokens[i] == ">":
                        opType = "gt"
                    elif tokens[i] == "<":
                        opType = "lt"
                    elif tokens[i] == ">=":
                        opType = "gte"
                    elif tokens[i] == "<=":
                        opType = "lte"

                    obj = { key: { opType: value } }
                    matchItem["bool"]["should"].append({ "range": obj })

                i+=1

        if len(matchItem["bool"]["should"]) > 0:
            matches["bool"]["must"].append(matchItem)

        return matches

    def handel_objects(self, tokens: list[str])->list[str]:
        """
        Handle the object tokens

        Args:
            tokens: list of tokens

        Return:
            list of tokens
        """

        newtokens = []
        tok = ""

        idx = 0
        length = len(tokens)
        hasdot = False
        while idx < length:
            val = tokens[idx]
            idx += 1

            if val == ".":
                continue
            elif idx < length and tokens[idx].startswith("."):
                if len(tokens[idx]) > 1:
                    tok += val
                else:
                    tok += val + "."

                hasdot = True
            else:
                if hasdot:
                    hasdot = False
                    tok += val
                else:
                    tok = val

                newtokens.append(tok)
                tok = ""

        return newtokens

    # 3. Return the Elasticsearch query
    def query_builder(self, query: str) -> dict:
        """
        Build an Elasticsearch query from the input string

        Args:
            query: input string

        Return:
            Elasticsearch query
        """
        tokens = self.tokenizer(query)
        tokens = self.handel_objects(tokens)
        es_query = self.__parse_query(tokens)

        return { 
                "query": es_query, 
                "size": self._size,
                "sort": [
                    {
                        "@timestamp": { 
                                       "order": "desc",
                                       "unmapped_type": "boolean"
                                       }
                        }
                    ]
                }

