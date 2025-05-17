class BacktrackingSolver:
    def __init__(self):
        self.board = []
        self.cnf = []
        self.variable_map = {}
        self.solution = []
        self.assignments = []
        self.unassigned_vars = []
        self.num_rows = 0
        self.num_cols = 0
        self.solved = False
        self.var_to_clauses = {}

    def is_clause_satisfied(self, clause):
        for literal in clause:
            var_idx = abs(literal)
            assigned_val = self.assignments[var_idx]
            if assigned_val == -1:
                return True
            if literal > 0 and assigned_val == 1:
                return True
            if literal < 0 and assigned_val == 0:
                return True
        return False

    def is_board_consistent_for_var(self, var):
        for clause in self.var_to_clauses.get(var, []):
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def backtrack(self, index=0):
        if self.solved:
            return

        if index == len(self.unassigned_vars):
            self.solved = True
            self.solution = [row[:] for row in self.board]
            for var_idx in range(1, len(self.assignments)):
                x = (var_idx - 1) // self.num_cols
                y = (var_idx - 1) % self.num_cols
                if self.assignments[var_idx] != -1:
                    self.solution[x][y] = "T" if self.assignments[var_idx] == 1 else "G"
            return

        var = self.unassigned_vars[index]

        for val in [0, 1]:
            self.assignments[var] = val
            if self.is_board_consistent_for_var(var):
                self.backtrack(index + 1)
                if self.solved:
                    return
            self.assignments[var] = -1

    def solve(self, board, cnf, variable_map):
        self.board = board
        self.cnf = [list(set(clause)) for clause in cnf]
        self.variable_map = variable_map
        self.num_rows, self.num_cols = len(board), len(board[0])
        self.solved = False

        max_var_idx = 0
        self.var_to_clauses = {}

        for clause in self.cnf:
            for literal in clause:
                var = abs(literal)
                if var not in self.var_to_clauses:
                    self.var_to_clauses[var] = []
                self.var_to_clauses[var].append(clause)
                max_var_idx = max(max_var_idx, var)

        self.assignments = [-1] * (max_var_idx + 1)

        # Build and sort unassigned vars by number of related clauses (heuristic)
        self.unassigned_vars = [
            self.variable_map[r, c]
            for r in range(self.num_rows)
                for c in range(self.num_cols)
                    if board[r][c] == "_"
        ]
        self.unassigned_vars.sort(key=lambda var: -len(self.var_to_clauses.get(var, [])))  # descending

        self.backtrack()

        return self.solution if self.solved else None
