# run.py
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .context import Context
from .symbolTable import *
from .number import *
from .values import *
from .position import *


global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("CLS", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUN", BuiltInFunction.is_function)
global_symbol_table.set("APPEND", BuiltInFunction.append)
global_symbol_table.set("POP", BuiltInFunction.pop)
global_symbol_table.set("EXTEND", BuiltInFunction.extend)

def run_without_prints(fn, text):
  # Generate tokens
  lexer = Lexer(fn, text)
  tokens, error = lexer.make_tokens()
  if error: return None, error
  
  # Generate AST
  parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error

  # Run program
  interpreter = Interpreter()
  context = Context('<program>')
  context.symbol_table = global_symbol_table
  result = interpreter.visit(ast.node, context)

  return result.value, result.error

def run(fn, text):
    print('=' * 60)
    print('🚀 STARTING INTERPRETATION PROCESS')
    print('=' * 60)
    print(f'📄 Source Code:\n{text}\n')

    try:
        # PHASE 1: LEXICAL ANALYSIS (TOKENIZATION)
        print('🔍 PHASE 1: LEXICAL ANALYSIS (TOKENIZATION)')
        print('-' * 50)
        
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        
        if error:
            print('❌ LEXICAL ERROR:', error.as_string())
            return None, error
        
        print('✅ Tokens generated successfully:')
        for index, token in enumerate(tokens):
            if token.type != TT_EOF:
                print(f'  {str(index).rjust(2)}: {token}')
        print(f'\n📊 Total tokens: {len(tokens) - 1} (excluding EOF)\n')

        # PHASE 2: SYNTAX ANALYSIS (PARSING)
        print('🌳 PHASE 2: SYNTAX ANALYSIS (PARSING)')
        print('-' * 50)
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast.error:
            print('❌ SYNTAX ERROR:', ast.error.as_string())
            return None, ast.error
        
        print('✅ Abstract Syntax Tree (AST) generated successfully:')
        print(f'  Root: {ast.node}')
        
        # Pretty print AST structure
        def print_ast_structure(node, indent=0):
            spaces = '  ' * indent
            node_name = type(node).__name__
            print(f'{spaces}├─ {node_name}')
            
            if hasattr(node, 'left_node') and hasattr(node, 'right_node'):
                print(f'{spaces}│  ├─ Left:')
                print_ast_structure(node.left_node, indent + 2)
                print(f'{spaces}│  └─ Right:')
                print_ast_structure(node.right_node, indent + 2)
            elif hasattr(node, 'node'):
                print(f'{spaces}│  └─ Operand:')
                print_ast_structure(node.node, indent + 2)
            elif hasattr(node, 'value_node'):
                print(f'{spaces}│  └─ Value:')
                print_ast_structure(node.value_node, indent + 2)
            elif hasattr(node, 'element_nodes'):
                print(f'{spaces}│  └─ Elements:')
                for i, elem in enumerate(node.element_nodes):
                    print(f'{spaces}     [{i}]:')
                    print_ast_structure(elem, indent + 3)
            elif hasattr(node, 'tok'):
                print(f'{spaces}│  └─ Value: {node.tok.value}')
        
        print('\n🌲 AST Structure:')
        print_ast_structure(ast.node)
        print()

        # PHASE 3: SEMANTIC ANALYSIS & INTERPRETATION
        print('⚡ PHASE 3: SEMANTIC ANALYSIS & INTERPRETATION')
        print('-' * 50)
        
        interpreter = Interpreter()
        context = Context('<program>')
        context.symbol_table = global_symbol_table
        result = interpreter.visit(ast.node, context)
        
        if result.error:
            print('❌ RUNTIME ERROR:', result.error.as_string())
            return None, result.error
        
        print('✅ Code executed successfully!')
        print(f'📤 Result: {result.value}')
        print(f'📊 Result Type: {type(result.value).__name__}')
        
        # Show variables in global scope
        if hasattr(context.symbol_table, 'symbols') and context.symbol_table.symbols:
            print('\n📋 Variables in scope:')
            for name, value in context.symbol_table.symbols.items():
                if not name.isupper():  # Skip built-in constants
                    print(f'  {name} = {value} ({type(value).__name__})')

        print('\n' + '=' * 60)
        print('🎉 INTERPRETATION COMPLETED SUCCESSFULLY')
        print('=' * 60)

        return result.value, result.error

    except Exception as e:
        print(f'\n❌ UNEXPECTED ERROR: {str(e)}')
        print('\n' + '=' * 60)
        print('💥 INTERPRETATION FAILED')
        print('=' * 60)
        return None, RTError(Position(0, 0, 0, fn, text), Position(0, 0, 0, fn, text), str(e), Context('<program>'))

# Test the enhanced interpreter
if __name__ == "__main__":
    print('🧪 TESTING ENHANCED INTERPRETER\n')
    
    # Test cases
    test_cases = [
        '5 + 3 * 2',
        'VAR x = 10 + 5',
        '"Hello" + " World"',
        '[1, 2, 3, 4]',
        '(10 + 5) * 2 - 3',
        '2 ^ 3 + 1'
    ]
    
    for i, test_code in enumerate(test_cases, 1):
        print(f'\n📝 TEST CASE {i}:')
        result, error = run('<stdin>', test_code)
        if error:
            print(f'Error: {error.as_string()}')
        print('\n' + '🔄' * 30 + '\n')
        
