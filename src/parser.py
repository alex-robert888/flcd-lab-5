from parse_tree_node import ParseTreeNode
from parsing_state import ParsingState
from LexicalAnalyzer import LexicalAnalyzer
from grammar import Grammar


class Parser(object):
    def __init__(self, grammar: Grammar, lexical_analyzer: LexicalAnalyzer):
        self.__grammar = grammar
        self.__lexical_analyzer = lexical_analyzer
        self.__pif = self.__lexical_analyzer.programInternalForm
        self.__parse_tree = list()
        self.__state = ParsingState.NORMAL_STATE
        self.__current_symbol_position = 0
        self.__working_stack = list()
        self.__input_stack = list()
        self.__input_stack.append(self.__pif[0].token)

    def run(self):
        while self.__state != ParsingState.FINAL_STATE and self.__state != ParsingState.ERROR_STATE:
            if self.__state == ParsingState.NORMAL_STATE:
                self.__handle_normal_state()
            elif self.__state == ParsingState.BACK_STATE:
                self.__handle_back_state()
            else:
                print("Something went quite wrong.")

    def __handle_normal_state(self):
        pif_len = len(self.__pif)
        if self.__current_symbol_position == pif_len - 1 and not self.__input_stack:
            return self.__success()
        else:
            input_stack_head = self.__input_stack[-1]
            if self.__grammar.is_non_terminal(input_stack_head):
                self.__expand()
            elif input_stack_head == self.__pif[self.__current_symbol_position]:
                self.__advance()
            else:
                self.__momentary_insuccess()

    def __handle_back_state(self):
        working_stack_head = self.__working_stack[-1]
        if self.__grammar.is_terminal(working_stack_head):
            self.__back()
        else:
            self.__another_try()

    def __success(self):
        pass

    def __expand(self):
        pass

    def __advance(self):
        pass

    def __momentary_insuccess(self):
        pass

    def __back(self):
        pass

    def __another_try(self):
        pass

