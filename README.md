# Lab: Gem Hunter

**Gem Hunter** is a grid-based puzzle solver that uses multiple algorithmic strategies (SAT solver, brute-force, backtracking) to find optimal paths, avoid traps, and collect gems. This project was developed as part of the **Intrduction to Artifical Intelligence (CSC14003)** course.

---

## System Requirements

- **Python**: Version **3.13.2** or later  
  Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## How to Run

### Method 1: **Run directly using command-line**

#### Step 1: Install Python and `pip`

Download and install Python from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/)

Make sure `pip` is available after installation.

#### Step 2: Download the source code

- **Option 1**: Unzip the provided `22120443.zip` file from the submission.
- **Option 2**: Clone from GitHub:

  ```bash
  git clone https://github.com/tlavu2004/csc14003-lab01-gem-hunter.git
  cd csc14003-lab01-gem-hunter
  ```

#### Step 3: Install required dependencies (PySAT)

```bash
pip install -r requirements.txt
```

#### Step 4: Run the program

```bash
python -m src.main <input_file_path> <algorithm_name>
```

**Parameters:**

- `<input_file_path>`: Path to the input file, for example:
  - `testcases/input/input_1.txt` (5x5)
  - `testcases/input/input_2.txt` (11x11)
  - `testcases/input/input_3.txt` (20x20)

- `<algorithm_name>`: Algorithm to use:
  - `Pysat`
  - `Bruteforce`
  - `Backtracking`

**Example**:

```bash
python -m src.main testcases/input/input_3.txt Pysat
```

#### Step 5: Check the result

- Output files will be generated under: `testcases/output/`
- File format: `output_<số thứ tự testcase>.txt`

Each output file includes:

- Algorithm name used
- Testcase metadata (path, board size, number of empty cells)
- Final solution (2D result grid)
- Statistics: number of gems, traps, filled cells, CNF clauses
- Execution time
- Or a message indicating no solution was found.

---

### Method 2: **Use interactive CLI menu**

#### Run the interface:

```bash
python menu.py
```

#### Features:

- Select an **input file** from a list of testcases
- Choose an **algorithm** from the menu (Pysat, Bruteforce, Backtracking)
- Display the solution grid directly in the **output file**
- Automatically save the output to `testcases/output/`
- Prompt the user to run another test or exit

---

## Project Structure

```
csc14003-lab01-gem-hunter/
├── src/                 
│   ├── __init__.py
│   ├── main.py  
│   ├── cli_handler.py   
│   ├── core/            
│   │   ├── __init__.py
│   │   ├── io_handler.py
│   │   ├── cnf_generator.py
│   │   └── storage.py
│   └── algorithms/      
│       ├── __init__.py
│       ├── bruteforce.py
│       ├── backtracking.py
│       └── pysat.py
├── testcases/ 
│   ├── input/      
│   │   ├── input_1.txt
│   │   ├── input_2.txt
│   │   └── input_3.txt
│   └── output/               # Auto-generated when running the program
│       ├── output_1.txt
│       ├── output_2.txt
│       └── output_3.txt
├── menu.py
├── requirements.txt
├── description.md
├── cnf_logic.md
└── README.md 
```

---

> [!Note]
> - All external packages are listed in `requirements.txt`
> - Compatible with all platforms that support Python (Windows, macOS, Linux)

---

## Author

- **Trương Lê Anh Vũ - 22120443** – [GitHub Profile](https://github.com/tlavu2004)
