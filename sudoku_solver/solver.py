
import time
from typing import List, Set, Tuple, Optional, Callable


class SudokuSolver:
  
    def __init__(self):
      
        self.row_constraints: List[Set[int]] = [set() for _ in range(9)]
        self.col_constraints: List[Set[int]] = [set() for _ in range(9)]
        self.box_constraints: List[Set[int]] = [set() for _ in range(9)]
      
        self.grid: List[List[int]] = [[0] * 9 for _ in range(9)]
        
        self.update_callback: Optional[Callable] = None
        self.delay: float = 0.0
        self.steps: int = 0
        self.solving: bool = False
        
    def get_box_index(self, row: int, col: int) -> int:
       
        return (row // 3) * 3 + (col // 3)
    
    def initialize_constraints(self, grid: List[List[int]]) -> bool:
        
        self.row_constraints = [set() for _ in range(9)]
        self.col_constraints = [set() for _ in range(9)]
        self.box_constraints = [set() for _ in range(9)]
        self.grid = [row[:] for row in grid]  # Deep copy
      
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                if num != 0:
                  
                    if not self._is_valid_placement(row, col, num):
                        return False
                    self._add_constraint(row, col, num)
        
        return True
    
    def _is_valid_placement(self, row: int, col: int, num: int) -> bool:
       
        box_idx = self.get_box_index(row, col)
        
        return (num not in self.row_constraints[row] and
                num not in self.col_constraints[col] and
                num not in self.box_constraints[box_idx])
    
    def _add_constraint(self, row: int, col: int, num: int) -> None:
       
        self.row_constraints[row].add(num)
        self.col_constraints[col].add(num)
        self.box_constraints[self.get_box_index(row, col)].add(num)
        self.grid[row][col] = num
    
    def _remove_constraint(self, row: int, col: int, num: int) -> None:
       
        self.row_constraints[row].discard(num)
        self.col_constraints[col].discard(num)
        self.box_constraints[self.get_box_index(row, col)].discard(num)
        self.grid[row][col] = 0
    
    def _find_empty_cell(self) -> Optional[Tuple[int, int]]:
        
        min_options = 10
        best_cell = None
        
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                  
                    options = sum(1 for num in range(1, 10) 
                                  if self._is_valid_placement(row, col, num))
                  
                    if options < min_options:
                        min_options = options
                        best_cell = (row, col)
                       
                        if options <= 1:
                            return best_cell
        
        return best_cell
    
    def solve(self, visualize: bool = False, delay: float = 0.05,
              callback: Optional[Callable] = None) -> bool:
        
        self.update_callback = callback
        self.delay = delay if visualize else 0
        self.steps = 0
        self.solving = True
        
        result = self._solve_recursive()
        self.solving = False
        return result
    
    def _solve_recursive(self) -> bool:
        
        if not self.solving:
            return False
            
     
        empty_cell = self._find_empty_cell()
    
        if empty_cell is None:
            return True
        
        row, col = empty_cell
        self.steps += 1
       
        for num in range(1, 10):
          
            if self._is_valid_placement(row, col, num):
           
                self._add_constraint(row, col, num)
           
                if self.update_callback and self.delay > 0:
                    self.update_callback(row, col, num, "trying")
                    time.sleep(self.delay)
               
                if self._solve_recursive():
                  
                    if self.update_callback:
                        self.update_callback(row, col, num, "solved")
                    return True
                
                self._remove_constraint(row, col, num)
                
                if self.update_callback and self.delay > 0:
                    self.update_callback(row, col, 0, "backtrack")
        
        return False
    
    def stop_solving(self) -> None:
        
        self.solving = False
    
    def get_solution(self) -> List[List[int]]:
        
        return [row[:] for row in self.grid]
    
    def get_steps(self) -> int:
        
        return self.steps

SAMPLE_PUZZLES = {
    "easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "medium": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ],
    "hard": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ],
    "invalid": [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],  # Two 5s in first row - invalid!
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
}


def get_sample_puzzle(difficulty: str = "easy") -> List[List[int]]:
  
    return [row[:] for row in SAMPLE_PUZZLES.get(difficulty, SAMPLE_PUZZLES["easy"])]
