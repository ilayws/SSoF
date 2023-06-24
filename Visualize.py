import pygame, os

image_folder = "Data"
screen = pygame.display

i = 0

def start(WIDTH, HEIGHT):
    global screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Spontanous Synchronization of Fireflies')

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
    screen.fill((0,0,0))

def save_image():
    global i
    directory = image_folder + "/frame" + str(i)
    pygame.image.save(screen, directory + '.png')
    i += 1


def draw(f):
    global screen
    color = (61,63,0)
    if f.state:
        l = lambda t: -4/9*t*t + 12/9*t
        r = (246-61)*l(f.t) + 61
        g = (255-63)*l(f.t) + 63
        color = (r,g,0)
    pygame.draw.circle(screen, color, (f.x, f.y), 5)

# Files :
def remove_images():
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    for img in images:
        os.remove(image_folder + "/" + img)

def image_to_vid():
    os.system("ffmpeg -r " +str(120)+ " -i " + image_folder + "/frame%1d.png -vcodec mpeg4 -y -vb " +str(10)+ "M movie.mp4")
