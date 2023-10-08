import pygame
from pygame import Vector2, Surface


class BitmapMaker:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # bitmaps found at https://www.computerarcheology.com/Arcade/SpaceInvaders/Code.html
        # These are bitmaps, rotated 90 degrees. Each byte is 8 pixels for a single column
        # of the bitmap. All of them are only 8 bits high, except for shield, which is 16.
        # They are bottom up left to right. The low order bit is low in the image.
        # If the code contradicts these commands, the code is correct.
        invader10 = (0x00, 0x00, 0x39, 0x79, 0x7A, 0x6E, 0xEC, 0xFA, 0xFA, 0xEC, 0x6E, 0x7A, 0x79, 0x39, 0x00, 0x00)
        invader11 = (0x00, 0x00, 0x38, 0x7A, 0x7F, 0x6D, 0xEC, 0xFA, 0xFA, 0xEC, 0x6D, 0x7F, 0x7A, 0x38, 0x00, 0x00)
        invader20 = (0x00, 0x00, 0x00, 0x78, 0x1D, 0xBE, 0x6C, 0x3C, 0x3C, 0x3C, 0x6C, 0xBE, 0x1D, 0x78, 0x00, 0x00)
        invader21 = (0x00, 0x00, 0x00, 0x0E, 0x18, 0xBE, 0x6D, 0x3D, 0x3C, 0x3D, 0x6D, 0xBE, 0x18, 0x0E, 0x00, 0x00)
        invader30 = (0x00, 0x00, 0x00, 0x00, 0x19, 0x3A, 0x6D, 0xFA, 0xFA, 0x6D, 0x3A, 0x19, 0x00, 0x00, 0x00, 0x00)
        invader31 = (0x00, 0x00, 0x00, 0x00, 0x1A, 0x3D, 0x68, 0xFC, 0xFC, 0x68, 0x3D, 0x1A, 0x00, 0x00, 0x00, 0x00)
        invaders = (invader10, invader11, invader20, invader21, invader30, invader31)
        invader_exploding = (0x00, 0x08, 0x49, 0x22, 0x14, 0x81, 0x42, 0x00,
                             0x42, 0x81, 0x14, 0x22, 0x49, 0x08, 0x00, 0x00)
        player = (0x00, 0x00, 0x0F, 0x1F, 0x1F, 0x1F, 0x1F, 0x7F, 0xFF, 0x7F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0F, 0x00)
        player_explosion0 = (0x00, 0x04, 0x01, 0x13, 0x03, 0x07, 0xB3, 0x0F, 0x2F, 0x03, 0x2F, 0x49, 0x04, 0x03, 0x00,
                             0x01)
        player_explosion1 = (0x40, 0x08, 0x05, 0xA3, 0x0A, 0x03, 0x5B, 0x0F, 0x27, 0x27, 0x0B, 0x4B, 0x40, 0x84, 0x11,
                             0x48)
        players = (player, player_explosion0, player_explosion1)
        player_shot = (0x0F, )
        player_shot_explosion = (0x99, 0x3C, 0x7E, 0x3D, 0xBC, 0x3E, 0x7C, 0x99)
        saucer = (0x00, 0x00, 0x00, 0x00, 0x04, 0x0C, 0x1E, 0x37,
                  0x3E, 0x7C, 0x74, 0x7E, 0x7E, 0x74, 0x7C, 0x3E,
                  0x37, 0x1E, 0x0C, 0x04, 0x00, 0x00, 0x00, 0x00)
        saucer_explosion = (0x00, 0x22, 0x00, 0xA5, 0x40, 0x08, 0x98, 0x3D, 0xB6, 0x3C, 0x36, 0x1D, 0x10, 0x48, 0x62,
                            0xB6, 0x1D, 0x98, 0x08, 0x42, 0x90, 0x08, 0x00, 0x00)
        saucers = (saucer, saucer_explosion)
        squiggles = ((0x44, 0xAA, 0x10), (0x88, 0x54, 0x22), (0x10, 0xAA, 0x44), (0x22, 0x54, 0x88))
        plungers = ((0x04, 0xFC, 0x04), (0x10, 0xFC, 0x10), (0x20, 0xFC, 0x20), (0x80, 0xFC, 0x80))
        rollers = ((0x00, 0xFE, 0x00), (0x24, 0xFE, 0x12), (0x00, 0xFE, 0x00), (0x48, 0xFE, 0x90))
        invader_shot_explosion = (0x4A, 0x15, 0xBE, 0x3F, 0x5E, 0x25)
        # shield is 22 pixels by 16 pixels, 44 bytes
        shield = (
            0xFF, 0x0F, 0xFF, 0x1F, 0xFF, 0x3F, 0xFF, 0x7F, 0xFF, 0xFF, 0xFC,
            0xFF, 0xF8, 0xFF, 0xF0, 0xFF, 0xF0, 0xFF, 0xF0, 0xFF, 0xF0, 0xFF,
            0xF0, 0xFF, 0xF0, 0xFF, 0xF0, 0xFF, 0xF8, 0xFF, 0xFC, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0xFF, 0x3F, 0xFF, 0x1F, 0xFF, 0x0F)
        scale = 4
        self.invader_explosion = self.make_and_scale_surface(invader_exploding, scale, (16, 8))
        self.invader_shot_explosion = self.make_and_scale_surface(invader_shot_explosion, scale, (6, 8))
        self.invaders = [self.make_and_scale_surface(invader, scale) for invader in invaders]
        self.player_shot = self.make_and_scale_surface(player_shot, scale, (1, 8))
        self.player_shot_explosion = self.make_and_scale_surface(player_shot_explosion, scale, (8, 8), "red")
        self.players = [self.make_and_scale_surface(player, scale, (16, 8),"green") for player in players]
        self.plungers = [self.make_and_scale_surface(plunger, scale, (3, 8)) for plunger in plungers]
        self.rollers = [self.make_and_scale_surface(plunger, scale, (3, 8)) for plunger in rollers]
        self.saucer = self.make_and_scale_surface(saucer, scale, (24, 8), "red")
        self.saucer_explosion = self.make_and_scale_surface(saucer_explosion, scale, (24, 8), "red")
        self.saucers = [self.make_and_scale_surface(saucer, scale, (24, 8), "red") for saucer in saucers]
        self.shield = self.make_and_scale_surface(shield, scale, (22, 16), "green")
        self.squiggles = [self.make_and_scale_surface(squig, scale, (3, 8)) for squig in squiggles]

    def make_and_scale_surface(self, pixel_bytes, scale, size=(16, 8), color="white"):
        return pygame.transform.scale_by(self.make_surface(pixel_bytes, size, color), scale)

    def make_surface(self, pixel_bytes, size, color):
        s = Surface(size)
        s.set_colorkey((0, 0, 0))
        width = size[0]
        layers = len(pixel_bytes) // width
        for x, byte in enumerate(pixel_bytes):
            x_in = x // layers
            y_offset = 0 if layers == 1 else 8 - (x % layers)*8
            self.store_byte(byte, x_in, y_offset, s, color)
        return s

    @staticmethod
    def store_byte(pixel_byte, x, y_offset, surface, color):
        for z in range(8):
            bit = pixel_byte & 1
            y = y_offset + 7 - z
            if bit:
                surface.set_at((x, y), color)
            pixel_byte = pixel_byte >> 1