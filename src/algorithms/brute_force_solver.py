class BruteforceSolver:
    def __init__(self):
        self.board = []  # 2D board with "_" (unknown), "T" (trap), or "G" (gem)
        self.cnf = []  # CNF clauses representing game rules (list of lists of literals)
        self.variable_map = {}  # Mapping from (row, column) to variable index (int)
        self.solution_board = []  # Final solved board after assigning traps/gems
        self.unknown_vars = []  # List of variable indices for unknown cells ("_")
        self.var_assignment = []  # List indexed by variable, values: -1 (unset), 0 (gem), 1 (trap)
        self.num_rows = 0
        self.num_columns = 0
        self.solved = False

    def is_clause_satisfied(self, clause):
        """
        Check if a clause is satisfied by current assignment.
        A literal is satisfied if:
          - positive literal: assigned 1 (trap)
          - negative literal: assigned 0 (gem)
        """
        for literal in clause:
            var_idx = abs(literal)
            assigned_val = self.var_assignment[var_idx]
            if (literal > 0 and assigned_val == 1) or (literal < 0 and assigned_val == 0):
                return True
        return False

    def validate_assignment(self, bitmask):
        """
        Assign truth values to unknown variables according to bitmask.
        Use bit operations for speed instead of string conversion.
        Return True if all CNF clauses satisfied; else False.
        """
        for i, var_idx in enumerate(self.unknown_vars):
            val = (bitmask >> i) & 1  # extract bit i
            self.var_assignment[var_idx] = val

        for clause in self.cnf:
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def solve(self, board, cnf, variable_map):
        # Remove duplicate literals in clauses to optimize
        self.cnf = [list(set(clause)) for clause in cnf]
        self.board = board
        self.variable_map = variable_map
        self.num_rows, self.num_columns = len(board), len(board[0])
        self.solved = False
        self.unknown_vars = []

        max_var_idx = 0

        # Identify unknown variables from the board
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                if board[r][c] == "_":
                    var_idx = variable_map[r, c]
                    self.unknown_vars.append(var_idx)
                    max_var_idx = max(max_var_idx, var_idx)

        # Initialize assignments: -1 means unassigned
        self.var_assignment = [-1] * (max_var_idx + 1)

        # Brute force all combinations of assignments for unknown vars
        for bitmask in range(1 << len(self.unknown_vars)):
            if self.validate_assignment(bitmask):
                self.solved = True
                # Build solution board (avoid deepcopy by reconstructing)
                self.solution_board = [
                    [None if cell == "_" else cell for cell in row] for row in board
                ]
                for var_idx in self.unknown_vars:
                    assigned_val = self.var_assignment[var_idx]
                    x = (var_idx - 1) // self.num_columns
                    y = (var_idx - 1) % self.num_columns
                    self.solution_board[x][y] = "T" if assigned_val == 1 else "G"
                break

        return self.solution_board if self.solved else None
