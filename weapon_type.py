from __future__ import annotations
from enum import IntEnum
import arcade

from typing import TYPE_CHECKING

if TYPE_CHECKING : # Need this to break circular import
    from weapon import Weapon

class WeaponType(IntEnum) : 

    """ Enum representing the different types of weapons available to the player.

    Each weapon type can:
        - Generate its own weapon instance via `create_weapon`
        - Provide an icon path for UI display
    """
     
    BOW = 0
    SWORD = 1

    def create_weapon(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> Weapon :
        """Creates and returns an instance of the selected weapon type."""
        match self :
            case WeaponType.BOW : 
                from bow import Bow # Need local import to break circular imports 
                return Bow(mouse_position, player_position, camera_bottom_left)
            case WeaponType.SWORD :
                from sword import Sword
                return Sword(mouse_position, player_position, camera_bottom_left)
            
    def weapon_icon(self) -> str :
        """Returns the file path to the icon representing this weapon type."""
        match self :
            case WeaponType.BOW : 
                return "assets/kenney-voxel-items-png/bow.png"
            case WeaponType.SWORD :
                return "assets/kenney-voxel-items-png/sword_silver.png" 