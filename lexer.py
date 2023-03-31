class Lexer:
    def __init__(self):
        self.spaces = [' ', '\t', '\n']
        self.reserved_words = ['begin', 'call', 'const', 'do', 'end', 'if', 'else', 'odd',
                               'procedure', 'read', 'then', 'var', 'while', 'write']
        self.operators = {'+': 'plus', '-': 'minus', '*': 'times', '/': 'slash', '=': 'eql', '#': 'neq',
                          '<': 'lss', '<=': 'leq', '>': 'gtr', '>=': 'geq', ':=': 'becomes'}
        self.delimiters = {'(': 'lparen', ')': 'rparen', ',': 'comma', ';': 'semicolon', '.': 'period'}

        self.lexing_results = []  # 词法分析结果
        self.error = 0  # 词法分析异常数量

    # 词法分析
    def lexing(self, code: str) -> list:
        self.error = 0
        self.lexing_results = []
        operator_buffer = ''  # 运算符缓冲区
        buffer = ''  # 缓冲区
        i = 0
        while i < len(code):
            # 判断分隔符
            if code[i] in self.spaces:
                operator_buffer = self.add_operator_to_lexing_results(operator_buffer, i)  # 将运算符缓冲区加入lexing_results并清空
                buffer = self.add_buffer_to_lexing_results(buffer, i)  # 将缓冲区加入lexing_results并清空

            # 判断定界符
            elif code[i] in self.delimiters:
                operator_buffer = self.add_operator_to_lexing_results(operator_buffer, i)  # 将运算符缓冲区加入lexing_results并清空
                buffer = self.add_buffer_to_lexing_results(buffer, i)  # 将缓冲区加入lexing_results并清空
                self.lexing_results.append([self.delimiters.get(code[i]), code[i]])

            # 判断运算符 + 额外判断冒号是否属于多字符运算符
            elif code[i] == ':' or code[i] in self.operators:
                buffer = self.add_buffer_to_lexing_results(buffer, i)  # 将缓冲区加入lexing_results并清空
                operator_buffer += code[i]

            # 如果非运算符或定界或空格等符 给buffer累计字符
            else:
                operator_buffer = self.add_operator_to_lexing_results(operator_buffer, i)  # 将运算符缓冲区加入lexing_results并清空
                buffer += code[i].lower()

            i += 1

        self.add_operator_to_lexing_results(operator_buffer, i)  # 在结尾时将运算符缓冲区加入lexing_results
        self.add_buffer_to_lexing_results(buffer, i)  # 在结尾时将缓冲加入lexing_results
        return self.lexing_results

    # 将词法分析的缓冲区加到词法分析结果列表
    def add_buffer_to_lexing_results(self, buffer: str, location: int) -> str:
        if buffer != '':
            if buffer in self.reserved_words:  # 保留字
                self.lexing_results.append([buffer + 'sym', buffer])
            elif buffer.isdigit():  # 纯数字
                self.lexing_results.append(['number', buffer])
            elif not buffer[0].isdigit() and buffer.isalnum():  # 合法标识符
                self.lexing_results.append(['ident', buffer])
            elif buffer[0].isdigit():  # 数字开头的非法标识符
                self.error_notice(location, buffer, 'ident can not start with number')
            else:
                self.error_notice(location, buffer, 'invalid_lex, undefined symbol')
        return ''

    # 将词法分析的运算符缓冲区加入结果列表
    def add_operator_to_lexing_results(self, operator_buffer: str, location: int) -> str:
        if operator_buffer != '':
            if operator_buffer in self.operators:  # 如果是多字符运算符 则一块加入lexing_results
                self.lexing_results.append([self.operators.get(operator_buffer), operator_buffer])
            elif operator_buffer == ':=-' or operator_buffer == ':=+':  # 单独判断 :=+ :=-
                self.lexing_results.append([self.operators.get(operator_buffer[0: 2]), operator_buffer[0: 2]])
                self.lexing_results.append([self.operators.get(operator_buffer[2]), operator_buffer[2]])
            else:
                self.error_notice(location, operator_buffer, 'invalid_lex, undefined operator')  # 异常
        return ''

    # 统计词法分析中某类单词出现的次数情况
    def count(self, word_type: str) -> dict:
        map = {}
        for type, word in self.lexing_results:
            if type == word_type and not map.get(word):
                map.update({word: 1})
            elif type == word_type:
                map.update({word: int(map.get(word)) + 1})
        return map

    # 报错
    def error_notice(self, location: int, word: str, reason: str) -> None:
        self.error += 1
        self.lexing_results.append(["ERROR", word, location, reason])
        print('\033[31m',
              'ERROR:', '\n',
              'location: ', location, '\n',
              'wrong_word: ', word, '\n',
              'reason: ', reason, '\n',
              '\033[0m')
