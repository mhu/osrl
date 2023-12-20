import os
import random

clear = lambda: os.system("tput reset")

map = None


class Player:
    fov = 5
    mode = "map"
    position = [1, 1]
    health = 100
    inventory = []


class Enemy:
    def __init__(self, symbol, health, damage, position):
        self.symbol = symbol
        self.health = health
        self.damage = damage
        self.position = position


player = Player()
enemies = []


def generate_map():
    import random

    height = random.randint(20, 40)
    width = random.randint(20, 40)

    # Create an empty grid
    grid = [["#" for _ in range(width)] for _ in range(height)]

    # Generate a path
    x, y = width // 2, height // 2
    grid[y][x] = "."
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for _ in range(5000):  # You can adjust the number of steps
        dx, dy = random.choice(directions)
        new_x, new_y = x + dx, y + dy
        if 0 < new_x < width - 1 and 0 < new_y < height - 1:
            grid[new_y][new_x] = "."
            x, y = new_x, new_y

    # Add borders
    for i in range(height):
        grid[i][0] = "#"
        grid[i][width - 1] = "#"
    for j in range(width):
        grid[0][j] = "#"
        grid[height - 1][j] = "#"

    global map
    map = ["".join(row) for row in grid]


def getch():
    import termios
    import sys, tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch()


def spawn_enemy(enemy_type, position):
    if enemy_type == "goblin":
        enemies.append(Enemy("g", 10, 5, position))
        return "g"


def draw_screen():
    if player.mode == "map":
        if map == None:
            generate_map()

        for y in range(0, len(map)):
            for x in range(0, len(map[y])):
                if x == player.position[0] and y == player.position[1]:
                    print("@", end="")
                else:
                    if (
                        player.position[0] - player.fov
                        <= x
                        <= player.position[0] + player.fov
                        and player.position[1] - player.fov
                        <= y
                        <= player.position[1] + player.fov
                    ):
                        if map[y][x] == "." and random.randint(1, 40) == 1:
                            symbol = spawn_enemy("goblin", [x, y])
                            print(symbol, end="")
                        else:
                            print(map[y][x], end="")
                    else:
                        print(" ", end="")
            print()

    elif player.mode == "inventory":
        print("Inventory")
        print("=========")
        print()

        if len(player.inventory) == 0:
            print("Empty")
        else:
            for item in player.inventory:
                print(f"- {item}")

    print()
    print("-" * 20)
    print()
    print(f"Health: {player.health}")
    print(f"[I]nventory: {len(player.inventory)}")
    print(f"[M]ap")


def move_entity(entity, direction):
    if direction == "north":
        if map[entity.position[1] - 1][entity.position[0]] == "#":
            return
        entity.position[1] -= 1

    elif direction == "south":
        if map[entity.position[1] + 1][entity.position[0]] == "#":
            return
        entity.position[1] += 1

    elif direction == "east":
        if map[entity.position[1]][entity.position[0] + 1] == "#":
            return
        entity.position[0] += 1

    elif direction == "west":
        if map[entity.position[1]][entity.position[0] - 1] == "#":
            return
        entity.position[0] -= 1


def move_player():
    global enemies

    if next_action == "w":
        move_entity(player, "north")
    elif next_action == "s":
        move_entity(player, "south")
    elif next_action == "d":
        move_entity(player, "east")
    elif next_action == "a":
        move_entity(player, "west")

    for enemy in enemies:
        if enemy.position[0] < player.position[0]:
            move_entity(enemy, "east")
        elif enemy.position[0] > player.position[0]:
            move_entity(enemy, "west")
        elif enemy.position[1] < player.position[1]:
            move_entity(enemy, "south")
        elif enemy.position[1] > player.position[1]:
            move_entity(enemy, "north")

    if map[player.position[1]][player.position[0]] == "/":
        generate_map()

        enemies = []
        player.position = [1, 1]


next_action = None

while True:
    clear()
    draw_screen()

    next_action = getch()
    if (
        next_action == "w"
        or next_action == "a"
        or next_action == "s"
        or next_action == "d"
    ):
        move_player()
    elif next_action == "m":
        player.mode = "map"
    elif next_action == "i":
        player.mode = "inventory"
    elif next_action == "q":
        clear()
        break
