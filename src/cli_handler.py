import os
import time
from .core.storage import Storage
from .core.cnf_generator import CNFGenerator
from .core.io_handler import load_input, export_output
from .algorithms.pysat_solver import PySATSolver
from .algorithms.backtracking_solver import BacktrackingSolver
from .algorithms.brute_force_solver import BruteForceSolver

ALGORITHMS = {
    "Pysat": PySATSolver(),
    "Bruteforce": BruteForceSolver(),
    "Backtracking": BacktrackingSolver()
}

def run_algorithm(input_path: str, algorithm_name: str):
    if algorithm_name not in ALGORITHMS:
        print(f"Algorithm '{algorithm_name}' not found. Available algorithms: {list(ALGORITHMS.keys())}")
        return

    board = load_input(input_path)
    cnf, variable_map = CNFGenerator().generate_cnf(board)

    Storage.board = board
    Storage.cnf = cnf
    Storage.variable_map = variable_map

    # Initialize the selected algorithm
    solver = ALGORITHMS[algorithm_name]

    if algorithm_name == "Pysat":
        # PysatSolver requires CNF and variable_map to be passed directly to the solver
        solver = PySATSolver(cnf)
        start = time.perf_counter()
        satisfiable = solver.solve()
        end = time.perf_counter()
        runtime = end - start

        if satisfiable:
            solution = solver.interpret_model_as_board(board, variable_map)
        else:
            solution = None

    else:
        # For other algorithms, we pass the board and variable_map directly to the solver
        start = time.perf_counter()
        solution = solver.solve(board, cnf, variable_map)
        end = time.perf_counter()
        runtime = end - start

    input_file = os.path.basename(input_path)
    output_path = input_file.replace("input", f"output")
    full_output_path = os.path.join("testcases", "output", output_path)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

    result = export_output(input_path, solution, algorithm_name, runtime)
    with open(full_output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Output written to {full_output_path}")

