import pygame


class Block:
    def __init__(self, pos: tuple):
        self.posx, self.posy = pos[0], pos[1]
        self.rect = pygame.Rect(self.posx, self.posy, 90, 90)
        self.is_available = True

    def reset(self):
        self.is_available = True

    # Needed for debugging
    def draw(self):
        pygame.draw.rect(screen, Black, self.rect, 1)


class Player:
    def __init__(self, xo: str, color: tuple):
        self.xo = xo.lower()
        self.color = color
        self.win = False
        # We make a list of the clicked blocks, so we can display the X/O on their place
        # TODO This can be optimized if i make the blocks into dictionary with indexes instead of 2 separate lists
        self.taken_blocks_id = []
        self.taken_blocks_pos = []
        # The pos of the X/O and the pos of the block have a small difference, padding
        # for X it's 18, for O it's 45
        self.padding = 18 if self.xo == "x" else 45

    def __str__(self):
        return f"Player {self.xo.upper()}"

    def on_click(self, ev, bloks: list):
        global Turn
        for index, blok in enumerate(bloks):
            if blok.rect.collidepoint(ev.pos):
                if blok.is_available:
                    blok.is_available = False
                    Turn = not Turn     # Changing the turn to the opposite player
                    # Appending the positions of the clicked block
                    self.taken_blocks_pos.append([blok.posx + self.padding, blok.posy + self.padding])
                    # And the IDs
                    self.taken_blocks_id.append(index)

    def reset(self):
        self.win = False
        self.taken_blocks_id = []
        self.taken_blocks_pos = []

    def check_win(self):
        if 0 in self.taken_blocks_id:
            if 1 in self.taken_blocks_id and 2 in self.taken_blocks_id:
                self.win = True
            if 3 in self.taken_blocks_id and 6 in self.taken_blocks_id:
                self.win = True
            if 4 in self.taken_blocks_id and 8 in self.taken_blocks_id:
                self.win = True
        if 1 in self.taken_blocks_id:
            if 4 in self.taken_blocks_id and 7 in self.taken_blocks_id:
                self.win = True
        if 2 in self.taken_blocks_id:
            if 5 in self.taken_blocks_id and 8 in self.taken_blocks_id:
                self.win = True
            if 4 in self.taken_blocks_id and 6 in self.taken_blocks_id:
                self.win = True
        if 3 in self.taken_blocks_id:
            if 4 in self.taken_blocks_id and 5 in self.taken_blocks_id:
                self.win = True
        if 6 in self.taken_blocks_id:
            if 7 in self.taken_blocks_id and 8 in self.taken_blocks_id:
                self.win = True

    # It checks wheter it's X or O and calls the correct method
    def draw(self):
        {'x': self.draw_x, 'o': self.draw_o}.get(self.xo)()
        # It can also be 'x': self.draw_x(),
        # but its better to call the function after the .get() unless arguments needed in them

    def draw_x(self):
        for posx, posy in self.taken_blocks_pos:
            pygame.draw.line(screen, self.color, (posx, posy), (posx+50, posy+60), 9)   # Left up to right down line
            pygame.draw.line(screen, self.color, (posx+50, posy), (posx, posy+60), 9)   # Right up to left down line

    def draw_o(self):
        for posx, posy in self.taken_blocks_pos:
            pygame.draw.circle(screen, self.color, (posx, posy), 43, 7)


def draw_2part_text(text1: str, text2: str, color_a: tuple, color_b: tuple, pos1: tuple, pos2: tuple):
    text_block_a = FONT2.render(text1, True, color_a)
    text_pos_a = text_block_a.get_rect()
    text_pos_a.center = pos1
    text_block_b = FONT2.render(text2, True, color_b)
    text_pos_b = text_block_b.get_rect()
    text_pos_b.center = pos2
    screen.blit(text_block_a, text_pos_a)
    screen.blit(text_block_b, text_pos_b)


def draw_dead_text(text: str, color: tuple, pos):
    text_block = FONT1.render(text, True, color)
    text_pos = text_block.get_rect()
    if type(pos) == str:
        if pos == 'topup':
            text_pos.center = (int(screenWidth / 2), 50)
        elif pos == 'center':
            text_pos.center = (int(screenWidth / 2), int(screenHeight / 2))
    else:
        text_pos.center = pos
    screen.blit(text_block, text_pos)


def reset_game():
    player_x.reset()
    player_o.reset()
    for block in blocks:
        block.reset()
    return True


def dead_scene():
    if player_x.win:
        Score['x'] += 1
    elif player_o.win:
        Score['o'] += 1

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # (R) to restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return reset_game()

        if player_x.win:
            draw_dead_text(f"{player_x} won", Red, 'topup')
        elif player_o.win:
            draw_dead_text(f"{player_o} won", Red, 'topup')
        else:
            draw_dead_text("Draw", Red, 'topup')

        draw_2part_text("Press   to try again", "R", White, Green, (300, 525), (235, 525))
        pygame.display.flip()


def play_scene():
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not player_x.win and not player_o.win:
                    if Turn:
                        player_x.on_click(event, blocks)
                    else:
                        player_o.on_click(event, blocks)

        screen.fill(Gray)
        screen.blit(board, board_pos)
        player_x.draw()
        player_o.draw()
        draw_2part_text("Turn: ", "X" if Turn else "O", White, Green, (300, 95), (345, 95))
        draw_2part_text("X: ", str(Score['x']), White, White, (50, 180), (68, 180))
        draw_2part_text(str(Score['o']), " :O ", White, White, (522, 180), (550, 180))

        player_x.check_win()
        player_o.check_win()

        pygame.display.flip()

        # If they want to restart the game without finishing it, (R) to restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()

        # This has to be after updating the display else it will trigger the dead scene without displaying the last tick
        if player_x.win or player_o.win or (len(player_x.taken_blocks_id) + len(player_o.taken_blocks_id) == 9):
            running = dead_scene()

    return False


White = (255, 255, 255)
Gray = (50, 50, 50)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)

pygame.init()
screenWidth, screenHeight = 600, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
pygame.display.set_caption("TicTacToe")
FONT1 = pygame.font.SysFont('Mono', 50, True)
FONT2 = pygame.font.SysFont('Mono', 30, True)


Turn = True     # If True it's X's turn, if False it's O's turn
Score = {
    'x': 0,
    'o': 0
}

player_x = Player("x", White)
player_o = Player("o", White)

# Creating the clickable blocks
bposx, bposy = 145, 146
blocks = []
for i in range(3):
    for j in range(3):
        blocks.append(Block((bposx, bposy)))
        bposx += 110
    bposy += 112
    bposx = 145

board = pygame.image.load("imgs/board.png")
board_pos = board.get_rect()
board_pos.center = (int(screenWidth / 2), int(screenHeight / 2))

#####################
play_scene()
#####################
pygame.quit()
