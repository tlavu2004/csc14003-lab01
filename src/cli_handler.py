import os
import time
from .core import storage
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
    cnf, var_map = CNFGenerator().generate_cnf(board)

    storage.board = board
    storage.cnf = cnf
    storage.var_map = var_map

    # Khởi tạo solver với cnf
    solver = ALGORITHMS[algorithm_name]

    if algorithm_name == "Pysat":
        # PysatSolver cần khởi tạo với clause, và gọi solve() không tham số
        solver = PySATSolver(cnf)
        start = time.perf_counter()
        satisfiable = solver.solve()
        end = time.perf_counter()
        runtime = end - start

        if satisfiable:
            solution = solver.interpret_model_as_board(board, var_map)
        else:
            solution = None

    else:
        # Các thuật toán khác, giả sử vẫn giữ nguyên tham số solve(board, cnf, var_map)
        start = time.perf_counter()
        solution = solver.solve(board, cnf, var_map)
        end = time.perf_counter()
        runtime = end - start

    input_file = os.path.basename(input_path)
    output_path = input_file.replace("input", f"output")
    full_output_path = os.path.join("testcases", "output", output_path)

    result = export_output(input_path, solution, algorithm_name, runtime)
    with open(full_output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Output written to {full_output_path}")

