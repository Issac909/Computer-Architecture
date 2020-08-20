"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        # This will hold out 8 general purpose registers
        self.reg = [0] * 8
        self.pc = 0
        
    def ram_read(self, MAR):
        # MAR = Memory Address Register
            # This will accept the address to read and return the value stored
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # MDR = Memory Data Register
            # This will accept the value to write, and the address to write it to
        self.ram[MAR] = MDR        

    def load(self):
        """Load a program into memory."""
        address = 0
        
        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit()
        
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')[0]
                    cmd = comment_split.strip()

                    if cmd == "":
                        continue

                    instruction = int(cmd, 2)
                    self.ram[address] = instruction
                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file was not found")
            sys.exit()
            
        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def prn(self, operand_a):
        print(operand_a)    

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111 # Print
        HLT = 0b00000001 # Halt
        MUL = 0b10100010 # Multiply
        ADD = 0b10100000 # Addition
        PUSH = 0b01000101 # Push on stack
        POP = 0b01000110 # Pop from stack
        CALL = 0b01010000
        RET = 0b00010001

        running = True

        while running:
            # Instruction register
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
                self.pc += 1

            elif ir == LDI:
                self.ldi(operand_a, operand_b)
                self.pc += 3

            elif ir == PRN:
                self.prn(operand_a)
                self.pc += 2
                
            elif ir == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
                
            elif ir == PUSH:
                self.reg[7] -= 1
                sp = self.reg[7]
                value = self.reg[operand_a]
                self.ram[sp] = value
                self.pc += 2
                
            elif ir == POP:
                sp = self.reg[7]
                value = self.ram[sp]
                self.reg[operand_a] = value
                self.reg[7] += 1
                self.pc += 2
                
            elif ir == CALL:
                address = self.reg[opperand_a]
                requested = self.pc + 2
                self.reg[7] -= 1
                sp = self.reg[7]
                self.ram[sp] = requested
                self.pc = address
                
            elif ir == RET:
                sp = self.reg[7]
                requested = self.ram[sp]
                self.reg[7] += 1
                self.pc = requested

            else:
                print(f"Bad input: {bin(ir)}")
                running = False
