class BacktrackingSolver:
    def __init__(self):
        self.board = []
        self.cnf = []
        self.variable_map = {}
        self.solution = []
        self.assignments = []
        self.unassigned_variables = []
        self.num_rows = 0
        self.num_cols = 0
        self.solved = False
        self.variable_to_clauses = {}

    def is_clause_satisfied(self, clause):
        for literal in clause:
            variable_idx = abs(literal)
            assigned_value = self.assignments[variable_idx]
            if assigned_value == -1:
                return True
            if (literal > 0 and assigned_value == 1) or (literal < 0 and assigned_value == 0):
                return True
        return False

    def is_assignment_consistent(self, variable_idx):
        for clause in self.variable_to_clauses.get(variable_idx, []):
            if not self.is_clause_satisfied(clause):
                return False
        return True

    def backtrack(self, index=0):
        if self.solved:
            return

        if index == len(self.unassigned_variables):
            self.solved = True
            self.solution = [row[:] for row in self.board]
            for variable_idx in range(1, len(self.assignments)):
                row = (variable_idx - 1) // self.num_cols
                col = (variable_idx - 1) % self.num_cols
                if self.assignments[variable_idx] != -1:
                    self.solution[row][col] = "T" if self.assignments[variable_idx] == 1 else "G"
            return

        variable_idx = self.unassigned_variables[index]

        for assigned_value in [0, 1]:
            self.assignments[variable_idx] = assigned_value
            if self.is_assignment_consistent(variable_idx):
                self.backtrack(index + 1)
                if self.solved:
                    return
            self.assignments[variable_idx] = -1

    def solve(self, board, cnf, variable_map):
        self.board = board
        self.cnf = [list(set(clause)) for clause in cnf]
        self.variable_map = variable_map
        self.num_rows, self.num_cols = len(board), len(board[0])
        self.solved = False
        self.variable_to_clauses = {}

        max_variable_index = 0
        for clause in self.cnf:
            for literal in clause:
                variable_idx = abs(literal)
                self.variable_to_clauses.setdefault(variable_idx, []).append(clause)
                max_variable_index = max(max_variable_index, variable_idx)

        self.assignments = [-1] * (max_variable_index + 1)

        self.unassigned_variables = [
            self.variable_map[row, col]
            for row in range(self.num_rows)
            for col in range(self.num_cols)
            if board[row][col] == "_"
        ]
        self.unassigned_variables.sort(key=lambda idx: -len(self.variable_to_clauses.get(idx, [])))

        self.backtrack()

        return self.solution if self.solved else None
