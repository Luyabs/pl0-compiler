from lexer import Lexer
from parser_ import Parser


class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        # TODO: 语义分析器, ...

    def run(self, input_file: str, output_file: str) -> None:
        result = self.lexing(input_file, output_file)
        if self.lexer.error > 0:
            print("\033[32m词法分析有误, 不再进行语法分析!\033[0m")
            return
        else:
            print("\033[34m词法分析无误, 进行语法分析...\033[0m")
        result1, result2 = self.parsing(result)
        if self.parser.error > 0:
            print("\033[32m语法分析有误!\033[0m")
            return
        else:
            print("\033[35m语法分析无误\033[0m")
        # TODO: 语义分析器, ...

    # 词法分析
    def lexing(self, input_file: str, output_file: str) -> list:
        with open(input_file) as _in:
            code = _in.read()
            self.lexer.lexing(code)

        with open(output_file, mode='w') as out:
            if self.lexer.error != 0:  # 错误数量
                out.write('ERROR_COUNTS: ' + str(self.lexer.error) + '\n')
            for word in self.lexer.lexing_results:
                out.write(str(word) + '\n')

        return self.lexer.lexing_results

    # 语法分析
    def parsing(self, lexing_result: list):
        self.parser.parsing(lexing_result)
        return self.parser.parsing_result, self.parser.semantic_result

    # 语义分析
