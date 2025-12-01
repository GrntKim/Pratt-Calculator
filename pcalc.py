from lexer import Lexer, TokenType
from parser import Parser         
import sys

TITLE = "Pratt Calculator"
AUTHOR = "Junmyeong Kim"
YEAR = "2025"

def main():
	print("--------------------------------------------------")
	print("Calculator CLI: Pratt-based Expression Solver")
	print(f"© {YEAR} Developed by {AUTHOR}")
	print("--------------------------------------------------")
	print(f"Type 'exit' to terminate.\n")
	while True:
		try:
			src = input("pcalc > ")
			
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
