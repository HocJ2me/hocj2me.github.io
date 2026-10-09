"""Interpreter – Python 3."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Expression(ABC):
    @abstractmethod
    def interpret(self, ctx: dict) -> int: ...


@dataclass
class NumberExpr(Expression):                       # Terminal
    value: int
    def interpret(self, ctx): return self.value
    def __str__(self): return str(self.value)


@dataclass
class VariableExpr(Expression):                     # Terminal
    name: str
    def interpret(self, ctx): return ctx.get(self.name, 0)
    def __str__(self): return self.name


@dataclass
class BinaryExpr(Expression):                       # Nonterminal (dùng chung cho + - *)
    op: str
    left: Expression
    right: Expression
    OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}

    def interpret(self, ctx):
        return self.OPS[self.op](self.left.interpret(ctx), self.right.interpret(ctx))

    def __str__(self): return f"({self.left} {self.op} {self.right})"


def parse(source: str) -> Expression:
    stack = []
    for tok in source.split():
        if tok in BinaryExpr.OPS:
            right, left = stack.pop(), stack.pop()
            stack.append(BinaryExpr(tok, left, right))
        elif tok.lstrip("-").isdigit():
            stack.append(NumberExpr(int(tok)))
        else:
            stack.append(VariableExpr(tok))
    return stack.pop()


if __name__ == "__main__":
    ctx = {"x": 5, "y": 3}
    for p in ("2 3 +", "x y * 4 -", "x 2 + y 1 - *"):
        ast = parse(p)
        print(f"{p:<16}=> cây: {str(ast):<22} = {ast.interpret(ctx)}")
    ctx["x"] = 10
    ast = parse("x 2 + y 1 - *")
    print(f"Khi x = 10: {ast} = {ast.interpret(ctx)}")
