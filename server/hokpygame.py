import pygame
# import deckcards
# import card
import time

window_width = 1000
window_height = 500
white = (255, 255, 255)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hok")
FONT_size = 32
FONT = pygame.font.Font(None, FONT_size)
max_width = 200
green = (0, 255, 0)
red = (255, 0, 0)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(max_width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def get_name(card):
    if 11 > card.number > 1:
        number = str(card.number)
    else:
        if card.number == 11:
            number = 'J'
        elif card.number == 12:
            number = 'Q'
        elif card.number == 13:
            number = 'K'
        elif card.number == 14:
            number = 'A'

    if card.kind == 'club':
        kind = 'C'
    elif card.kind == 'diamond':
        kind = 'D'
    elif card.kind == 'heart':
        kind = 'H'
    elif card.kind == 'spade':
        kind = 'S'

    return number + kind + '.PNG'


class CardsImg:

    def __init__(self):
        self.imgs = {}
        self.deck = deckcards.DeckCards(create=True)
        for kind in card.Card.cards_kind:
            self.imgs[kind] = {}

        for car in self.deck.deck:
            self.imgs[car.kind][car.number] = pygame.image.load(get_name(car))

    def show_card(self, card, x, y):
        img = self.imgs[card.kind][card.number]
        screen.blit(img, (x, y))

    def show_deck(self, deck, x, y, x_step):
        for card in deck.deck:
            self.show_card(card, x, y)
            x += x_step


def text_objects(text, font):
    text_surf = font.render(text, True, white)
    return text_surf, text_surf.get_rect()


def print_pygame(text, x, y):
    text_surf, text_rect = text_objects(text, FONT)
    text_rect.topleft = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()
    return text_surf, text_rect


def button(x, y, w, h, msg=None, ic=None, ac=None, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if ac is not None:
            pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1:
            if action is not None:
                action()
                return False
            else:
                return True

    else:
        if ic is not None:
            pygame.draw.rect(screen, ic, (x, y, w, h))

    if msg is not None:
        smallText = FONT
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = (x + (w / 2), (y + (h / 2)))
        screen.blit(textSurf, textRect)

    return False


def main():
    pass


if __name__ == '__main__':
    main()
    pygame.quit()
