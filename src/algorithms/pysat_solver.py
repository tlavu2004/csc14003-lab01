from typing import List, Tuple, Optional, Any
from pysat.solvers import Glucose3

class PySATSolver:
    def __init__(self, clauses: Optional[List[List[int]]] = None):
        """
        Initialize the PySATSolver with an optional list of clauses.
        :param clauses: A list of clauses, where each clause is a list of integers.
        """
        self._solver = Glucose3()
        self._solved = False
        self._result = None
        self._model = None

        if clauses:
            for clause in clauses:
                self._solver.add_clause(clause)

    def add_clause(self, clause: List[int]) -> None:
        """
        Add a single CNF clause to the solver.
        :param clause: A list of integers representing a clause.
        """
        self._solver.add_clause(clause)
        self._solved = False
        self._result = None
        self._model = None

    def solve(self) -> bool:
        """
        Solve the given CNF and return a formatted board solution.
        :return: True if satisfiable, False otherwise.
        """
        self._result = self._solver.solve()
        self._solved = True
        self._model = set(self._solver.get_model()) if self._result else None

        return self._result

    def get_model(self) -> Optional[List[int]]:
        """
        Return the satisfying assignment if available.
        :return: A list of integers representing the satisfying assignment, or None if unsatisfiable.
        """
        return list(self._model) if self._model else None
    
    def interpret_model_as_board(
            self,
            board: List[List[Any]],
            variable_map: dict[Tuple[int, int], int],
        ) -> Optional[List[List[str]]]:
        """
        Convert the SAT model into a 2D board of 'T', 'G', or original values.

        :param board: Original board layout.
        :param variable_map: Mapping of (i, j) positions to CNF variables.
        :return: Interpreted board or None if unsatisfiable.
        """
        if self._model is None:
            return None
        
        return [
            [
                str(board[row][column]) if isinstance(board[row][column], int)
                else ("T" if variable_map[row, column] in self._model else "G")
                for column in range(len(board[0]))
            ]
            for row in range(len(board))
        ]

    def reset(self):
        """
        Reset the solver to its initial state.
        """
        self._solver.delete()
        self._solver = Glucose3()
        self._solved = False
        self._result = None
        self._model = None