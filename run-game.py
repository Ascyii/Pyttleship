import sys
import random

# TODO: check nearby fields in valid function
# TODO: figure out system for ship detection


CAPTION = r"""
           ___       __  __  __        __   _    
          / _ \__ __/ /_/ /_/ /__ ___ / /  (_)__ 
         / ___/ // / __/ __/ / -_|_-</ _ \/ / _ \
        /_/   \_, /\__/\__/_/\__/___/_//_/_/ .__/
             /___/                        /_/    
        """ + "\n\u00AEAscyii 2021\n"


def check_for_commands(inp):
    if inp == "exit":
        sys.exit(1)


def user_input(q):
    inp = input(q)
    check_for_commands(inp)
    return inp


class Field:
    field_status = {"default": ".", "water_shot": "o", "ship_dead": "X",
                    "carrier": "C", "battleship": "B", "destroyer": "D",
                    "submarine": "S", "patrol": "P"}

    def __init__(self, status: str = "default"):
        self.status = Field.field_status[status]

    def __str__(self):
        return str(self.status)

    def __repr__(self):
        return str(self)

    def show_hidden(self):
        if self.status == Field.field_status["water_shot"]:
            return str(Field.field_status["water_shot"])
        elif self.status == Field.field_status["ship_dead"]:
            return str(Field.field_status["ship_dead"])
        else:
            return str(Field.field_status["default"])

    def reset(self):
        self.status = Field.field_status["default"]

    def set(self, status):
        self.status = Field.field_status[status]

    def hit(self):
        pass


class Ship:
    ship_lenght = {"carrier": 5, "battleship": 4, "destroyer": 3,
                   "submarine": 3, "patrol": 2}
    orientations = {"S": [0, 1], "E": [1, 0], "N": [0, -1], "W": [-1, 0]}

    # Orientation has to be a capital compass direction
    def __init__(self, name: str, x, y, orientation: str = "S"):
        self.name = name
        self.length = Ship.ship_lenght[name]
        self.origin = [x, y]
        self.orientation = orientation
        self.fields = []
        self.update_fields()

    # Checks if ship is valid important to call before adding to board
    def valid(self, alert=False, ships=None):
        for field in self.fields:
            if 0 > field[0] or field[0] > 9 or 0 > field[1] or field[1] > 9:
                if alert:
                    print(f"{self.name} out of boundaries!")
                return False
        for ship in ships:
            if any(coord in ship.fields for coord in self.fields):
                if alert:
                    print(f"{self.name} is colliding with {ship.name}!")
                return False
        return True

    def update_fields(self):
        for i in range(self.length):
            field = [self.origin[0] + Ship.orientations[self.orientation][0] * i,
                     self.origin[1] + Ship.orientations[self.orientation][1] * i]
            self.fields.append(field)


class Board:
    horizontal_row = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    vertical_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    grid_size = len(vertical_row)

    # Can be initialized with type "own" or type "opp"
    def __init__(self, owner):
        self.owner = owner
        self.field = []
        self.ships = []
        self.reset()

    def reset(self):
        for _ in range(10):
            self.field.append([Field() for _ in range(Board.grid_size)])

    def show_caption(self, shift):
        print("     " + " " * shift + f"{self.owner}'s Board")

    def update(self):
        for ship in self.ships:
            for field in ship.fields:
                self.field[field[1]][field[0]].set(ship.name)

    def show(self, ships_hidden=False, shift=0):
        self.show_caption(shift)
        print(" " * (shift + 2), *Board.horizontal_row)
        for i, line in enumerate(self.field):
            if ships_hidden:
                line_str = ""
                for field in line:
                    line_str += field.show_hidden() + " "
                print(" " * shift, Board.vertical_row[i], line_str)
            else:
                print(" " * shift, Board.vertical_row[i], *line)

    def place_ship(self, ship):
        self.ships.append(ship)
        self.update()


class Player:
    ships = ["carrier", "battleship", "destroyer", "submarine", "patrol"]
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    orientations = ["N", "S", "E", "W"]

    def __init__(self, player_id=0):
        self.id = player_id
        self.board = Board(self)
        self.ships = []
        self.ships_alive = 5

    def __str__(self):
        return f"Player{self.id}"

    def show_board(self, hidden=False):
        self.board.show(hidden)

    def place_ships(self, place_random=True):
        if not place_random:
            self.show_board()
            alert = True
        else:
            alert = False
        for ship in Player.ships:
            # Syntax: X(Letter)Y(Number)Orientation(N, E, S, W)
            while True:
                if not place_random:
                    inp = user_input(f"Enter coordinates and orientation of {ship}({Ship.ship_lenght[ship]}): ")
                else:
                    inp = f"{random.choice(Player.letters)}{random.randrange(9)}{random.choice(Player.orientations)}"
                try:
                    temp_ship = Ship(ship, int(Player.letters.index(inp[0])), int(inp[1]), str(inp[2]))
                except (NameError, IndexError):
                    temp_ship = None
                    print("syntax: X(Letter)Y(Number)Orientation(N, E, S, W)")
                    continue
                if temp_ship.valid(alert, self.ships):
                    break
            self.ships.append(temp_ship)
            self.board.place_ship(temp_ship)
            if not place_random:
                self.show_board()


class Game:
    def __init__(self):
        self.players = [Player(player_id) for player_id in range(2)]
        self.active_player = random.choice(self.players)
        self.init_game()

    def check_win(self):
        for player in self.players:
            if player.ships_alive <= 0:
                print(f"{player} lost the game!")
                sys.exit(1)

    def init_game(self):
        print(CAPTION)
        random_placement = bool(input("press enter for random placement  "))
        for player in self.players:
            player.place_ships(not random_placement)

    def turn(self, fire_random=False):
        player = self.active_player
        other_player = self.players[abs(self.players.index(player)-1)]
        other_player.show_board(False)
        print(f"{player}'s turn")
        while True:
            if not fire_random:
                inp = user_input("Fire at:  ")
            else:
                inp = f"{random.choice(Player.letters)}{random.randrange(9)}"
            try:
                other_player.board.field[int(inp[1])][Player.letters.index(inp[0].upper())].hit()
                break
            except (NameError, IndexError, ValueError):
                print("syntax: X(Letter)Y(Number)")
                continue
        self.active_player = other_player

    def loop(self):
        while True:
            self.turn()
            self.check_win()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
