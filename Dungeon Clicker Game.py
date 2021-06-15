import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect

BLUE = (000, 000, 255)
WHITE = (255, 255, 255)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
     font = pygame.freetype.SysFont("Courier", font_size, bold = True)
     surface, _ = font.render(text= text, fgcolor= text_rgb, bgcolor= bg_rgb)
     return surface.convert_alpha()

class UIElement(Sprite):
     
     def __init__(self, center_position, text, font_size, text_rgb, bg_rgb):
          
          
          super().__init__()
          self.mouse_over = False
          

          default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
          
          highlighted_image = create_surface_with_text(text, font_size* 1.2, text_rgb, bg_rgb)
          
          self.images = [default_image, highlighted_image]
          self.rects = [
               default_image.get_rect(center = center_position), 
               highlighted_image.get_rect(center = center_position)]
     @property
     def image(self):
          return self.images[1] if self.mouse_over else self.image[0]
     
     @property
     def rect(self):
          return self.rects[1] if self.mouse_over else self.rects[0]
     
     
     def update(self, mouse_pos):
          if self.rect.collidepoint(mouse_pos):
               self.mouse_over = True
          else:
               self.mouse_over = False
     def draw(self, surface):
          surface.blit(self.image, self.rect)
          
def main():
     pygame.init()
     screen = pygame.display.set_mode((800, 600))
     uielement = UIElement(
          center_position=(400, 400),
          font_size=30,
          bg_rgb = BLUE,
          text_rgb = WHITE,
          text="Hello"
     )
     
     while True:
          for event in pygame.event.get():
               pass
          screen.fill(BLUE)
          uielement.update(pygame.mouse.get_pos())
          uielement.draw(screen)
          pygame.display.flip()
main()
                           
     
          
          
     