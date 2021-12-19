import sys
import random

# TODO: check nearby fields in valid function


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

    def reset(self):
        self.status = Field.field_status["default"]

    def set(self, status):
        self.status = Field.field_status[status]


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
    def __init__(self, owner, board_type: str = "own"):
        self.owner = owner
        self.field = []
        self.ships = []
        self.type = board_type
        self.reset()

    def reset(self):
        for _ in range(10):
            self.field.append([Field() for _ in range(Board.grid_size)])

    def show_caption(self, shift):
        if self.type == "own":
            print("   " + " " * shift + f"Player{self.owner.id+1}: " + " Own Board")
        elif self.type == "opp":
            print("   " + " " * shift + f"Player{self.owner.id+1}: " + "Opp Board")
        else:
            raise TypeError(f"wrong board_type: {self.type}")

    def update(self):
        for ship in self.ships:
            for field in ship.fields:
                self.field[field[1]][field[0]].set(ship.name)

    def show(self, shift=0):
        self.show_caption(shift)
        print(" " * (shift + 2), *Board.horizontal_row)
        for i, line in enumerate(self.field):
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
        self.boards = [Board(self, "own"), Board(self, "opp")]
        self.ships = []
        self.ships_alive = 5

    def __str__(self):
        return f"Player{self.id}"

    def show_own_board(self):
        self.boards[0].show()

    def show_opp_board(self):
        self.boards[1].show()

    def show_boards(self):
        for board in self.boards:
            board.show()

    def user_input(self, q):
        inp = input(q)
        if inp == "exit":
            sys.exit(1)
        if inp == "show":
            self.show_boards()
        return inp

    def place_ships(self, place_random=True):
        if not place_random:
            self.show_own_board()
            alert = True
        else:
            alert = False
        for ship in Player.ships:
            # Syntax: X(Letter)Y(Number)Orientation(N, E, S, W)
            while True:
                if not place_random:
                    inp = self.user_input(f"Enter coordinates and orientation of {ship}({Ship.ship_lenght[ship]}): ")
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
            self.boards[0].place_ship(temp_ship)
            if not place_random:
                self.show_own_board()
        if place_random:
            self.show_own_board()


class Game:
    def __init__(self):
        self.players = [Player(player_id) for player_id in range(2)]

    def check_win(self):
        for player in self.players:
            if player.ships_alive <= 0:
                print(f"{player} lost the game!")
                sys.exit(1)

    def init_game(self):
        random_placement = bool(input("enter for random placement  "))
        for player in self.players:
            player.place_ships(not random_placement)

    def loop(self):
        self.init_game()
        while True:
            self.check_win()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
