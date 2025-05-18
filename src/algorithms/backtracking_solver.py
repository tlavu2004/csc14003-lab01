class BacktrackingSolver:
    def __init__(self):
        self.board = []
        self.cnf = []
        self.variable_map = {}
        self.solution = []
        self.assignments = []
        self.unassigned_variables = []
        self.num_rows = 0
        self.num_columns = 0
        self.solved = False
        self.variable_to_clauses = {}
        self.clause_status_cache = {}

    def is_clause_satisfied(self, clause):
        key = tuple(sorted(clause))
        if key in self.clause_status_cache:
            return self.clause_status_cache[key]

        for literal in clause:
            var_idx = abs(literal)
            val = self.assignments[var_idx]
            if val == -1:
                self.clause_status_cache[key] = True
                return True
            if (literal > 0 and val == 1) or (literal < 0 and val == 0):
                self.clause_status_cache[key] = True
                return True

        self.clause_status_cache[key] = False
        return False

    def is_assignment_consistent(self, variable_idx):
        for clause in self.variable_to_clauses.get(variable_idx, []):
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def invalidate_clause_cache(self, variable_idx):
        for clause in self.variable_to_clauses.get(variable_idx, []):
            key = tuple(sorted(clause))
            self.clause_status_cache.pop(key, None)

    def backtrack(self, index=0):
        if self.solved:
            return

        if index == len(self.unassigned_variables):
            self.solved = True
            self.solution = []
            for r in range(self.num_rows):
                row_result = []
                for c in range(self.num_columns):
                    cell = self.board[r][c]
                    if cell == "_":
                        var_idx = self.variable_map[r, c]
                        val = self.assignments[var_idx]
                        row_result.append("T" if val == 1 else "G")
                    else:
                        row_result.append(str(cell))
                self.solution.append(row_result)
            return

        var_idx = self.unassigned_variables[index]

        # Try both assignments, prioritize based on polarity heuristic (optional tweak)
        for val in [1, 0]:
            self.assignments[var_idx] = val
            self.invalidate_clause_cache(var_idx)

            if self.is_assignment_consistent(var_idx):
                self.backtrack(index + 1)
                if self.solved:
                    return

            self.assignments[var_idx] = -1
            self.invalidate_clause_cache(var_idx)

    def solve(self, board, cnf, variable_map):
        self.board = board
        # Remove duplicate literals in clause, and redundant clauses
        self.cnf = list({tuple(sorted(set(clause))) for clause in cnf})
        self.variable_map = variable_map
        self.num_rows = len(board)
        self.num_columns = len(board[0])
        self.solved = False
        self.variable_to_clauses = {}
        self.clause_status_cache = {}

        max_idx = 0
        for clause in self.cnf:
            for literal in clause:
                var_idx = abs(literal)
                self.variable_to_clauses.setdefault(var_idx, []).append(clause)
                max_idx = max(max_idx, var_idx)

        self.assignments = [-1] * (max_idx + 1)

        self.unassigned_variables = [
            self.variable_map[r, c]
            for r in range(self.num_rows)
            for c in range(self.num_columns)
            if board[r][c] == "_"
        ]
        # Heuristic: variable with more clauses first
        self.unassigned_variables.sort(key=lambda idx: -len(self.variable_to_clauses.get(idx, [])))

        self.backtrack()

        return self.solution if self.solved else None
