import sys
from .cli_handler import run_algorithm

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m src.main <input_file_path> <algorithm_name>")
        print("Available algorithms: Pysat, Bruteforce, Backtracking")
        return

    input_path = sys.argv[1]
    algorithm_name = sys.argv[2]

    try:
        run_algorithm(input_path, algorithm_name)
    except ValueError as ve:
        print(f"[ERROR] {ve}")
        print("Please use one of the following algorithms: Pysat, Bruteforce, Backtracking")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_path}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    main()
