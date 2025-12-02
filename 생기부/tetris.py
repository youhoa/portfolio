import pygame, random, sys, os

pygame.init()

# 화면 기본 설정
WIDTH, HEIGHT = 430, 600
GAME_WIDTH = 300
BLOCK = 30
COLS, ROWS = GAME_WIDTH // BLOCK, HEIGHT // BLOCK
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 테트리스")
clock = pygame.time.Clock()

# 색상
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
LIGHTGRAY = (150, 150, 150)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# 블록 모양
SHAPES = [
    [[1, 1, 1, 1]],                       # I
    [[1, 0, 0], [1, 1, 1]],               # J
    [[0, 0, 1], [1, 1, 1]],               # L
    [[1, 1], [1, 1]],                     # O
    [[0, 1, 1], [1, 1, 0]],               # S
    [[0, 1, 0], [1, 1, 1]],               # T
    [[1, 1, 0], [0, 1, 1]]                # Z
]

# 사운드 (선택)
pygame.mixer.init()
# 효과음을 사용하고 싶다면 아래 파일 경로를 교체 (없으면 무시)
try:
    pygame.mixer.music.load(pygame.mixer.Sound)
except:
    pass

# 게임 보드
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Tetromino 클래스
class Tetromino:
    def __init__(self, shape=None):
        self.shape = shape if shape else random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated = list(zip(*self.shape[::-1]))
        rotated = [list(row) for row in rotated]
        if self.valid(rot_shape=rotated):
            self.shape = rotated

    def valid(self, dx=0, dy=0, rot_shape=None):
        shape = rot_shape if rot_shape else self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return False
                    if ny >= 0 and board[ny][nx]:
                        return False
        return True

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and self.y + y >= 0:
                    board[self.y + y][self.x + x] = self.color


# 함수들
def clear_lines():
    global board
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    board = new_board
    return lines_cleared


def draw_board():
    for y in range(ROWS):
        for x in range(COLS):
            color = board[y][x]
            if color:
                pygame.draw.rect(screen, color, (x * BLOCK, y * BLOCK, BLOCK - 1, BLOCK - 1))
            pygame.draw.rect(screen, GRAY, (x * BLOCK, y * BLOCK, BLOCK, BLOCK), 1)


def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    tetromino.color,
                    ((tetromino.x + x) * BLOCK, (tetromino.y + y) * BLOCK, BLOCK - 1, BLOCK - 1)
                )


def draw_next_block(next_block):
    x_offset = GAME_WIDTH + 20
    y_offset = 100
    label = font.render("NEXT", True, WHITE)
    screen.blit(label, (x_offset + 20, 60))
    for y, row in enumerate(next_block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_block.color,
                                 (x_offset + x * BLOCK, y_offset + y * BLOCK, BLOCK - 2, BLOCK - 2))


def game_over():
    font_big = pygame.font.SysFont("Arial", 50, bold=True)
    text = font_big.render("GAME OVER", True, (255, 80, 80))
    screen.blit(text, (50, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


# 메인 루프
font = pygame.font.SysFont("Arial", 20)
current = Tetromino()
next_block = Tetromino()
fall_time = 0
speed = 0.5
score = 0
level = 1
lines_total = 0

while True:
    dt = clock.tick(FPS) / 1000.0
    fall_time += dt

    # 자동 낙하
    if fall_time >= speed:
        fall_time = 0
        if current.valid(dy=1):
            current.y += 1
        else:
            current.lock()
            lines = clear_lines()
            if lines:
                lines_total += lines
                score += lines * 100 * level
                if lines_total >= level * 5:  # 5줄마다 레벨업
                    level += 1
                    speed = max(0.1, speed - 0.05)
            current = next_block
            next_block = Tetromino()
            if not current.valid():
                game_over()

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current.valid(dx=-1):
                current.x -= 1
            elif event.key == pygame.K_RIGHT and current.valid(dx=1):
                current.x += 1
            elif event.key == pygame.K_DOWN and current.valid(dy=1):
                current.y += 1
            elif event.key == pygame.K_UP:
                current.rotate()
            elif event.key == pygame.K_SPACE:
                while current.valid(dy=1):
                    current.y += 1
                current.lock()
                lines = clear_lines()
                score += lines * 100
                current = next_block
                next_block = Tetromino()
                if not current.valid():
                    game_over()

    # 그리기
    screen.fill(BLACK)
    draw_board()
    draw_tetromino(current)
    draw_next_block(next_block)

    # 점수판
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lines_text = font.render(f"Lines: {lines_total}", True, WHITE)
    screen.blit(score_text, (GAME_WIDTH + 20, 300))
    screen.blit(level_text, (GAME_WIDTH + 20, 330))
    screen.blit(lines_text, (GAME_WIDTH + 20, 360))

    pygame.display.flip()