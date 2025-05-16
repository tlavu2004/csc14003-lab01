from itertools import product, combinations
from typing import List, Tuple, Dict, Union

GridType = List[List[Union[int, str]]]

class CNFGenerator:
    def __init__(self):
        # Initialize the CNF generator, which will hold the CNF clauses and variable mapping
        # CNF clauses are stored as a list of lists, where each inner list represents a clause
        self.cnf_clauses: List[List[int]] = []

        # Mapping of grid coordinates to CNF variables
        # This mapping is used to convert grid coordinates to CNF variable indices
        self.variable_mapping: Dict[Tuple[int, int], int] = {}

    def generate_cnf(self, grid: GridType) -> Tuple[List[List[int]], Dict[Tuple[int, int], int]]:
        """
        Generate CNF clauses from a given grid.
        :param grid: 2D list representing the grid.
        :return: Tuple of CNF clauses and variable mapping.
        """
        self.cnf_clauses = []
        self._init_variable_mapping(grid)
        
        for x, y in product(range(len(grid)), range(len(grid[0]))):
            # Check if the cell is an integer
            if isinstance(grid[x][y], int):
                self._encode_exact_traps(x, y, grid[x][y], grid)
        
        self._remove_duplicate_clauses()
        return self.cnf_clauses, self.variable_mapping
    
    def _init_variable_mapping(self, grid: GridType) -> None:
        """
        Initialize the variable mapping for the grid.
        :param grid: 2D list representing the grid.
        """
        X_MAX, Y_MAX = len(grid), len(grid[0])

        self.variable_mapping = {
            (x, y): x * Y_MAX + y + 1
            for x, y in product(range(X_MAX), range(Y_MAX))
            if grid[x][y] == '_'
        }

    def _get_neighbors(self, x: int, y: int, grid: GridType) -> List[Tuple[int, int]]:
        """
        Get the neighbors of a cell in the grid.
        :param x: Row index of the cell.
        :param y: Column index of the cell.
        :param grid: 2D list representing the grid.
        :return: List of tuples representing the coordinates of the neighbors.
        """
        X_MAX, Y_MAX = len(grid), len(grid[0])

        return [
            (nx, ny)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx != 0 or dy != 0)
            and 0 <= (nx := x + dx) < X_MAX
            and 0 <= (ny := y + dy) < Y_MAX
            and grid[nx][ny] == '_'
        ]
    
    def _encode_exact_traps(self, x: int, y: int, num_traps: int, grid: GridType) -> None:
        """
        Encode the exact number of traps in a cell.
        :param x: Row index of the cell.
        :param y: Column index of the cell.
        :param num_traps: Number of traps to be encoded.
        :param grid: 2D list representing the grid.
        """
        neighbors = self._get_neighbors(x, y, grid)
        variables = [self.variable_mapping[position] for position in neighbors]

        # Check if there are enough variables to encode the traps
        if not variables or len(variables) < num_traps:
            return

        # # Clause to ensure at most `num_traps` traps
        # for comb in combinations(variables, num_traps + 1):
        #     # Create a clause with the negation of the variables in the combination
        #     # This means that at least one of the variables in the combination must be false
        #     clause = [-v for v in comb]
        #     self.cnf_clauses.append(clause)

        # # Clause to ensure at least `num_traps` traps (i.e. at most `len(vars) - num_traps` gems)
        # for comb in combinations(variables, len(variables) - num_traps + 1):
        #     # Create a clause with the variables in the combination
        #     # This means that at least one of the variables in the combination must be true
        #     # This is the opposite of the previous clause and ensures that at least `num_traps` traps are present in the neighbors of the cell
        #     clause = list(comb)
        #     self.cnf_clauses.append(clause)

        # Clause to ensure at most `num_traps` traps

        self.cnf_clauses.extend(
            [[-variable for variable in comb] for comb in combinations(variables, num_traps + 1)]
        )

        # Clause to ensure at least `num_traps` traps (i.e. at most `len(vars) - num_traps` gems)
        self.cnf_clauses.extend(
            [list(comb) for comb in combinations(variables, len(variables) - num_traps + 1)]
        )

    def _remove_duplicate_clauses(self) -> None:
        """
        Remove duplicate CNF clauses (ignoring clause order or literal order).
        This is the most performant method if clause order does not matter.
        """
        self.cnf_clauses = [list(clause) for clause in {frozenset(c) for c in self.cnf_clauses}]
