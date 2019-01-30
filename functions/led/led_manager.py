#!/usr/bin/python
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import paho.mqtt.client as paho
import math
from rpi_ws281x import *
from collections import Iterable
import signal
import sys
from core.tools.config import getConfig

# Color Constants from https://www.webucator.com/blog/2015/03/python-color-constants-module/
ALICEBLUE = Color(240, 248, 255)
ANTIQUEWHITE = Color(250, 235, 215)
ANTIQUEWHITE1 = Color(255, 239, 219)
ANTIQUEWHITE2 = Color(238, 223, 204)
ANTIQUEWHITE3 = Color(205, 192, 176)
ANTIQUEWHITE4 = Color(139, 131, 120)
AQUA = Color(0, 255, 255)
AQUAMARINE1 = Color(127, 255, 212)
AQUAMARINE2 = Color(118, 238, 198)
AQUAMARINE3 = Color(102, 205, 170)
AQUAMARINE4 = Color(69, 139, 116)
AZURE1 = Color(240, 255, 255)
AZURE2 = Color(224, 238, 238)
AZURE3 = Color(193, 205, 205)
AZURE4 = Color(131, 139, 139)
BANANA = Color(227, 207, 87)
BEIGE = Color(245, 245, 220)
BISQUE1 = Color(255, 228, 196)
BISQUE2 = Color(238, 213, 183)
BISQUE3 = Color(205, 183, 158)
BISQUE4 = Color(139, 125, 107)
BLACK = Color(0, 0, 0)
BLANCHEDALMOND = Color(255, 235, 205)
BLUE = Color(0, 0, 255)
BLUE2 = Color(0, 0, 238)
BLUE3 = Color(0, 0, 205)
BLUE4 = Color(0, 0, 139)
BLUEVIOLET = Color(138, 43, 226)
BRICK = Color(156, 102, 31)
BROWN = Color(165, 42, 42)
BROWN1 = Color(255, 64, 64)
BROWN2 = Color(238, 59, 59)
BROWN3 = Color(205, 51, 51)
BROWN4 = Color(139, 35, 35)
BURLYWOOD = Color(222, 184, 135)
BURLYWOOD1 = Color(255, 211, 155)
BURLYWOOD2 = Color(238, 197, 145)
BURLYWOOD3 = Color(205, 170, 125)
BURLYWOOD4 = Color(139, 115, 85)
BURNTSIENNA = Color(138, 54, 15)
BURNTUMBER = Color(138, 51, 36)
CADETBLUE = Color(95, 158, 160)
CADETBLUE1 = Color(152, 245, 255)
CADETBLUE2 = Color(142, 229, 238)
CADETBLUE3 = Color(122, 197, 205)
CADETBLUE4 = Color(83, 134, 139)
CADMIUMORANGE = Color(255, 97, 3)
CADMIUMYELLOW = Color(255, 153, 18)
CARROT = Color(237, 145, 33)
CHARTREUSE1 = Color(127, 255, 0)
CHARTREUSE2 = Color(118, 238, 0)
CHARTREUSE3 = Color(102, 205, 0)
CHARTREUSE4 = Color(69, 139, 0)
CHOCOLATE = Color(210, 105, 30)
CHOCOLATE1 = Color(255, 127, 36)
CHOCOLATE2 = Color(238, 118, 33)
CHOCOLATE3 = Color(205, 102, 29)
CHOCOLATE4 = Color(139, 69, 19)
COBALT = Color(61, 89, 171)
COBALTGREEN = Color(61, 145, 64)
COLDGREY = Color(128, 138, 135)
CORAL = Color(255, 127, 80)
CORAL1 = Color(255, 114, 86)
CORAL2 = Color(238, 106, 80)
CORAL3 = Color(205, 91, 69)
CORAL4 = Color(139, 62, 47)
CORNFLOWERBLUE = Color(100, 149, 237)
CORNSILK1 = Color(255, 248, 220)
CORNSILK2 = Color(238, 232, 205)
CORNSILK3 = Color(205, 200, 177)
CORNSILK4 = Color(139, 136, 120)
CRIMSON = Color(220, 20, 60)
CYAN2 = Color(0, 238, 238)
CYAN3 = Color(0, 205, 205)
CYAN4 = Color(0, 139, 139)
DARKGOLDENROD = Color(184, 134, 11)
DARKGOLDENROD1 = Color(255, 185, 15)
DARKGOLDENROD2 = Color(238, 173, 14)
DARKGOLDENROD3 = Color(205, 149, 12)
DARKGOLDENROD4 = Color(139, 101, 8)
DARKGRAY = Color(169, 169, 169)
DARKGREEN = Color(0, 100, 0)
DARKKHAKI = Color(189, 183, 107)
DARKOLIVEGREEN = Color(85, 107, 47)
DARKOLIVEGREEN1 = Color(202, 255, 112)
DARKOLIVEGREEN2 = Color(188, 238, 104)
DARKOLIVEGREEN3 = Color(162, 205, 90)
DARKOLIVEGREEN4 = Color(110, 139, 61)
DARKORANGE = Color(255, 140, 0)
DARKORANGE1 = Color(255, 127, 0)
DARKORANGE2 = Color(238, 118, 0)
DARKORANGE3 = Color(205, 102, 0)
DARKORANGE4 = Color(139, 69, 0)
DARKORCHID = Color(153, 50, 204)
DARKORCHID1 = Color(191, 62, 255)
DARKORCHID2 = Color(178, 58, 238)
DARKORCHID3 = Color(154, 50, 205)
DARKORCHID4 = Color(104, 34, 139)
DARKSALMON = Color(233, 150, 122)
DARKSEAGREEN = Color(143, 188, 143)
DARKSEAGREEN1 = Color(193, 255, 193)
DARKSEAGREEN2 = Color(180, 238, 180)
DARKSEAGREEN3 = Color(155, 205, 155)
DARKSEAGREEN4 = Color(105, 139, 105)
DARKSLATEBLUE = Color(72, 61, 139)
DARKSLATEGRAY = Color(47, 79, 79)
DARKSLATEGRAY1 = Color(151, 255, 255)
DARKSLATEGRAY2 = Color(141, 238, 238)
DARKSLATEGRAY3 = Color(121, 205, 205)
DARKSLATEGRAY4 = Color(82, 139, 139)
DARKTURQUOISE = Color(0, 206, 209)
DARKVIOLET = Color(148, 0, 211)
DEEPPINK1 = Color(255, 20, 147)
DEEPPINK2 = Color(238, 18, 137)
DEEPPINK3 = Color(205, 16, 118)
DEEPPINK4 = Color(139, 10, 80)
DEEPSKYBLUE1 = Color(0, 191, 255)
DEEPSKYBLUE2 = Color(0, 178, 238)
DEEPSKYBLUE3 = Color(0, 154, 205)
DEEPSKYBLUE4 = Color(0, 104, 139)
DIMGRAY = Color(105, 105, 105)
DIMGRAY = Color(105, 105, 105)
DODGERBLUE1 = Color(30, 144, 255)
DODGERBLUE2 = Color(28, 134, 238)
DODGERBLUE3 = Color(24, 116, 205)
DODGERBLUE4 = Color(16, 78, 139)
EGGSHELL = Color(252, 230, 201)
EMERALDGREEN = Color(0, 201, 87)
FIREBRICK = Color(178, 34, 34)
FIREBRICK1 = Color(255, 48, 48)
FIREBRICK2 = Color(238, 44, 44)
FIREBRICK3 = Color(205, 38, 38)
FIREBRICK4 = Color(139, 26, 26)
FLESH = Color(255, 125, 64)
FLORALWHITE = Color(255, 250, 240)
FORESTGREEN = Color(34, 139, 34)
GAINSBORO = Color(220, 220, 220)
GHOSTWHITE = Color(248, 248, 255)
GOLD1 = Color(255, 215, 0)
GOLD2 = Color(238, 201, 0)
GOLD3 = Color(205, 173, 0)
GOLD4 = Color(139, 117, 0)
GOLDENROD = Color(218, 165, 32)
GOLDENROD1 = Color(255, 193, 37)
GOLDENROD2 = Color(238, 180, 34)
GOLDENROD3 = Color(205, 155, 29)
GOLDENROD4 = Color(139, 105, 20)
GRAY = Color(128, 128, 128)
GRAY1 = Color(3, 3, 3)
GRAY10 = Color(26, 26, 26)
GRAY11 = Color(28, 28, 28)
GRAY12 = Color(31, 31, 31)
GRAY13 = Color(33, 33, 33)
GRAY14 = Color(36, 36, 36)
GRAY15 = Color(38, 38, 38)
GRAY16 = Color(41, 41, 41)
GRAY17 = Color(43, 43, 43)
GRAY18 = Color(46, 46, 46)
GRAY19 = Color(48, 48, 48)
GRAY2 = Color(5, 5, 5)
GRAY20 = Color(51, 51, 51)
GRAY21 = Color(54, 54, 54)
GRAY22 = Color(56, 56, 56)
GRAY23 = Color(59, 59, 59)
GRAY24 = Color(61, 61, 61)
GRAY25 = Color(64, 64, 64)
GRAY26 = Color(66, 66, 66)
GRAY27 = Color(69, 69, 69)
GRAY28 = Color(71, 71, 71)
GRAY29 = Color(74, 74, 74)
GRAY3 = Color(8, 8, 8)
GRAY30 = Color(77, 77, 77)
GRAY31 = Color(79, 79, 79)
GRAY32 = Color(82, 82, 82)
GRAY33 = Color(84, 84, 84)
GRAY34 = Color(87, 87, 87)
GRAY35 = Color(89, 89, 89)
GRAY36 = Color(92, 92, 92)
GRAY37 = Color(94, 94, 94)
GRAY38 = Color(97, 97, 97)
GRAY39 = Color(99, 99, 99)
GRAY4 = Color(10, 10, 10)
GRAY40 = Color(102, 102, 102)
GRAY42 = Color(107, 107, 107)
GRAY43 = Color(110, 110, 110)
GRAY44 = Color(112, 112, 112)
GRAY45 = Color(115, 115, 115)
GRAY46 = Color(117, 117, 117)
GRAY47 = Color(120, 120, 120)
GRAY48 = Color(122, 122, 122)
GRAY49 = Color(125, 125, 125)
GRAY5 = Color(13, 13, 13)
GRAY50 = Color(127, 127, 127)
GRAY51 = Color(130, 130, 130)
GRAY52 = Color(133, 133, 133)
GRAY53 = Color(135, 135, 135)
GRAY54 = Color(138, 138, 138)
GRAY55 = Color(140, 140, 140)
GRAY56 = Color(143, 143, 143)
GRAY57 = Color(145, 145, 145)
GRAY58 = Color(148, 148, 148)
GRAY59 = Color(150, 150, 150)
GRAY6 = Color(15, 15, 15)
GRAY60 = Color(153, 153, 153)
GRAY61 = Color(156, 156, 156)
GRAY62 = Color(158, 158, 158)
GRAY63 = Color(161, 161, 161)
GRAY64 = Color(163, 163, 163)
GRAY65 = Color(166, 166, 166)
GRAY66 = Color(168, 168, 168)
GRAY67 = Color(171, 171, 171)
GRAY68 = Color(173, 173, 173)
GRAY69 = Color(176, 176, 176)
GRAY7 = Color(18, 18, 18)
GRAY70 = Color(179, 179, 179)
GRAY71 = Color(181, 181, 181)
GRAY72 = Color(184, 184, 184)
GRAY73 = Color(186, 186, 186)
GRAY74 = Color(189, 189, 189)
GRAY75 = Color(191, 191, 191)
GRAY76 = Color(194, 194, 194)
GRAY77 = Color(196, 196, 196)
GRAY78 = Color(199, 199, 199)
GRAY79 = Color(201, 201, 201)
GRAY8 = Color(20, 20, 20)
GRAY80 = Color(204, 204, 204)
GRAY81 = Color(207, 207, 207)
GRAY82 = Color(209, 209, 209)
GRAY83 = Color(212, 212, 212)
GRAY84 = Color(214, 214, 214)
GRAY85 = Color(217, 217, 217)
GRAY86 = Color(219, 219, 219)
GRAY87 = Color(222, 222, 222)
GRAY88 = Color(224, 224, 224)
GRAY89 = Color(227, 227, 227)
GRAY9 = Color(23, 23, 23)
GRAY90 = Color(229, 229, 229)
GRAY91 = Color(232, 232, 232)
GRAY92 = Color(235, 235, 235)
GRAY93 = Color(237, 237, 237)
GRAY94 = Color(240, 240, 240)
GRAY95 = Color(242, 242, 242)
GRAY97 = Color(247, 247, 247)
GRAY98 = Color(250, 250, 250)
GRAY99 = Color(252, 252, 252)
GREEN = Color(0, 128, 0)
GREEN1 = Color(0, 255, 0)
GREEN2 = Color(0, 238, 0)
GREEN3 = Color(0, 205, 0)
GREEN4 = Color(0, 139, 0)
GREENYELLOW = Color(173, 255, 47)
HONEYDEW1 = Color(240, 255, 240)
HONEYDEW2 = Color(224, 238, 224)
HONEYDEW3 = Color(193, 205, 193)
HONEYDEW4 = Color(131, 139, 131)
HOTPINK = Color(255, 105, 180)
HOTPINK1 = Color(255, 110, 180)
HOTPINK2 = Color(238, 106, 167)
HOTPINK3 = Color(205, 96, 144)
HOTPINK4 = Color(139, 58, 98)
INDIANRED = Color(176, 23, 31)
INDIANRED = Color(205, 92, 92)
INDIANRED1 = Color(255, 106, 106)
INDIANRED2 = Color(238, 99, 99)
INDIANRED3 = Color(205, 85, 85)
INDIANRED4 = Color(139, 58, 58)
INDIGO = Color(75, 0, 130)
IVORY1 = Color(255, 255, 240)
IVORY2 = Color(238, 238, 224)
IVORY3 = Color(205, 205, 193)
IVORY4 = Color(139, 139, 131)
IVORYBLACK = Color(41, 36, 33)
KHAKI = Color(240, 230, 140)
KHAKI1 = Color(255, 246, 143)
KHAKI2 = Color(238, 230, 133)
KHAKI3 = Color(205, 198, 115)
KHAKI4 = Color(139, 134, 78)
LAVENDER = Color(230, 230, 250)
LAVENDERBLUSH1 = Color(255, 240, 245)
LAVENDERBLUSH2 = Color(238, 224, 229)
LAVENDERBLUSH3 = Color(205, 193, 197)
LAVENDERBLUSH4 = Color(139, 131, 134)
LAWNGREEN = Color(124, 252, 0)
LEMONCHIFFON1 = Color(255, 250, 205)
LEMONCHIFFON2 = Color(238, 233, 191)
LEMONCHIFFON3 = Color(205, 201, 165)
LEMONCHIFFON4 = Color(139, 137, 112)
LIGHTBLUE = Color(173, 216, 230)
LIGHTBLUE1 = Color(191, 239, 255)
LIGHTBLUE2 = Color(178, 223, 238)
LIGHTBLUE3 = Color(154, 192, 205)
LIGHTBLUE4 = Color(104, 131, 139)
LIGHTCORAL = Color(240, 128, 128)
LIGHTCYAN1 = Color(224, 255, 255)
LIGHTCYAN2 = Color(209, 238, 238)
LIGHTCYAN3 = Color(180, 205, 205)
LIGHTCYAN4 = Color(122, 139, 139)
LIGHTGOLDENROD1 = Color(255, 236, 139)
LIGHTGOLDENROD2 = Color(238, 220, 130)
LIGHTGOLDENROD3 = Color(205, 190, 112)
LIGHTGOLDENROD4 = Color(139, 129, 76)
LIGHTGOLDENRODYELLOW = Color(250, 250, 210)
LIGHTGREY = Color(211, 211, 211)
LIGHTPINK = Color(255, 182, 193)
LIGHTPINK1 = Color(255, 174, 185)
LIGHTPINK2 = Color(238, 162, 173)
LIGHTPINK3 = Color(205, 140, 149)
LIGHTPINK4 = Color(139, 95, 101)
LIGHTSALMON1 = Color(255, 160, 122)
LIGHTSALMON2 = Color(238, 149, 114)
LIGHTSALMON3 = Color(205, 129, 98)
LIGHTSALMON4 = Color(139, 87, 66)
LIGHTSEAGREEN = Color(32, 178, 170)
LIGHTSKYBLUE = Color(135, 206, 250)
LIGHTSKYBLUE1 = Color(176, 226, 255)
LIGHTSKYBLUE2 = Color(164, 211, 238)
LIGHTSKYBLUE3 = Color(141, 182, 205)
LIGHTSKYBLUE4 = Color(96, 123, 139)
LIGHTSLATEBLUE = Color(132, 112, 255)
LIGHTSLATEGRAY = Color(119, 136, 153)
LIGHTSTEELBLUE = Color(176, 196, 222)
LIGHTSTEELBLUE1 = Color(202, 225, 255)
LIGHTSTEELBLUE2 = Color(188, 210, 238)
LIGHTSTEELBLUE3 = Color(162, 181, 205)
LIGHTSTEELBLUE4 = Color(110, 123, 139)
LIGHTYELLOW1 = Color(255, 255, 224)
LIGHTYELLOW2 = Color(238, 238, 209)
LIGHTYELLOW3 = Color(205, 205, 180)
LIGHTYELLOW4 = Color(139, 139, 122)
LIMEGREEN = Color(50, 205, 50)
LINEN = Color(250, 240, 230)
MAGENTA = Color(255, 0, 255)
MAGENTA2 = Color(238, 0, 238)
MAGENTA3 = Color(205, 0, 205)
MAGENTA4 = Color(139, 0, 139)
MANGANESEBLUE = Color(3, 168, 158)
MAROON = Color(128, 0, 0)
MAROON1 = Color(255, 52, 179)
MAROON2 = Color(238, 48, 167)
MAROON3 = Color(205, 41, 144)
MAROON4 = Color(139, 28, 98)
MEDIUMORCHID = Color(186, 85, 211)
MEDIUMORCHID1 = Color(224, 102, 255)
MEDIUMORCHID2 = Color(209, 95, 238)
MEDIUMORCHID3 = Color(180, 82, 205)
MEDIUMORCHID4 = Color(122, 55, 139)
MEDIUMPURPLE = Color(147, 112, 219)
MEDIUMPURPLE1 = Color(171, 130, 255)
MEDIUMPURPLE2 = Color(159, 121, 238)
MEDIUMPURPLE3 = Color(137, 104, 205)
MEDIUMPURPLE4 = Color(93, 71, 139)
MEDIUMSEAGREEN = Color(60, 179, 113)
MEDIUMSLATEBLUE = Color(123, 104, 238)
MEDIUMSPRINGGREEN = Color(0, 250, 154)
MEDIUMTURQUOISE = Color(72, 209, 204)
MEDIUMVIOLETRED = Color(199, 21, 133)
MELON = Color(227, 168, 105)
MIDNIGHTBLUE = Color(25, 25, 112)
MINT = Color(189, 252, 201)
MINTCREAM = Color(245, 255, 250)
MISTYROSE1 = Color(255, 228, 225)
MISTYROSE2 = Color(238, 213, 210)
MISTYROSE3 = Color(205, 183, 181)
MISTYROSE4 = Color(139, 125, 123)
MOCCASIN = Color(255, 228, 181)
NAVAJOWHITE1 = Color(255, 222, 173)
NAVAJOWHITE2 = Color(238, 207, 161)
NAVAJOWHITE3 = Color(205, 179, 139)
NAVAJOWHITE4 = Color(139, 121, 94)
NAVY = Color(0, 0, 128)
OLDLACE = Color(253, 245, 230)
OLIVE = Color(128, 128, 0)
OLIVEDRAB = Color(107, 142, 35)
OLIVEDRAB1 = Color(192, 255, 62)
OLIVEDRAB2 = Color(179, 238, 58)
OLIVEDRAB3 = Color(154, 205, 50)
OLIVEDRAB4 = Color(105, 139, 34)
ORANGE = Color(255, 128, 0)
ORANGE1 = Color(255, 165, 0)
ORANGE2 = Color(238, 154, 0)
ORANGE3 = Color(205, 133, 0)
ORANGE4 = Color(139, 90, 0)
ORANGERED1 = Color(255, 69, 0)
ORANGERED2 = Color(238, 64, 0)
ORANGERED3 = Color(205, 55, 0)
ORANGERED4 = Color(139, 37, 0)
ORCHID = Color(218, 112, 214)
ORCHID1 = Color(255, 131, 250)
ORCHID2 = Color(238, 122, 233)
ORCHID3 = Color(205, 105, 201)
ORCHID4 = Color(139, 71, 137)
PALEGOLDENROD = Color(238, 232, 170)
PALEGREEN = Color(152, 251, 152)
PALEGREEN1 = Color(154, 255, 154)
PALEGREEN2 = Color(144, 238, 144)
PALEGREEN3 = Color(124, 205, 124)
PALEGREEN4 = Color(84, 139, 84)
PALETURQUOISE1 = Color(187, 255, 255)
PALETURQUOISE2 = Color(174, 238, 238)
PALETURQUOISE3 = Color(150, 205, 205)
PALETURQUOISE4 = Color(102, 139, 139)
PALEVIOLETRED = Color(219, 112, 147)
PALEVIOLETRED1 = Color(255, 130, 171)
PALEVIOLETRED2 = Color(238, 121, 159)
PALEVIOLETRED3 = Color(205, 104, 137)
PALEVIOLETRED4 = Color(139, 71, 93)
PAPAYAWHIP = Color(255, 239, 213)
PEACHPUFF1 = Color(255, 218, 185)
PEACHPUFF2 = Color(238, 203, 173)
PEACHPUFF3 = Color(205, 175, 149)
PEACHPUFF4 = Color(139, 119, 101)
PEACOCK = Color(51, 161, 201)
PINK = Color(255, 192, 203)
PINK1 = Color(255, 181, 197)
PINK2 = Color(238, 169, 184)
PINK3 = Color(205, 145, 158)
PINK4 = Color(139, 99, 108)
PLUM = Color(221, 160, 221)
PLUM1 = Color(255, 187, 255)
PLUM2 = Color(238, 174, 238)
PLUM3 = Color(205, 150, 205)
PLUM4 = Color(139, 102, 139)
POWDERBLUE = Color(176, 224, 230)
PURPLE = Color(128, 0, 128)
PURPLE1 = Color(155, 48, 255)
PURPLE2 = Color(145, 44, 238)
PURPLE3 = Color(125, 38, 205)
PURPLE4 = Color(85, 26, 139)
RASPBERRY = Color(135, 38, 87)
RAWSIENNA = Color(199, 97, 20)
RED1 = Color(255, 0, 0)
RED2 = Color(238, 0, 0)
RED3 = Color(205, 0, 0)
RED4 = Color(139, 0, 0)
ROSYBROWN = Color(188, 143, 143)
ROSYBROWN1 = Color(255, 193, 193)
ROSYBROWN2 = Color(238, 180, 180)
ROSYBROWN3 = Color(205, 155, 155)
ROSYBROWN4 = Color(139, 105, 105)
ROYALBLUE = Color(65, 105, 225)
ROYALBLUE1 = Color(72, 118, 255)
ROYALBLUE2 = Color(67, 110, 238)
ROYALBLUE3 = Color(58, 95, 205)
ROYALBLUE4 = Color(39, 64, 139)
SALMON = Color(250, 128, 114)
SALMON1 = Color(255, 140, 105)
SALMON2 = Color(238, 130, 98)
SALMON3 = Color(205, 112, 84)
SALMON4 = Color(139, 76, 57)
SANDYBROWN = Color(244, 164, 96)
SAPGREEN = Color(48, 128, 20)
SEAGREEN1 = Color(84, 255, 159)
SEAGREEN2 = Color(78, 238, 148)
SEAGREEN3 = Color(67, 205, 128)
SEAGREEN4 = Color(46, 139, 87)
SEASHELL1 = Color(255, 245, 238)
SEASHELL2 = Color(238, 229, 222)
SEASHELL3 = Color(205, 197, 191)
SEASHELL4 = Color(139, 134, 130)
SEPIA = Color(94, 38, 18)
SGIBEET = Color(142, 56, 142)
SGIBRIGHTGRAY = Color(197, 193, 170)
SGICHARTREUSE = Color(113, 198, 113)
SGIDARKGRAY = Color(85, 85, 85)
SGIGRAY12 = Color(30, 30, 30)
SGIGRAY16 = Color(40, 40, 40)
SGIGRAY32 = Color(81, 81, 81)
SGIGRAY36 = Color(91, 91, 91)
SGIGRAY52 = Color(132, 132, 132)
SGIGRAY56 = Color(142, 142, 142)
SGIGRAY72 = Color(183, 183, 183)
SGIGRAY76 = Color(193, 193, 193)
SGIGRAY92 = Color(234, 234, 234)
SGIGRAY96 = Color(244, 244, 244)
SGILIGHTBLUE = Color(125, 158, 192)
SGILIGHTGRAY = Color(170, 170, 170)
SGIOLIVEDRAB = Color(142, 142, 56)
SGISALMON = Color(198, 113, 113)
SGISLATEBLUE = Color(113, 113, 198)
SGITEAL = Color(56, 142, 142)
SIENNA = Color(160, 82, 45)
SIENNA1 = Color(255, 130, 71)
SIENNA2 = Color(238, 121, 66)
SIENNA3 = Color(205, 104, 57)
SIENNA4 = Color(139, 71, 38)
SILVER = Color(192, 192, 192)
SKYBLUE = Color(135, 206, 235)
SKYBLUE1 = Color(135, 206, 255)
SKYBLUE2 = Color(126, 192, 238)
SKYBLUE3 = Color(108, 166, 205)
SKYBLUE4 = Color(74, 112, 139)
SLATEBLUE = Color(106, 90, 205)
SLATEBLUE1 = Color(131, 111, 255)
SLATEBLUE2 = Color(122, 103, 238)
SLATEBLUE3 = Color(105, 89, 205)
SLATEBLUE4 = Color(71, 60, 139)
SLATEGRAY = Color(112, 128, 144)
SLATEGRAY1 = Color(198, 226, 255)
SLATEGRAY2 = Color(185, 211, 238)
SLATEGRAY3 = Color(159, 182, 205)
SLATEGRAY4 = Color(108, 123, 139)
SNOW1 = Color(255, 250, 250)
SNOW2 = Color(238, 233, 233)
SNOW3 = Color(205, 201, 201)
SNOW4 = Color(139, 137, 137)
SPRINGGREEN = Color(0, 255, 127)
SPRINGGREEN1 = Color(0, 238, 118)
SPRINGGREEN2 = Color(0, 205, 102)
SPRINGGREEN3 = Color(0, 139, 69)
STEELBLUE = Color(70, 130, 180)
STEELBLUE1 = Color(99, 184, 255)
STEELBLUE2 = Color(92, 172, 238)
STEELBLUE3 = Color(79, 148, 205)
STEELBLUE4 = Color(54, 100, 139)
TAN = Color(210, 180, 140)
TAN1 = Color(255, 165, 79)
TAN2 = Color(238, 154, 73)
TAN3 = Color(205, 133, 63)
TAN4 = Color(139, 90, 43)
TEAL = Color(0, 128, 128)
THISTLE = Color(216, 191, 216)
THISTLE1 = Color(255, 225, 255)
THISTLE2 = Color(238, 210, 238)
THISTLE3 = Color(205, 181, 205)
THISTLE4 = Color(139, 123, 139)
TOMATO1 = Color(255, 99, 71)
TOMATO2 = Color(238, 92, 66)
TOMATO3 = Color(205, 79, 57)
TOMATO4 = Color(139, 54, 38)
TURQUOISE = Color(64, 224, 208)
TURQUOISE1 = Color(0, 245, 255)
TURQUOISE2 = Color(0, 229, 238)
TURQUOISE3 = Color(0, 197, 205)
TURQUOISE4 = Color(0, 134, 139)
TURQUOISEBLUE = Color(0, 199, 140)
VIOLET = Color(238, 130, 238)
VIOLETRED = Color(208, 32, 144)
VIOLETRED1 = Color(255, 62, 150)
VIOLETRED2 = Color(238, 58, 140)
VIOLETRED3 = Color(205, 50, 120)
VIOLETRED4 = Color(139, 34, 82)
WARMGREY = Color(128, 128, 105)
WHEAT = Color(245, 222, 179)
WHEAT1 = Color(255, 231, 186)
WHEAT2 = Color(238, 216, 174)
WHEAT3 = Color(205, 186, 150)
WHEAT4 = Color(139, 126, 102)
WHITE = Color(255, 255, 255)
WHITESMOKE = Color(245, 245, 245)
YELLOW1 = Color(255, 255, 0)
YELLOW2 = Color(238, 238, 0)
YELLOW3 = Color(205, 205, 0)
YELLOW4 = Color(139, 139, 0)

# LED strip configuration:
LED_COUNT = 5  # Number of LED pixels.
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 40  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

NOSE = 0
LEFT = 1
CENTER = 2
RIGHT = 3
BOTTOM = 4

broker="127.0.0.1"

def signal_handler(sig, frame):
    clearStrip(strip)
    client.disconnect()  # disconnect
    client.loop_stop()  # stop loop
    sys.exit(0)

def occultationOneColor(t, on, off, offset, color):
    period = on + off
    phase = (t + offset) % period
    if phase > on:
        return BLACK
    return color


def waveOneColor(t, period, offset, r, g, b):
    phase = (t + offset) * math.pi * 2 / period
    k = (math.sin(phase) + 1) / 2
    return Color(int(k * r), int(k * g), int(k * b))


def waveTwoColor(t, period, offset, r1, g1, b1, r2, g2, b2, fading):
    phase = (t + offset) * math.pi * 2 / period
    if fading:
        k = (math.sin(phase) + 1) / 2
        kk = 1 - k
        return Color(int(k * r1) + int(kk * r2), int(k * g1) + int(kk * g2), int(k * b1) + int(kk * b2))
    else:
        k = math.sin(phase)
        if k > 0:
            return Color(int(k * r1), int(k * g1), int(k * b1))
        else:
            return Color(int(-k * r2), int(-k * g2), int(-k * b2))


def fixedColor(t, color):
    return color


def clearStrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()

#define callback
def on_message(client, userdata, message):
    message =str(message.payload.decode("utf-8"))
    print("received message =", message)
    if message == "stop":
        signal_handler(null, null)
    if message == "on":
        func_table[0] = (waveOneColor, (4., 0, 255, 0, 0))
        func_table[1] = (waveOneColor, (4., 0, 255, 0, 0))
        func_table[2] = (waveOneColor, (4., 0, 255, 0, 0))
    if message == "off":
        func_table[0] = (waveOneColor, (3., 0, 255, 0, 0))
        func_table[1] = (waveOneColor, (3., 1.0, 255, 255, 0))
        func_table[2] = (waveOneColor, (3., 2.0, 0, 0, 255))
    if message == "random":
        func_table[0] = (occultationOneColor, (2., 1.0, 1.0, BLUE))
        func_table[1] = (occultationOneColor, (2.5, 0.5, 0., YELLOW1))
        func_table[2] = (occultationOneColor, (1.0, 2., 0.5, RED1))


# Main program logic follows:
if __name__ == '__main__':
    conf = getConfig()
    led_pin = getConfig()['LED_PIN']

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    clearStrip(strip)
    fd = 1 / 5
    func_table = {
        0: (fixedColor, (BLACK)),
        1: (fixedColor, (BLACK)),
        2: (fixedColor, (BLACK)),
        3: (occultationOneColor, (5, 1, 0, RED1)),
        4: (waveOneColor, (4., 0, 128, 0, 255)),
        #5: (waveTwoColor, (4., 0, 255, 0, 0, 0, 0, 255, False)),
    }

    # init mqtt connection and subscribe
    client = paho.Client("led_manager")  # create client
    client.on_message = on_message # Bind function to callback
    client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    client.subscribe("leds")  # subscribe

    # set signal handler to catch ctrl C
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        t = time.time()
        for i in range(LED_COUNT):
            func, args = func_table[i]
            if isinstance(args, Iterable):
                strip.setPixelColor(i, func(t, *args))
            else:
                strip.setPixelColor(i, func(t, args))
            strip.show()
        time.sleep(fd)
