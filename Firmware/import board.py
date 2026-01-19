import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Macros, Press, Release, Tap

# =====================
# Keyboard setup
# =====================
keyboard = KMKKeyboard()

# Enable macros
macros = Macros()
keyboard.modules.append(macros)

# =====================
# Key pins (4 keys)
# =====================
PINS = [
    board.D1,
    board.D2,
    board.D3,
    board.D4,
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# REQUIRED for KeysScanner
keyboard.coord_mapping = [0, 1, 2, 3]

# =====================
# LED setup (2 LEDs)
# =====================
led_power = digitalio.DigitalInOut(board.D5)
led_power.direction = digitalio.Direction.OUTPUT

led_activity = digitalio.DigitalInOut(board.D6)
led_activity.direction = digitalio.Direction.OUTPUT

# Turn on power LED at boot
led_power.value = True

# =====================
# Macros with LED feedback
# =====================
def led_macro(*keys):
    return KC.MACRO(
        Press(led_activity),
        *keys,
        Release(led_activity),
    )

# =====================
# Keymap (Fusion 360)
# =====================
keyboard.keymap = [
    [
        led_macro(Tap(KC.S)),                          # Sketch
        led_macro(Tap(KC.E)),                          # Extrude
        led_macro(Press(KC.LCTL), Tap(KC.Z), Release(KC.LCTL)),  # Undo
        led_macro(Press(KC.LCTL), Tap(KC.S), Release(KC.LCTL)),  # Save
    ]
]

# =====================
# Start keyboard
# =====================
if __name__ == '__main__':
    keyboard.go()
