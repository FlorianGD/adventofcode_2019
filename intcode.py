"""Intcode program interpreter"""

from pathlib import Path
from typing import List, Generator, Tuple, Dict, DefaultDict
from collections import namedtuple, defaultdict
from itertools import permutations

Instruction = namedtuple("Instruction", "opcode mode1 mode2 mode3")

Intcodes = DefaultDict[int, int]


def read_input(day: str = "day09_input.txt") -> List[int]:
    puzzle_input = Path(day).read_text()
    puzzle = [int(x) for x in puzzle_input.split(",")]
    return puzzle


class Program:

    opcodes = {
        99: "end",
        1: "add",
        2: "mul",
        3: "set_input",
        4: "set_output",
        5: "jump-if-true",
        6: "jump-if-false",
        7: "less than",
        8: "equals",
        9: "adjust_base",
    }

    def __init__(self, puzzle: List[int], input_: List[int] = []):
        self.puzzle = puzzle
        self.intcodes = self._make_intcodes()
        self.pointer = 0
        self.base = 0
        self.input = input_

    def _make_intcodes(self) -> Intcodes:
        intcodes: Intcodes = defaultdict(int)
        for i, val in enumerate(self.puzzle):
            intcodes[i] = val
        return intcodes

    def _get_instruction(self, param: int) -> Instruction:
        opcode = self.opcodes[param % 100]
        modes = {0: "position", 1: "immediate", 2: "relative"}
        mode1 = modes[param // 100 % 10]
        mode2 = modes[param // 1000 % 10]
        mode3 = modes[param // 10000 % 10]
        return Instruction(opcode, mode1, mode2, mode3)

    def _value_from_mode(self, mode: str, val: int) -> int:
        if mode == "position":
            return self.intcodes[val]
        elif mode == "immediate":
            return val
        elif mode == "relative":
            return self.intcodes[self.base + val]
        else:
            raise ValueError(f"Not recognized mode: {mode}.")

    def reset(self, input_: List[int] = []):
        self.intcodes = self._make_intcodes()
        self.pointer = 0
        self.base = 0
        self.input = input_

    def add_input(self, value):
        self.input.append(value)

    def operate(self) -> Generator[int, None, None]:
        """yields the output and the pointer for a given program."""
        while True:
            instr = self._get_instruction(self.intcodes[self.pointer])
            if instr.opcode == "end":
                return

            # 1 parameter instructions
            if instr.opcode == "set_input":
                target = self.intcodes[self.pointer + 1]
                if instr.mode1 == "relative":
                    target += self.base
                self.intcodes[target] = self.input.pop()
                self.pointer += 2
                continue

            a = self._value_from_mode(instr.mode1, self.intcodes[self.pointer + 1])
            if instr.opcode == "set_output":
                self.pointer += 2
                yield a
                continue

            if instr.opcode == "adjust_base":
                self.base += a
                self.pointer += 2
                continue

            # 2 parameters instructions
            # a defined above
            b = self._value_from_mode(instr.mode2, self.intcodes[self.pointer + 2])
            if instr.opcode == "jump-if-true":
                if a:
                    self.pointer = b
                else:
                    self.pointer += 3
                continue

            if instr.opcode == "jump-if-false":
                if not a:
                    self.pointer = b
                else:
                    self.pointer += 3
                continue
            # 3 parameters instructions
            # a, b defined above already
            target = self.intcodes[self.pointer + 3]
            if instr.mode3 == "relative":
                target += self.base

            if instr.opcode == "add":
                self.intcodes[target] = a + b
                self.pointer += 4
                continue

            if instr.opcode == "mul":
                self.intcodes[target] = a * b
                self.pointer += 4
                continue

            if instr.opcode == "less than":
                if a < b:
                    self.intcodes[target] = 1
                    self.pointer += 4
                else:
                    self.intcodes[target] = 0
                    self.pointer += 4
                continue

            if instr.opcode == "equals":
                if a == b:
                    self.intcodes[target] = 1
                    self.pointer += 4
                else:
                    self.intcodes[target] = 0
                    self.pointer += 4
                continue

            raise ValueError(f"opcode {instr.opcode} not recognised.")
