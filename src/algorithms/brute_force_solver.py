class BruteforceSolver:
    def __init__(self):
        self.board = []  # 2D board with "_" (unknown), "T" (trap), or "G" (gem)
        self.cnf = []  # CNF clauses representing game rules
        self.variable_map = {}  # Mapping from (x, y) coordinates to variable index
        self.solution_board = []  # Final solved board
        self.unknown_variables = []  # List of variables corresponding to unknown cells
        self.assignment = []  # List of assigned values (0 or 1) indexed by variable
        self.num_rows = 0
        self.num_cols = 0
        self.solved = False

    def is_clause_satisfied(self, clause):
        """
        Check if a clause is satisfied by current assignment.
        Each literal is satisfied if:
        - Positive literal: its variable is assigned 1 (trap)
        - Negative literal: its variable is assigned 0 (gem)
        """
        for literal in clause:
            variable_index = literal if literal > 0 else -literal
            assigned_value = self.assignment[variable_index]
            if (literal > 0 and assigned_value == 1) or (literal < 0 and assigned_value == 0):
                return True
        return False

    def is_assignment_valid(self, bitmask):
        """
        Assign a truth value to each unknown variable based on the current bitmask.
        Then check if all clauses are satisfied (early pruning applied).
        """
        bit_string = bin(bitmask)[2:].zfill(len(self.unknown_variables))  # Precompute bits as string
        for i, variable_index in enumerate(self.unknown_variables):
            self.assignment[variable_index] = int(bit_string[i])

        # Early exit if any clause is not satisfied
        for clause in self.cnf:
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def solve(self, board, cnf, variable_map):
        self.board = board
        self.cnf = [list(set(clause)) for clause in cnf] # Remove duplicate literals in each clause
        self.variable_map = variable_map
        self.num_rows, self.num_cols = len(board), len(board[0])
        self.solved = False
        self.unknown_variables = []

        # Determine the maximum variable index to size the assignment list
        max_variable_index = 0

        # Identify unknown positions and initialize variable list
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if board[row][col] == "_":
                    variable_index = variable_map[row, col]
                    self.unknown_variables.append(variable_index)
                    max_variable_index = max(max_variable_index, variable_index)

        self.assignment = [-1] * (max_variable_index + 1)  # Use list instead of dict for faster access

        # Try all possible 2^n combinations of truth assignments
        for bitmask in range(1 << len(self.unknown_variables)):
            if self.is_assignment_valid(bitmask):
                self.solved = True

                # Construct solution board only once, avoiding deepcopy
                self.solution_board = [
                    [None if cell == "_" else cell for cell in row] for row in board
                ]
                for variable_index in self.unknown_variables:
                    assigned_value = self.assignment[variable_index]
                    x = (variable_index - 1) // self.num_cols
                    y = (variable_index - 1) % self.num_cols
                    self.solution_board[x][y] = "T" if assigned_value == 1 else "G"
                break  # Stop at the first valid solution

        return self.solution_board if self.solved else None
