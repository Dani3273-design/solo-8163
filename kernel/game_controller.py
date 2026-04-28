import time
from .sudoku_validator import SudokuValidator
from .sudoku_generator import SudokuGenerator


class GameController:
    """
    游戏控制器，负责管理游戏状态和操作
    """
    
    def __init__(self):
        self.validator = SudokuValidator()
        self.generator = SudokuGenerator()
        
        # 游戏状态
        self.currentLevel = 0
        self.startTime = None
        self.elapsedTime = 0
        self.isGameActive = False
        self.isAnswerShown = False
        self.isPaused = False
        
        # 关卡数据
        self.puzzle = None
        self.solution = None
        self.initialPuzzle = None
        
        # 玩家输入
        self.playerBoard = None
        self.selectedCell = None
        self.errorCells = set()
    
    def start_new_game(self, difficulty='medium', resetTimer=True):
        """
        开始新游戏
        参数:
            difficulty: 难度级别
            resetTimer: 是否重置计时（新游戏时为True，继续下一关时为False）
        """
        # 生成新关卡
        puzzleData = self.generator.generate_puzzle_with_solution(difficulty)
        self.puzzle = puzzleData['puzzle']
        self.solution = puzzleData['solution']
        self.initialPuzzle = [row[:] for row in self.puzzle]
        
        # 初始化玩家棋盘
        self.playerBoard = [row[:] for row in self.puzzle]
        
        # 重置游戏状态
        self.currentLevel += 1
        
        # 根据参数决定是否重置计时
        if resetTimer:
            self.startTime = time.time()
            self.elapsedTime = 0
        else:
            # 继续下一关时，保持累计计时，只更新 startTime
            # 先保存当前已用时间（不依赖 isGameActive 状态）
            if self.startTime is not None:
                # 直接根据 startTime 计算时间差并累加
                # 这样无论 isGameActive 是什么状态，都能正确累加时间
                currentTime = time.time()
                timeDelta = currentTime - self.startTime
                # 确保时间差是正数（避免系统时间调整导致的问题）
                if timeDelta > 0:
                    self.elapsedTime += timeDelta
            # 更新 startTime 为当前时间，用于计算下一关卡的时间
            self.startTime = time.time()
        
        self.isGameActive = True
        self.isAnswerShown = False
        self.selectedCell = None
        self.errorCells = set()
    
    def restart_level(self):
        """
        重新开始当前关卡
        """
        if self.initialPuzzle is None:
            return
        
        # 重置玩家棋盘
        self.playerBoard = [row[:] for row in self.initialPuzzle]
        
        # 重置游戏状态
        self.startTime = time.time()
        self.elapsedTime = 0
        self.isGameActive = True
        self.isAnswerShown = False
        self.isPaused = False
        self.selectedCell = None
        self.errorCells = set()
    
    def pause_game(self):
        """
        暂停游戏
        """
        if self.isGameActive and not self.isPaused:
            # 将当前关卡已用时间累加到 elapsedTime
            if self.startTime is not None:
                timeDelta = time.time() - self.startTime
                if timeDelta > 0:
                    self.elapsedTime += timeDelta
            self.isPaused = True
    
    def resume_game(self):
        """
        继续游戏
        """
        if self.isGameActive and self.isPaused:
            # 重新设置开始时间为当前时间
            # elapsedTime 已经包含了暂停前的累计时间
            self.startTime = time.time()
            self.isPaused = False
    
    def select_cell(self, row, col):
        """
        选择单元格
        参数:
            row: 行索引
            col: 列索引
        """
        if 0 <= row < 9 and 0 <= col < 9:
            self.selectedCell = (row, col)
    
    def input_number(self, num):
        """
        输入数字到当前选中的单元格
        参数:
            num: 要输入的数字 (1-9) 或 0 表示清除
        """
        if not self.isGameActive or self.isAnswerShown:
            return
        
        if self.selectedCell is None:
            return
        
        row, col = self.selectedCell
        
        # 检查是否是初始给定的数字（不可修改）
        if self.initialPuzzle[row][col] != 0:
            return
        
        # 输入数字
        self.playerBoard[row][col] = num
        
        # 检查是否有错误
        if num != 0:
            # 检查是否符合规则
            if not self.validator.is_valid_move(self.playerBoard, row, col, num):
                self.errorCells.add((row, col))
            else:
                # 如果之前标记为错误，现在移除
                if (row, col) in self.errorCells:
                    self.errorCells.remove((row, col))
        else:
            # 清除数字时移除错误标记
            if (row, col) in self.errorCells:
                self.errorCells.remove((row, col))
    
    def increment_number(self):
        """
        递增当前选中单元格的数字（用于鼠标点击递增）
        返回:
            bool: 是否成功递增数字
        """
        if not self.isGameActive or self.isAnswerShown:
            return False
        
        if self.selectedCell is None:
            return False
        
        row, col = self.selectedCell
        
        # 检查是否是初始给定的数字（不可修改）
        if self.initialPuzzle[row][col] != 0:
            return False
        
        # 获取当前数字并递增
        currentNum = self.playerBoard[row][col]
        # 递增逻辑：0 -> 1, 1 -> 2, ..., 9 -> 1
        if currentNum == 0:
            newNum = 1
        elif currentNum == 9:
            newNum = 1
        else:
            newNum = currentNum + 1
        
        # 输入新数字
        self.input_number(newNum)
        return True
    
    def check_completion(self):
        """
        检查玩家是否完成了数独
        返回:
            dict: 包含检查结果的字典
        """
        # 检查是否完全填满
        if not self.validator.is_board_complete(self.playerBoard):
            return {
                'isComplete': False,
                'isCorrect': False,
                'message': '数独尚未完成，请继续填写！'
            }
        
        # 检查是否正确
        validationResult = self.validator.validate_board(self.playerBoard)
        
        if validationResult['is_valid']:
            # 停止计时
            self.isGameActive = False
            return {
                'isComplete': True,
                'isCorrect': True,
                'message': '恭喜！数独完成正确！'
            }
        else:
            # 标记错误单元格
            self._mark_error_cells(validationResult['errors'])
            return {
                'isComplete': True,
                'isCorrect': False,
                'message': '数独完成但存在错误，请检查红色标记的单元格！'
            }
    
    def _mark_error_cells(self, errors):
        """
        根据错误信息标记错误单元格
        参数:
            errors: 错误列表
        """
        self.errorCells = set()
        
        for error in errors:
            errorType = error.get('type')
            
            if errorType == 'row_duplicate':
                row = error['row']
                for col in error['columns']:
                    self.errorCells.add((row, col))
            
            elif errorType == 'column_duplicate':
                col = error['column']
                for row in error['rows']:
                    self.errorCells.add((row, col))
            
            elif errorType == 'box_duplicate':
                for pos in error['positions']:
                    self.errorCells.add(pos)
    
    def show_answer(self):
        """
        显示答案
        """
        if self.solution is None:
            return
        
        # 将玩家棋盘设置为答案
        self.playerBoard = [row[:] for row in self.solution]
        self.isAnswerShown = True
        self.isGameActive = False
    
    def get_elapsed_time(self):
        """
        获取已用时间（累计时间 + 当前关卡已用时间）
        返回:
            float: 已用时间（秒）
        """
        if self.isGameActive and not self.isPaused and self.startTime is not None:
            # 返回累计时间 + 当前关卡已用时间
            # 注意：不覆盖 elapsedTime，它专门用来保存各关卡的累计时间
            return self.elapsedTime + (time.time() - self.startTime)
        # 暂停或游戏结束时，直接返回累计时间
        return self.elapsedTime
    
    def is_board_full(self):
        """
        检查棋盘是否完全填满
        返回:
            bool: 棋盘是否完全填满
        """
        return self.validator.is_board_complete(self.playerBoard)
    
    def get_formatted_time(self):
        """
        获取格式化的时间
        返回:
            str: 格式化的时间字符串 (MM:SS)
        """
        elapsed = self.get_elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def is_cell_initial(self, row, col):
        """
        检查单元格是否是初始给定的数字
        参数:
            row: 行索引
            col: 列索引
        返回:
            bool: 是否是初始给定的数字
        """
        if self.initialPuzzle is None:
            return False
        return self.initialPuzzle[row][col] != 0
    
    def is_cell_error(self, row, col):
        """
        检查单元格是否有错误
        参数:
            row: 行索引
            col: 列索引
        返回:
            bool: 是否有错误
        """
        return (row, col) in self.errorCells
    
    def get_current_level(self):
        """
        获取当前关卡数
        返回:
            int: 当前关卡数
        """
        return self.currentLevel
    
    def get_game_state(self):
        """
        获取游戏状态
        返回:
            dict: 包含游戏状态的字典
        """
        return {
            'currentLevel': self.currentLevel,
            'elapsedTime': self.get_elapsed_time(),
            'formattedTime': self.get_formatted_time(),
            'isGameActive': self.isGameActive,
            'isAnswerShown': self.isAnswerShown,
            'selectedCell': self.selectedCell,
            'errorCells': list(self.errorCells)
        }
