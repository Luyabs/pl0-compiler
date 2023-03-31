from lexer import Lexer


class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        # TODO: 语法分析器, 语义分析器, ...

    def run(self, input_file: str, output_file: str) -> None:
        self.lexing(input_file, output_file)
        # TODO: 语法分析器, 语义分析器, ...

    # 词法分析
    def lexing(self, input_file: str, output_file: str) -> list:
        with open(input_file) as _in:
            code = _in.read()
            self.lexer.lexing(code)

        with open(output_file, mode='w') as out:
            if self.lexer.error != 0:  # 错误数量
                out.write('ERROR_COUNTS: ' + str(self.lexer.error) + '\n')
                out.write('ERROR_COUNTS: ' + str(self.lexer.error) + '\n')
                out.write('ERROR_COUNTS: ' + str(self.lexer.error) + '\n')
            for word in self.lexer.lexing_results:
                out.write(str(word) + '\n')

        return self.lexer.lexing_results

