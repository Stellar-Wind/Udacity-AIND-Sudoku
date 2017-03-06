# Dear code reviewer:
# Is there a more compact way to write the if statement code on line 38?
# if box != naked_twin_1 and box != naked_twin_2 and (exclusion_value_0 in values[box] or exclusion_value_1 in values[box]):


from utils import *



def naked_twins(values):
#     """Eliminate values using the naked twins strategy.
#     Args:
#         values(dict): a dictionary of the form {'box_name': '123456789', ...}

#     Returns:
#         the values dictionary with the naked twins eliminated from peers.
#     """

    for box in boxes:
        if len(values[box]) == 2:
            for peer in peers[box]:
                if values[peer] == values[box] and peer != box:
                    naked_twin_1 = box
                    naked_twin_2 = peer
                    print("\n")
                    print ("naked twins in boxes",naked_twin_1,"and",naked_twin_2)
                    # print(values[box])
                    # print(peers[box])
                    # print(box,values[box],values[peer])
                    for unit in unitlist:
                        if naked_twin_1 in unit and naked_twin_2 in unit:
                            exclusion_value_0 = values[naked_twin_1][0] # could also be values[naked_twin_2][0]
                            exclusion_value_1 = values[naked_twin_2][1] # could also be values[naked_twin_1][1]
                            print('unit',unit)
                            print("exclusion_values",exclusion_value_0,",",exclusion_value_1)  
                            for box in unit:
                                # if the box is not either of the naked twins, and contains either of the exclusion values...
                                if box != naked_twin_1 and box != naked_twin_2 and (exclusion_value_0 in values[box] or exclusion_value_1 in values[box]):
                                    # then remove the exclusion values from said box:
                                    print("BEFORE box = " + box, "value=" + values[box])
                                    values[box] = values[box].replace(exclusion_value_0, "")
                                    values[box] = values[box].replace(exclusion_value_1, "")
                                    print("AFTER box = " + box, "value=" + values[box])

    display(values)
    return values

def only_choice(values):
    """Eliminate values using the 'only choice' strategy."""
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """Eliminate values iteratively using all strategies."""
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Eliminate values by searching the game tree."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)


    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = reduce_puzzle(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
