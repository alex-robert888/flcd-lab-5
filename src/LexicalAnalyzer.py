import re

from CustomHashMap import CustomHashMap
from LexicalError import LexicalError

PIFOutputFileName = "PIF.out"
STOutputFileName = "ST.out"
CTOutputFileName = "CT.out"


class LexicalAnalyzer:
    def __init__(self):
        self.file = None
        self.symbolTable = CustomHashMap(16)
        self.constantTable = CustomHashMap(16)
        self.programInternalForm = []

        self.fileContent = []
        self.reservedWords = []
        self.typeNames = []
        self.functions = []
        self.separators = []
        self.arithmetic_operators = []
        self.logical_operators = []
        self.relational_operators = []
        self.assignment_operators = []
        self.tokens = []

        self.functionMapping = {
            "enter": self.checkProgram,
            "integer": self.checkDeclaration,
            "character": self.checkDeclaration,
            "string": self.checkDeclaration,
            "boolean": self.checkDeclaration,
            "list": self.checkDeclaration,
            "dictionary": self.notImplemented,
            "if": self.checkIfAction,
            "while": self.checkWhileAction
        }

        self.typeMapping = {
            "integer": self.validateIntegerConstant,
            "character": self.validateCharacterConstant,
            "string": self.validateStringConstant,
            "boolean": self.validateBooleanConstant,
            "list": self.checkListConstant,
            "dictionary": self.notImplemented
        }

        self.tokenIndex = 0

    def open_file(self, filename):
        self.file = open("resources/" + filename, "r")
        if self.file.closed:
            return False

        self.fileContent = self.file.readlines()

        return True

    def close_file(self):
        if not self.file.closed:
            self.file.close()

    def writeReport(self):
        PIFfile = open("output/" + PIFOutputFileName, "w+")
        STFile = open("output/" + STOutputFileName, "w+")
        CTFile = open("output/" + CTOutputFileName, "w+")
        if PIFfile.closed or STFile.closed or CTFile.closed:
            return False

        PIFfile.write("Token | ST/CT position\n")

        for i in self.programInternalForm:
            PIFfile.write(str(i) + "\n")

        PIFfile.close()

        STFile.write("Position | Tokens\n")
        for i in range(self.symbolTable.capacity):
            st_list = self.symbolTable.get(i)
            if st_list is None:
                STFile.write(str(i) + " None\n")
            else:
                STFile.write(str(i) + " - " + str(st_list) + "\n")

        STFile.close()

        CTFile.write("Position | Tokens\n")
        for i in range(self.constantTable.capacity):
            st_list = self.constantTable.get(i)
            if st_list is None:
                CTFile.write(str(i) + " None\n")
            else:
                CTFile.write(str(i) + " - " + str(st_list) + "\n")

        CTFile.close()

        return True

    def get_file_content(self):
        return self.fileContent

    def read_tokens_input(self, filename):
        token_file = open("resources/" + filename, "r")
        if self.file.closed:
            return False

        self.reservedWords = token_file.readline().split(":")[1].replace(' ', '').strip().split(",")
        self.typeNames = token_file.readline().split(":")[1].replace(' ', '').strip().split(",")
        self.functions = token_file.readline().split(":")[1].replace(' ', '').strip().split(",")
        self.separators = token_file.readline().split(":")[1].replace('"', '').strip().split(", ")
        self.arithmetic_operators = token_file.readline().split(":")[1].replace('"', '').replace(' ', '').strip().split(",")
        self.logical_operators = token_file.readline().split(":")[1].replace('"', '').replace(' ', '').strip().split(",")
        self.relational_operators = token_file.readline().split(":")[1].replace('"', '').replace(' ', '').strip().split(",")
        self.assignment_operators = token_file.readline().split(":")[1].replace('"', '').replace(' ', '').strip().split(",")

    def tokenize(self):
        rePattern = re.compile('(' + '\".*\"|' + '[' + r'\s' + '\\'.join(self.separators) + '])')
        l = 0
        for line in self.fileContent:
            l += 1
            initialSplit = rePattern.split(line)
            for i in initialSplit:
                if i and not i.isspace():
                    self.tokens.append(Token(l, i))

    def addToSymbolTable(self, value):
        if not self.symbolTable.search(value):
            self.symbolTable.add(value)

    def addToConstantTable(self, value):
        if not self.constantTable.search(value):
            self.constantTable.add(value)

    def analyze(self):
        self.tokenIndex = 0
        try:
            self.analyzeCurrent()
            print("Lexically correct")
            self.writeReport()
        except LexicalError as lexicalError:
            print("Lexical error on line " + str(lexicalError.line) + ": " + lexicalError.message)
            self.writeReport()

    def analyzeCurrent(self):
        if self.tokenIndex >= len(self.tokens):
            return

        if self.currentToken() in self.reservedWords:
            self.functionMapping[self.currentToken()]()
        elif self.currentToken() in self.functions:
            self.checkFunction()
        else:
            if self.symbolTable.search(self.currentToken()) is None:
                raise LexicalError(self.currentLine(), "Unknown token - " + self.currentToken())
            if self.tokenIndex + 1 < len(self.tokens) and self.nextToken() in self.assignment_operators:
                self.programInternalForm.append(PIFPair("variable", self.symbolTable.search(self.currentToken())))
                self.tokenIndex += 1
                self.checkAssignment()
            else:
                self.checkExpression()

    def currentToken(self):
        return self.tokens[self.tokenIndex].value

    def nextToken(self):
        if self.tokenIndex < len(self.tokens) - 1:
            return self.tokens[self.tokenIndex + 1].value

        return None

    def previousToken(self):
        if self.tokenIndex > 1:
            return self.tokens[self.tokenIndex - 1].value

        return None

    def currentLine(self):
        return self.tokens[self.tokenIndex].line

    def endOfProgram(self):
        if self.tokenIndex >= len(self.tokens):
            return True
        return False

    # region Language Elements

    def validateVariable(self, value):
        return value not in self.reservedWords and re.fullmatch(r'[a-zA-Z][a-zA-Z0-9]*', value)

    def validateTypeName(self, value):
        return value in self.typeNames

    def validateIntegerConstant(self, value):
        return re.fullmatch(r'[-+]?[1-9][0-9]*|0', value) is not None

    def validateBooleanConstant(self, value):
        return value in ["true", "false"]

    def validateCharacterConstant(self, value):
        return re.fullmatch(r"\'[0-9a-zA-Z!?$@&.]\'", value) is not None

    def validateStringConstant(self, value):
        return re.fullmatch(r'\"[a-zA-Z0-9!?$@&.\s]*\"', value) is not None

    def checkListConstant(self):
        if self.currentToken() != "[":
            raise LexicalError(self.currentLine(), "Expecting list constant")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        listConstant = []

        self.tokenIndex += 1
        while self.identifyConstant():
            listConstant.append(self.currentToken())
            self.tokenIndex += 1

        position = self.constantTable.search(listConstant)

        if position is None:
            ct_hash, list_position = self.constantTable.add(listConstant)
        else:
            ct_hash, list_position = position

        self.programInternalForm.append(PIFPair("constant", (ct_hash, list_position)))

        if self.currentToken() != "]":
            raise LexicalError(self.currentLine(), "List constant not closed")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))

    def checkDictionaryConstant(self):
        return False

    def identifyConstant(self):
        if self.currentToken() == '[':
            return "list"
        if self.validateIntegerConstant(self.currentToken()):
            return "integer"
        if self.validateBooleanConstant(self.currentToken()):
            return "boolean"
        if self.validateCharacterConstant(self.currentToken()):
            return "character"
        if self.validateStringConstant(self.currentToken()):
            return "string"
        return None

    # Enter keyword
    def checkProgram(self):
        if self.currentToken() != "enter":
            raise LexicalError(self.currentLine(), "Program expecting enter keyword")
        self.programInternalForm.append(PIFPair(self.currentToken(), None))

        self.tokenIndex += 1
        self.checkActionList()

        if self.currentToken() != "exit":
            raise LexicalError(self.currentLine(), "Program expecting exit keyword")
        self.programInternalForm.append(PIFPair(self.currentToken(), None))

    # Return on finding closing token
    def checkActionList(self):
        while self.tokenIndex < len(self.tokens):
            if self.currentToken() == "exit" or self.currentToken() == "}":
                return
            self.checkAction()

        raise LexicalError(self.tokens[self.tokenIndex - 1].line, "Missing action list closing token")

    def checkAction(self):
        self.analyzeCurrent()
        if self.currentToken() != ";":
            raise LexicalError(self.currentLine(), "Missing semicolon")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

    def checkDeclaration(self):
        if self.currentToken() not in self.typeNames:
            raise LexicalError(self.currentLine(), "Not a valid type name")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))

        self.tokenIndex += 1
        if self.endOfProgram():
            raise LexicalError(self.currentLine() - 1, "Missing variable declaration")

        if not self.validateVariable(self.currentToken()):
            raise LexicalError(self.currentLine(), "Wrong variable format")

        if self.symbolTable.search(self.currentToken()) is None:
            st_hash, list_position = self.symbolTable.add(self.currentToken())
            self.programInternalForm.append(PIFPair("variable", (st_hash, list_position)))
        else:
            raise LexicalError(self.currentLine(), "Variable already declared")

        self.tokenIndex += 1

    def checkAssignment(self):
        if self.currentToken() not in self.assignment_operators:
            raise LexicalError(self.currentLine(), "Expected assignment operator")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))

        self.tokenIndex += 1
        self.checkExpression()

    def checkExpression(self):
        constant = self.identifyConstant()
        if constant is not None or self.symbolTable.search(self.currentToken()) is not None:
            if constant in ["integer", "boolean", "character", "string"]:
                position = self.constantTable.search(self.currentToken())

                if position is None:
                    ct_hash, list_position = self.constantTable.add(self.currentToken())
                else:
                    ct_hash, list_position = position

                self.programInternalForm.append(PIFPair("constant", (ct_hash, list_position)))
            elif constant == "list":
                self.checkListConstant()
            else:
                self.programInternalForm.append(PIFPair("variable", self.symbolTable.search(self.currentToken())))
                if self.nextToken() == "[":
                    self.tokenIndex += 1
                    self.programInternalForm.append(PIFPair(self.currentToken(), None))
                    self.tokenIndex += 1
                    self.checkExpression()
                    if self.currentToken() == "]":
                        self.programInternalForm.append(PIFPair(self.currentToken(), None))
                    else:
                        raise LexicalError(self.currentLine(), "Designation not closed")

            self.tokenIndex += 1

            if self.currentToken() in self.arithmetic_operators:
                self.programInternalForm.append(PIFPair(self.currentToken(), None))
                self.tokenIndex += 1
                self.checkExpression()

        else:
            raise LexicalError(self.currentLine(), "Unknown element in expression: " + self.currentToken())

    def checkIfAction(self):
        if self.currentToken() != "if":
            raise LexicalError(self.currentLine(), "Expecting if action")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1
        self.checkCondition()
        self.checkActionBlock()

        if self.currentToken() == "elif":
            self.checkElifComponent()

        if self.currentToken() == "else":
            self.programInternalForm.append(PIFPair(self.currentToken(), None))
            self.tokenIndex += 1
            self.checkActionBlock()

    def checkCondition(self):
        if self.currentToken() != "(":
            raise LexicalError(self.currentLine(), "Expecting condition")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1
        self.checkLogicalExpression()

        if self.currentToken() != ")":
            raise LexicalError(self.currentLine(), "Expecting condition closing token")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

    def checkElifComponent(self):
        if self.currentToken() != "elif":
            raise LexicalError(self.currentLine(), "Expecting elif component")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1
        self.checkCondition()
        self.checkActionBlock()

        if self.currentToken() == "elif":
            self.checkElifComponent()

    def checkLogicalExpression(self):
        self.checkExpression()
        if self.currentToken() in self.logical_operators:
            self.programInternalForm.append(PIFPair(self.currentToken(), None))
            self.tokenIndex += 1
            self.checkLogicalExpression()
        elif self.currentToken() in self.relational_operators:
            self.programInternalForm.append(PIFPair(self.currentToken(), None))
            self.tokenIndex += 1
            self.checkExpression()

    def checkWhileAction(self):
        if self.currentToken() != "while":
            raise LexicalError(self.currentLine(), "Expecting while action")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

        self.checkCondition()
        self.checkActionBlock()

    def checkActionBlock(self):
        if self.currentToken() != "{":
            raise LexicalError(self.currentLine(), "Expecting action block")
        self.programInternalForm.append(PIFPair(self.currentToken(), None))

        self.tokenIndex += 1
        self.checkActionList()

        if self.currentToken() != "}":
            raise LexicalError(self.currentLine(), "Expecting action block closing token")
        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

    def checkFunction(self):
        if self.currentToken() not in self.functions:
            raise LexicalError(self.currentLine(), "Unknown function " + self.currentToken())

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

        if self.currentToken() != "(":
            raise LexicalError(self.currentLine(), "Expecting list of parameters")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

        self.checkParameterList()

        if self.currentToken() != ")":
            raise LexicalError(self.currentLine(), "Parameter list not closed")

        self.programInternalForm.append(PIFPair(self.currentToken(), None))
        self.tokenIndex += 1

    def checkParameterList(self):
        self.checkExpression()
        if self.currentToken() == ",":
            self.programInternalForm.append(PIFPair(self.currentToken(), None))
            self.tokenIndex += 1
            self.checkParameterList()

    def notImplemented(self):
        print("Not implemented")

    # endregion

class Token:
    def __init__(self, line, value):
        self._line = line
        self._value = value

    @property
    def line(self):
        return self._line

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._line) + " " + self._value


class PIFPair:
    def __init__(self, token, tablePosition=None):
        self._token = token
        self._tablePosition = tablePosition

    @property
    def token(self):
        return self._token

    @property
    def tablePosition(self):
        return self._tablePosition

    def __str__(self):
        return str(self._token) + " - " + str(self._tablePosition)