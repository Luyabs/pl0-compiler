# pl0-compiler (only lexing)
### 项目构成:
> `main.py` - 程序运行入口  
> `compiler.py` - 编译器(外观模式)  
> `lexer.py` - 词法分析器  
> `parser_.py` - 语法分析器  
>  
> ```<TODO>``` 优化语义分析器,   
> ```<TODO>``` 语义分析器, ...  
>  
> `\code` - pl/0代码示例目录  
> `\output` - 输出结果目录    



### 支持的语法规则   
| 文法                                       |
|------------------------------------------|
| <表达式> ::= \[\+\|\-\]<项>\{<加法运算符> <项>\}   |
| <项> ::= <因子>\{<乘法运算符> <因子>\}             |
| <因子> ::= <标识符>\|<无符号整数>\| ‘\(’<表达式>‘\)’  |
| <加法运算符> ::= \+\|\-                       |
| <乘法运算符> ::= \*\|/                        |

