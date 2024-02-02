# Pesudo code for tic tac toe game

## GLOBAL VARIABLES
field_size = 3
user_record = [[], []]
win_line = [[1,2,3],[4,5,6]]
## Functions
### INIT PLAYFIELD  INIT(tsize,  board=None)
- **INPU** size of playfield
- **OUTPUT** winline, ttt
### Display field = DISPLAY
- **INPUT** list LIST of all `X` and `O`s and the configuraitons (size)
- **OUTPUT** grid with `X`s and `O`s
def display(playfield, field_size):
    print xxx
| x | O |
|
### Validate input - VALIDATE
- **INPUT** current game field & the current input
- **WHILE NOT VALID**
   - **INPUT again** current game field & the current input
   - **VALIDATE** check is the field is already filled
      - if input value within [1,9]
      - if input value within occupied positions
- **UPDATE** the current LIST of `X` and `O`s
- **OUTPUT** update the list of `X` and `O` coordinates
def validate(playfield, field_size)
### UPDATE WINLINE - update_winline(ttt, winline):
- **MERGE USER SPOTS**
- **IF** one winline list exists within the merged list
  -- remove that from winline list
- **OUTPUT** updated winline
### Check status - CHECKSTATUS
- **INPUT** list of all `X` and `O`s and winline
- **IF** one winline list exits in user1 or 2 list
    - print winner X/O
    - print game stopped
    - **RETURN False**
- **ELSEIF LEN(winline) == 0**
    - print  NO WINNER and FINISHED**
    - print game stopped
    - **RETURN FALSE**
- **UPDATE winline**
- **OUTPUT** True (True is someone won OR 9 turns are exhausted)
## Main body
- **INIT** initialize playfield
- **DISPLAY** the empty gamefield
- **REPEAT** –
  - **INPUT** Take the X as the input
  - **DISPLAY** the updated field
  - **CHECKSTATUS** the status
- **UNTIL** CHECKSTATUS == True