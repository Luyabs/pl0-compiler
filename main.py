from compiler import Compiler

if __name__ == '__main__':
    compiler = Compiler()
    compiler.run(input_file='code/code08.pas', output_file='output/code08.out')
    print('词法分析结果 ===>', compiler.lexer.lexing_results)
    print('语法分析结果 ===>\n', '结果 | 最后一词位置 | 最后一词内容')
    for result in compiler.parser.parsing_result:
        print(result)
    print('语义分析结果 ===>')
    for result in compiler.parser.semantic_result:
        print(result)
