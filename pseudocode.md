* **INPUT**: indicates a user will be inputting something
* **OUTPUT**: indicates that an output will appear on the screen
* **WHILE**: a loop (iteration that has a condition at the beginning)
* **FOR**: a counting loop (iteration)
* **REPEAT – UNTIL**: a loop (iteration) that has a condition at the end
* **IF – THEN – ELSE**: a decision (selection) in which a choice is made
* any instructions that occur inside a selection or iteration are usually indented

# Planning

## Functions

### Display field = DISPLAY
- **INPUT** list LIST of all `X` and `O`s and the configuraitons (size)
- **OUTPUT** grid with `X`s and `O`s

### Validate input - VALIDATE
- **INPUT** current game field & the current input
- **VALIDATE** check is the field is already filled
- **OUTPUT** update the list of `X` and `O` coordinates

### Check status - CHECKSTATUS
- **INPUT** list of all `X` and `O`s and the configuraitons (size)
- **COUNT** the number of turns
- **OUTPUT** True is someone won OR 9 turns are exhausted

## Main body

- **DISPLAY** the empty gamefield
- **REPEAT – UNTIL**
    - **INPUT** Take the X as the input
    - **VALIDATE**
    - **UPDATE** the current LIST of `X` and `O`s
    - **DISPLAY** the updated field
    - **CHECKSTATUS** the status
- **UNTIL** CHECK == True
- **OUTPUT** Print who won
