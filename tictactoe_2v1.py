def set_symbols():
    default = ['\033[1mX\033[0;0m', '\033[1mO\033[0;0m'] # bold X and O as default
    for i in range(2): # 2 players
        while len(symbols[i]) > 1: 
            symbols[i] = input(f'Player {i+1}: enter your symbol (default: \033[1m{symbols[i]}\033[0;0m): ')
            if len(symbols[i]) > 1:
                print('Please, only enter a single symbol')
                break
            if not symbols[i]: # if the string is empty
                print('Setting to default')
                symbols[i] = default[i] 
                break

def build_empty_field(field_size):
    """Initialize the play field - visual only
      Parameters: 
      - field_size - the globally defined size of the field"""
    row_up = "╔═══" + "════" * (field_size - 2) + "════╗" + "\n" 
    row_inter = "╠═══" + "╬═══" * (field_size - 2) + "╬═══╣" + "\n"
    row_bott = "╚═══" + "════" * (field_size - 2) + "════╝"
    numbers = [str(n).center(3, ' ') for n in range(1, field_size**2+1)]
    numbers = [numbers[i*field_size:(i+1)*field_size] for i in range(field_size)]
    rows_w_numbers = [['║'+number for number in row] for row in numbers]
    rows_w_numbers = [''.join(row)+'║\n' for row in rows_w_numbers] 

    field = row_up 
    for row_w_numbers in rows_w_numbers:
        field += row_w_numbers
        field += row_inter
    field = field.removesuffix(row_inter) # removing the last one
    field += row_bott
    return field

def convert_positions(n, field_size):
    """Converts cell numbers into the indicies of the 
    elements in the `field` string to change.

    The string will be split into rows and reassembled. The row 
    where the number goes to should be split into the list of 
    individual symbols. 
    Parameters: 
    - n: user input (the cell number)
    - field_size (str) - globally defined field size"""
    
    row =  (n-1) // (field_size) # 0 based
    col = (n-1) % (field_size)  # 0 based
    return(row, col)

def insert_symbol_into_field(field, symbol, row, col):
    _ = field.splitlines()
    new_row = _[row*2+1].split('║')
    new_row[col+1]  = f' {symbol}'
    new_row = '║'.join(new_row)
    _[row*2+1] = new_row
    # print('\n'.join(_))
    field = '\n'.join(_)
    return field

def write_field(field, turn_history):
    """Populates the field (string) with the 
    Xs and Os from the turn record. 
    This function is responsible for graphics only!
    
    Parameters:
    - field (str) - the field 
    - turn_history - the turn log 
    """
    for pos_X in turn_history[0]:
        row, col = convert_positions(pos_X, field_size)
        field = insert_symbol_into_field(field, symbolX, row, col)
    # turn history of "O"s is shorter by one every second turn, 
    # hence can not use `zip`
    for pos_O in turn_history[1]:
        row, col = convert_positions(pos_O, field_size)
        field = insert_symbol_into_field(field, symbolO, row, col)
    return field

def init_field(field_size_n, user_history=None):
    """ Initialize the play field - logic only

    Parameters:
        field_size_n (int): a general play field nxn
        user_history (list): list of two user position history:
              [[usr1_pos1, usr2_pos2, usr1_pos3], [usr2_pos1, usr2_pos2]]].
              Defaults to None.
    Returns: 
        - win_line - all possible win conditions
        - available_pos_label - list of available positions
    """
    field_size = field_size_n
    field_pos_label = list(range(1, 1+field_size**2))
    if user_history == None:
        user_record = [[], []]
        available_pos_label = field_pos_label
    else:
        user_record = user_history
        ## check consistence
        if len(user_record[0]) != len(set(user_record[0])):
               print("warning: duplicate turns of Xs")
               user_record[0] = set(user_record[0]) # warning: the history is reshuffled
        if len(user_record[1]) != len(set(user_record[1])):
               print("warning: duplicate turns of Os")
               user_record[1] = set(user_record[1]) # warning: the history is reshuffled
        available_pos_label = list(set(field_pos_label)
                                   - set(user_record[0])
                                   - set(user_record[1]))
    win_line = []
    tmp = list(range(field_size))
    for i in range(field_size):
        win_line.append([1+x+i*field_size for x in tmp])
        win_line.append([1+x*field_size+i for x in tmp])
    win_line.append([1+x*field_size+x for x in tmp])
    win_line.append([(1+x)*field_size-x for x in tmp])
    # return user_record, win_line, available_pos_label
    return win_line, available_pos_label

def make_turn():
    """Takes a cell number as an input, validates it 
    and removes the newly occupied cell from the available position list
    Note: Modifies global variables hence does not return anything. 
    """
    turn_valid = False
    while not turn_valid:
        if whose_turn_is_it:
        # means it is the first player's turn
            try:
                turn = int(input(
                "Player 1 (X): Choose a cell and enter its number: "))
            except ValueError:
                continue
            if isinstance(turn, int) and turn in available_pos_label:
                 user_record[0].append(turn)
                 available_pos_label.remove(turn)
                 turn_valid = True
        else:
        # means it is the second player's turn
            try:
                turn = int(input(
                "Player 2 (O): Choose a cell and enter its number: "))
            except ValueError:
                continue
            if isinstance(turn, int) and turn in available_pos_label:
                 user_record[1].append(turn)
                 available_pos_label.remove(turn)
                 turn_valid = True

def is_game_over():
    """Checks the win and tie conditions
    Returns True is the game is over
    """
    for condition in win_line:
        if set(condition).issubset(set(user_record[0])):
            print(f'🐍🐍 {symbolX} has won! 🐍🐍')
            return True
        elif set(condition).issubset(set(user_record[1])):
            print(f'🐍🐍 {symbolO} has won! 🐍🐍')
            return True
    if len(available_pos_label) == 0:
        print('There are no more free cells! It is a tie!')
        return True
    else:
        return False

if __name__ == "__main__":
    
    print('This is a game of Tic-Tac-Toe')
    symbols = ['XX', 'OO']
    field_size = int(input('Chose field size (1-31): '))   # NxN
    user_record = [[], []]       # list of lists with the turn record
    win_line = []                # list of lists, win conditions that are still possible
    field_pos_label = []         # position label for whole play field
    available_pos_label = []     # position label for empty spot
    game_over = False            # flag for the end of the game
    symbols = ['X ', 'O ']

    ## initialization of the field
    field = build_empty_field(field_size)
    win_line, available_pos_label = init_field(field_size, user_record)

    # setting symbols for each player
    symbolX = 'XX' # placeholder
    while len(symbolX) > 1 or symbolX == 'X':
        symbolX = input('Player 1: enter your symbol (default: \033[1mX\033[0;0m): ')
        if not symbolX: # if the string is empty
            print('Setting to default')
            symbolX = '\033[1mX\033[0;0m' # bold X for player 1 as default
            break
    
    symbolO = 'O ' # placeholder
    while len(symbolO) > 1 or symbolO == 'O':
        symbolO = input('Player 2: enter your symbol (default: \033[1mO\033[0;0m):')
        if not symbolO: # if the string is empty
            print('Setting to default')
            symbolO = '\033[1mO\033[0;0m' # bold X for player 1 as default
            break

    # game starts
    while not game_over:
        print(field)
        if len(user_record[0]) == len(user_record[1]):
            whose_turn_is_it = 1
        else:
            whose_turn_is_it = 0
        make_turn()
        field = write_field(field, user_record)
        game_over = is_game_over()
    
    print(field)    
    print('Thanks for playing!')
