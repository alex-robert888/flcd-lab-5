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
        self.__input_stack.append(self.__grammar.get_start_symbol())

    def run(self):
        print(f"input stack: {self.__input_stack}")
        print("working stack: ")
        for elem in self.__working_stack:
            print(elem, end=" ")

        while self.__state != ParsingState.FINAL_STATE and self.__state != ParsingState.ERROR_STATE:
            if self.__state == ParsingState.NORMAL_STATE:
                self.__handle_normal_state()
            elif self.__state == ParsingState.BACK_STATE:
                self.__handle_back_state()
            else:
                print("Something went quite wrong.")
            print(f"input stack: {self.__input_stack}")
            print("working stack: ")
            for elem in self.__working_stack:
                if isinstance(elem, str):
                    print(elem)
                else:
                    print(f"{elem[0].left_side[:]} -> {elem[0].right_side[:]}")
            print("")



    def __handle_normal_state(self):
        pif_len = len(self.__pif)
        if self.__current_symbol_position == pif_len and len(self.__input_stack) == 0:
            return self.__success()
        else:
            self.input_stack_head = self.__input_stack[-1]
            if self.__grammar.is_non_terminal(self.input_stack_head):
                self.__expand()
            elif self.input_stack_head.lower() == self.__pif[self.__current_symbol_position].token.lower():
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
        self.__state = ParsingState.FINAL_STATE

    def __expand(self):
        input_head_stack_productions = self.__grammar.get_productions_for_non_terminal(self.input_stack_head)
        first_production = input_head_stack_productions[0]
        self.__working_stack.append((first_production, 1))

        # Remove ex-top of the input stack
        self.__input_stack.pop()

        # Add symbols to input stack in reversed order
        for symbol in first_production.right_side[0][::-1]:
            self.__input_stack.append(symbol)

    # input_stack: [exit, action_list, enter]
    # working stack: [program -> (enter, action_list, exit, 1)]
    # pif_current_index = 1
    def __advance(self):
        self.__current_symbol_position += 1
        self.__working_stack.append(self.input_stack_head)

        # Remove top of the input stack
        self.__input_stack.pop()

    def __momentary_insuccess(self):
        pass

    def __back(self):
        pass

    def __another_try(self):
        pass

