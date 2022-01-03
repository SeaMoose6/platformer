from settings import *

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False
    pygame.Surface.blit("assets/sci_fi_bg1.jpg")




    screen.fill(BLACK)
    pygame.display.flip()

    clock.tick(FPS)