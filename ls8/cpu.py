"""CPU functionality."""

import sys
program_filename = sys.argv[1]


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # memory or RAM, 256 bytes (1 byte = 8 bits)
        self.ram = [None] * 256
        self.reg = [0] * 8  # register
        self.pc = 0   # program counter (pc)
        self.running = True
        self.function_table = {}
        self.function_table[0x82] = self.alu
        self.function_table[0xa3] = self.alu
        self.function_table[0x65] = self.alu
        self.function_table[0xa4] = self.alu
        self.function_table[0xa2] = self.alu
        self.function_table[0xaa] = self.alu
        self.function_table[0xab] = self.alu
        self.function_table[0xac] = self.alu
        self.function_table[0xad] = self.alu
        self.function_table[0xa1] = self.alu
        self.ldi = 0b10000010
        self.prn = 0b01000111
        self.hlt = 0b00000001

    def ram_read(self, address):
        """
        Returns the value (MDR) stored at a memory address (MAR)
        """
        if self.ram[address] is not None:
            return self.ram[address]
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

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8  --> load integer directly into the register
        #     0b00000000,  # op_a  --> address pointer index
        #     0b00001000,  # op_b --> value: 8
        #     0b01000111,  # PRN R0 --> print the value
        #     0b00000000,  # empty
        #     0b00000001,  # HLT  --> halt/stop
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line)

            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        hex_value = hex(op)
        if op == 0x82:  # !ADD
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 0xa3:  # !DIV
            if self.reg[reg_b] == 0:
                raise ValueError("cannot divide by 0")
                self.running = False
            else:
                self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]
        elif op == 0x65:  # !INC  (increment by 1)
            self.reg[reg_a] += 1
        elif op == 0xa4:  # !MOD
            if self.reg[reg_b] == 0:
                raise ValueError("cannot divide by 0")
                self.running = False
            else:
                self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == 0xa2:  # !MUL (multiply)
            self.reg[reg_a] *= self.reg[reg_b]

        """
        ?Get clarification on these two ALU functions
        elif op == 0xaa: #! OR - bitwise
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 0xab: #! XOR
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        """

        elif op == 0xac:  # ! SHL  bitwise shift left
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 0xad:  # ! SHR  bitwise shift right
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == 0xa1:  # ! SUB
            self.reg[reg_a] -= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        # print(f"TRACE: %02X | %02X %02X %02X |" % (
        print(f"TRACE: %s | %s %s %s |" % (
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
            # Read the instruction stored in memory
            # *ir == instruction reader
            ir = hex(self.ram_read(self.pc))
            op_a = self.ram_read(self.pc + 1')
            op_b = self.ram_read(self.pc + 2')

            if function_table[ir] is not None:
                self.function_table[hex(ir)](ir, op_a, op_b)

            if ir == self.ldi:  # LDI: Load immediate
                self.reg[op_a] = op_b
                self.pc += 3
            elif ir == self.prn:
                op = self.ram_read(self.pc + 1)
                print(self.reg[op])
                self.pc += 2

            elif ir == self.hlt:
                self.running = False
            else:  # Catch invalid / other instruction
                print(
                    f"Unrecognized instruction please review instruction:{ir}")
                self.running = False
            # self.trace()
