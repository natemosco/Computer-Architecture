"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # memory or RAM, 256 bytes (1 byte = 8 bits)
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0   # program counter (pc)
        self.running = True
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001

    def ram_read(self, address):
        """
        Returns the value (MDR) stored at a memory address (MAR)
        """
        if address in self.ram:
            print(self.ram[address])
        else:
            print(
                f"error, address:{address} either out of bounds or not a valid index")

    def ram_write(self, address, value):
        """Writes a value (MDR =memory data register ) to a memory address register (MAR)."""
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8  --> load integer directly into the register
            0b00000000,  # operand_a  --> address pointer index
            0b00001000,  # operand_b --> value: 8
            0b01000111,  # PRN R0 --> print the value
            0b00000000,  # empty
            0b00000001,  # HLT  --> halt/stop
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            # Read memory address stored in register PC
            # Store result in Instruction Register
            ir = self.ram_read(self.pc)

            # Read the instruction stored in memory
            if ir == self.ldi:  # LDI: Load immediate
                # Read bytes at ram[self.pc + 1]
                operand_a = self.ram_read(self.pc + 1)
                # And ram[self.pc + 2]
                operand_b = self.ram_read(self.pc + 2)

                self.reg[operand_a] = operand_b

            elif ir == self.prn:  # PRN: Print operand
                operand = self.ram_read(self.pc + 1)
                print(self.reg[operand])
                pc += 2

            elif ir == self.hlt:  # HLT: Halt
                running = False

            else:  # Catch invalid / other instruction
                print("Unrecognized instruction")
                self.running = False
