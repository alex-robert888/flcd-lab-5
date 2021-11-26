class LexicalError(Exception):
    def __init__(self, line, message):
        super().__init__(message)
        self.message = message
        self.line = line

