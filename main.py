from compiler import Compiler

if __name__ == '__main__':
    compiler = Compiler()
    compiler.run(input_file='code/code01.pas', output_file='output/code01.out')
    print('词法分析 ===>', compiler.lexer.lexing_results)