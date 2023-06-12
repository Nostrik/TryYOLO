from __future__ import print_function
import colorama
from time import sleep

colorama.init()

# # ESC [ n A       # move cursor n lines up
# # ESC [ n B       # move cursor n lines down

cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
cursor_down = lambda lines: '\x1b[{0}B'.format(lines)


print("meow :)")
print("meow-meow :)")
print("meow-meow-meow :)")
lines_up = 3
print(cursor_up(lines_up), end='')
sleep(1)
print("woof", " " * 10)
sleep(1)
lines_down = 1
sleep(1)
print(cursor_down(lines_down), end='')
sleep(1)
print("woof-woof-woof", " " * 10)
sleep(1)
lines_up = 2
sleep(1)
print(cursor_up(lines_up), end='')
print("woof-woof", " " * 10)
sleep(1)
