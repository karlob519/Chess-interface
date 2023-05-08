import pygame.mixer as mx
mx.init()
# Defining sound effects 
# Mute is off by default, toggled by TAB
mute_val = False

def mute():
    global mute_val
    if not mute_val:
        mute_val = True
    else:
        mute_val = False

    return

def intro():
    sound = mx.Sound('SFX/start.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def move():
    sound = mx.Sound('SFX/move.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def check():
    sound = mx.Sound('SFX/check.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def capture():
    sound = mx.Sound('SFX/capture.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def castling():
    sound = mx.Sound('SFX/castling.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def checkmate():
    sound = mx.Sound('SFX/checkmate.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def none():
    sound = mx.Sound('SFX/none.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def promotion():
    sound = mx.Sound('SFX/promotion.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

