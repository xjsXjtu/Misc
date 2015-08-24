from code_gen import Parser
from lang_backend import LangEnum

if __name__ == "__main__":
    p = Parser(LangEnum.c)
    p.parse_file("test_input.txt")