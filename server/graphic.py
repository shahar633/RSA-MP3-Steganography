import pygame
import hokpygame

window_width = 900
window_height = 700
white = (255, 255, 255)
background_color = (110, 150, 75)
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("mp3")
FONT = hokpygame.FONT
FONT_size = hokpygame.FONT_size


def reset_screen(color=background_color):
    screen.fill(color)


def text_objects(text, font):
    text_surf = font.render(text, True, white)
    return text_surf, text_surf.get_rect()


def print_pygame(text, x, y):
    text_surf, text_rect = text_objects(text, FONT)
    text_rect.topleft = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()
    return text_surf, text_rect


def input_pygame(x, y, text=''):
    text_surf, text_rect = print_pygame(text, x, y - FONT_size)
    text_box = hokpygame.InputBox(x, y, hokpygame.max_width, FONT_size)
    done = False
    text = ''

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            text = text_box.handle_event(event)

        if text is not None and text != '':
            return True, text

        reset_screen()
        screen.blit(text_surf, text_rect)
        text_box.update()
        text_box.draw(screen)

        pygame.display.update()

    return False, ''


def main():
    x, txt = input_pygame(41,32,"beni")
    print txt
    print_pygame(txt, 100,300)


if __name__ == '__main__':
    main()
