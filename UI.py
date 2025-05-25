from boss import Boss
import constants
import arcade

from monster import Monster
from weapon_type import WeaponType

class UI : 
    """Creates and draws all UI elements, like the score or the boss life bar"""

    def __init__(self, fixed_camera : arcade.camera.Camera2D, monster_list : arcade.SpriteList[Monster], coin_score : int) -> None :
        self.__fixed_camera = fixed_camera
        self.__monster_list = monster_list
        self.__create_ui(coin_score)

    def __create_ui(self, coin_score : int) -> None :
        # Icône montrant l'arme active 
        weapon_rect = arcade.Rect(0, 0, 0, 0, 50, 50, 
                            self.__fixed_camera.top_left.x+30,
                            self.__fixed_camera.top_left.y-30,)
        self.__weapon_icon : dict[str, arcade.Rect | str] = {'rect' : weapon_rect, 
                                                'texture' : 'assets/kenney-voxel-items-png/sword_silver.png' }
        
        # Compteur de pièces 
        coin_rect = arcade.Rect(0, 0, 0, 0, 50, 50,
                        self.__fixed_camera.bottom_left.x+35,
                        self.__fixed_camera.bottom_left.y+20)
        self.__coin_icon : dict[str, arcade.Rect | str] = {'rect' : coin_rect, 
                                                'texture' : ":resources:images/items/coinGold.png" }
        self.__coin_score = arcade.Text("", self.__fixed_camera.bottom_left.x+50, self.__fixed_camera.bottom_left.y+12, arcade.color.BLACK, 16)
        
        self.__textured_ui_list = (self.__weapon_icon, self.__coin_icon)
        
        # Montre la vie du boss, s'il y en a un
        self.__text_boss_life = arcade.Text("", self.__fixed_camera.bottom_left.x+125, self.__fixed_camera.bottom_left.y+10, arcade.color.RED, 12)

        for monster in self.__monster_list:
            self.update_boss_life(monster)

        # Ici est crée le texte de victoire
        self.__win_text = arcade.Text(
                        "Congratulations, you've won !",
                        color = arcade.color.BLACK,
                        font_size= 54,
                        font_name="Impact",
                        x = constants.WINDOW_WIDTH/2,
                        y = constants.WINDOW_HEIGHT/2,
                        anchor_x="center",
                        anchor_y="center"
                        )
        
        # Set initial scores
        self.update_coin_score(coin_score)
        for monster in self.__monster_list :
             self.update_boss_life(monster)


    def update_boss_life(self, monster : Monster) -> None :
        """Takes in argument a monster, and if it is a boss, updates its life bar"""
        if isinstance(monster, Boss):
                    string_score : str
                    if monster.hit_points == 0:
                        string_score = "The boss has been defeated"
                    else : 
                        string_score ="Malenia, Blade of Miquella: "
                        for i in range (monster.hit_points):
                            string_score += " ♥ "
                    self.__text_boss_life.text = string_score

    def update_coin_score(self, coin_score : int) -> None :
        """"Updates the on screen coin counter"""
        self.__coin_score.text = " " + str(coin_score)

    def draw_winning_text(self) -> None :
        """Draws winning text"""
        self.__win_text.draw()

    def draw_in_game(self) -> None :
        """Draws everything needed while in the normal gameplay ie no winning or error text."""
        with self.__fixed_camera.activate(): 
            self.__draw_icons()
            self.__coin_score.draw()
            self.__text_boss_life.draw()

    def update_weapon_icon(self, weapon : WeaponType) -> None :
        """Updates the active weapon icon on screen"""
        self.__weapon_icon['texture'] = weapon.weapon_icon()
    
    def __draw_icons(self) -> None :
        """Draws UI elements that have icons"""
        for texture_rect in self.__textured_ui_list:
            if 'rect' in texture_rect and 'texture' in texture_rect:           
                rect = texture_rect['rect']
                texture = texture_rect['texture']
                assert(isinstance(rect, arcade.Rect) and isinstance(texture, str))
                arcade.draw_texture_rect(arcade.load_texture(texture), rect)
