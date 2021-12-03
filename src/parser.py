from parse_tree_node import ParseTreeNode
from parsing_state import ParsingState
from LexicalAnalyzer import LexicalAnalyzer
from grammar import Grammar
from production import Production


class Parser(object):
    def __init__(self, grammar: Grammar, lexical_analyzer: LexicalAnalyzer):
        self.__grammar = grammar
        self.__lexical_analyzer = lexical_analyzer
        self.__pif = self.__lexical_analyzer.programInternalForm
        self.__parse_tree = list()
        self.__parse_tree_current_index = 0
        self.__working_stack_global_index = 0
        self.__state = ParsingState.NORMAL_STATE
        self.__current_symbol_position = 0
        self.__working_stack = list()
        self.__input_stack = list()
        self.__input_stack.append(self.__grammar.get_start_symbol())

    def run(self):
        self.__log()

        while self.__state != ParsingState.FINAL_STATE and self.__state != ParsingState.ERROR_STATE:
            if self.__state == ParsingState.NORMAL_STATE:
                self.__handle_normal_state()
            elif self.__state == ParsingState.BACK_STATE:
                self.__handle_back_state()
            else:
                print("Something went quite wrong.")
            self.__log()

        if self.__state == ParsingState.FINAL_STATE:
            self.__build_tree()

    def __log(self):
        print(f"============= status: {self.__state}")
        if 0 <= self.__current_symbol_position < len(self.__pif):
            print(f"============ PIF current symbol {self.__pif[self.__current_symbol_position].token.lower()}")
        print(f"============ input stack: {self.__input_stack}")
        print("============= working stack: ")
        for elem in self.__working_stack:
            if isinstance(elem, str):
                print(elem)
            else:
                print(f"{elem[0].left_side[:]} -> {elem[0].right_side[:]}")
        print("")
        print("")
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
        self.working_stack_head = self.__working_stack[-1]
        if self.__grammar.is_terminal(self.working_stack_head):
            self.__back()
        else:
            self.__another_try()

    def __success(self):
        self.__state = ParsingState.FINAL_STATE

    def __expand(self):
        input_head_stack_productions = self.__grammar.get_productions_for_non_terminal(self.input_stack_head)
        first_production = Production(input_head_stack_productions[0].left_side, input_head_stack_productions[0].right_side[0])
        self.__working_stack.append((first_production, 0))

        # Remove ex-top of the input stack
        self.__input_stack.pop()

        # Add symbols to input stack in reversed order
        for symbol in first_production.right_side[::-1]:
            self.__input_stack.append(symbol)

    def __advance(self):
        self.__current_symbol_position += 1
        self.__working_stack.append(self.input_stack_head)

        # Remove top of the input stack
        self.__input_stack.pop()

    def __momentary_insuccess(self):
        self.__state = ParsingState.BACK_STATE

    def __back(self):
        self.__current_symbol_position -= 1
        self.__input_stack.append(self.working_stack_head)
        self.__working_stack.pop()

    def __another_try(self):
        working_stack_head_left_side = self.working_stack_head[0].left_side[0]
        working_stack_head_productions = self.__grammar.get_productions_for_non_terminal(working_stack_head_left_side)

        if self.__current_symbol_position == 0 and working_stack_head_left_side == self.__grammar.get_start_symbol():
            self.__state = ParsingState.ERROR_STATE
            return

        current_production_index = self.working_stack_head[1] + 1
        if current_production_index < len(working_stack_head_productions[0].right_side):
            # Remove symbols from the input stack
            ex_production_right_side_count = len(self.working_stack_head[0].right_side)
            for i in range(ex_production_right_side_count):
                self.__input_stack.pop()

            # Remove production from working stack
            self.__working_stack.pop()

            # Add the next production into the working stack
            next_production = Production((working_stack_head_left_side, ), working_stack_head_productions[0].right_side[current_production_index])
            self.__working_stack.append((next_production, current_production_index))
            self.__state = ParsingState.NORMAL_STATE

            # Add the symbols from the right side of the next production into the input stack
            for symbol in next_production.right_side[::-1]:
                self.__input_stack.append(symbol)
        else:
            # Remove symbols from the input stack
            ex_production_right_side_count = len(self.working_stack_head[0].right_side)
            for i in range(ex_production_right_side_count):
                self.__input_stack.pop()

            # Remove production from working stack
            self.__working_stack.pop()
            self.__input_stack.append(working_stack_head_left_side)

    def __build_tree(self):
        # Add starting symbol
        first_row = self.__working_stack[0]
        self.__parse_tree.append(ParseTreeNode(0, first_row[0].left_side[0], None, None))
        self.__working_stack_global_index += 1
        self.__add_children(0, 0)
        self.__print_parse_tree()

    def __add_children(self, row_index, parent_index):
        right_sibling = None
        children_indices = []
        for child in self.__working_stack[row_index][0].right_side:
            next_index = len(self.__parse_tree)
            children_indices.append(next_index)
            self.__parse_tree.append(ParseTreeNode(next_index, child, parent_index, right_sibling))
            right_sibling = len(self.__parse_tree) - 1

        for index, child in enumerate(self.__working_stack[row_index][0].right_side):
            if self.__grammar.is_terminal(child):
                continue

            self.__working_stack_global_index = self.__find_next_row(child)
            if self.__working_stack_global_index is None:
                return
            self.__add_children(self.__working_stack_global_index, children_indices[index])

    def __find_next_row(self, child):
        next_index = self.__working_stack_global_index + 1
        while isinstance(self.__working_stack[next_index], str):
            if self.__working_stack_global_index == len(self.__working_stack):
                return None
            next_index += 1

        return next_index

    def __print_parse_tree(self):
        f = open("output/parse-tree.out", "w")

        for row in self.__parse_tree:
            f.write(f"{str(row)}\n")