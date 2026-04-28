import pygame
import sys
import os
import random

# 添加kernel目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernel.sudoku_validator import SudokuValidator
from kernel.sudoku_generator import SudokuGenerator
from kernel.game_controller import GameController
from kernel.utils import Utils


class SudokuGame:
    """
    数独游戏主类
    """
    
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        pygame.mixer.init()
        
        # 游戏设置
        self.screenWidth = 600
        self.screenHeight = 700
        self.cellSize = 50
        self.gridOffsetX = 75
        self.gridOffsetY = 120
        
        # 创建窗口
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('数独游戏')
        
        # 字体设置
        self.titleFont = Utils.get_chinese_font(36)
        self.infoFont = Utils.get_chinese_font(24)
        self.cellFont = Utils.get_chinese_font(32)
        self.buttonFont = Utils.get_chinese_font(20)
        
        # 游戏控制器
        self.gameController = GameController()
        
        # 游戏状态
        self.gameStarted = False
        self.message = ''
        self.messageTimer = 0
        self.isPaused = False
        
        # 按钮位置
        self.buttonWidth = 120
        self.buttonHeight = 40
        self.buttonY = self.gridOffsetY + 9 * self.cellSize + 30
        
        # 音效系统
        self.sounds = []
        self._init_sounds()
        
        # 按钮定义
        self.newGameButton = {
            'x': 100,
            'y': self.buttonY,
            'width': self.buttonWidth,
            'height': self.buttonHeight,
            'text': '新游戏',
            'hovered': False
        }
        
        self.checkButton = {
            'x': 240,
            'y': self.buttonY,
            'width': self.buttonWidth,
            'height': self.buttonHeight,
            'text': '暂停',
            'hovered': False
        }
        
        self.answerButton = {
            'x': 380,
            'y': self.buttonY,
            'width': self.buttonWidth,
            'height': self.buttonHeight,
            'text': '答案',
            'hovered': False
        }
        
        # 开始新游戏
        self.start_new_game()
    
    def _init_sounds(self):
        """
        初始化音效系统，创建3个不同的简单音效
        """
        try:
            sampleRate = 44100
            duration = 0.1
            
            # 音效1：高音
            freq1 = 880
            sound1 = self._create_tone(freq1, duration, sampleRate)
            self.sounds.append(sound1)
            
            # 音效2：中音
            freq2 = 660
            sound2 = self._create_tone(freq2, duration, sampleRate)
            self.sounds.append(sound2)
            
            # 音效3：低音
            freq3 = 523
            sound3 = self._create_tone(freq3, duration, sampleRate)
            self.sounds.append(sound3)
            
        except Exception as e:
            print(f"音效初始化失败: {e}")
            self.sounds = []
    
    def _create_tone(self, frequency, duration, sampleRate):
        """
        创建一个简单的音调音效
        参数:
            frequency: 频率 (Hz)
            duration: 持续时间 (秒)
            sampleRate: 采样率
        返回:
            pygame.Sound 对象
        """
        import numpy as np
        
        nSamples = int(round(duration * sampleRate))
        buf = np.zeros((nSamples, 2), dtype=np.int16)
        
        maxSample = 2**15 - 1
        volume = 0.3
        
        for i in range(nSamples):
            t = float(i) / sampleRate
            value = int(maxSample * volume * np.sin(2 * np.pi * frequency * t))
            buf[i][0] = value
            buf[i][1] = value
        
        sound = pygame.sndarray.make_sound(buf)
        sound.set_volume(0.5)
        return sound
    
    def _play_random_sound(self):
        """
        随机播放一个音效
        """
        if self.sounds:
            soundIndex = random.randint(0, len(self.sounds) - 1)
            try:
                self.sounds[soundIndex].play()
            except:
                pass
    
    def start_new_game(self):
        """
        开始新游戏，关卡、时间清零
        """
        # 重置关卡数
        self.gameController.currentLevel = 0
        self.gameController.start_new_game('medium')
        self.gameStarted = True
        self.isPaused = False
        self.message = '游戏开始！请填写数独。'
        self.messageTimer = 120  # 显示2秒
    
    def show_answer(self):
        """
        显示答案
        """
        self.gameController.show_answer()
        self.message = '答案已显示！'
        self.messageTimer = 180
    
    def clear_and_reset(self):
        """
        清空重置，清空关卡、时间
        """
        # 重置关卡数和时间（关卡从1开始）
        self.gameController.currentLevel = 0
        self.gameController.restart_level()
        # 确保关卡为1
        self.gameController.currentLevel = 1
        self.isPaused = False
        self.message = '关卡已重置！'
        self.messageTimer = 120
    
    def toggle_pause(self):
        """
        切换暂停/继续状态
        """
        if self.isPaused:
            # 继续游戏
            self.gameController.resume_game()
            self.isPaused = False
            self.message = '游戏继续'
            self.messageTimer = 60
        else:
            # 暂停游戏
            self.gameController.pause_game()
            self.isPaused = True
            self.message = '游戏已暂停'
            self.messageTimer = 60
    
    def check_and_go_to_next_level(self):
        """
        检查完成状态，如果正确则自动下一关
        """
        # 先刷新屏幕显示输入的数字
        self.draw()
        
        # 显示"检查中"的消息
        self.message = '检查中'
        self.messageTimer = 60
        self.draw()
        pygame.time.delay(300)  # 短暂延迟让用户看到检查中状态
        
        # 执行检查
        result = self.gameController.check_completion()
        self.message = result['message']
        self.messageTimer = 180
        self.draw()
        
        # 如果完成正确，自动开始下一关
        if result['isCorrect']:
            # 等待一下让玩家看到结果
            pygame.time.delay(800)
            
            # 显示"通关，正在准备下一关"的消息
            self.message = '通关，正在准备下一关'
            self.messageTimer = 120
            self.draw()
            pygame.time.delay(500)  # 短暂延迟让用户看到准备下一关状态
            
            # 开始新关卡（不重置计时，保持累计时间）
            self.gameController.start_new_game('medium', resetTimer=False)
            self.isPaused = False
            self.message = '游戏开始！请填写数独。'
            self.messageTimer = 120
    
    def check_board_full_and_validate(self):
        """
        检查棋盘是否填满，如果填满则自动检查
        """
        if self.gameController.is_board_full():
            self.check_and_go_to_next_level()
    
    def handle_events(self):
        """
        处理事件
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
    
    def handle_mouse_click(self, pos):
        """
        处理鼠标点击
        参数:
            pos: 鼠标位置 (x, y)
        """
        x, y = pos
        
        # 检查按钮点击
        # 新游戏按钮
        if Utils.is_mouse_over(
            self.newGameButton['x'], self.newGameButton['y'],
            self.newGameButton['width'], self.newGameButton['height'],
            x, y
        ):
            self.start_new_game()
            return
        
        # 检查中间按钮（暂停/继续 或 清空重置）
        if Utils.is_mouse_over(
            self.checkButton['x'], self.checkButton['y'],
            self.checkButton['width'], self.checkButton['height'],
            x, y
        ):
            # 如果答案已显示，中间按钮是清空重置
            if self.gameController.isAnswerShown:
                self.clear_and_reset()
            else:
                # 否则是暂停/继续
                self.toggle_pause()
            return
        
        # 答案按钮
        if Utils.is_mouse_over(
            self.answerButton['x'], self.answerButton['y'],
            self.answerButton['width'], self.answerButton['height'],
            x, y
        ):
            if not self.gameController.isAnswerShown:
                self.show_answer()
            return
        
        # 检查棋盘点击
        if self.gameStarted and not self.gameController.isAnswerShown:
            col = (x - self.gridOffsetX) // self.cellSize
            row = (y - self.gridOffsetY) // self.cellSize
            
            if 0 <= row < 9 and 0 <= col < 9:
                # 如果游戏暂停，点击棋盘则继续游戏
                if self.isPaused:
                    self.toggle_pause()
                
                # 检查是否点击的是同一个已激活的单元格
                currentSelected = self.gameController.selectedCell
                if currentSelected == (row, col):
                    # 同一个单元格，递增数字
                    success = self.gameController.increment_number()
                    if success:
                        # 播放随机音效
                        self._play_random_sound()
                        # 检查棋盘是否填满
                        self.check_board_full_and_validate()
                else:
                    # 新单元格，激活选中
                    self.gameController.select_cell(row, col)
    
    def handle_key_press(self, key):
        """
        处理键盘按键
        参数:
            key: 按键代码
        """
        if not self.gameStarted or self.gameController.isAnswerShown:
            return
        
        # 如果游戏暂停，按下任意键则继续游戏
        if self.isPaused:
            self.toggle_pause()
            return
        
        # 数字键 1-9
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            self.gameController.input_number(num)
            # 输入数字后检查棋盘是否填满
            self.check_board_full_and_validate()
        
        # 小键盘数字键 1-9
        elif pygame.K_KP1 <= key <= pygame.K_KP9:
            num = key - pygame.K_KP0
            self.gameController.input_number(num)
            # 输入数字后检查棋盘是否填满
            self.check_board_full_and_validate()
        
        # 退格键或删除键清除数字
        elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            self.gameController.input_number(0)
            # 清除数字后也检查棋盘是否填满（如果之前填满过，现在可能不再填满）
            # 不需要自动检查，只在填满时检查
        
        # 方向键移动选择
        elif self.gameController.selectedCell:
            row, col = self.gameController.selectedCell
            
            if key == pygame.K_UP and row > 0:
                self.gameController.select_cell(row - 1, col)
            elif key == pygame.K_DOWN and row < 8:
                self.gameController.select_cell(row + 1, col)
            elif key == pygame.K_LEFT and col > 0:
                self.gameController.select_cell(row, col - 1)
            elif key == pygame.K_RIGHT and col < 8:
                self.gameController.select_cell(row, col + 1)
    
    def update(self):
        """
        更新游戏状态
        """
        # 更新消息计时器
        if self.messageTimer > 0:
            self.messageTimer -= 1
        
        # 更新按钮悬停状态
        mouseX, mouseY = pygame.mouse.get_pos()
        
        # 新游戏按钮
        self.newGameButton['hovered'] = Utils.is_mouse_over(
            self.newGameButton['x'], self.newGameButton['y'],
            self.newGameButton['width'], self.newGameButton['height'],
            mouseX, mouseY
        )
        
        # 中间按钮（暂停/继续 或 清空重置）
        self.checkButton['hovered'] = Utils.is_mouse_over(
            self.checkButton['x'], self.checkButton['y'],
            self.checkButton['width'], self.checkButton['height'],
            mouseX, mouseY
        )
        
        # 根据状态更新中间按钮文本
        if self.gameController.isAnswerShown:
            # 答案已显示，中间按钮是清空重置
            self.checkButton['text'] = '清空重置'
        else:
            # 正常状态，中间按钮是暂停/继续
            if self.isPaused:
                self.checkButton['text'] = '继续'
            else:
                self.checkButton['text'] = '暂停'
        
        # 答案按钮
        self.answerButton['hovered'] = Utils.is_mouse_over(
            self.answerButton['x'], self.answerButton['y'],
            self.answerButton['width'], self.answerButton['height'],
            mouseX, mouseY
        )
    
    def draw(self):
        """
        绘制游戏界面
        """
        # 填充背景
        self.screen.fill(Utils.GAME_COLORS['background'])
        
        # 绘制标题
        Utils.draw_text(
            self.screen, '数独游戏',
            self.screenWidth // 2, 40,
            self.titleFont, Utils.GAME_COLORS['titleText'],
            center=True
        )
        
        # 绘制游戏信息
        if self.gameStarted:
            # 关卡数
            levelText = f'关卡: {self.gameController.get_current_level()}'
            Utils.draw_text(
                self.screen, levelText,
                80, 80,
                self.infoFont, Utils.GAME_COLORS['infoText']
            )
            
            # 计时
            timeText = f'时间: {self.gameController.get_formatted_time()}'
            Utils.draw_text(
                self.screen, timeText,
                380, 80,
                self.infoFont, Utils.GAME_COLORS['infoText']
            )
        
        # 绘制棋盘
        self.draw_board()
        
        # 绘制按钮
        Utils.draw_button(
            self.screen, self.newGameButton['text'],
            self.newGameButton['x'], self.newGameButton['y'],
            self.newGameButton['width'], self.newGameButton['height'],
            self.buttonFont, self.newGameButton['hovered']
        )
        
        Utils.draw_button(
            self.screen, self.checkButton['text'],
            self.checkButton['x'], self.checkButton['y'],
            self.checkButton['width'], self.checkButton['height'],
            self.buttonFont, self.checkButton['hovered']
        )
        
        Utils.draw_button(
            self.screen, self.answerButton['text'],
            self.answerButton['x'], self.answerButton['y'],
            self.answerButton['width'], self.answerButton['height'],
            self.buttonFont, self.answerButton['hovered']
        )
        
        # 绘制消息或暂停提示
        messageY = self.buttonY + self.buttonHeight + 20
        
        # 暂停状态提示（优先显示）
        if self.isPaused:
            pauseText = '游戏已暂停'
            Utils.draw_text(
                self.screen, pauseText,
                self.screenWidth // 2, messageY,
                self.infoFont, Utils.COLORS['red'],
                center=True
            )
        # 绘制其他消息
        elif self.messageTimer > 0 and self.message:
            Utils.draw_text(
                self.screen, self.message,
                self.screenWidth // 2, messageY,
                self.infoFont, Utils.GAME_COLORS['titleText'],
                center=True
            )
        
        # 更新显示
        pygame.display.flip()
    
    def draw_board(self):
        """
        绘制数独棋盘
        """
        if not self.gameStarted or self.gameController.playerBoard is None:
            return
        
        board = self.gameController.playerBoard
        selectedCell = self.gameController.selectedCell
        
        # 绘制单元格背景
        for row in range(9):
            for col in range(9):
                x = self.gridOffsetX + col * self.cellSize
                y = self.gridOffsetY + row * self.cellSize
                
                # 确定单元格背景颜色
                bgColor = Utils.GAME_COLORS['cellBackground']
                
                # 选中的单元格
                if selectedCell and selectedCell == (row, col):
                    bgColor = Utils.GAME_COLORS['selectedCell']
                
                # 初始数字的单元格
                elif self.gameController.is_cell_initial(row, col):
                    bgColor = Utils.GAME_COLORS['initialCell']
                
                # 错误的单元格
                if self.gameController.is_cell_error(row, col):
                    bgColor = Utils.GAME_COLORS['errorCell']
                
                # 绘制单元格背景
                pygame.draw.rect(
                    self.screen, bgColor,
                    (x, y, self.cellSize, self.cellSize)
                )
                
                # 绘制数字
                num = board[row][col]
                if num != 0:
                    # 确定数字颜色
                    if self.gameController.is_cell_error(row, col):
                        textColor = Utils.GAME_COLORS['errorText']
                    elif self.gameController.is_cell_initial(row, col):
                        textColor = Utils.GAME_COLORS['initialText']
                    else:
                        textColor = Utils.GAME_COLORS['playerText']
                    
                    # 绘制数字
                    Utils.draw_text(
                        self.screen, str(num),
                        x + self.cellSize // 2, y + self.cellSize // 2,
                        self.cellFont, textColor,
                        center=True
                    )
        
        # 绘制网格线
        for i in range(10):
            # 确定线的宽度
            lineWidth = 1
            if i % 3 == 0:
                lineWidth = 3
            
            # 垂直线
            x = self.gridOffsetX + i * self.cellSize
            pygame.draw.line(
                self.screen, Utils.GAME_COLORS['gridLine'],
                (x, self.gridOffsetY),
                (x, self.gridOffsetY + 9 * self.cellSize),
                lineWidth
            )
            
            # 水平线
            y = self.gridOffsetY + i * self.cellSize
            pygame.draw.line(
                self.screen, Utils.GAME_COLORS['gridLine'],
                (self.gridOffsetX, y),
                (self.gridOffsetX + 9 * self.cellSize, y),
                lineWidth
            )
    
    def run(self):
        """
        运行游戏主循环
        """
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)


def main():
    """
    主函数
    """
    game = SudokuGame()
    game.run()


if __name__ == '__main__':
    main()
