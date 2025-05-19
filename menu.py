import os
import subprocess

TESTCASES = {
    "1": "testcases/input/input_1.txt",
    "2": "testcases/input/input_2.txt",
    "3": "testcases/input/input_3.txt"
}

ALGORITHMS = {
    "1": "Pysat",
    "2": "Bruteforce",
    "3": "Backtracking"
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_testcase_menu():
    print("GEM HUNTER PROGRAM")
    print("AUTHOR: Trương Lê Anh Vũ.")
    print("STUDENT ID: 22120443.")
    print("---")
    print("List of testcases:")
    for key, path in TESTCASES.items():
        size = os.path.basename(path).split("_")[1].split(".")[0]
        print(f"{key}. Testcase {key}: {size}*{size}")
    print("0. Exit")

def print_algorithm_menu():
    print("---")
    print("List of algorithms:")
    for key, name in ALGORITHMS.items():
        print(f"{key}. Algorithm {key}: {name}")
    print("0. Back")

def main():
    while True:
        clear_screen()
        print_testcase_menu()
        tc_choice = input("Choose testcase: ").strip()
        if tc_choice == "0":
            break
        if tc_choice not in TESTCASES:
            input("Invalid choice. Press Enter to continue...")
            continue

        input_path = TESTCASES[tc_choice]
        clear_screen()
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Bản đồ đã chọn {tc_choice}:")
        print(content)

        print_algorithm_menu()
        algo_choice = input("Choose algorithm: ").strip()
        if algo_choice == "0":
            continue
        if algo_choice not in ALGORITHMS:
            input("Invalid choice. Press Enter to continue...")
            continue

        algorithm_name = ALGORITHMS[algo_choice]

        print("\nRunning algorithm...\n")
        subprocess.run(["python", "-m", "src.main", input_path, algorithm_name])

        cont = input("\nDo you want to continue?\n1. Yes\n0. No\nChoose: ").strip()
        if cont != "1":
            break

if __name__ == "__main__":
    main()
