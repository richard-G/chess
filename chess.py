# Chess


class Piece:
    def __init__(self, colour):
        self.colour = colour
        self.is_alive = True

    def move(self, target_indices):
        # check first if move is allowed
        if True:
            self.position[0] = target_indices[0]
            self.position[1] = target_indices[1]

    # general function for filtering moves
    def get_possible_moves(self, moves):
        filtered_moves = []

        for move in moves:
            # filter move if indices are invalid
            if move[0] not in range(0, 8) or move[1] not in range(0, 8):
                continue

            filtered_moves.append(move)

        return filtered_moves


# ** position could probably be inherited from the super class **
class Pawn(Piece):
    # call with nest loops - for colour in colours: for number in range(1, 9)
    def __init__(self, colour, number):
        # give each instance a unique 4 character identifier
        self.type = 'PN'
        self.name = 'Pawn'
        self.piece_id = colour[0] + 'PN' + str(number)
        super().__init__(colour)

        # give each pawn a position
        if self.colour == 'White':
            self.position = [6, number - 1]
            self.symbol = chr(9823)
        else:
            self.position = [1, number - 1]
            self.symbol = chr(9817)

    # initialise moves to empty list, append for each condition
    def get_moves(self, pieces):
        all_moves = []
        # own_pieces = [piece.position for piece in pieces[colour].values() for colour in ['White', 'Black']]
        # * more efficient way of achieving this, some kind of nested list comprehension *
        white_pieces = [piece.position for piece in pieces['White'].values()]
        black_pieces = [piece.position for piece in pieces['Black'].values()]
        all_pieces = white_pieces + black_pieces
        # opposing_pieces = [piece.position for piece in pieces[opposing].values()]
        if self.colour == 'White':
            if self.position[0] == 6:

                for i in range(1, 3):
                    move = [self.position[0] - i, self.position[1]]
                    if move in all_pieces:
                        break
                    else:
                        all_moves.append(move)

            elif self.position[0] == 0:
                # logic for turning into a queen here, and also not letting the pawn move more
                pass
            else:
                # need to check if position is occupied by a piece already
                all_moves.append([self.position[0] - 1, self.position[1]])

            # logic for diagonal movements
            all_moves.append([self.position[0] - 1, self.position[1] + 1])
            all_moves.append([self.position[0] - 1, self.position[1] - 1])

        # lots of redundant lines here, could set some a +/- coefficient that is cycled
        elif self.colour == 'Black':
            if self.position[0] == 1:
                for i in range(1, 3):
                    move = [self.position[0] + i, self.position[1]]
                    if move in all_pieces:
                        break
                    else:
                        all_moves.append(move)
            elif self.position[0] == 7:
                # logic for turning into a queen here, and also not letting the pawn move more
                pass
            else:
                # need to check if position is occupied by a piece already
                all_moves.append([self.position[0] + 1, self.position[1]])

            all_moves.append([self.position[0] + 1, self.position[1] + 1])
            all_moves.append([self.position[0] + 1, self.position[1] - 1])

        # run all possible moves through filter, returning only allowed moves
        moves = self.get_pawn_moves(all_moves, pieces)

        return moves

    # function to test all moves in .get_moves(), returns only those that are allowed
    # probably call this within get_moves()
    # ** need logic to prevent pawns jumping over opposing pieces **
    def get_pawn_moves(self, moves, pieces):
        filtered_moves = []
        # colours = ['White', 'Black'] # only needed for denying pawns jumping.
        if self.colour == 'White':
            opposing = 'Black'
        else:
            opposing = 'White'

        for move in moves:
            # can never move into a square occupied by same colour piece
            if move in [piece.position for piece in pieces[self.colour].values()]:
                continue

            # logic for only allowing forward move if target square is unoccupied
            if move[1] == self.position[1]:
                if move in [piece.position for piece in pieces[opposing].values()]:
                    continue
            # if opposing piece is present diagonally, ONLY THEN keep the move
            # logic for allowing diagonal move only when occupied by opposing piece
            # ie. if diagonal move isn't occupied by opposing colour, pop it
            else:
                if move not in [piece.position for piece in pieces[opposing].values()]:
                    continue

            if move[0] not in range(0, 8) or move[1] not in range(0, 8):
                continue

            # if no continue statement has been reached, means that the move is allowed.
            filtered_moves.append(move)

        return filtered_moves


class King(Piece):
    def __init__(self, colour):
        # ** i think this will work **
        super().__init__(colour)
        self.name = 'King'
        if self.colour == 'Black':
            self.position = convert_coords('E8')
            self.symbol = chr(9812)
        else:
            self.position = convert_coords('E1')
            self.symbol = chr(9818)
        self.piece_id = colour[0] + 'KNG'

        self.type = 'KNG'

    def get_moves(self, pieces):
        moves = []
        if self.colour == 'White':
            opposing = 'Black'
        else:
            opposing = 'White'

        own_pieces = [piece.position for piece in pieces[self.colour].values()]
        # opposing_pieces = [piece.position for piece in pieces[opposing].values()]

        # * not clean *
        # orthogonal moves
        move = [self.position[0] + 1, self.position[1]]
        if move not in own_pieces:
            moves.append(move)
        move = [self.position[0] - 1, self.position[1]]
        if move not in own_pieces:
            moves.append(move)
        move = [self.position[0], self.position[1] + 1]
        if move not in own_pieces:
            moves.append(move)
        move = [self.position[0], self.position[1] - 1]
        if move not in own_pieces:
            moves.append(move)

        # diagonal moves
        move = [self.position[0] + 1, self.position[1] + 1]
        if move not in own_pieces:
            moves.append(move)
        move = [self.position[0] + 1, self.position[1] - 1]
        if move not in own_pieces:
            moves.append(move)
        move = [self.position[0] - 1, self.position[1] + 1]
        if move not in own_pieces:
            moves.append(move)
        move = [self.position[0] - 1, self.position[1] - 1]
        if move not in own_pieces:
            moves.append(move)

        moves = self.get_possible_moves(moves)

        return moves


# **
# need logic for creating a new instance of Queen class due to pawn reaching the end of the board.
class Queen(Piece):
    def __init__(self, colour, position=None, id=None):
        super().__init__(colour)
        self.name = 'Queen'

        if self.colour == 'White':
            self.symbol = chr(9819)
            if position is None:
                self.position = convert_coords('D1')
            else:
                self.position = position
        else:
            self.symbol = chr(9813)
            if position is None:
                self.position = convert_coords('D8')
            else:
                self.position = position

        # need to clean here, can send self.type to the parent where a piece_id is given
        # ** need to change this, but it does work **
        if id is None:
            self.piece_id = colour[0] + 'QUN'
        else:
            self.piece_id = colour[0] + 'QN' + id[-1]

        self.type = 'QUN'

    def get_moves(self, pieces):
        moves = []
        if self.colour == 'White':
            opposing = 'Black'
        else:
            opposing = 'White'

        own_pieces = [piece.position for piece in pieces[self.colour].values()]
        opposing_pieces = [piece.position for piece in pieces[opposing].values()]

        # * definitely a cleaner way of achieving this *
        # orthogonal moveset
        for i in range(1, 8):
            move = [self.position[0] + i, self.position[1]]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] - i, self.position[1]]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0], self.position[1] + i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0], self.position[1] - i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        # diagonal moveset
        for i in range(1, 8):
            move = [self.position[0] + i, self.position[1] + i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] + i, self.position[1] - i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] - i, self.position[1] + i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] - i, self.position[1] - i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        moves = self.get_possible_moves(moves)

        return moves


class Rook(Piece):
    def __init__(self, colour, number):
        self.piece_id = colour[0] + 'RK' + str(number)
        super().__init__(colour)
        self.name = 'Rook'

        if self.colour == 'White':
            row = 7
            self.symbol = chr(9820)
        else:
            row = 0
            self.symbol = chr(9814)

        if number == 1:
            self.position = [row, 0]
        elif number == 2:
            self.position = [row, 7]

        self.type = 'RK'

    def get_moves(self, pieces):
        moves = []
        if self.colour == 'White':
            opposing = 'Black'
        else:
            opposing = 'White'

        own_pieces = [piece.position for piece in pieces[self.colour].values()]
        opposing_pieces = [piece.position for piece in pieces[opposing].values()]

        # * definitely a cleaner way of achieving this *
        for i in range(1, 8):
            move = [self.position[0] + i, self.position[1]]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] - i, self.position[1]]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0], self.position[1] + i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0], self.position[1] - i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        moves = self.get_possible_moves(moves)

        return moves


class Knight(Piece):
    def __init__(self, colour, number):
        self.piece_id = colour[0] + 'KN' + str(number)
        super().__init__(colour)
        self.name = 'Knight'

        if self.colour == 'White':
            row = 7
            self.symbol = chr(9822)
        else:
            row = 0
            self.symbol = chr(9816)

        if number == 1:
            self.position = [row, 1]
        elif number == 2:
            self.position = [row, 6]

        self.type = 'KN'

    def get_moves(self, pieces):
        moves = []
        own_pieces = [piece.position for piece in pieces[self.colour].values()]

        # * find a more efficient way to do this *
        # eg [position[0], position[1]] + [1, 2] X [1, -1] where x is cartesian product
        move_set = [
            [self.position[0] + 1, self.position[1] + 2],
            [self.position[0] + 1, self.position[1] - 2],
            [self.position[0] - 1, self.position[1] + 2],
            [self.position[0] - 1, self.position[1] - 2],
            [self.position[0] + 2, self.position[1] + 1],
            [self.position[0] + 2, self.position[1] - 1],
            [self.position[0] - 2, self.position[1] + 1],
            [self.position[0] - 2, self.position[1] - 1]
        ]

        for move in move_set:
            if move not in own_pieces:
                moves.append(move)

        moves = self.get_possible_moves(moves)

        return moves


class Bishop(Piece):
    def __init__(self, colour, number):
        self.piece_id = colour[0] + 'BI' + str(number)
        super().__init__(colour)
        self.name = 'Bishop'

        if self.colour == 'White':
            row = 7
            self.symbol = chr(9821)
        else:
            row = 0
            self.symbol = chr(9815)

        if number == 1:
            self.position = [row, 2]
        elif number == 2:
            self.position = [row, 5]

        self.type = 'BI'

    def get_moves(self, pieces):
        moves = []
        if self.colour == 'White':
            opposing = 'Black'
        else:
            opposing = 'White'

        own_pieces = [piece.position for piece in pieces[self.colour].values()]
        opposing_pieces = [piece.position for piece in pieces[opposing].values()]

        # * definitely a cleaner way of achieving this *
        for i in range(1, 8):
            move = [self.position[0] + i, self.position[1] + i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] + i, self.position[1] - i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] - i, self.position[1] + i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        for i in range(1, 8):
            move = [self.position[0] - i, self.position[1] - i]
            if move in own_pieces:
                break
            elif move in opposing_pieces:
                moves.append(move)
                break
            else:
                moves.append(move)

        moves = self.get_possible_moves(moves)

        return moves


def print_board_state(board_state):
    # print('-----------------------------------')
    print('--|---|---|---|---|---|---|---|---|')
    for i, row in enumerate(board_state):
        print(abs(i - 8), '|', ' | '.join(row), '|')
        print('--|---|---|---|---|---|---|---|---|')
    # print('\t A \t\t B \t\t C \t\t D \t\t E \t\t F \t\t G \t\t H')
    print('  | A | B | C | D | E | F | G | H |')

    print('')


# function to convert between given input string and indices in the form [row, column]
def convert_coords(string):
    if len(string) != 2:
        return False
    column = string[0].upper()
    try:
        row = int(string[1])
    except ValueError:
        return False

    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    rows = [i for i in range(1, 9)]

    if column not in columns or row not in rows:
        return False

    for j, element in enumerate(columns):
        if column == element:
            column_i = j

    # rows are flipped due to the print statement, therefore need to return the compliment value
    # this leads to row_i = row - 1 - (len(rows) - 1), simplifies to below
    row_i = abs(row - len(rows))

    return [row_i, column_i]


# function to convert back from indices to chess notation. input is a list
def convert_indices(lst):
    # no need for validation as no user input
    # columns = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    converted_list = []

    for index_pair in lst:
        row = index_pair[0]
        column = index_pair[1]

        # need to flip the rows as it's printed in reverse.
        converted_row = abs(row - 8)
        converted_col = columns[column]

        converted_pair = str(converted_col) + str(converted_row)

        converted_list.append(converted_pair)

    return converted_list


# need a function that updates the board state whenever a position is changed
def update_board_state(pieces, board_state):
    # first, empty the board
    for i, row in enumerate(board_state):
        for j, col in enumerate(row):
            board_state[i][j] = ' '

    # update the board to reflect all new piece positions
    colours = ['White', 'Black']
    for colour in colours:
        for piece in pieces[colour].values():
            board_state[piece.position[0]][piece.position[1]] = piece.symbol # change to piece.symbol


# logic to get a piece given the coordinates of the piece
def get_piece(pieces, indices, colour):
    new_dict = pieces[colour]
    return next(name for name, value in new_dict.items() if value.position == indices)

# if __name__ == "__main__":
#     new_game()


def new_game():
    # initialise empty board
    board_state = [['    ' for i in range(8)] for i in range(8)]
    colours = ['White', 'Black']

    # initialize empty pieces dictionary
    pieces = {
        'White': {},
        'Black': {}
    }
    # {black: ..., white: ...}
    for colour in colours:
        # this isn't perfect but it works well
        pieces[colour][colour[0] + 'KNG'] = King(colour)
        pieces[colour][colour[0] + 'QUN'] = Queen(colour)

        for number in range(1, 3):
            pieces[colour][colour[0] + 'RK' + str(number)] = Rook(colour, number)
            pieces[colour][colour[0] + 'KN' + str(number)] = Knight(colour, number)
            pieces[colour][colour[0] + 'BI' + str(number)] = Bishop(colour, number)

        for number in range(1, 9):
            pieces[colour][colour[0] + 'PN' + str(number)] = Pawn(colour, number)

    update_board_state(pieces, board_state)
    print_board_state(board_state)

    # testing
    print(pieces)

    # initialise turn counter to 0
    turn = 0

    while True:
        # turn % 2 will cycle between 0 and 1, 'White' and 'Black'
        colour = colours[turn % 2]
        opposing = colours[(turn + 1) % 2]
        print(colour + '\'s turn.')

        # option to return to start of players turn
        while True:
            # ask for coordinates
            input_coordinates = input('Choose a piece to move: ')

            # check if coordinates are valid, and correspond to a piece that belongs to colour
            while not convert_coords(input_coordinates) in [piece.position for piece in pieces[colour].values()]:
                input_coordinates = input('Enter valid coordinates: ')

            # convert coordinates to indices
            input_indices = convert_coords(input_coordinates)

            print()

            # grab the piece from the input indices
            chosen_piece = get_piece(pieces, input_indices, colour)

            # ** find best place to implement this **
            piece = pieces[colour][chosen_piece]

            # testing
            # * change this to piece.type later *
            print('Chosen piece: ', piece.name)
            print('Available moves...')
            print(convert_indices(piece.get_moves(pieces)))
            print()

            # option here to go back and choose another piece.

            # check here if piece can be moved ('no valid moves..., enter r to return')
            # condition only met if list of moves is empty
            if not piece.get_moves(pieces):
                temp = ''
                while temp != 'r':
                    temp = input('No valid moves... press r to return')
                # if temp == 'r' then outer while loop will restart
                continue

            # while loop only broken through this break statement
            break
        # ** make sure only 1 piece can occupy each board position **

        # movements must be made on the selection of a piece
        target_coordinates = input('Enter coordinates to move your piece: ')
        # option to return to start of while loop
        if target_coordinates == 'r':
            continue
        # .get_moves() must return all VALID moves for the piece
        # later, must also add logic to prevent entering checkmate
        while not convert_coords(target_coordinates) in piece.get_moves(pieces):
            target_coordinates = input('Enter valid coordinates: ')

            # ** here, continue will only go to the beginning of the nested loop. **
            # option to return to start of while loop
            if target_coordinates == 'r':
                continue

        target_indices = convert_coords(target_coordinates)

        # logic for if a piece is being taken
        if target_indices in [piece.position for piece in pieces[opposing].values()]:
            # opposing_piece = board_state[target_indices[0]][target_indices[1]]
            opposing_piece = get_piece(pieces, target_indices, opposing)
            print('Taking piece: ', pieces[opposing][opposing_piece].name)
            # removes opposing piece from dictionary
            pieces[opposing].pop(opposing_piece)

        # finally, move the piece to the chosen index
        piece.move(target_indices)

        # logic for turning a pawn into a queen
        if piece.type == 'PN' and (piece.position[0] == 7 or piece.position[0] == 0):
            pieces[colour].pop(chosen_piece)
            print('New queen!')
            # add a new queen
            # turn variable added just to ensure key is unique! (not clean at all)
            pieces[colour][colour[0] + 'QN' + piece.piece_id[-1]] = Queen(piece.colour, piece.position, piece.piece_id)

        update_board_state(pieces, board_state)
        print_board_state(board_state)

        turn += 1

#
# if __name__ == "__main__":
#     new_game()
#
