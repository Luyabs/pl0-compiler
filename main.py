from compiler import Compiler

if __name__ == '__main__':
    compiler = Compiler()
    compiler.run(input_file='code/code06.pas', output_file='output/code06.out')
    print('词法分析 ===>', compiler.lexer.lexing_results)
    print('语法分析 ===>\n', '结果 | 最后一词位置 | 最后一词内容')
    for result in compiler.parser.parsing_result:
        print(result)
