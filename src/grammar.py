from collections import defaultdict


class Grammar(object):
    def __init__(self, input_file):
        self.__terminals = set()
        self.__non_terminals = set()
        self.__start_symbol = ""
        self.__productions = defaultdict(list)
        self.__input_file = input_file
        self.__is_cfg = True

        self.__load()

    def get_terminals(self) -> set:
        return self.__terminals

    def get_non_terminals(self) -> set:
        return self.__non_terminals

    def get_start_symbol(self):
        return self.__start_symbol

    def get_productions(self):
        output = ""
        for (left, right) in self.__productions.items():
            left_to_str = self.__tuple_to_str(left)
            right_to_str = ""
            for index, t in enumerate(right):
                right_to_str += self.__tuple_to_str(t)
                if index < len(right) - 1:
                    right_to_str += " | "

            to_str = f"{left_to_str} -> {right_to_str}\n"
            output += to_str

        return output

    def get_productions_for_non_terminal(self, non_terminal):
        if non_terminal not in self.__non_terminals:
            return ""

        output = ""
        for (left, right) in self.__productions.items():
            if non_terminal not in left:
                continue

            left_to_str = self.__tuple_to_str(left)
            right_to_str = ""
            for index, t in enumerate(right):
                right_to_str += self.__tuple_to_str(t)
                if index < len(right) - 1:
                    right_to_str += " | "

            to_str = f"{left_to_str} -> {right_to_str}\n"
            output += to_str

        return output

    def is_cfg(self):
        return self.__is_cfg

    def is_non_terminal(self, symbol):
        return symbol in self.__non_terminals

    def is_terminal(self, symbol):
        return symbol in self.__terminals

    def __load(self):
        self.__f = open(self.__input_file)
        self.__non_terminals = self.__load_non_terminals()
        self.__terminals = self.__load_terminals()
        self.__start_symbol = self.__load_start_symbol()
        self.__productions = self.__load_productions()

    def __load_terminals(self):
        return self.__f.readline().split()

    def __load_non_terminals(self):
        return self.__f.readline().split()

    def __load_start_symbol(self):
        start_symbol =  self.__f.readline().split()[0]
        if start_symbol not in self.__non_terminals:
            raise Exception('Start symbol is not in the set of non-terminals.')
        return start_symbol

    def __load_productions(self):
        productions = defaultdict(list)
        while line := self.__f.readline():
            line = line.split(" - ")
            left = self.__to_tuple(line[0])

            if len(left) > 1 or left[0] not in self.__non_terminals:
                self.__is_cfg = False

            right = self.__to_tuple(line[1])
            if right not in productions[left]:
                productions[left].append(right)
        return productions

    def __to_tuple(self, side):
        side = side.split()
        return tuple(side)

    def __tuple_to_str(self, t):
        output = ""
        for elem in t:
            output += (elem.strip() + " ")
        return output.strip()


