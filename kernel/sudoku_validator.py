class SudokuValidator:
    """
    数独校验器，负责验证数独的合法性
    """
    
    def __init__(self):
        pass
    
    def is_valid_board(self, board):
        """
        检查整个数独棋盘是否有效
        参数:
            board: 9x9的二维列表，表示数独棋盘
        返回:
            bool: 棋盘是否有效
        """
        # 检查每一行
        for row in board:
            if not self.is_valid_row(row):
                return False
        
        # 检查每一列
        for col in range(9):
            if not self.is_valid_column(board, col):
                return False
        
        # 检查每个3x3小九宫格
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not self.is_valid_box(board, row, col):
                    return False
        
        return True
    
    def is_valid_row(self, row):
        """
        检查一行是否有效（不包含重复的非零数字）
        参数:
            row: 包含9个数字的列表
        返回:
            bool: 行是否有效
        """
        seen = set()
        for num in row:
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True
    
    def is_valid_column(self, board, col):
        """
        检查一列是否有效（不包含重复的非零数字）
        参数:
            board: 9x9的二维列表
            col: 要检查的列索引
        返回:
            bool: 列是否有效
        """
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True
    
    def is_valid_box(self, board, start_row, start_col):
        """
        检查一个3x3小九宫格是否有效（不包含重复的非零数字）
        参数:
            board: 9x9的二维列表
            start_row: 小九宫格的起始行
            start_col: 小九宫格的起始列
        返回:
            bool: 小九宫格是否有效
        """
        seen = set()
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = board[row][col]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
        return True
    
    def is_valid_move(self, board, row, col, num):
        """
        检查在指定位置放置数字是否有效
        参数:
            board: 9x9的二维列表
            row: 行索引
            col: 列索引
            num: 要放置的数字
        返回:
            bool: 是否可以在该位置放置该数字
        """
        # 检查行
        for i in range(9):
            if board[row][i] == num and i != col:
                return False
        
        # 检查列
        for i in range(9):
            if board[i][col] == num and i != row:
                return False
        
        # 检查3x3小九宫格
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    if (i + start_row != row) or (j + start_col != col):
                        return False
        
        return True
    
    def is_board_complete(self, board):
        """
        检查棋盘是否完全填满
        参数:
            board: 9x9的二维列表
        返回:
            bool: 棋盘是否完全填满
        """
        for row in board:
            for num in row:
                if num == 0:
                    return False
        return True
    
    def validate_board(self, board):
        """
        验证棋盘并返回详细错误信息
        参数:
            board: 9x9的二维列表
        返回:
            dict: 包含验证结果和错误信息的字典
        """
        errors = []
        
        # 检查每一行
        for row_idx, row in enumerate(board):
            seen = {}
            for col_idx, num in enumerate(row):
                if num != 0:
                    if num in seen:
                        errors.append({
                            'type': 'row_duplicate',
                            'row': row_idx,
                            'columns': [seen[num], col_idx],
                            'number': num
                        })
                    seen[num] = col_idx
        
        # 检查每一列
        for col_idx in range(9):
            seen = {}
            for row_idx in range(9):
                num = board[row_idx][col_idx]
                if num != 0:
                    if num in seen:
                        errors.append({
                            'type': 'column_duplicate',
                            'column': col_idx,
                            'rows': [seen[num], row_idx],
                            'number': num
                        })
                    seen[num] = row_idx
        
        # 检查每个3x3小九宫格
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = {}
                for row_offset in range(3):
                    for col_offset in range(3):
                        row_idx = box_row + row_offset
                        col_idx = box_col + col_offset
                        num = board[row_idx][col_idx]
                        if num != 0:
                            if num in seen:
                                errors.append({
                                    'type': 'box_duplicate',
                                    'box': (box_row // 3, box_col // 3),
                                    'positions': [seen[num], (row_idx, col_idx)],
                                    'number': num
                                })
                            seen[num] = (row_idx, col_idx)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'is_complete': self.is_board_complete(board)
        }
