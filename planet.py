import pygame, sys, math
from buttonforplanet import ButtonPlanet
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

display_button = ButtonPlanet("C:\\Users\\nomen\\Desktop\\websitenewpython\\Mini Python Projects\\Graphics\\start_button.png", (580, 0), 0.65)

class Planet:
    AU = 149.6e6 * 1000 #distance from earth to sun
    G = 6.67428e-11
    SCALE = 230 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 #1 day


    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    
    def get_position_on_screen(self):
        """Helper function to get the position of the planet in screen coordinates"""
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        return x, y


    def is_hovered(self, mouse_pos):

        x, y = self.get_position_on_screen()
        distance = math.sqrt((mouse_pos[0] - x)**2 + (mouse_pos[1] - y)**2)
        return distance < self.radius



        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))




    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun",0, 0, 30, YELLOW, 1.9891 * 10**30)
    sun.sun = True

    earth = Planet("Earth",-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    
    mars = Planet("Mars",-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury",0.387 * Planet.AU, 0, 8, DARK_GREY, 0.30 * 10**24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus",0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]
    
    paused = False

    while run:

        clock.tick(60)
        WIN.fill((0, 0, 0))
    


        display_button.draw(WIN)

        if display_button.is_pressed():
            paused = not paused
            print("Display button pressed, paused =", paused)

        if not paused:
            for planet in planets:
                planet.update_position(planets)
                planet.draw(WIN)
        else:
            facts = FONT.render("Planet Facts:", True, WHITE)
            WIN.blit(facts, (WIDTH // 2 - facts.get_width() // 2, HEIGHT // 2 - 50))
        
            y_offset = HEIGHT // 2
            spacing = 20
            for i in range (len(planets)):
                planet = planets[i]
                fact = f"{planet.name} planet with mass {planet.mass:.2e} KG"
                fact_surface = FONT.render(fact, True, WHITE)

                WIN.blit(fact_surface, (WIDTH // 2 - fact_surface.get_width() // 2, y_offset + i * spacing))

        mouse_pos = pygame.mouse.get_pos()
        for planet in planets:
            if planet.is_hovered(mouse_pos):
                label = FONT.render(planet.name, True, WHITE)
                label_x, label_y = planet.get_position_on_screen()
                WIN.blit(label, (label_x - label.get_width() / 2, label_y - planet.radius - label.get_height()))



        
        pygame.display.update()
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()

main()