class Parser:
    def __init__(self):
        self.lexing_result = []  # 先前词法分析得到的结果
        self.parsing_result = []  # 语法分析结果
        self.token = []  # 当前词 [词性, 内容]
        self.current = -1  # 当前词位置
        self.error = 0  # 语法分析异常数量

    # 语法分析
    def parsing(self, lexing_result: list) -> list:
        self.lexing_result = lexing_result
        self.get_next_token()

        rollback_stack = []     # 回溯栈
        while self.current < len(self.lexing_result):  # 每一句表达式结束 就开始判断下一句是否为表达式
            rollback_stack.append([self.current, self.token])
            success = self.parse_condition()        # 条件表达式?
            tag = '条件表达式'
            if not success:
                self.current, self.token = rollback_stack.pop(-1)
                rollback_stack.append([self.current, self.token])
                success = self.parse_expression()       # 表达式?
                tag = '表达式'

            rollback_stack.pop(-1)

            if self.current > len(self.lexing_result):
                self.parsing_result.append(['fail', 'EOF', 'EOF'])
                self.error += 1
            else:
                if success:
                    self.parsing_result.append(['success', tag, self.current - 1, self.lexing_result[self.current - 1]])
                else:
                    self.parsing_result.append(['fail', self.current - 1, self.lexing_result[self.current - 1]])
                    self.error += 1

        return self.parsing_result

    # 从词法分析结果中取词
    def get_next_token(self) -> None:
        self.current += 1
        self.token = self.lexing_result[self.current] if self.current < len(self.lexing_result) else ['EOF', 'EOF']
        # 获取新token 最后一词则设为EOF

    # 条件分析
    def parse_condition(self) -> bool:  # <条件> ::=<表达式>[=|#|<|>|<=|>=]<表达式>
        if self.token[0] == 'oddsym':
            self.get_next_token()
            success = self.parse_expression()
        else:
            success = self.parse_expression()  # <表达式>
            if success and self.is_compare_operator():  # <比较运算符>
                self.get_next_token()
                success = self.parse_expression()
            else:
                return False
        return success

    # 表达式 分析
    def parse_expression(self) -> bool:  # <表达式> ::= [+|-]<项>{<加法运算符> <项>}
        if self.is_add_operator():  # [+|-]
            self.get_next_token()
        success = self.parse_term()  # <项>

        while success and self.is_add_operator():  # {<加法运算符> ...}
            self.get_next_token()
            success = self.parse_term()  # <项>

        return success

    # 项 分析
    def parse_term(self) -> bool:  # <项> ::= <因子>{<乘法运算符> <因子>}
        success = self.parse_factor()  # <因子>

        while success and self.is_multiply_operator():  # {<乘法运算符> ...}
            self.get_next_token()
            success = self.parse_factor()  # <因子>

        return success

    # 因子 分析
    def parse_factor(self) -> bool:  # <因子> ::= <标识符>|<无符号整数>| '('<表达式>')'
        if self.is_ident() or self.is_number():  # <标识符>|<无符号整数>
            self.get_next_token()
            return True

        elif self.token[0] == 'lparen':  # | '('<表达式>')'
            self.get_next_token()
            if not self.parse_expression():
                return False
            if self.token[0] == 'rparen':
                self.get_next_token()
                return True

        self.get_next_token()
        return False

    # 加法运算符
    def is_add_operator(self) -> bool:
        pos, content = self.token
        return pos == 'plus' or pos == 'minus'

    # 乘法运算符
    def is_multiply_operator(self) -> bool:
        pos, content = self.token
        return pos == 'times' or pos == 'slash'

    # 标识符
    def is_ident(self) -> bool:
        pos, content = self.token
        return pos == 'ident'

    # 无符号整数(非标识符整数)
    def is_number(self) -> bool:
        pos, content = self.token
        return pos == 'number'

    # 比较运算符
    def is_compare_operator(self) -> bool:
        pos, content = self.token
        return pos == 'eql' or pos == 'neq' or pos == 'lss' or pos == 'leq' or pos == 'gtr' or pos == 'geq'
