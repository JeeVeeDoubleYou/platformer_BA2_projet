le mecanisme qui gere l'arret avec les fleches depend de la vitesse de la joueuse

Gaëlle : Dans GameView, n'initialise pas player dans __init__ mais dans create_map(). C'est ok?
            
Assert height is correct ie next line is ---
Create list of all lists (gameview) to loop through for draw, for example
Die is falls for too long

Run sur maps du prof?

QUESTION : def move(self, wall_list: arcade.SpriteList[arcade.Sprite] = None) -> None: 
ou def move(self, *args) -> None: + def move(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None: ?
IF réponse 1, assert dans bat que wall list = None ou juste ignorer?