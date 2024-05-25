import pygame
import random
from PIL import Image

# عشان نعمل الابعاد تبعت الصورة صح 
def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        resized_img.save(output_path)

# نعدل الابعاد للابعاد المناسبة
resize_image(r'FlappyBirdGameAssets\Bird.png', 'bird_resized.png', (34, 24))
resize_image(r'FlappyBirdGameAssets\pipe.png', 'pipe_resized.png', (50, 320))
resize_image(r'FlappyBirdGameAssets\Background.png', 'background_resized.png', (600, 600))

# pygameنبلش ال
pygame.init()

# ابعاد الشاشة
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100

# الالوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# ابعاد وخصائص العصفور
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = 50
BIRD_Y = 300
BIRD_GRAVITY = 0.3
BIRD_JUMP_STRENGTH = -7

# ابعاد وخصائص الانابيب
PIPE_WIDTH = 50
PIPE_HEIGHT = 320
PIPE_GAP = 250  # نكبر الفتحة عشان نخلي اللعبة اسهل
PIPE_FREQUENCY = 2000  # الثواني 

# FPSخصائص ال
FPS = 60

# نحمل الصور 
BIRD_IMAGE = pygame.image.load('bird_resized.png')
PIPE_IMAGE = pygame.image.load('pipe_resized.png')
BACKGROUND_IMAGE = pygame.image.load('background_resized.png')

# نحمل الاصوات
FLAP_SOUND = pygame.mixer.Sound(r'FlappyBirdGameAssets\flap.mp3')
HIT_SOUND = pygame.mixer.Sound(r'FlappyBirdGameAssets\hit.mp3')

# نحمل اللعبة ونحطلها عنوان
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# FPSالنبضة او اللحظة عشان ال
clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    while True:
        # متغيرات العصفور
        bird_y = BIRD_Y
        bird_velocity = 0

        # متغيرات الانبوب
        pipe_x = SCREEN_WIDTH
        pipe_height = random.randint(100, 400)
        pipe_passed = False

        # عداد النتيجة
        score = 0

        # وضع الغش
        cheat_mode = False

        # main Loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_velocity = BIRD_JUMP_STRENGTH
                        FLAP_SOUND.play()
                    if event.key == pygame.K_p:
                        cheat_mode = not cheat_mode

            # حركة العصفور
            bird_velocity += BIRD_GRAVITY
            bird_y += bird_velocity

            # عشان نخلي العصفور يضل جوا الاشاشة بوضع الغش
            if cheat_mode:
                if bird_y < 0:
                    bird_y = 0
                if bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:
                    bird_y = SCREEN_HEIGHT - BIRD_HEIGHT

            # حركة الانبوب
            pipe_x -= 5
            if pipe_x < -PIPE_WIDTH:
                pipe_x = SCREEN_WIDTH
                pipe_height = random.randint(100, 400)
                pipe_passed = False

            # نتحقق او نشوف الخبطات بالانبوب (ازا وضع الغش شغال مش هيشتغل)
            if not cheat_mode:
                if (BIRD_X < pipe_x + PIPE_WIDTH and BIRD_X + BIRD_WIDTH > pipe_x and
                        (bird_y < pipe_height or bird_y + BIRD_HEIGHT > pipe_height + PIPE_GAP)):
                    HIT_SOUND.play()
                    running = False

                # تا نشوف ازا العصفور خبط بالارض او طلع جوا الشاشة
                if bird_y > SCREEN_HEIGHT - GROUND_HEIGHT or bird_y < 0:
                    HIT_SOUND.play()
                    running = False

            # تا يعد العداد
            if pipe_x + PIPE_WIDTH < BIRD_X and not pipe_passed:
                pipe_passed = True
                score += 1

            # نرسم كلشي
            screen.blit(BACKGROUND_IMAGE, (0, 0))
            screen.blit(BIRD_IMAGE, (BIRD_X, bird_y))
            screen.blit(PIPE_IMAGE, (pipe_x, pipe_height - PIPE_HEIGHT))
            screen.blit(PIPE_IMAGE, (pipe_x, pipe_height + PIPE_GAP))

            draw_text(f'Score: {score}', pygame.font.Font(None, 36), BLACK, screen, 10, 10)
            if cheat_mode:
                draw_text('Cheat Mode ON', pygame.font.Font(None, 36), RED, screen, 10, 50)

            pygame.display.update()
            clock.tick(FPS)

        # GAMEOVERشاشة ال
        screen.fill(WHITE)
        draw_text('Game Over', pygame.font.Font(None, 72), RED, screen, 100, 250)
        draw_text('Press Space to Restart', pygame.font.Font(None, 36), BLACK, screen, 80, 350)
        pygame.display.update()

        # RESTART نستنى اللاعب تا يعمل 
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        
# MAINعشان ندخل جوا ال
if __name__ == '__main__':
    main()
