import random

def make_random_move(position):
    empty_cells = [i for i, cell in enumerate(position) if cell == " "]
    if empty_cells:
        return random.choice(empty_cells)
    else:
        return None
