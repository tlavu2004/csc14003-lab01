class BruteforceSolver:
    def __init__(self):
        self.board = []  # 2D board with "_" (unknown), "T" (trap), or "G" (gem)
        self.cnf = []  # CNF clauses representing game rules
        self.variable_map = {}  # Mapping from (x, y) coordinates to variable index
        self.solution_board = []  # Final solved board
        self.unknown_vars = []  # List of variables corresponding to unknown cells
        self.assignment = {}  # Mapping from variable index to assigned value (0 or 1)
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
            var = abs(literal)
            if literal > 0 and self.assignment[var] == 1:
                return True
            elif literal < 0 and self.assignment[var] == 0:
                return True
        return False

    def is_assignment_valid(self, bitmask):
        """
        Assign a truth value to each unknown variable based on the current bitmask.
        Then check if all clauses are satisfied (early pruning applied).
        """
        num_unknowns = len(self.unknown_vars)
        for i in range(num_unknowns):
            var = self.unknown_vars[i]
            bit_value = (bitmask >> (num_unknowns - i - 1)) & 1
            self.assignment[var] = bit_value

        # Early exit if any clause is not satisfied
        for clause in self.cnf:
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def solve(self, board, cnf, variable_map):
        self.board = board
        self.cnf = cnf
        self.variable_map = variable_map
        self.num_rows, self.num_cols = len(board), len(board[0])
        self.solved = False
        self.unknown_vars = []
        self.assignment = {}

        # Identify unknown positions and initialize variable list
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if board[row][col] == "_":
                    var = variable_map[row, col]
                    self.unknown_vars.append(var)
                    self.assignment[var] = -1  # Unassigned initially

        # Try all possible 2^n combinations of truth assignments
        for bitmask in range(1 << len(self.unknown_vars)):
            if self.is_assignment_valid(bitmask):
                self.solved = True

                # Deep copy the original board and fill in the values
                self.solution_board = [row[:] for row in board]
                for var, value in self.assignment.items():
                    x = (var - 1) // self.num_cols
                    y = (var - 1) % self.num_cols
                    self.solution_board[x][y] = "T" if value == 1 else "G"
                break  # Stop at the first valid solution

        return self.solution_board if self.solved else None
