
from lever import Lever
import random
from typing import Final
from monster import Monster
 
from helper import Disk
import arcade
import math
from enum import IntEnum
import constants


class Attack(IntEnum) : 
        PAUSE = 0
        RUSH = 1
        WALK = 2
        DASH = 3


class Boss(Monster, Lever):
    """Represents a Boss, defines how it moves"""

    __slots__ = ('__initial_x', '__initial_y', 'choice', 'hit_points', 
                 'angle_deplacement', 'action_area', 'frame_until_action', )
    
    __initial_x : Final[float]
    __initial_y : Final[float]

    def __init__(self, x: float, y: float) -> None :
        
        super().__init__("assets/kenney-extended-enemies-png/bat.png")

        self.center_x = x
        self.center_y = y

        self.change_x = 0
        self.change_y = 0
        self.speed = constants.BOSS_SPEED

        self.__initial_x = x
        self.__initial_y = y

        self.__choice : Attack = Attack.WALK

        self.hit_points = 3
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/spinner.png")
        self.sync_hit_box_to_texture()
        self.scale = (1,1)

        self.angle_deplacement = 0.0

        self.frame_until_action = constants.BOSS_FRAMES

        self.action_area = Disk(self.__initial_x, self.__initial_y, constants.BOSS_ACTION_RADIUS)

    def move(self, wall : arcade.SpriteList[arcade.Sprite], player_position : arcade.Vec2) -> None:
        """Execute the boss's AI decision and update its position accordingly."""
        self.__ia(player_position)
        self.__update_position()

    def __ia(self, player_position : arcade.Vec2) -> None:
        """
        Choose the boss's next movement and speed randomly at the end of the current action.
        Change the boss's color to indicate the upcoming move.
        Choose the boss's next move randomly at the end of the current action, among possible moves.
        """
        self.frame_until_action -= 1
        if self.frame_until_action == 15:             # indicate the next move, with colors because cool
                match self.__choice:
                    case Attack.PAUSE:  #bleu
                        self.rgb = 0, 0, 255

                    case Attack.RUSH:   #rouge
                        self.rgb = 255, 0, 0
                        
                    case Attack.WALK:   #cyan   
                        self.rgb = 0, 255, 255   
                       
                    case Attack.DASH:   #magenta
                        self.rgb = 255, 0, 255

        if self.frame_until_action == 0:
            self.rgb = 255, 255, 255
            if not self.action_area.contains_point((self.center_x, self.center_y)):
                self.angle_deplacement = math.pi + math.atan2(self.center_y - self.__initial_y ,self.center_x - self.__initial_x)
                self.frame_until_action = constants.BOSS_FRAMES
                self.speed = 2*constants.BOSS_SPEED
            elif self.action_area.contains_point(player_position):
                match self.__choice:          #chooses a random move to do 
                    case Attack.PAUSE:  #the boss stop moving
                        self.speed = 0
                        self.frame_until_action = random.randint(40,80)
                        can_do = [Attack.WALK, Attack.RUSH, Attack.DASH]
                        self.__choice = random.choice(can_do)

                    case Attack.RUSH:   #the boss move fast toward the player
                        self.angle_deplacement = math.pi + math.atan2(self.center_y - player_position.y, self.center_x - player_position.x)
                        self.speed = constants.BOSS_SPEED_RUSH*constants.BOSS_SPEED
                        self.frame_until_action = random.randint(20,60)
                        can_do = [Attack.PAUSE, Attack.RUSH, Attack.DASH]
                        self.__choice = random.choice(can_do)

                    case Attack.WALK:   #the boss choose a random dirction and move
                        self.frame_until_action = random.randint(60,100)
                        self.angle_deplacement = 45*random.randint(0,7)       #pour obtenire une mouvement mecanique de scie
                        self.speed = constants.BOSS_SPEED
                        can_do = [Attack.WALK, Attack.RUSH, Attack.DASH]
                        self.__choice = random.choice(can_do)
                        

                    case Attack.DASH:   # the boss move very fast around the player 
                        self.frame_until_action = random.randint(20,40)
                        if random.getrandbits(1):
                            left_or_right = 2*math.pi/3
                        else:
                            left_or_right = -2*math.pi/3
                        self.angle_deplacement =left_or_right + math.atan2(self.center_y - player_position.y, self.center_x - player_position.x)
                        self.speed =constants.BOSS_SPEED_DASH*constants.BOSS_SPEED
                        can_do =[Attack.RUSH, Attack.DASH]
                        self.__choice = random.choice(can_do)                 
            else :
                self.speed=0
                self.frame_until_action = constants.BOSS_FRAMES
                    
            self.__new_speed()
        
        

    
    def __update_position(self) -> None:
        """Update the boss's position by adding the current speed components."""
        self.center_x += self.change_x
        self.center_y += self.change_y

    def __new_speed(self) -> None:
        """Calculate the x and y speed components based on the current angle (in radians)
        to maintain the set total speed."""
        self.change_x = math.cos(self.angle_deplacement) * self.speed
        self.change_y = math.sin(self.angle_deplacement) * self.speed

    def die(self) -> None:
        """Reduce boss hit points. If zero, trigger death effects and remove the boss."""
        self.hit_points -=1

        self.__choice = Attack.WALK       #Make the boss back off 
        self.speed = -2*constants.BOSS_SPEED
        self.frame_until_action = 30

        self.__new_speed()
        if self.hit_points == 0 :
            self.on_action()
            self.remove_from_sprite_lists() 

    
    
            




        

