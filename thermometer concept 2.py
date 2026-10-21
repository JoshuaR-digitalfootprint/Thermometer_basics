# project
import random
import numpy as np
import math

def temp_input():
    """
    some method to retreive an array of temperatures, figure out something smarter later
    """
    # Array of 10 random floats between 1.0 and 100.0
    random_temp_array = [random.uniform(1, 100) for _ in range(10)]
    
    return random_temp_array

def temp_analyser(random_temp_array):
    """
    Inputs: 
        random_temp_array:
            an array containing float values
    Outputs:
        
    """
    t_max = np.max(random_temp_array)
    t_min = np.min(random_temp_array)
    t_last = random_temp_array[-1] #last element in array (duh)
    
    return t_max, t_min, t_last

def zero_fixer(x, sf=4):
    """
    Format x to `sf` significant figures, to keep pesky trailing zeros.
    e.g. 26.9   -> '26.90'
    """
    if x == 0:
        return '0.' + '0' * (sf - 1)
    int_digits = int(math.floor(math.log10(abs(x)))) + 1
    dp = max(sf - int_digits, 0)
    return f'{x:.{dp}f}'

def visual_character(ch, dot_pos=None):
    """
    Render one character as a 3-line list of strings.
    ch      : a key in DIGITS ('0'..'9' or '.')
    dot_pos : optional (row, col) to stamp a dot onto the digit's grid

    """
    # Each digit is a 3x3 list of strings (row, col).
    DIGITS = {
        '0': [" _ ",
              "| |",
              "|_|"],
        '1': ["   ",
              "  |",
              "  |"],
        '2': [" _ ",
              " _|",
              "|_ "],
        '3': [" _ ",
              " _|",
              " _|"],
        '4': ["   ",
              "|_|",
              "  |"],
        '5': [" _ ",
              "|_ ",
              " _|"],
        '6': [" _ ",
              "|_ ",
              "|_|"],
        '7': [" _ ",
              "  |",
              "  |"],
        '8': [" _ ",
              "|_|",
              "|_|"],
        '9': [" _ ",
              "|_|",
              " _|"],
        '.': ["   ",
              "   ",
              "  ."],
    }
    if ch not in DIGITS:
        return ["   ", "   ", "   "]
    grid = DIGITS[ch]
    if dot_pos is not None:
        grid = place_dot(grid, *dot_pos)
    return grid


def place_dot(grid, row=2, col=2):
    """
    Return a new 3x3 grid with '.' stamped at (row, col).
    Row is expected to change most of the time
    """
    g = [list(r) for r in grid]
    g[row][col] = '.'
    return [''.join(r) for r in g]

def visual_string(value, sf=4):
    """
    Render a number (or string) as 3 lines of 7-segment-style text.
    value : number or string
    sf    : significant figures if value is a number
    """
    if isinstance(value, (int, float)):
        s = f'{value:.{sf}g}'
    else:
        s = str(value)

    rows = ['', '', '']
    for ch in s:
        g = visual_character(ch)
        rows[0] += g[0]
        rows[1] += g[1]
        rows[2] += g[2]
    return '\n'.join(rows)




def presenter(compound_t):
    """
    Make a display on something like 8, 
    compount_t is np.array containing: 
        (t_max, t_min, t_last)
    """
    t_max, t_min, t_last = compound_t     # unpack, don't index [1][2][3]

    vis_t_max  = visual_string(t_max)
    vis_t_min  = visual_string(t_min)
    vis_t_last = visual_string(t_last)

    return vis_t_max, vis_t_min, vis_t_last




    

def main():
    """
    main body of logic
    """
    random_temp_array = temp_input()
    
    t_max, t_min, t_last = temp_analyser(random_temp_array)
    
    t_max  = zero_fixer(t_max,  4)
    t_min  = zero_fixer(t_min,  4)
    t_last = zero_fixer(t_last, 4)
    #now put to 4sf cause... well maybe display limits
    #t_max.4g for print
    # t_max = round(t_max, 4)   # 4dp example
    
    # t_max = float(f'{t_max}') #4sf i think
    # t_min = float(f'{t_min}')
    # t_last = float(f'{t_last}')
    
    compound_t = np.array([t_max, t_min, t_last])
    
    vis_t_max, vis_t_min, vis_t_last = presenter(compound_t)
    
    print(f'Maximum temperature: {t_max}')#remember variable in curly bracket
    print(f'Minimum temperature: {t_min}')
    print(f'Previous temperature: {t_last}')
    
    print(vis_t_max)
    print(vis_t_min)
    print(vis_t_last)
    
    
    
    
    return 0

if __name__ == "__main__":
    main()