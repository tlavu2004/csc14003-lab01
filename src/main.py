import sys
from .cli_handler import run_algorithm

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m src.main <input_file_path> <algorithm_name>")
        print("Available algorithms: Pysat, Bruteforce, Backtracking")
        return
    input_path = sys.argv[1]
    algorithm_name = sys.argv[2]
    run_algorithm(input_path, algorithm_name)

if __name__ == "__main__":
    main()
