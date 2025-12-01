from lexer import Lexer, TokenType
from parser import Parser         
import sys

def main():
	while True:
		try:
			src = input("calc > ")
			
			if src.lower() == "exit":
				break
			
			lexer = Lexer(src)
			
			parser = Parser(lexer)
			
			result = parser.parseExpression(0) 
			
			print(f"Result: {result}")
			
		except SystemExit as e:
			print(f"\nError: {e}")
			
		except Exception as e:
			print(f"\nAn unexpected error occurred: {e}")

main()
