import sys

class Machine:
    def __init__(self, program):
        self.tape = [0]
        self.ip = 0
        self.pc = 0
        self.ops = {
                ">":self.rshift,"<":self.lshift,"+":self.inc,
                "-":self.dec,".":self.show,",":self.take,
                "[":self.open_bracket,"]":self.closed_bracket}
        self.program = list(filter(lambda x: x in self.ops.keys(), program))
    
    def run(self):
        while self.pc < len(self.program)-1:
            self.ops[self.program[self.pc]]()
            self.pc += 1
    
    def rshift(self):
        self.ip += 1
        if self.ip > len(self.tape) - 1:
            self.tape.append(0)

    def lshift(self):
        if self.ip == 0:
            raise Exception("Index out of bounds: Underflow")
        self.ip -= 1
    
    def inc(self):
        self.tape[self.ip] = (self.tape[self.ip] + 1) % 255

    def dec(self):
        self.tape[self.ip] = (self.tape[self.ip] - 1) % 255

    def show(self):
        print(chr(self.tape[self.ip]), end='')

    def take(self):
        self.tape[self.ip] = ascii(input(">")[0])

    def open_bracket(self):
        seeker = self.pc
        counter = 0
        while seeker < len(self.program):
            if self.program[seeker] == "[":
                counter += 1
            if self.program[seeker] == "]":
                counter -= 1
            if counter == 0:
                break
            seeker += 1
        if self.tape[self.ip] == 0:
            self.pc = seeker

    def closed_bracket(self):
        seeker = self.pc
        counter = 0
        while seeker > 0:
            if self.program[seeker] == "]":
                counter += 1
            if self.program[seeker] == "[":
                counter -= 1
            if counter == 0:
                break
            seeker -= 1
        if self.tape[self.ip] != 0:
            self.pc = seeker


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Provide one File path")
        exit(1)

    with open(sys.argv[1], "r") as file:
        program = file.read()
    
    bf = Machine(program)
    bf.run()
