instructions: list[str] = []
programmcounter: int = 0
memory: list[int] = [0]*8 #8 bytes, ein speicherplatz = 1 byte



def read_program(path: str = "prog.txt") -> list[str]:
    with open(path, "r") as program_file:
        instructions = program_file.readlines()
    print(instructions)


def syntax_check(instructions: list[str]) -> int:
    pass


def execute(instructions: list[str]) -> int:
    '''returns Errorcode'''
    pass


#funktionnen
def add():
    pass
def mul():
    pass
#usw