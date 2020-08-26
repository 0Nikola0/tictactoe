import pygame


class Block:
    def __init__(self, pos: tuple):
        self.posx, self.posy = pos[0], pos[1]
        self.rect = pygame.Rect(self.posx, self.posy, 90, 90)
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


def draw_text(text: str, color: tuple):
    text_block = FONT1.render(text, True, color)
    text_pos = text_block.get_rect()
    text_pos.center = (int(screenWidth / 2), int(screenHeight / 2))
    screen.blit(text_block, text_pos)


White = (255, 255, 255)
Gray = (50, 50, 50)
Black = (0, 0, 0)

pygame.init()
screenWidth, screenHeight = 600, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("TicTacToe")
FONT1 = pygame.font.SysFont('Mono', 50, True)

Turn = True     # If True it's X's turn, if False it's O's turn


player_x = Player("x", Black)
player_o = Player("o", Black)

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


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if Turn:
                player_x.on_click(event, blocks)
            else:
                player_o.on_click(event, blocks)

    screen.fill(Gray)
    screen.blit(board, board_pos)
    player_x.draw()
    player_o.draw()

    if player_x.win:
        draw_text(f"{player_x} won", White)
    elif player_o.win:
        draw_text(f"{player_o} won", White)
    else:
        player_x.check_win()
        player_o.check_win()

    pygame.display.flip()

pygame.quit()
