import sympy as sp

def solve_equation(eq):
    try:
        if eq == "":
            return "", []

        steps = []

        if "=" in eq:
            left, right = eq.split("=")
            x = sp.symbols('x')

            expr = sp.Eq(sp.sympify(left), sp.sympify(right))
            steps.append(f"Given: {expr}")

            sol = sp.solve(expr, x)
            steps.append("Solve for x")

            return str(sol), steps

        else:
            expr = sp.sympify(eq)
            steps.append(f"Expression: {expr}")

            result = expr.evalf()
            steps.append(f"Result: {result}")

            return str(result), steps

    except:
        return "Invalid", ["Error in solving"]
