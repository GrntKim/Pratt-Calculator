import sys 
from lexer import TokenType
class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.curToken = None
		self.peekToken = self.lexer.getToken()
		self.nextToken()
		self.precedence = {
			TokenType.PLUS: 10,
			TokenType.MINUS: 10,
			TokenType.TIMES: 20,
			TokenType.DIVIDE: 20,
		}
		self.prefix_parse_function = {}
		self.infix_parse_function = {}
		self.register_parsing_functions()

	def register_parsing_functions(self):
		self.prefix_parse_function[TokenType.POSNUM] = self.nud_number
		self.prefix_parse_function[TokenType.NEGNUM] = self.nud_number

		self.prefix_parse_function[TokenType.OPBR] = self.nud_grouping

		self.infix_parse_function[TokenType.PLUS] = self.led_bin_op
		self.infix_parse_function[TokenType.MINUS] = self.led_bin_op
		self.infix_parse_function[TokenType.TIMES] = self.led_bin_op
		self.infix_parse_function[TokenType.DIVIDE] = self.led_bin_op

	def nextToken(self):
		self.curToken = self.peekToken
		self.peekToken = self.lexer.getToken()

	def match(self, tokenType):
		if self.curToken.kind == tokenType:
			self.nextToken()
		else:
			sys.exit("Parsing Error")

	def get_precedence(self, kind):
		return self.precedence.get(kind, 0)

	def nud_number(self):
		val = float(self.curToken.text)
		self.nextToken()
		return val

	def nud_grouping(self):
		self.nextToken()
		inner_exp = self.parseExpression(0)
		self.match(TokenType.CLBR) 
		return inner_exp

	def led_bin_op(self, left):
		op = self.curToken.kind
		bp = self.get_precedence(op)

		self.nextToken()

		right = self.parseExpression(bp)

		if op == TokenType.PLUS:
			return left + right
		elif op == TokenType.MINUS:
			return left - right
		elif op == TokenType.TIMES:
			return left * right
		elif op == TokenType.DIVIDE:
			return left / right

		return left

	def parseExpression(self, precedence):
		prefix_fn = self.prefix_parse_function[self.curToken.kind]
		left = prefix_fn()
		while precedence < self.get_precedence(self.curToken.kind):
			infix_fn = self.infix_parse_function[self.curToken.kind]
			left = infix_fn(left)
		return left
