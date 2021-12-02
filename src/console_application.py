import sys
from grammar import Grammar
from LexicalAnalyzer import LexicalAnalyzer
from parser import Parser


class ConsoleApplication(object):
    def __init__(self, input_file):
        self.__main_menu = [
            "0. Exit.",
            "1. Print terminal symbols.",
            "2. Print non-terminal symbols.",
            "3. Print start symbol.",
            "4. Print productions.",
            "5. Print production for a non-terminal.",
            "6. CFG check",
            "7. Parse program"
        ]
        self.__grammar = Grammar(input_file)

        self.__lexical_analyzer = LexicalAnalyzer()
        self.init_parser()

        self.__parser = Parser(self.__grammar, self.__lexical_analyzer)

    def init_parser(self):
        self.__lexical_analyzer.open_file("p2-simplified.txt")
        self.__lexical_analyzer.read_tokens_input("token.in")
        self.__lexical_analyzer.close_file()
        self.__lexical_analyzer.tokenize()
        self.__lexical_analyzer.analyze()

    def run(self):
        while True:
            try:
                self.print_menu()
                option = int(input("Enter option: "))
                assert 0 <= option < len(self.__main_menu)

                if option == 0:
                    sys.exit()
                elif option == 1:
                    print(self.__grammar.get_terminals())
                elif option == 2:
                    print(self.__grammar.get_non_terminals())
                elif option == 3:
                    print(self.__grammar.get_start_symbol())
                elif option == 4:
                    print(self.__grammar.get_productions())
                elif option == 5:
                    non_terminal = input("Enter a non-terminal symbol: ")
                    print(self.__grammar.get_productions_for_non_terminal_to_str(non_terminal))
                elif option == 6:
                    print("Yes." if self.__grammar.is_cfg() else "No.")
                elif option == 7:
                    print(self.__parser.run())

            except Exception as e:
                print(e)



    def print_menu(self):
        for item in self.__main_menu:
            print(item)