#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

#######################################
# ERRORS
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        if self.pos_start and self.pos_end:
            result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class DivisionByZeroError(Error):
    def __init__(self, pos_start, pos_end):
        super().__init__(pos_start, pos_end, 'Division by Zero', 'Attempted to divide by zero')

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result


#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


##############################################
# TOKENS
##############################################

T_INT = 'T_INT'
T_BOOLEAN = 'T_BOOLEAN'
T_IDENTIFIER= 'T_IDENTIFIER'
T_PLUS = 'T_PLUS'
T_SUB = 'T_SUB'
T_MUL = 'T_MUL'
T_DIV = 'T_DIV'
T_MODULO = 'T_MODULO'
T_AND = 'T_AND'
T_OR = 'T_OR'
T_NOT = 'T_NOT'
T_EQEQ = 'T_EQEQ'
T_NOTEQUAL = 'T_NOTEQUAL'
T_GREATERTHAN = 'T_GREATERTHAN'
T_LESSTHAN = 'T_LESSTHAN'
T_EQGREATERTHAN = 'T_EQGREATERTHAN'
T_EQLESSTHAN = 'T_EQLESSTHAN'
T_LPAREN = 'T_LPAREN'
T_RPAREN = 'T_RPAREN'
T_IF = 'T_IF'
T_THEN = 'T_THEN'
T_ELSE = 'T_ELSE'
T_ELSEIF = 'T_ELSEIF'
T_WHILE = 'T_WHILE'
T_FOR = 'T_FOR'
T_TO = 'T_TO'
T_STEP = 'T_STEP'
T_DO = 'T_DO'
T_DEFUN = 'T_DEFUN'
T_COLON = 'T_COLON'
T_COMMA = 'T_COMMA'
T_LAMBDA = 'T_LAMBDA'



class my_Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
        else:
            self.pos_start = None

        if pos_end:
            self.pos_end = pos_end.copy()
        else:
            self.pos_end = None

        if pos_start:
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

    def matches(self, type_, value=None):
        return self.type == type_ and (self.value == value or value is None)

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


##############################################
# LEXER
##############################################

class my_Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):  # the next char in the token
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '-' and self.peek_next_char() in DIGITS:
                tokens.append(self.make_negative_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(my_Token(T_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(my_Token(T_SUB))
                self.advance()
            elif self.current_char == '*':
                tokens.append(my_Token(T_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(my_Token(T_DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(my_Token(T_MODULO))
                self.advance()
            elif self.current_char == '&':
                tokens.append(my_Token(T_AND))
                self.advance()
            elif self.current_char == '|':
                tokens.append(my_Token(T_OR))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
                self.advance()
            elif self.current_char == '(':
                tokens.append(my_Token(T_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(my_Token(T_RPAREN))
                self.advance()
            elif self.current_char == ':':
                tokens.append(my_Token(T_COLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(my_Token(T_COMMA, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        return my_Token(T_INT, int(num_str), pos_start, self.pos)

    def make_negative_number(self):
        num_str = '-'
        pos_start = self.pos.copy()
        self.advance()
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        return my_Token(T_INT, int(num_str), pos_start, self.pos)

    def make_equals(self):
        tok_type = T_EQEQ
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
        return my_Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return my_Token(T_NOTEQUAL, pos_start=pos_start, pos_end=self.pos), None

        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_greater_than(self):
        tok_type = T_GREATERTHAN
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = T_EQGREATERTHAN

        return my_Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = T_LESSTHAN
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = T_EQLESSTHAN

        return my_Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def peek_next_char(self):
        peek_pos = self.pos.idx + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS:
            id_str += self.current_char
            self.advance()

        id_str_lower = id_str.lower()

        if id_str_lower == 'if':
            return my_Token(T_IF, pos_start=pos_start)
        elif id_str_lower == 'then':
            return my_Token(T_THEN, pos_start=pos_start)
        elif id_str_lower == 'else':
            return my_Token(T_ELSE, pos_start=pos_start)
        elif id_str_lower == 'elseif':
            return my_Token(T_ELSEIF, pos_start=pos_start)
        elif id_str_lower == 'while':
            return my_Token(T_WHILE, pos_start=pos_start)
        elif id_str_lower == 'for':
            return my_Token(T_FOR, pos_start=pos_start)
        elif id_str_lower == 'to':
            return my_Token(T_TO, pos_start=pos_start)
        elif id_str_lower == 'step':
            return my_Token(T_STEP, pos_start=pos_start)
        elif id_str_lower == 'do':
            return my_Token(T_DO, pos_start=pos_start)
        elif id_str_lower == 'and':
            return my_Token(T_AND, pos_start=pos_start)
        elif id_str_lower == 'or':
            return my_Token(T_OR, pos_start=pos_start)
        elif id_str_lower == 'not':
            return my_Token(T_NOT, pos_start=pos_start)
        elif id_str_lower == 'defun':
            return my_Token(T_DEFUN, pos_start=pos_start)
        elif id_str_lower == 'lambda':
            return my_Token(T_LAMBDA, pos_start=pos_start)
        elif id_str_lower == 'true':
            return my_Token(T_BOOLEAN, True, pos_start=pos_start)
        elif id_str_lower == 'false':
            return my_Token(T_BOOLEAN, False, pos_start=pos_start)
        else:
            return my_Token(T_IDENTIFIER, id_str, pos_start=pos_start)

    def peek_next_word(self):
        current_pos = self.pos.idx
        word = ''

        # Skip spaces
        while current_pos < len(self.text) and self.text[current_pos] in ' \t':
            current_pos += 1

        # Collect characters of the next word
        while current_pos < len(self.text) and self.text[current_pos] in LETTERS:
            word += self.text[current_pos]
            current_pos += 1

        return word.lower()


#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BooleanNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][1]).pos_end

    def __repr__(self):
        return f'IfNode(cases={self.cases}, else_case={self.else_case})'


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

    def __repr__(self):
        return f'WhileNode(condition={self.condition_node}, body={self.body_node})'


class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

    def __repr__(self):
        return f'ForNode(var_name={self.var_name_tok}, start={self.start_value_node}, end={self.end_value_node}, step={self.step_value_node}, body={self.body_node})'

class FunctionDefNode:
    def __init__(self, name_tok, arg_name_toks, body_node):
        self.name_tok = name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        self.pos_start = self.name_tok.pos_start
        self.pos_end = self.body_node.pos_end
class FunctionCallNode:
    def __init__(self, name_tok, arg_nodes):
        self.name_tok = name_tok
        self.arg_nodes = arg_nodes

        self.pos_start = self.name_tok.pos_start
        self.pos_end = (self.arg_nodes[-1].pos_end if self.arg_nodes
                        else self.name_tok.pos_end)
class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

class IdentifierNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class LambdaNode:
    def __init__(self, arg_name_toks, body_node):
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        self.pos_start = self.arg_name_toks[0].pos_start if self.arg_name_toks else self.body_node.pos_start
        self.pos_end = self.body_node.pos_end

#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

#######################################
# PARSER
#######################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if self.token_idx >= 0 and self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = None

    def parse(self):
        res = ParseResult()
        while self.current_token != None:
            if self.current_token.type == T_DEFUN:
                func_def = res.register(self.func_def())
                if res.error: return res
                return res.success(func_def)
            else:
                expr = res.register(self.expr())
                if res.error: return res
                return res.success(expr)
        return res.failure(IllegalCharError(
            self.current_token.pos_start, self.current_token.pos_end,
            f"Expected end of input but got '{self.current_token}'"
            ))

    def expr(self):
        res = ParseResult()

        if self.current_token.type == T_LAMBDA:
            lambda_node = res.register(self.lambda_expr())
            if res.error: return res
            return res.success(lambda_node)

        return self.expression()

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token != None:
            statement = res.register(self.statement())
            if res.error: return res
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_token.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type == T_DEFUN:
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        expr = res.register(self.expr())
        if res.error:
            return res.failure(IllegalCharError(
                pos_start, self.current_token.pos_end,
                "Expected 'DEFUN', 'IF', 'FOR', 'INT', 'IDENTIFIER', '+', '-', '('"
            ))
        return res.success(expr)

    def func_def(self):
        res = ParseResult()

        if not self.current_token.matches(T_DEFUN):
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'DEFUN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type != T_IDENTIFIER:
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected identifier"
            ))

        func_name = self.current_token
        res.register_advancement()
        self.advance()

        if self.current_token.type != T_LPAREN:
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '('"
            ))

        res.register_advancement()
        self.advance()

        arg_name_toks = []

        if self.current_token.type == T_IDENTIFIER:
            arg_name_toks.append(self.current_token)
            res.register_advancement()
            self.advance()

            while self.current_token.type == T_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != T_IDENTIFIER:
                    return res.failure(IllegalCharError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_token)
                res.register_advancement()
                self.advance()

        if self.current_token.type != T_RPAREN:
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ',' or ')'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type != T_COLON:
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(FunctionDefNode(
            func_name,
            arg_name_toks,
            body
        ))
    def expression(self):
        res = ParseResult()
        if self.current_token.type == T_IF:
            return self.if_expr()
        elif self.current_token.type == T_FOR:
            return self.for_expr()

        left = res.register(self.comparison())
        if res.error: return res

        while self.current_token != None and self.current_token.type in (T_AND, T_OR):
            op_tok = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(self.comparison())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def comparison(self):
        res = ParseResult()

        left = res.register(self.term())
        if res.error: return res

        while self.current_token != None and self.current_token.type in (
        T_EQEQ, T_NOTEQUAL, T_GREATERTHAN, T_LESSTHAN, T_EQGREATERTHAN, T_EQLESSTHAN):
            op_tok = self.current_token
            self.advance()
            right = res.register(self.term())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def term(self):
        res = ParseResult()

        left = res.register(self.factor())
        if res.error: return res

        while self.current_token != None and self.current_token.type in (T_MUL, T_DIV, T_MODULO, T_PLUS, T_SUB):
            op_tok = self.current_token
            self.advance()
            right = res.register(self.factor())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def factor(self):
        res = ParseResult()
        tok = self.current_token

        if tok.type in (T_PLUS, T_SUB, T_NOT):
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.primary()

    def primary(self):
        res = ParseResult()
        tok = self.current_token

        if tok.type in (T_INT, T_BOOLEAN):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok) if tok.type == T_INT else BooleanNode(tok))

        elif tok.type == T_IDENTIFIER:
            res.register_advancement()
            self.advance()
            if self.current_token and self.current_token.type == T_LPAREN:
                return self.function_call(IdentifierNode(tok))
            return res.success(IdentifierNode(tok))

        elif tok.type == T_LPAREN:
            res.register_advancement()
            self.advance()

            if self.current_token.type == T_LAMBDA:
                lambda_node = res.register(self.lambda_expr())
                if res.error: return res

                if self.current_token.type == T_RPAREN:
                    res.register_advancement()
                    self.advance()
                    return self.function_call(lambda_node)
                else:
                    return res.failure(IllegalCharError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Expected ')'"
                    ))

            expr = res.register(self.expr())
            if res.error: return res

            if self.current_token.type == T_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(IllegalCharError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))

        return res.failure(IllegalCharError(
            tok.pos_start, tok.pos_end,
            "Expected INT, IDENTIFIER, '+', '-', '(', or 'lambda'"
        ))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(T_IF):
            return res.failure(
                IllegalCharError(self.current_token.pos_start, self.current_token.pos_end, "Expected 'if'"))

        self.advance()

        condition = res.register(self.expression())
        if res.error: return res

        if self.current_token.matches(T_LPAREN):
            self.advance()

        if self.current_token.matches(T_THEN):
            self.advance()

        body = res.register(self.expression())
        if res.error: return res

        cases.append((condition, body))

        while self.current_token != None and self.current_token.matches(T_ELSEIF):
            self.advance()

            condition = res.register(self.expression())
            if res.error: return res

            if self.current_token.matches(T_THEN):
                self.advance()

            body = res.register(self.expression())
            if res.error: return res

            cases.append((condition, body))

        if self.current_token != None and self.current_token.matches(T_ELSE):
            self.advance()
            else_case = res.register(self.expression())
            if res.error: return res

        return res.success(IfNode(cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_token.matches(T_FOR):
            return res.failure(
                IllegalCharError(self.current_token.pos_start, self.current_token.pos_end, "Expected 'for'"))
        self.advance()

        start_value = res.register(self.expression())
        if res.error: return res

        if not self.current_token.matches(T_TO):
            return res.failure(
                IllegalCharError(self.current_token.pos_start, self.current_token.pos_end, "Expected 'to'"))
        self.advance()

        end_value = res.register(self.expression())
        if res.error: return res

        if self.current_token.matches(T_STEP):
            self.advance()
            step_value = res.register(self.expression())
            if res.error: return res
        else:
            step_value = None

        if not self.current_token.matches(T_DO):
            return res.failure(
                IllegalCharError(self.current_token.pos_start, self.current_token.pos_end, "Expected 'do'"))
        self.advance()

        body = res.register(self.expression())
        if res.error: return res

        return res.success(ForNode(None, start_value, end_value, step_value, body))

    def function_call(self, func_name_or_lambda):
        res = ParseResult()
        arg_nodes = []

        if not self.current_token.type == T_LPAREN:
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '('"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == T_RPAREN:
            res.register_advancement()
            self.advance()
        else:
            arg_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(IllegalCharError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')', 'IF', 'FOR', 'FUN', INT, IDENTIFIER, '+', '-', '(', or 'lambda'"
                ))

            while self.current_token.type == T_COMMA:
                res.register_advancement()
                self.advance()

                arg_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_token.type != T_RPAREN:
                return res.failure(IllegalCharError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected ',' or ')'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(FunctionCallNode(func_name_or_lambda, arg_nodes))

    def lambda_expr(self):
        res = ParseResult()

        if not self.current_token.matches(T_LAMBDA):
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'lambda'"
            ))

        res.register_advancement()
        self.advance()

        arg_name_toks = []

        if self.current_token.type == T_IDENTIFIER:
            arg_name_toks.append(self.current_token)
            res.register_advancement()
            self.advance()

            while self.current_token.type == T_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != T_IDENTIFIER:
                    return res.failure(IllegalCharError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_token)
                res.register_advancement()
                self.advance()

        if self.current_token.type != T_COLON:
            return res.failure(IllegalCharError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(LambdaNode(arg_name_toks, body))

#######################################
# function
#######################################

class Function:
    def __init__(self, name, body_node, arg_names, parent_context, global_symbol_table):
        self.name = name
        self.body_node = body_node
        self.arg_names = arg_names
        self.parent_context = parent_context
        self.global_symbol_table = global_symbol_table

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter(self.global_symbol_table.copy())
        new_context = Context(self.name, self.parent_context)

        if len(args) != len(self.arg_names):
            return res.failure(RTError(
                self.body_node.pos_start, self.body_node.pos_end,
                f"{len(self.arg_names)} arguments expected, got {len(args)}",
                self.parent_context
            ))

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            interpreter.global_symbol_table[arg_name] = arg_value

        interpreter.context = new_context
        value = res.register(interpreter.visit(self.body_node))
        if res.error: return res
        return res.success(value)

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

#######################################
# INTERPRETER
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if isinstance(res, RTResult):
            if res.error: self.error = res.error
            return res.value
        return res

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

class Interpreter:
    def __init__(self, global_symbol_table):
        self.global_symbol_table = global_symbol_table
        self.context = Context('<program>')

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def visit_FunctionDefNode(self, node):
        res = RTResult()
        func_name = node.name_tok.value
        body_node = node.body_node
        arg_names = [arg_tok.value for arg_tok in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, self.context, self.global_symbol_table)

        self.global_symbol_table[func_name] = func_value
        return res.success(f"Function '{func_name}' defined successfully")

    def visit_FunctionCallNode(self, node):
        res = RTResult()
        args = []

        if isinstance(node.name_tok, LambdaNode):
            func_value = res.register(self.visit_LambdaNode(node.name_tok))
        elif isinstance(node.name_tok, IdentifierNode):
            func_value = self.global_symbol_table.get(node.name_tok.tok.value)
        else:
            func_value = res.register(self.visit(node.name_tok))

        if res.error:
            return res

        if not func_value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{node.name_tok.tok.value if isinstance(node.name_tok, IdentifierNode) else '<anonymous>'}'  is not defined",
                self.context
            ))

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node)))
            if res.error: return res

        return_value = res.register(func_value.execute(args))
        if res.error: return res
        return res.success(return_value)

    def visit_IdentifierNode(self, node):
        var_name = node.tok.value
        value = self.global_symbol_table.get(var_name)

        if value is None:
            return RTResult().failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                self.context
            ))

        return RTResult().success(value)

    def visit_VarAccessNode(self, node):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = self.global_symbol_table.get(var_name)

        if value is None:
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
            ))

        return res.success(value)
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_NumberNode(self, node):
        return RTResult().success(node.tok.value)

    def visit_BooleanNode(self, node):
        return RTResult().success(node.tok.value)

    def visit_BinOpNode(self, node):
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
        if res.error: return res

        if node.op_tok.type == T_DIV:
            if right == 0:
                pos_start = node.op_tok.pos_start if node.op_tok.pos_start else node.left_node.pos_start
                pos_end = node.op_tok.pos_end if node.op_tok.pos_end else node.right_node.pos_end
                return res.failure(DivisionByZeroError(
                    pos_start, pos_end
                ))
            result = left // right
        elif node.op_tok.type == T_PLUS:
            result = left + right
        elif node.op_tok.type == T_SUB:
            result = left - right
        elif node.op_tok.type == T_MUL:
            result = left * right
        elif node.op_tok.type == T_MODULO:
            result = left % right
        elif node.op_tok.type == T_EQEQ:
            result = left == right
        elif node.op_tok.type == T_NOTEQUAL:
            result = left != right
        elif node.op_tok.type == T_GREATERTHAN:
            result = left > right
        elif node.op_tok.type == T_LESSTHAN:
            result = left < right
        elif node.op_tok.type == T_EQGREATERTHAN:
            result = left >= right
        elif node.op_tok.type == T_EQLESSTHAN:
            result = left <= right
        elif node.op_tok.type == T_AND:
            result = left if not left else right
        elif node.op_tok.type == T_OR:
            result = left if left else right

        return res.success(result)

    def visit_UnaryOpNode(self, node):
        res = RTResult()
        value = res.register(self.visit(node.node))
        if res.error: return res

        if node.op_tok.type == T_NOT:
            value = not value
        elif node.op_tok.type == T_SUB:
            value = -value

        return res.success(value)

    def visit_IfNode(self, node):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition))
            if res.error: return res

            if condition_value:
                return res.success(res.register(self.visit(expr)))

        if node.else_case:
            return res.success(res.register(self.visit(node.else_case)))

        return res.success(None)

    def visit_WhileNode(self, node):
        res = RTResult()
        while res.register(self.visit(node.condition_node)):
            if res.error: return res
            res.register(self.visit(node.body_node))
            if res.error: return res
        return res.success(None)

    def visit_ForNode(self, node):
        res = RTResult()

        start_value = res.register(self.visit(node.start_value_node))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value_node))
        if res.error: return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node))
            if res.error: return res
        else:
            step_value = 1

        current_value = start_value
        last_value = None

        while current_value <= end_value:
            last_value = res.register(self.visit(node.body_node))
            if res.error: return res

            print(last_value)

            current_value += step_value

        return res.success(last_value)

    def visit_LambdaNode(self, node):
        res = RTResult()

        func_name = f"<anonymous_{id(node)}>"
        body_node = node.body_node
        arg_names = [arg_tok.value for arg_tok in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, self.context, self.global_symbol_table)

        return res.success(func_value)


#######################################
# RUN
#######################################
global_symbol_table = {}


def run(fn, text):
    # Lexing
    lexer = my_Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Interpreting
    interpreter = Interpreter(global_symbol_table)
    result = interpreter.visit(ast.node)

    return result.value, result.error