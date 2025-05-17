class BacktrackingSolver:
    def __init__(self):
        self.board = []  # Input board: 2D list with "_" (unknown), "T", "G"
        self.cnf = []  # List of clauses (list of literals)
        self.variable_map = {}  # Mapping (row, col) -> variable index (int)
        self.solution = []  # Final solution board after assignment
        self.assignments = []  # List indexed by variable index, values: -1 (unset), 0 (gem), 1 (trap)
        self.unassigned_vars = []  # List of variable indices yet to assign
        self.num_rows = 0
        self.num_cols = 0
        self.solved = False

    def is_clause_satisfied(self, clause):
        """
        Check if the clause is satisfied by current assignments.
        A clause is satisfied if any literal evaluates to True:
        - For positive literal: variable assigned 1 (trap)
        - For negative literal: variable assigned 0 (gem)
        - If variable not assigned (-1), treat literal as potentially satisfied (optimistic)
        """
        for literal in clause:
            var_idx = abs(literal)
            assigned_val = self.assignments[var_idx]
            if assigned_val == -1:
                # Variable not assigned yet, clause might still be satisfiable
                return True
            if literal > 0 and assigned_val == 1:
                return True
            if literal < 0 and assigned_val == 0:
                return True
        return False

    def is_board_consistent(self):
        """
        Check if all clauses are satisfied or still possibly satisfiable
        under current partial assignments.
        """
        for clause in self.cnf:
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def backtrack(self, index=0):
        if self.solved:
            return
        if index == len(self.unassigned_vars):
            # All variables assigned without conflict -> solution found
            self.solved = True
            # Copy the board and fill in assigned values
            self.solution = [row[:] for row in self.board]
            for var_idx in range(1, len(self.assignments)):
                x = (var_idx - 1) // self.num_cols
                y = (var_idx - 1) % self.num_cols
                if self.assignments[var_idx] != -1:
                    self.solution[x][y] = "T" if self.assignments[var_idx] == 1 else "G"
            return

        var = self.unassigned_vars[index]

        for val in [0, 1]:  # Try gem=0 and trap=1
            self.assignments[var] = val
            if self.is_board_consistent():
                self.backtrack(index + 1)
                if self.solved:
                    return
            self.assignments[var] = -1  # Reset on backtrack

    def solve(self, board, cnf, variable_map):
        self.board = board
        self.cnf = [list(set(clause)) for clause in cnf]  # Remove duplicate literals
        self.variable_map = variable_map
        self.num_rows, self.num_cols = len(board), len(board[0])
        self.solved = False
        self.unassigned_vars = []

        max_var_idx = 0
        # Initialize assignments with -1 (unset)
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if board[r][c] == "_":
                    var_idx = variable_map[r, c]
                    self.unassigned_vars.append(var_idx)
                    max_var_idx = max(max_var_idx, var_idx)

        self.assignments = [-1] * (max_var_idx + 1)

        self.backtrack()

        if self.solved:
            return self.solution
        else:
            return None
