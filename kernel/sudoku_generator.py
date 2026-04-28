import random
from .sudoku_validator import SudokuValidator


class SudokuGenerator:
    """
    数独生成器，负责生成数独游戏关卡
    """
    
    def __init__(self):
        self.validator = SudokuValidator()
        self.difficultyLevels = {
            'easy': 30,
            'medium': 40,
            'hard': 50,
            'expert': 58
        }
    
    def generate_board(self, difficulty='medium'):
        """
        生成一个完整的数独棋盘
        参数:
            difficulty: 难度级别，影响移除的数字数量
        返回:
            tuple: (solution, puzzle) 分别是完整解决方案和游戏谜题
        """
        # 创建空棋盘
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # 填充完整的数独解决方案
        self._fill_board(board)
        
        # 保存完整解决方案
        solution = [row[:] for row in board]
        
        # 根据难度移除数字
        cellsToRemove = self.difficultyLevels.get(difficulty, 40)
        self._remove_numbers(board, cellsToRemove)
        
        return solution, board
    
    def _fill_board(self, board):
        """
        使用回溯算法填充完整的数独棋盘
        参数:
            board: 9x9的二维列表
        返回:
            bool: 是否成功填充
        """
        emptyCell = self._find_empty_cell(board)
        if not emptyCell:
            return True
        
        row, col = emptyCell
        
        # 随机尝试1-9的数字
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self.validator.is_valid_move(board, row, col, num):
                board[row][col] = num
                
                if self._fill_board(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def _find_empty_cell(self, board):
        """
        查找棋盘上的空单元格
        参数:
            board: 9x9的二维列表
        返回:
            tuple: (row, col) 空单元格的坐标，如果没有空单元格则返回None
        """
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return (row, col)
        return None
    
    def _remove_numbers(self, board, count):
        """
        从棋盘上移除指定数量的数字
        参数:
            board: 9x9的二维列表
            count: 要移除的数字数量
        """
        cells = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= count:
                break
            
            # 保存当前值
            temp = board[row][col]
            board[row][col] = 0
            
            # 检查是否仍然有唯一解
            if self._has_unique_solution(board):
                removed += 1
            else:
                # 如果没有唯一解，恢复数字
                board[row][col] = temp
    
    def _has_unique_solution(self, board):
        """
        检查当前棋盘是否有唯一解
        参数:
            board: 9x9的二维列表
        返回:
            bool: 是否有唯一解
        """
        # 创建棋盘副本
        boardCopy = [row[:] for row in board]
        solutions = []
        
        # 求解数独，最多找到2个解就停止
        self._solve_and_count(boardCopy, solutions, maxSolutions=2)
        
        return len(solutions) == 1
    
    def _solve_and_count(self, board, solutions, maxSolutions=2):
        """
        求解数独并统计解的数量
        参数:
            board: 9x9的二维列表
            solutions: 存储解的列表
            maxSolutions: 最大解数量，超过此数量后停止
        """
        if len(solutions) >= maxSolutions:
            return
        
        emptyCell = self._find_empty_cell(board)
        if not emptyCell:
            # 找到一个解
            solutions.append([row[:] for row in board])
            return
        
        row, col = emptyCell
        
        for num in range(1, 10):
            if self.validator.is_valid_move(board, row, col, num):
                board[row][col] = num
                self._solve_and_count(board, solutions, maxSolutions)
                board[row][col] = 0
                
                if len(solutions) >= maxSolutions:
                    return
    
    def solve_board(self, board):
        """
        求解数独棋盘
        参数:
            board: 9x9的二维列表
        返回:
            bool: 是否成功求解
        """
        emptyCell = self._find_empty_cell(board)
        if not emptyCell:
            return True
        
        row, col = emptyCell
        
        for num in range(1, 10):
            if self.validator.is_valid_move(board, row, col, num):
                board[row][col] = num
                
                if self.solve_board(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def generate_puzzle_with_solution(self, difficulty='medium'):
        """
        生成一个数独谜题及其解决方案
        参数:
            difficulty: 难度级别
        返回:
            dict: 包含puzzle和solution的字典
        """
        solution, puzzle = self.generate_board(difficulty)
        return {
            'puzzle': puzzle,
            'solution': solution,
            'difficulty': difficulty
        }
    
    def get_available_difficulties(self):
        """
        获取可用的难度级别
        返回:
            list: 难度级别列表
        """
        return list(self.difficultyLevels.keys())
