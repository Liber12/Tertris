import tkinter as tk
import random

CELL_SIZE = 30
FIELD_WIDTH = 10
FIELD_HEIGHT = 20

# 各ミノの形状（4x4配列）と色
TETROMINOS = [
    {  # I
        'shape': [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'color': 'cyan', 'id': 1
    },
    {  # O
        'shape': [
            [0, 0, 0, 0],
            [0, 2, 2, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0]
        ],
        'color': 'yellow', 'id': 2
    },
    {  # T
        'shape': [
            [0, 0, 0, 0],
            [3, 3, 3, 0],
            [0, 3, 0, 0],
            [0, 0, 0, 0]
        ],
        'color': 'purple', 'id': 3
    },
    {  # S
        'shape': [
            [0, 0, 0, 0],
            [0, 4, 4, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ],
        'color': 'lime', 'id': 4
    },
    {  # Z
        'shape': [
            [0, 0, 0, 0],
            [5, 5, 0, 0],
            [0, 5, 5, 0],
            [0, 0, 0, 0]
        ],
        'color': 'red', 'id': 5
    },
    {  # J
        'shape': [
            [0, 0, 0, 0],
            [6, 6, 6, 0],
            [0, 0, 6, 0],
            [0, 0, 0, 0]
        ],
        'color': 'blue', 'id': 6
    },
    {  # L
        'shape': [
            [0, 0, 0, 0],
            [7, 7, 7, 0],
            [7, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'color': 'orange', 'id': 7
    },
]

COLOR_MAP = {
    0: 'black',
    1: 'cyan',
    2: 'yellow',
    3: 'purple',
    4: 'lime',
    5: 'red',
    6: 'blue',
    7: 'orange',
}

class TetrisApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=CELL_SIZE*FIELD_WIDTH, height=CELL_SIZE*FIELD_HEIGHT, bg='black')
        self.canvas.pack()
        self.field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 500
        self.spawn_tetromino()
        self.master.bind('<Key>', self.on_key)
        self.game_running = True
        self.game_over = False
        self.game_loop()

    def spawn_tetromino(self):
        self.tetromino = random.choice(TETROMINOS)
        self.tetromino_x = 3
        self.tetromino_y = 0
        if not self.can_move(0, 0):
            self.game_running = False
            self.game_over = True

    def draw(self):
        self.canvas.delete('all')
        self.draw_field()
        self.draw_tetromino()
        self.canvas.create_text(10, 10, anchor='nw', text=f'SCORE: {self.score}', fill='white', font=('Arial', 14))
        self.canvas.create_text(10, 30, anchor='nw', text=f'LEVEL: {self.level}', fill='white', font=('Arial', 14))
        if self.game_over:
            self.canvas.create_text(
                CELL_SIZE*FIELD_WIDTH//2, CELL_SIZE*FIELD_HEIGHT//2,
                text='GAME OVER', fill='white', font=('Arial', 32)
            )

    def draw_field(self):
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                color = COLOR_MAP[self.field[y][x]]
                self.canvas.create_rectangle(
                    x*CELL_SIZE, y*CELL_SIZE,
                    (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                    outline='gray', fill=color
                )

    def draw_tetromino(self):
        shape = self.tetromino['shape']
        color = self.tetromino['color']
        for dy in range(4):
            for dx in range(4):
                if shape[dy][dx]:
                    x = self.tetromino_x + dx
                    y = self.tetromino_y + dy
                    if 0 <= x < FIELD_WIDTH and 0 <= y < FIELD_HEIGHT:
                        self.canvas.create_rectangle(
                            x*CELL_SIZE, y*CELL_SIZE,
                            (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                            outline=color, fill=color
                        )

    def can_move(self, dx, dy):
        shape = self.tetromino['shape']
        for dy_shape in range(4):
            for dx_shape in range(4):
                if shape[dy_shape][dx_shape]:
                    x = self.tetromino_x + dx_shape + dx
                    y = self.tetromino_y + dy_shape + dy
                    if not (0 <= x < FIELD_WIDTH and 0 <= y < FIELD_HEIGHT):
                        return False
                    if 0 <= y < FIELD_HEIGHT and 0 <= x < FIELD_WIDTH:
                        if self.field[y][x] != 0:
                            return False
        return True

    def fix_tetromino(self):
        shape = self.tetromino['shape']
        block_id = self.tetromino['id']
        for dy in range(4):
            for dx in range(4):
                if shape[dy][dx]:
                    x = self.tetromino_x + dx
                    y = self.tetromino_y + dy
                    if 0 <= x < FIELD_WIDTH and 0 <= y < FIELD_HEIGHT:
                        self.field[y][x] = block_id
        self.clear_lines()

    def clear_lines(self):
        new_field = [row for row in self.field if any(cell == 0 for cell in row)]
        cleared = FIELD_HEIGHT - len(new_field)
        for _ in range(cleared):
            new_field.insert(0, [0]*FIELD_WIDTH)
        self.field = new_field
        # スコア・レベル加算
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += [0, 100, 300, 500, 800][cleared]  # テトリス式
            self.level = 1 + self.lines_cleared // 10
            self.fall_speed = max(100, 500 - (self.level-1)*40)

    def game_loop(self):
        if not self.game_running:
            self.draw()
            return
        if self.can_move(0, 1):
            self.tetromino_y += 1
        else:
            self.fix_tetromino()
            self.spawn_tetromino()
        self.draw()
        self.master.after(self.fall_speed, self.game_loop)

    def rotate_tetromino(self):
        # 右回転（時計回り）
        shape = self.tetromino['shape']
        rotated = [[0]*4 for _ in range(4)]
        for y in range(4):
            for x in range(4):
                rotated[x][3-y] = shape[y][x]
        # 衝突判定
        for dy in range(4):
            for dx in range(4):
                if rotated[dy][dx]:
                    x = self.tetromino_x + dx
                    y = self.tetromino_y + dy
                    if not (0 <= x < FIELD_WIDTH and 0 <= y < FIELD_HEIGHT):
                        return  # 回転不可
                    if self.field[y][x] != 0:
                        return  # 回転不可
        self.tetromino['shape'] = rotated

    def on_key(self, event):
        if not self.game_running:
            return
        if event.keysym == 'Left':
            if self.can_move(-1, 0):
                self.tetromino_x -= 1
        elif event.keysym == 'Right':
            if self.can_move(1, 0):
                self.tetromino_x += 1
        elif event.keysym == 'Down':
            if self.can_move(0, 1):
                self.tetromino_y += 1
        elif event.keysym == 'Up':
            self.rotate_tetromino()
        self.draw()

root = tk.Tk()
app = TetrisApp(root)
root.mainloop()
