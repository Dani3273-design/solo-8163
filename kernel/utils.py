import pygame
import sys
import os


class Utils:
    """
    工具类，提供常用的工具函数
    """
    
    # 颜色定义
    COLORS = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'gray': (128, 128, 128),
        'lightGray': (200, 200, 200),
        'darkGray': (64, 64, 64),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'lightBlue': (173, 216, 230),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'cyan': (0, 255, 255),
        'pink': (255, 192, 203),
        'brown': (165, 42, 42)
    }
    
    # 游戏特定颜色
    GAME_COLORS = {
        'background': (240, 240, 245),
        'gridLine': (50, 50, 50),
        'thickGridLine': (0, 0, 0),
        'cellBackground': (255, 255, 255),
        'selectedCell': (173, 216, 230),
        'initialCell': (240, 240, 240),
        'errorCell': (255, 200, 200),
        'initialText': (0, 0, 128),
        'playerText': (0, 100, 0),
        'errorText': (200, 0, 0),
        'buttonNormal': (70, 130, 180),
        'buttonHover': (100, 160, 210),
        'buttonText': (255, 255, 255),
        'titleText': (50, 50, 100),
        'infoText': (80, 80, 80)
    }
    
    @staticmethod
    def get_system_fonts():
        """
        获取系统中可用的字体
        返回:
            list: 字体名称列表
        """
        return pygame.font.get_fonts()
    
    @staticmethod
    def get_chinese_font(size=24):
        """
        获取支持中文的字体
        参数:
            size: 字体大小
        返回:
            pygame.font.Font: 字体对象
        """
        # 尝试获取系统中支持中文的字体
        chineseFontNames = [
            'stkaiti',  # 华文楷体
            'simhei',   # 黑体
            'simsun',   # 宋体
            'microsoftyahei',  # 微软雅黑
            'pingfang', # 苹方
            'heiti',    # 黑体
            'songti',   # 宋体
            'kaiti',    # 楷体
            'fangsong', # 仿宋
            'notosanscjksc',  # Noto Sans CJK SC
            'notoserifcjksc'  # Noto Serif CJK SC
        ]
        
        # 尝试使用系统中可用的中文字体
        availableFonts = pygame.font.get_fonts()
        for fontName in chineseFontNames:
            if fontName in availableFonts:
                try:
                    return pygame.font.SysFont(fontName, size)
                except:
                    continue
        
        # 如果没有找到中文字体，尝试使用默认字体
        try:
            return pygame.font.Font(None, size)
        except:
            return pygame.font.SysFont(None, size)
    
    @staticmethod
    def draw_text(surface, text, x, y, font, color=None, center=False):
        """
        在表面上绘制文本
        参数:
            surface: pygame Surface对象
            text: 要绘制的文本
            x: X坐标
            y: Y坐标
            font: 字体对象
            color: 文本颜色
            center: 是否居中
        """
        if color is None:
            color = Utils.GAME_COLORS['infoText']
        
        textSurface = font.render(str(text), True, color)
        textRect = textSurface.get_rect()
        
        if center:
            textRect.center = (x, y)
        else:
            textRect.topleft = (x, y)
        
        surface.blit(textSurface, textRect)
    
    @staticmethod
    def draw_button(surface, text, x, y, width, height, font, isHovered=False):
        """
        绘制按钮
        参数:
            surface: pygame Surface对象
            text: 按钮文本
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            font: 字体对象
            isHovered: 是否悬停状态
        """
        # 选择按钮颜色
        if isHovered:
            buttonColor = Utils.GAME_COLORS['buttonHover']
        else:
            buttonColor = Utils.GAME_COLORS['buttonNormal']
        
        # 绘制按钮背景
        pygame.draw.rect(surface, buttonColor, (x, y, width, height))
        
        # 绘制按钮边框
        pygame.draw.rect(surface, Utils.GAME_COLORS['gridLine'], (x, y, width, height), 2)
        
        # 绘制按钮文本
        Utils.draw_text(
            surface, 
            text, 
            x + width // 2, 
            y + height // 2, 
            font, 
            Utils.GAME_COLORS['buttonText'], 
            center=True
        )
    
    @staticmethod
    def is_mouse_over(x, y, width, height, mouseX, mouseY):
        """
        检查鼠标是否在指定区域内
        参数:
            x: 区域X坐标
            y: 区域Y坐标
            width: 区域宽度
            height: 区域高度
            mouseX: 鼠标X坐标
            mouseY: 鼠标Y坐标
        返回:
            bool: 是否在区域内
        """
        return x <= mouseX <= x + width and y <= mouseY <= y + height
    
    @staticmethod
    def get_resource_path(relativePath):
        """
        获取资源文件的绝对路径
        参数:
            relativePath: 相对路径
        返回:
            str: 绝对路径
        """
        if hasattr(sys, '_MEIPASS'):
            # 如果是打包后的应用
            return os.path.join(sys._MEIPASS, relativePath)
        else:
            # 如果是开发环境
            return os.path.join(os.path.dirname(__file__), '..', relativePath)
    
    @staticmethod
    def format_time(seconds):
        """
        格式化时间
        参数:
            seconds: 秒数
        返回:
            str: 格式化的时间字符串 (MM:SS)
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def create_empty_board():
        """
        创建空的数独棋盘
        返回:
            list: 9x9的二维列表，所有元素为0
        """
        return [[0 for _ in range(9)] for _ in range(9)]
    
    @staticmethod
    def copy_board(board):
        """
        复制数独棋盘
        参数:
            board: 9x9的二维列表
        返回:
            list: 复制后的棋盘
        """
        return [row[:] for row in board]
    
    @staticmethod
    def is_valid_position(row, col):
        """
        检查位置是否在数独棋盘范围内
        参数:
            row: 行索引
            col: 列索引
        返回:
            bool: 是否有效
        """
        return 0 <= row < 9 and 0 <= col < 9
    
    @staticmethod
    def get_box_index(row, col):
        """
        获取单元格所在的3x3小九宫格索引
        参数:
            row: 行索引
            col: 列索引
        返回:
            tuple: (boxRow, boxCol) 小九宫格的行和列索引
        """
        return (row // 3, col // 3)
