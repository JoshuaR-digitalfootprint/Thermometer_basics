# project
import random
import numpy as np
import math
from time import sleep

def temp_input():
    """
    some method to retreive an array of temperatures, figure out something smarter later
    """
    # Array of 10 random floats between 1.0 and 100.0
    random_temp_array = [random.uniform(-10, 10) for _ in range(10)]
    
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
        '-': ["   ",
              " _ ",
              "   "],
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


def fit_4_cells(value, width=4):
    """
    Truncates to 4 cells long

    """
    if isinstance(value, str): #Is obj an instance of classinfo? Returns True or False.
        s = value 
        
    else:
        for dp in range(6, -1, -1): #dp (decimal places) starts at 6 and shrinks
            s = f'{value:.{dp}f}'
            if s.startswith('0.'):
                s = s[1:]
            elif s.startswith('-0.'):
                s = '-' + s[2:]
            if len(s) <= width:
                break
        else:
            s = f'{value:.0f}'


    if len(s) > width:
        s = s[:width]
    return s.rjust(width)

def colour_crystal(random_temp_array):
    """
    Walk the array in order; return a list of (index, temp, colour) tuples.
    
    Note: in real cold chain any above certain temp (say 8) illegal,
    Just keep this in mind

    Rule:
      - while temp >= limit  -> 'red'
      - after temp <  limit, stay 'red' for `cooldown` indices,
        then flip to 'blue'.

    The "distance" from an above-limit reading to the current reading
    is just (current_index - last_hot_index), since each index is 1 time unit.
    """
    SAFE_MAX = 8.0
    unit_retreival = 60     # 1 array index = like 60 s  (just to name it; unused for now)
    reset = 183 #say 183s
    cooldown = math.ceil(reset/unit_retreival)
    last_hot_index = None          # index of most recent >= limit reading

    for i, t in enumerate(random_temp_array):
        if t >= SAFE_MAX:
            colour = 'red'
            last_hot_index = i
        else:
            # temp is below the limit — is the cooldown still running?
            if last_hot_index is None:
                colour = 'blue'                # never been hot
            else:
                elapsed = i - last_hot_index   # distance in array = time units
                colour = 'red' if elapsed < cooldown else 'blue'
    return colour
    
def interactive(colour):
    """
    Ask whether the current colour is safe.
    Input 'n' (any case) -> binned.
    """
    print("so that colour, is it safe?")
    answer = input("(y/n): ").strip().lower()
    
    chance = random.randint(1,6)
    if answer == 'n':
        print("binned")
        if colour == 'blue':
            if chance >= 3:
                print("U got fired")
            else:
                print("Coworker looks at you funny")         
        else:
            return
    else:
        print("shipped")
        if colour == 'red':
            if chance == [3,4,5]:
                print("U got fired")
            elif chance == 6:
                print("you read the news...")
                sleep(5)
                print() #or print("\n") # TWO newlines — string is "\n", then print adds one
                print("Breaking news!")
                sleep(2)
                print()
                print("Mr man found **** after eating [insert brand]")
            else:
                print("Coworker looks at you funny")  
    return
    

def temp():
    """
    main logic to compile other functions
    """
    random_temp_array = temp_input()

    t_max, t_min, t_last = temp_analyser(random_temp_array)

    # display: 4 sf, then clamp to 4 cells (minus and '.' each count as 1)
    t_max_s  = fit_4_cells(zero_fixer(t_max,  4))
    t_min_s  = fit_4_cells(zero_fixer(t_min,  4))
    t_last_s = fit_4_cells(zero_fixer(t_last, 4))

    vis_t_max  = visual_string(t_max_s)
    vis_t_min  = visual_string(t_min_s)
    vis_t_last = visual_string(t_last_s)

    print(f'Maximum temperature: {zero_fixer(t_max,  4)}')
    print(f'Minimum temperature: {zero_fixer(t_min,  4)}')
    print(f'Previous temperature: {zero_fixer(t_last, 4)}')

    print(vis_t_max)
    print(vis_t_min)
    print(vis_t_last)
    colour = colour_crystal(random_temp_array)
    print(colour)
    interactive(colour) #blue safe to ship, red not safe to ship
    
    #unfinished logic for reset to blue but still unsafe but thats future me problem
    
    
def main():
    temp()

if __name__ == "__main__":
    main()