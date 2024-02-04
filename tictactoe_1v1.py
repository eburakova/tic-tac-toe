def init_field(field_size_n=3, users_history=None):
    """ Initialize tic-tac-toe play field
    Args:
        field_size_n (int): for a general play field nxn
        users_history (list): list of two user position history: 
              [[usr1_pos1, usr2_pos2, usr1_pos3], [usr2_pos1, usr2_pos2]]]. 
              Defaults to None.
    """
    field_pos_label = list(range(1, 1+field_size_n**2))
    if users_history == None:
        users_history = [[], []]
    else:
        ## check consistence
        if len(users_history[0]) != len(set(users_history[0])) \
           or len(users_history[1]) != len(set(users_history[1])):
            raise ValueError("init_field(): <users_history> duplicates")
        if len(set(sum(users_history,[])) - set(field_pos_label)) > 0:
            raise ValueError("init_field(): <users_history> out of val range")
        if len(users_history[0]) < len(users_history[1]) or \
           len(users_history[0]) > len(users_history[1]) + 1:
            raise ValueError("init_field(): <users_history> wrong lengths")
    ## lines on play field for winning
    win_lines = []
    tmp = list(range(field_size_n))
    for i in range(field_size_n):
        win_lines.append({1+x+i*field_size_n for x in tmp})
        win_lines.append({1+x*field_size_n+i for x in tmp})
    win_lines.append({1+x*field_size_n+x for x in tmp})
    win_lines.append({(1+x)*field_size_n-x for x in tmp})
    return users_history, win_lines


def display(field_size_n, position_list):
    """ Box-drawing of tic-tac-toe play field
    Args:
        field_size_n (int): for a general play field nxn, with n < 32, 
              i.e. sqrt(999), since each text box reserved only for 3 digits.
        position_list (list): a list of position numbers within [1, n**2], or
              a list of two position lists of user-1/2 history
    """
    if field_size_n >=32:
        raise ValueError("display(): <field_size_n> >= 32, as 32**2 > 999.")
    if isinstance(position_list[0], list):
        tmp = sum(list(position_list),[])
    else:
        tmp = list(position_list)
    if len(tmp) > 0 and ( min(tmp) < 1 or max(tmp) > field_size_n**2 ):
        raise ValueError("display(): <position_list> out of range: [1,n**2]")
                                             ## case of user-1/2 lists
    if isinstance(position_list[0], list):  
        show_list = [str(i) for i in list(range(1, 1+field_size_n**2))]
        for y in position_list[0]:
            show_list[y-1] = 'X'
        for y in position_list[1]:
            show_list[y-1] = 'O'
    else:                                    ## case of single list
        if len(position_list) == field_size_n**2:  ## ready to show
            show_list = position_list
        else:                                ## fill incomplete list
            show_list = [' '] * field_size_n**2
            for y in position_list:
                show_list[y-1] = str(y)
    boxdraw = ["┌---" + "┬---" * (field_size_n - 1) + "┐"]
    for i in range(field_size_n):
        row = show_list[i*field_size_n:(i+1)*field_size_n]
        for j in range(field_size_n,-1,-1):
            rspace = 1
            lspace = 1
            if j == field_size_n or len(row[j]) > 2:
                rspace = 0
            if j == 0 or len(row[j-1]) > 1:
                lspace = 0
            row.insert(j, ' '*lspace + '│' + ' '*rspace)
        boxdraw.append(''.join(row))
        boxdraw.append("├---" + "┼---" * (field_size_n - 1) + "┤")
    boxdraw[-1] = "└---" + "┴---" * (field_size_n - 1) + "┘"
    for line in boxdraw:
        print(line.replace('X','\033[1mX\033[0;0m')\
                  .replace('O','\033[1mO\033[0;0m'))  # with bold font
    return boxdraw
    

def update_winline(win_lines, users_history):
    """ Update <win_lines>
    Purpose: to reduce unnecessary searching space of winning conditions
    """
    for i in range(len(win_lines)-1, -1, -1):
        if len(win_lines[i].intersection(set(users_history[0]))) > 0 and \
           len(win_lines[i].intersection(set(users_history[1]))) > 0:
            win_lines.pop(i)
    return win_lines


def check_status(win_lines, users_history):
    """ Check status of play field, see if game is over
    Args:
        win_lines (list of list): collection of winning conditions
        users_history (list of two lists): input recorded for user-1/2
    """
    win = 0
    for w in win_lines:
        if len(w - set(users_history[0])) == 0:
            print('User-1 (X) won the game, congratulations!')
            win += 1
        if len(w - set(users_history[1])) == 0:
            print('User-2 (O) won the game, congratulations!')
            win += 1
    if win == 1:
        return False
    elif win == 2:
        raise ValueError('check_status(): <win> = 2, somewhere is wrong :(')
    win_lines = update_winline(win_lines, users_history)
    if len(win_lines) == 0:
        print('No one can win the game any more!\nThe game is over.')
        return False
    return True



if __name__ == '__main__':

    print('**********************')
    print('*  Tic Tac Toe game  *')
    print('**********************')

 ## initialize a game   
    field_size_n = 3                   ## by default
    p = input('Please input a number for size of the playfield [3]: ')
    while len(p) > 0 and (not p.isdigit() or int(p) < 3):
        p = input('  > not a number or too small (<3). try again [3]: ')
    if len(p) > 0:
        field_size_n = int(p)
    users_history = None               ## by default
    p = input('Do you want continue an unfinished game? (y/n) [n]: ')
    if p.lower() == 'y' or p.lower() == 'yes':
        print('  > please input history of two users in list form below:')
        print('    [[usr1_pos1, usr1_pos2, ...], [usr2_pos1]]:')
        p = input('    ')
        chk_input = True
        while chk_input:
            try:
                exec('users_history = ' + p)
            except:
                print('  > not valid expression, try again:')
                p = input('    ')
                continue
            if not isinstance(users_history, list):
                print('  > not a list, try again:')
                p = input('    ')
            elif len(users_history) != 2 or \
                 not isinstance(users_history[0], list) or \
                 not isinstance(users_history[1], list):
                print('  > not a list of two lists, try again:')
                p = input('    ')
            elif len(set(sum(users_history[0:2],[])) \
                     - set(range(1, field_size_n**2+1))) > 0:
                print(f'  > not int or out of [1,{field_size_n**2}], ' \
                      + 'try again:')
                p = input('    ')
            elif len(sum(users_history,[])) > len(set(sum(users_history,[]))):
                print(f'  > duplicate position numbers, try again')
                p = input('    ')
            else:
                chk_input = False
#    users_history = [[2,7],[5,4]]    ## test example
    users_record, win_line = init_field(field_size_n, users_history)

## display generated winning conditions
#    print(f'Here list all {len(win_line)} winning conditions for ' \
#          + f'{field_size_n} x {field_size_n} game:')
#    for wl in win_line:
#        display(field_size_n, list(wl))

    display(field_size_n, users_record)
    available_pos_label = list(set(range(1, field_size_n**2+1)) \
                               - set(users_record[0])         \
                               - set(users_record[1]))

    while check_status(win_line, users_record):
        if len(users_record[0]) == len(users_record[1]):
            print('User-1 (X):')
            print('  %% `a` - available positions')
            print('  %% `d` - draw game status')
            print('  %% `q` - quit')
            p = input(f'  > please input position [1-{field_size_n**2}]: ')
            while not p.isdigit() or (int(p) not in available_pos_label):
                 if p == 'a':
                      print(f'  available positions: {available_pos_label}')
                      p = input('  > input your position choice: ')
                 elif p == 'd':
                      display(field_size_n, users_record)
                      p = input(f'  > input position [1-{field_size_n**2}]: ')
                 elif p == 'q':
                      print('Quit game now.')
                      exit(0)
                 else:
                     p = input(f'  > invalid, try again [1-{field_size_n**2}]: ')
            users_record[0].append(int(p))
        elif len(users_record[0]) == 1 + len(users_record[1]):
            print('User-2 (O):')
            print('  %% `a` - available positions')
            print('  %% `d` - draw game status')
            print('  %% `q` - quit')
            p = input(f'  > please input position [1-{field_size_n**2}]: ')
            while not p.isdigit() or int(p) not in available_pos_label:
                 if p == 'a':
                      print(f'  available positions: {available_pos_label}')
                      p = input('  > input your position choice: ')
                 elif p == 'd':
                      display(field_size_n, users_record)
                      p = input(f'  > input position [1-{field_size_n**2}]: ')
                 elif p == 'q':
                      print('Quit game now.')
                      exit(0)
                 else:
                     p = input(f'  > invalid, try again [1-{field_size_n**2}]: ')
            users_record[1].append(int(p))
        else:
            raise ValueError('main(): something wrong with <users_record> :()')
        available_pos_label.remove(int(p))
        print(users_record)

        display(field_size_n, users_record)
    print('')