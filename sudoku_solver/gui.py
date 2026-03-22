

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import List, Optional

from solver import SudokuSolver, get_sample_puzzle
from utils import (
    is_valid_cell_value,
    find_all_conflicts,
    is_puzzle_valid,
    is_puzzle_solved,
    count_empty_cells,
    get_difficulty_estimate
)

class SudokuGUI:
   
    COLORS = {
        'bg': '#f0f0f0',
        'grid_bg': '#ffffff',
        'prefilled': '#e8e8e8',
        'empty': '#ffffff',
        'solved': '#90EE90',
        'trying': '#FFFFE0',
        'invalid': '#FFB6C1',
        'border': '#000000',
        'box_border': '#333333',
        'text': '#000000',
        'prefilled_text': '#333333',# Pre-filled text
        'button': '#4CAF50',
        'button_text': '#ffffff'
    }
    
    def __init__(self, root: tk.Tk):
       
        self.root = root
        self.root.title("Sudoku Solver - DP + Backtracking")
        self.root.configure(bg=self.COLORS['bg'])
        self.root.resizable(False, False)
        
        self.solver = SudokuSolver()
        
        self.cells: List[List[tk.Entry]] = []
        
        self.prefilled: List[List[bool]] = [[False] * 9 for _ in range(9)]
        
        self.solving = False
        self.solve_thread: Optional[threading.Thread] = None
        
        self.start_time: float = 0
        self.timer_running = False
        
        self.visualize_var = tk.BooleanVar(value=True)
        self.speed_var = tk.StringVar(value="Medium")
        
        self._create_widgets()
        
        self._center_window()
    
    def _center_window(self):
        
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def _create_widgets(self):
        
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg'], padx=20, pady=20)
        main_frame.pack()
        
        title_label = tk.Label(
            main_frame,
            text="🧩 Sudoku Solver",
            font=('Helvetica', 24, 'bold'),
            bg=self.COLORS['bg'],
            fg='#2196F3'
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Dynamic Programming + Backtracking Algorithm",
            font=('Helvetica', 10),
            bg=self.COLORS['bg'],
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 15))
        
        self._create_grid(main_frame)
        
        self._create_controls(main_frame)
        
        self._create_status_bar(main_frame)
    
    def _create_grid(self, parent: tk.Frame):
        
        grid_container = tk.Frame(
            parent,
            bg=self.COLORS['box_border'],
            padx=3,
            pady=3
        )
        grid_container.pack(pady=10)
        
        for box_row in range(3):
            for box_col in range(3):
                box_frame = tk.Frame(
                    grid_container,
                    bg=self.COLORS['border'],
                    padx=1,
                    pady=1
                )
                box_frame.grid(row=box_row, column=box_col, padx=1, pady=1)
                
                for cell_row in range(3):
                    for cell_col in range(3):
                        row = box_row * 3 + cell_row
                        col = box_col * 3 + cell_col
                        
                        cell = tk.Entry(
                            box_frame,
                            width=3,
                            font=('Helvetica', 20, 'bold'),
                            justify='center',
                            bg=self.COLORS['empty'],
                            fg=self.COLORS['text'],
                            relief='solid',
                            borderwidth=1
                        )
                        cell.grid(row=cell_row, column=cell_col, padx=1, pady=1)
                        
                        cell.bind('<KeyRelease>', lambda e, r=row, c=col: self._on_cell_change(r, c))
                        cell.bind('<FocusOut>', lambda e, r=row, c=col: self._validate_cell(r, c))
                        
                        if len(self.cells) <= row:
                            self.cells.append([])
                        self.cells[row].append(cell)
    
    def _create_controls(self, parent: tk.Frame):
        
        control_frame = tk.Frame(parent, bg=self.COLORS['bg'])
        control_frame.pack(pady=15)
        
        button_style = {
            'font': ('Helvetica', 11, 'bold'),
            'width': 15,
            'height': 2,
            'relief': 'raised',
            'cursor': 'hand2'
        }
        
        btn_row1 = tk.Frame(control_frame, bg=self.COLORS['bg'])
        btn_row1.pack(pady=5)
        
        self.solve_btn = tk.Button(
            btn_row1,
            text="🔍 Solve Sudoku",
            command=self._solve_puzzle,
            bg='#4CAF50',
            fg='white',
            **button_style
        )
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            btn_row1,
            text="⏹ Stop",
            command=self._stop_solving,
            bg='#f44336',
            fg='white',
            **button_style
        )
        
        self.clear_btn = tk.Button(
            btn_row1,
            text="🗑 Clear Grid",
            command=self._clear_grid,
            bg='#FF9800',
            fg='white',
            **button_style
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        btn_row2 = tk.Frame(control_frame, bg=self.COLORS['bg'])
        btn_row2.pack(pady=5)
        
        tk.Label(
            btn_row2,
            text="Load Sample:",
            font=('Helvetica', 10),
            bg=self.COLORS['bg']
        ).pack(side=tk.LEFT, padx=5)
        
        difficulties = ['Easy', 'Medium', 'Hard']
        for diff in difficulties:
            btn = tk.Button(
                btn_row2,
                text=diff,
                command=lambda d=diff.lower(): self._load_sample(d),
                font=('Helvetica', 10),
                width=8,
                bg='#2196F3',
                fg='white',
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        opt_row = tk.Frame(control_frame, bg=self.COLORS['bg'])
        opt_row.pack(pady=10)
        
        viz_check = tk.Checkbutton(
            opt_row,
            text="Show Animation",
            variable=self.visualize_var,
            font=('Helvetica', 10),
            bg=self.COLORS['bg']
        )
        viz_check.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            opt_row,
            text="Speed:",
            font=('Helvetica', 10),
            bg=self.COLORS['bg']
        ).pack(side=tk.LEFT, padx=5)
        
        speed_combo = ttk.Combobox(
            opt_row,
            textvariable=self.speed_var,
            values=['Slow', 'Medium', 'Fast'],
            width=10,
            state='readonly'
        )
        speed_combo.pack(side=tk.LEFT, padx=5)
    
    def _create_status_bar(self, parent: tk.Frame):
        
        status_frame = tk.Frame(parent, bg=self.COLORS['bg'])
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Ready. Enter a puzzle or load a sample.")
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Helvetica', 11),
            bg=self.COLORS['bg'],
            fg='#333333'
        )
        self.status_label.pack()
        
        info_frame = tk.Frame(status_frame, bg=self.COLORS['bg'])
        info_frame.pack(pady=5)
        
        self.timer_var = tk.StringVar(value="Time: 0.00s")
        self.timer_label = tk.Label(
            info_frame,
            textvariable=self.timer_var,
            font=('Helvetica', 10),
            bg=self.COLORS['bg'],
            fg='#666666'
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        self.steps_var = tk.StringVar(value="Steps: 0")
        self.steps_label = tk.Label(
            info_frame,
            textvariable=self.steps_var,
            font=('Helvetica', 10),
            bg=self.COLORS['bg'],
            fg='#666666'
        )
        self.steps_label.pack(side=tk.LEFT, padx=20)
        
        self.empty_var = tk.StringVar(value="Empty cells: 0")
        self.empty_label = tk.Label(
            info_frame,
            textvariable=self.empty_var,
            font=('Helvetica', 10),
            bg=self.COLORS['bg'],
            fg='#666666'
        )
        self.empty_label.pack(side=tk.LEFT, padx=20)
    
    def _get_grid(self) -> List[List[int]]:
        
        grid = []
        for row in range(9):
            grid_row = []
            for col in range(9):
                value = self.cells[row][col].get().strip()
                if value == "" or not value.isdigit():
                    grid_row.append(0)
                else:
                    grid_row.append(int(value))
            grid.append(grid_row)
        return grid
    
    def _set_grid(self, grid: List[List[int]], mark_prefilled: bool = True):
        
        for row in range(9):
            for col in range(9):
                self.cells[row][col].config(state='normal')
                self.cells[row][col].delete(0, tk.END)
                
                value = grid[row][col]
                if value != 0:
                    self.cells[row][col].insert(0, str(value))
                    if mark_prefilled:
                        self.prefilled[row][col] = True
                        self.cells[row][col].config(
                            bg=self.COLORS['prefilled'],
                            fg=self.COLORS['prefilled_text']
                        )
                else:
                    self.prefilled[row][col] = False
                    self.cells[row][col].config(
                        bg=self.COLORS['empty'],
                        fg=self.COLORS['text']
                    )
        
        empty = count_empty_cells(grid)
        self.empty_var.set(f"Empty cells: {empty}")
    
    def _on_cell_change(self, row: int, col: int):
        
        cell = self.cells[row][col]
        value = cell.get()
        
        if len(value) > 1:
            cell.delete(0, tk.END)
            cell.insert(0, value[-1])
            value = value[-1]
        
        if value and not is_valid_cell_value(value):
            cell.delete(0, tk.END)
        
        grid = self._get_grid()
        empty = count_empty_cells(grid)
        self.empty_var.set(f"Empty cells: {empty}")
        
        self._highlight_conflicts()
    
    def _validate_cell(self, row: int, col: int):
        
        self._highlight_conflicts()
    
    def _highlight_conflicts(self):
        
        grid = self._get_grid()
        conflicts = find_all_conflicts(grid)
        
        for row in range(9):
            for col in range(9):
                if not self.prefilled[row][col]:
                    self.cells[row][col].config(
                        bg=self.COLORS['empty'],
                        fg=self.COLORS['text']
                    )
        
        for row, col in conflicts:
            self.cells[row][col].config(bg=self.COLORS['invalid'])
    
    def _load_sample(self, difficulty: str):
        
        if self.solving:
            messagebox.showwarning("Warning", "Please stop the current solve first.")
            return
        
        self._reset_state()
        
        puzzle = get_sample_puzzle(difficulty)
        self._set_grid(puzzle, mark_prefilled=True)
        
        estimate = get_difficulty_estimate(puzzle)
        self.status_var.set(f"Loaded {difficulty.capitalize()} puzzle. Difficulty: {estimate}")
    
    def _clear_grid(self):
        
        if self.solving:
            messagebox.showwarning("Warning", "Please stop the current solve first.")
            return
        
        self._reset_state()
        
        for row in range(9):
            for col in range(9):
                self.cells[row][col].config(state='normal')
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].config(
                    bg=self.COLORS['empty'],
                    fg=self.COLORS['text']
                )
                self.prefilled[row][col] = False
        
        self.status_var.set("Grid cleared. Enter a puzzle or load a sample.")
        self.empty_var.set("Empty cells: 81")
    
    def _reset_state(self):
        
        self.timer_var.set("Time: 0.00s")
        self.steps_var.set("Steps: 0")
        self.timer_running = False
    
    def _solve_puzzle(self):
        
        if self.solving:
            return
        
        grid = self._get_grid()
        
        is_valid, error_msg = is_puzzle_valid(grid)
        if not is_valid:
            self.status_var.set(f"❌ Invalid Sudoku: {error_msg}")
            messagebox.showerror("Invalid Puzzle", f"Invalid Sudoku Configuration:\n{error_msg}")
            return
        
        if is_puzzle_solved(grid):
            self.status_var.set("✅ Puzzle is already solved!")
            return
        
        if count_empty_cells(grid) == 81:
            self.status_var.set("⚠ Please enter a puzzle first.")
            return
        
        for row in range(9):
            for col in range(9):
                if grid[row][col] != 0:
                    self.prefilled[row][col] = True
                    self.cells[row][col].config(
                        bg=self.COLORS['prefilled'],
                        state='disabled'
                    )
        
        visualize = self.visualize_var.get()
        speed_map = {'Slow': 0.1, 'Medium': 0.03, 'Fast': 0.005}
        delay = speed_map.get(self.speed_var.get(), 0.03)
        
        self.solving = True
        self.solve_btn.pack_forget()
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.clear_btn.config(state='disabled')
        
        self.status_var.set("🔄 Solving... Please wait.")
        self.start_time = time.time()
        self.timer_running = True
        self._update_timer()
        
        self.solve_thread = threading.Thread(
            target=self._solve_thread,
            args=(grid, visualize, delay)
        )
        self.solve_thread.start()
    
    def _solve_thread(self, grid: List[List[int]], visualize: bool, delay: float):
        
        if not self.solver.initialize_constraints(grid):
            self.root.after(0, self._on_solve_error, "Invalid initial configuration")
            return
        
        def update_callback(row: int, col: int, value: int, state: str):
            self.root.after(0, self._update_cell_visual, row, col, value, state)
        
        success = self.solver.solve(
            visualize=visualize,
            delay=delay,
            callback=update_callback if visualize else None
        )
        
        if success:
            self.root.after(0, self._on_solve_complete)
        else:
            self.root.after(0, self._on_solve_error, "No solution exists")
    
    def _update_cell_visual(self, row: int, col: int, value: int, state: str):
        
        if not self.solving:
            return
        
        cell = self.cells[row][col]
        
        if self.prefilled[row][col]:
            return
        
        cell.config(state='normal')
        cell.delete(0, tk.END)
        
        if value != 0:
            cell.insert(0, str(value))
        
        if state == "trying":
            cell.config(bg=self.COLORS['trying'])
        elif state == "solved":
            cell.config(bg=self.COLORS['solved'])
        elif state == "backtrack":
            cell.config(bg=self.COLORS['empty'])
        
        self.steps_var.set(f"Steps: {self.solver.steps}")
    
    def _on_solve_complete(self):
        
        self.solving = False
        self.timer_running = False
        
        solution = self.solver.get_solution()
        
        for row in range(9):
            for col in range(9):
                if not self.prefilled[row][col]:
                    self.cells[row][col].config(state='normal')
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].insert(0, str(solution[row][col]))
                    self.cells[row][col].config(bg=self.COLORS['solved'])
        
        elapsed = time.time() - self.start_time
        self.timer_var.set(f"Time: {elapsed:.2f}s")
        self.steps_var.set(f"Steps: {self.solver.steps}")
        
        self.status_var.set(f"✅ Sudoku Solved Successfully! (Time: {elapsed:.2f}s, Steps: {self.solver.steps})")
        
        self.stop_btn.pack_forget()
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        self.clear_btn.config(state='normal')
        
        self.empty_var.set("Empty cells: 0")
    
    def _on_solve_error(self, error_msg: str):
        
        self.solving = False
        self.timer_running = False
        
        self.status_var.set(f"❌ {error_msg}")
        messagebox.showerror("Solve Error", error_msg)
        
        self.stop_btn.pack_forget()
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        self.clear_btn.config(state='normal')
        
        for row in range(9):
            for col in range(9):
                self.cells[row][col].config(state='normal')
    
    def _stop_solving(self):
        
        self.solver.stop_solving()
        self.solving = False
        self.timer_running = False
        
        self.status_var.set("⏹ Solving stopped by user.")
        
        self.stop_btn.pack_forget()
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        self.clear_btn.config(state='normal')
        
        for row in range(9):
            for col in range(9):
                self.cells[row][col].config(state='normal')
    
    def _update_timer(self):
        
        if self.timer_running:
            elapsed = time.time() - self.start_time
            self.timer_var.set(f"Time: {elapsed:.2f}s")
            self.root.after(100, self._update_timer)
    
    def run(self):
        
        self.root.mainloop()

def create_app() -> SudokuGUI:
    
    root = tk.Tk()
    app = SudokuGUI(root)
    return app
