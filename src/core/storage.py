# src/core/storage.py
from typing import Optional, Dict, Tuple, List, Union

Board = List[List[Union[int, str]]]

CNF = List[List[int]]

VariableMap = Dict[Tuple[int, int], int]

board: Optional[Board] = None
cnf: Optional[CNF] = None
variable_map: Optional[VariableMap] = None
