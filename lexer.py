# -----------------------------------------------------------------------------
# [Reference Note]
# The basic structure of this Lexer (including nextChar, peek, abort methods)
# was adapted from 'teenytinycompiler' by Austin Henley.
#
# Original Source: https://github.com/AZHenley/teenytinycompiler/blob/master/lex.py
# License: MIT License
#
# Modifications:
# - Simplified to support arithmetic expressions (no keywords/strings).
# - Added support for negative numbers and parentheses.
# - Changed TokenType implementation to use enum.auto().
# -----------------------------------------------------------------------------

import enum
import sys

class Lexer:
	def __init__(self, src):
		self.src = src
		self.curChar = ''
		self.curPos = -1
		self.nextChar()

	def nextChar(self):
		self.curPos += 1
		if self.curPos >= len(self.src):
			self.curChar = '\0'
		else:
		 	self.curChar = self.src[self.curPos]

	def peek(self):
		if self.curPos + 1 >= len(self.src):
			return '\0'
		return self.src[self.curPos+1]

	def abort(self, msg):
		sys.exit("Lexing error. " + msg)

	def skipWhitespace(self):
		while self.curChar == ' ':
			self.nextChar()

	def getToken(self):
		self.skipWhitespace()
		token = None
		minusSign = False

		if self.curChar == '-':
			if not self.peek().isdigit():
				token = Token(self.curChar, TokenType.MINUS)
				self.nextChar()
				self.skipWhitespace()
				return token
			else: 
				minusSign = True
				self.nextChar()

		if self.curChar.isdigit():
			startPos = self.curPos
			while self.peek().isdigit():
				self.nextChar()
			if self.peek() == '.':
				self.nextChar()
				if not self.peek().isdigit():
					self.abort("Illegal character in number.")
				while self.peek().isdigit():
					self.nextChar()
			number = self.src[startPos : self.curPos+1]
			if minusSign: 
				token = Token('-' + number, TokenType.NEGNUM)
			else:
				token = Token(number, TokenType.POSNUM)
			self.nextChar()
			return token
				
		if self.curChar == '+':
			token = Token(self.curChar, TokenType.PLUS)
		elif self.curChar == '*':
			token = Token(self.curChar, TokenType.TIMES)
		elif self.curChar == '/':
			token = Token(self.curChar, TokenType.DIVIDE)
		elif self.curChar == '(':
			token = Token(self.curChar, TokenType.OPBR)
		elif self.curChar == ')':
			token = Token(self.curChar, TokenType.CLBR)
		elif self.curChar == '\n':
			token = Token(self.curChar, TokenType.NEWLINE)
		elif self.curChar == '\0':
			token = Token(self.curChar, TokenType.EOF)
		else:
			self.abort("Unknown token: " + self.curChar)

		self.nextChar()
		return token

class Token:
	def __init__(self, tokenText, tokenKind):
		self.text = tokenText
		self.kind = tokenKind

	@staticmethod
	def checkToken(tokenText):
		for kind in TokenType:
			if kind.name == tokenText:
				return kind

class TokenType(enum.Enum):
	EOF = enum.auto()
	NEWLINE = enum.auto()
	POSNUM = enum.auto()
	NEGNUM = enum.auto()
	OPBR = enum.auto()
	CLBR = enum.auto()
	PLUS = enum.auto()
	MINUS = enum.auto()
	TIMES = enum.auto()
	DIVIDE = enum.auto()
