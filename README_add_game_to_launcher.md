
Uitleg voor het toevoegen van games aan de launcher
___________________________________________________

Waarschijnlijk heeft jullie game een soort main bestand met logica die er ongeveer zo uit ziet:

```python
pygame.init()
FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DISPLAY_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    # game logic (handle events, update en draw)
```

deze loop wordt al afgehandeld in de main van het gehele programma (zie main.py)

Het is de bedoeling om jullie main file om te zetten in een class die erft van de class Game(State). Vernoem deze class naar jullie game

```python voorbeeld4
from game import Game

def SpaceInvaders(Game):
    def __init__(self, screen):
        super().__init__(screen)
        # voeg hier alle opzet logica van de game toe. Het aanmaken van game-objecten, variabelen waar de logica van gebruik maakt,
        # opzet van het eerste level, etc.
        # bijvoorbeeld:
        self.player = ...
        self.enemies = []
        self.score = 0        
        etc.

        # voor het importeren van sprites, sounds en andere resources kun je dit gebruiken voor de relative path naar deze class
        # als het goed is werkt dit voor Windows, Linux en MacOS
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # gebruik dan 
        os.path.join(current_dir, ...)
        # om naar specifieke files te navigeren

    # zet hier je game logic in (wat in jullie while True loop staat)
    def update(self, dt):
        # waarschijnlijk staat hier ook een handle_events blok in
        # dit blok bestaat al in de main loop waar alle states(games en menu) op draaien
        # de state class gebruikt deze loop voor het bijhouden van de dictionary self.pressed
        # vervang het handle_events blok en al jullie key press checks met self.pressed[""] of self.just_pressed[""] voor een True/False of deze key is ingedrukt
        # bekijk state.py voor meer uitleg over hoe dit werkt. Het is heel eenvoudig om dit te gebruiken

        # gebruik dt voor het tracken van tijd (zie state.py)
    
    def draw():
        # zet hier alle draw logic in 
        (self.screen.blit(...))

        # als jullie update en draw logic heel erg met elkaar verweven zit in dezelfde loop kun je def draw() achterwege laten en gewoon alles in update doen
        # dat werkt ook gewoon, het is gewoon iets minder netjes
     ```

     extra tip: zorg ervoor dat alle imports werken, mogelijk moeten deze worden aangepast wanneer je de game folder naar dit project verplaatst
    





    