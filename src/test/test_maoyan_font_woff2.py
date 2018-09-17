# -*- coding: utf-8 -*-
# create by Aramis
from fontTools import ttLib

font = ttLib.TTFont('current.woff')
glyphNames = font.getGlyphNames()
print(glyphNames)
glyphNames2=font.getGlyphNames2()
print(glyphNames2)

print(font.getGlyphName(font.getGlyphID('uniE073')))

font.getGlyphSet().keys()

# for i in font.getGlyphSet().keys():

    # print(font.getGlyphSet().get(i))
