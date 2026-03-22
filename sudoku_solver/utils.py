
from typing import List, Tuple, Optional


def is_valid_number(value) -> bool:
    
    return value.isdigit() and 1 <= int(value) <= 9


def is_valid_cell_value(value: str) -> bool:
   
    if value == "" or value == "0":
        return True
    return is_valid_number(value)


def validate_grid_format(grid: List[List[int]]) -> Tuple[bool, str]:
    
    if not isinstance(grid, list):
        return False, "Grid must be a list"
    
    if len(grid) != 9:
        return False, f"Grid must have 9 rows, found {len(grid)}"
    
    for i, row in enumerate(grid):
        if not isinstance(row, list):
            return False, f"Row {i} must be a list"
        if len(row) != 9:
            return False, f"Row {i} must have 9 columns, found {len(row)}"
        

        for j, val in enumerate(row):
            if not isinstance(val, int):
                return False, f"Cell ({i},{j}) must be an integer"
            if val < 0 or val > 9:
                return False, f"Cell ({i},{j}) has invalid value {val}"
    
    return True, "Valid format"


def check_row_validity(grid: List[List[int]], row: int) -> Tuple[bool, List[int]]:
   
    seen = {}
    duplicates = []
    
    for col in range(9):
        val = grid[row][col]
        if val != 0:
            if val in seen:
                duplicates.append(col)
                if seen[val] not in duplicates:
                    duplicates.append(seen[val])
            else:
                seen[val] = col
    
    return len(duplicates) == 0, duplicates


def check_column_validity(grid: List[List[int]], col: int) -> Tuple[bool, List[int]]:
   
    seen = {}
    duplicates = []
    
    for row in range(9):
        val = grid[row][col]
        if val != 0:
            if val in seen:
                duplicates.append(row)
                if seen[val] not in duplicates:
                    duplicates.append(seen[val])
            else:
                seen[val] = row
    
    return len(duplicates) == 0, duplicates


def check_box_validity(grid: List[List[int]], box_row: int, box_col: int) -> Tuple[bool, List[Tuple[int, int]]]:
    
    seen = {}
    duplicates = []
    
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            val = grid[r][c]
            if val != 0:
                if val in seen:
                    duplicates.append((r, c))
                    if seen[val] not in duplicates:
                        duplicates.append(seen[val])
                else:
                    seen[val] = (r, c)
    
    return len(duplicates) == 0, duplicates


def find_all_conflicts(grid: List[List[int]]) -> List[Tuple[int, int]]:
    
    conflicts = set()
 
    for row in range(9):
        is_valid, duplicate_cols = check_row_validity(grid, row)
        if not is_valid:
            for col in duplicate_cols:
                conflicts.add((row, col))
    
    for col in range(9):
        is_valid, duplicate_rows = check_column_validity(grid, col)
        if not is_valid:
            for row in duplicate_rows:
                conflicts.add((row, col))
    
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            is_valid, duplicate_cells = check_box_validity(grid, box_row, box_col)
            if not is_valid:
                for cell in duplicate_cells:
                    conflicts.add(cell)
    
    return list(conflicts)


def is_puzzle_valid(grid: List[List[int]]) -> Tuple[bool, str]:
    
    format_valid, format_msg = validate_grid_format(grid)
    if not format_valid:
        return False, format_msg
    
    for row in range(9):
        is_valid, _ = check_row_validity(grid, row)
        if not is_valid:
            return False, f"Duplicate value in row {row + 1}"

    for col in range(9):
        is_valid, _ = check_column_validity(grid, col)
        if not is_valid:
            return False, f"Duplicate value in column {col + 1}"
 
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            is_valid, _ = check_box_validity(grid, box_row, box_col)
            if not is_valid:
                box_num = (box_row // 3) * 3 + (box_col // 3) + 1
                return False, f"Duplicate value in box {box_num}"
    
    return True, "Valid"


def is_puzzle_complete(grid: List[List[int]]) -> bool:
 
    for row in grid:
        for val in row:
            if val == 0:
                return False
    return True


def is_puzzle_solved(grid: List[List[int]]) -> bool:
   
    if not is_puzzle_complete(grid):
        return False
    
    is_valid, _ = is_puzzle_valid(grid)
    return is_valid


def count_empty_cells(grid: List[List[int]]) -> int:
   
    count = 0
    for row in grid:
        for val in row:
            if val == 0:
                count += 1
    return count


def grid_to_string(grid: List[List[int]]) -> str:
  
    lines = []
    lines.append("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
    
    for i, row in enumerate(grid):
        row_str = "|"
        for j, val in enumerate(row):
            cell = str(val) if val != 0 else "."
            row_str += f" {cell}"
            if (j + 1) % 3 == 0:
                row_str += " |"
        lines.append(row_str)
        
        if (i + 1) % 3 == 0:
            lines.append("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
    
    return "\n".join(lines)


def parse_grid_string(grid_string: str) -> Optional[List[List[int]]]:
    
    cleaned = "".join(c for c in grid_string if c.isdigit() or c == ".")
    cleaned = cleaned.replace(".", "0")
    
    if len(cleaned) != 81:
        return None
    
    grid = []
    for i in range(9):
        row = [int(cleaned[i * 9 + j]) for j in range(9)]
        grid.append(row)
    
    return grid


def get_difficulty_estimate(grid: List[List[int]]) -> str:

    empty = count_empty_cells(grid)
    
    if empty <= 35:
        return "Easy"
    elif empty <= 45:
        return "Medium"
    elif empty <= 55:
        return "Hard"
    else:
        return "Expert"
