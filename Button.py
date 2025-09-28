import pygame as p

class Button:
    def __init__(self, rect, text, callback, font, color=(200, 200, 200), hover_color=(180, 180, 180), text_color=(0, 0, 0)):
        self.rect = p.Rect(rect)  # (x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = p.mouse.get_pos()
        # Change color if hovering
        if self.rect.collidepoint(mouse_pos):
            p.draw.rect(surface, self.hover_color, self.rect)
        else:
            p.draw.rect(surface, self.color, self.rect)

        # Draw button border
        p.draw.rect(surface, (0, 0, 0), self.rect, 2)

        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()