import re

class ParserException(Exception):
    pass

class Parser():
    def __init__(self):
        self._last_lexeme = None
        self._tokens = []

        self._patterns = [
            ("number", re.compile(r"\d+(\.\d+)")),
            ("plus", re.compile(r"\+")),
            ("minus", re.compile(r"\-")),
            ("asterisk", re.compile(r"\*")),
            ("slash", re.compile(r"/")),
            ("select keyword", re.compile(r"select")),
            ("from keyword", re.compile(r"from")),
            ("order keyword", re.compile(r"order")),
            ("by keyword", re.compile(r"by")),
            ("identifier", re.compile(r"[a-zA-Z_]+")),
            ("comma", re.compile(r"\,"))
        ]

    def _tokenize(self, text):
        self._tokens = []

        while text:
            text = text.lstrip()

            found = False

            for name, pattern in self._patterns:
                matcher = pattern.match(text)

                if not matcher:
                    continue

                found = True

                self._tokens.append({
                    "name": name,
                    "lexeme": matcher.group()
                })

                text = text[matcher.end():]

            if not found:
                raise ParserException("Symbol not recognized")

    def _consume(self, name):
        if not self._tokens:
            message = "Expected '{0}', found EOF".format(name)

            raise ParserException(message)

        token = self._tokens[0]

        if self._tokens[0]["name"] != name:
            message = "Expected '{0}', found '{1}'".format(name, token["name"])

            raise ParserException(message)

        self._last_lexeme = token["lexeme"]
        del self._tokens[0]

    def _try_consume(self, name):
        try:
            self._consume(name)
        except ParserException:
            return False

        return True

    def _parse_expr0(self):
        if not (self._try_consume("number") or self._try_consume("identifier")):
            raise ParserException("Expected number or identifier")

    def _parse_expr1(self):
        self._parse_expr0()

        while self._try_consume("asterisk") or self._try_consume("slash"):
            self._parse_expr0()

    def _parse_expr2(self):
        self._parse_expr0()

        while self._try_consume("plus") or self._try_consume("minus"):
            self._parse_expr0()

    def _parse_query(self):
        query = {}

        self._consume("select keyword")

        if self._try_consume("asterisk"):
            query["columns"] = "*"
        else:
            query["columns"] = []

            self._consume("identifier")

            query["columns"].append(self._last_lexeme)

            while self._try_consume("comma"):
                self._consume("identifier")

                query["columns"].append(self._last_lexeme)

        self._consume("from keyword")

        self._consume("identifier")

        query["tables"] = [self._last_lexeme]

        if self._try_consume("order keyword"):
            self._consume("by keyword")
            self._consume("identifier")
            query["order by"] = self._last_lexeme

        return query

    def parse(self, text):
        self._tokenize(text)

        return self._parse_query()
