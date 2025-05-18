from . import Storage

def load_input(file_path: str) -> list[list[int | str]]:
    """
    Load the input board from a file.
    Args:
        file_path (str): The path to the input file.
    Returns:
        list[list[int | str]]: The board represented as a list of lists.
    """
    board = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            row = [int(x) if x != "_" else "_" for x in line.strip().split(", ")]
            board.append(row)
    return board


def _format_solution_output(
    algorithm: str,
    input_path: str,
    solution: list[list[str]],
    runtime: float,
    cnfs: int
) -> str:
    """
    Format the solution output for the given algorithm and input path.
    Args:
        algorithm (str): The name of the algorithm used.
        input_path (str): The path to the input file.
        solution (list[list[str]]): The solution board.
        runtime (float): The runtime of the algorithm.
        cnfs (int): The number of CNF clauses.
    """
    height = len(solution)
    width = len(solution[0]) if height > 0 else 0
    cells = height * width
    blanks = sum(cell in ("T", "G") for row in solution for cell in row)
    gems = sum(cell == "G" for row in solution for cell in row)
    traps = sum(cell == "T" for row in solution for cell in row)
    filled = gems + traps

    header = [
        f"Algorithm: {algorithm}",
        "",
        "TESTCASE INFORMATION",
        f"Input Path: {input_path}",
        f"Size: {height}x{width}",
        f"Blanks: {blanks}/{cells}",
        "",
        "SOLUTION"
    ]

    solution_lines = [', '.join(row) for row in solution]

    summary = [
        "",
        "SUMMARY",
        f"Filled: {filled}",
        f"  Gems: {gems}",
        f" Traps: {traps}",
        "",
        f"Number of CNF clauses: {cnfs}",
        f"Run time: {runtime:.6f} seconds"
    ]

    output_lines = header + solution_lines + summary

    return "\n".join(output_lines)


def export_output(input_path: str, solution: list[list[str]], algorithm: str, runtime: float) -> str:
    """
    Export the solution to a formatted string.
    Args:
        input_path (str): The path to the input file.
        solution (list[list[str]]): The solution board.
        algorithm (str): The name of the algorithm used.
        runtime (float): The runtime of the algorithm.
    Returns:
        str: The formatted output string.
    """
    if solution is None:
        return f"Algorithm: {algorithm}\nNo solution found.\n"

    cnfs = len(Storage.cnf)

    return _format_solution_output(algorithm, input_path, solution, runtime, cnfs)
