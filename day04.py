"""AoC 2019 day 4: Secure Container"""

import re

puzzle = "168630-718098"

start, end = map(int, puzzle.split("-"))

DOUBLES = re.compile(r"(\d)\1")


def validate(password: str) -> bool:
    if not DOUBLES.search(password):
        return False
    a = password[0]
    for b in password[1:]:
        if int(b) < int(a):
            return False
        a = b
    return True


print(f"Solution for part 1: {sum(validate(str(a)) for a in range(start, end +1))}")

TRIPLES = re.compile(r"(\d)\1\1+")


def validate_p2(password: str) -> bool:
    if not (m := DOUBLES.findall(password)):
        return False
    if not set(m) - set(TRIPLES.findall(password)):
        return False
    a = password[0]
    for b in password[1:]:
        if int(b) < int(a):
            return False
        a = b
    return True


print(f"Solution for part 2: {sum(validate_p2(str(a)) for a in range(start, end +1))}")
