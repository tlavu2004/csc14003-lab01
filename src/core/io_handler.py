def load_input(file_path: str) -> list[list[int | str]]:
    board = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            row = [int(x) if x != "_" else "_" for x in line.strip().split(", ")]
            board.append(row)
    return board

def export_output(input_path: str, solution: list[list[str]], algorithm: str, runtime: float) -> str:
    if solution is None:
        return f"Algorithm: {algorithm}\nNo solution found.\n"

    height = len(solution)
    width = len(solution[0])
    cells = height * width
    blanks = sum(cell in ("T", "G") for row in solution for cell in row)
    gems = sum(cell == "G" for row in solution for cell in row)
    traps = sum(cell == "T" for row in solution for cell in row)
    filled = gems + traps

    from . import storage
    cnfs = len(storage.cnf)

    result = []
    result.append(f"Algorithm: {algorithm}")
    result.append("")
    result.append("TESTCASE INFORMATION")
    result.append(f"Input Path: {input_path}")
    result.append(f"Size: {height}x{width}")
    result.append(f"Blanks: {blanks}/{cells}")
    result.append("")
    result.append("SOLUTION")
    for row in solution:
        result.append(', '.join(row))
    result.append("")
    result.append(f"Filled: {filled}")
    result.append(f"  Gems: {gems}")
    result.append(f" Traps: {traps}")
    result.append("")
    result.append(f"Number of CNF clauses: {cnfs}")
    result.append(f"Run time: {runtime:.6f} seconds")

    return "\n".join(result)
