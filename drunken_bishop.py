#!/usr/bin/env python


CHARS = ' .o+=*BOX@%&#/^SE'

def draw_board(arr):
    w = 17
    h = 9

    print('+' + ('-'*w) + '+')
    for i in range(h):
        print('|', end='')
        for j in range(w):
            print(arr[i][j], end='')
        
        print('|')

    print('+' + ('-'*w) + '+')


def create_arr():
    w = 17
    h = 9

    arr = [list() for i in range(h)]
    for i in range(h):
        arr[i] = [' ' for j in range(w)]

    return arr


def insert_vals(vals, arr):
    arr = arr.copy()
    counts = {}

    for idx,val in enumerate(vals):
        y = val[0]
        x = val[1]

        # Set the Starting char
        if idx == 0:
            arr[y][x] = CHARS[15]
            continue

        # Set the Ending char
        if idx == len(vals) - 1:
            arr[y][x] = CHARS[16]
            continue
        
        if (y,x) in counts:
            counts[(y,x)] += 1
        else:
            counts[(y,x)] = 1

        arr[y][x] = CHARS[counts[(y,x)] % (len(CHARS)-2)]

    return arr


def walk(inp):
    path = [(4,8)]

    if ':' in inp:
        inp = inp.replace(':', '')

    for i in range(0, len(inp), 2):
        hex_pair = inp[i:i+2]
        bit_pairs = hex_to_bits(hex_pair)[::-1]

        for bits in bit_pairs:
            last = path[len(path)-1]
            move = step(bits, last)
            path.append(move)

    return path


def hex_to_bits(val):
    bits = bin(int(val, 16))[2:].zfill(8)
    return [bits[i:i+2] for i in range(0,8,2)]


def step(bits, last):
    moves = {
        '00': (-1,-1),
        '01': (-1,1),
        '10': (1,-1),
        '11': (1,1)
    }

    dirn = moves[bits]
    y = last[0] + dirn[0]
    x = last[1] + dirn[1]

    # Slide along the walls
    # TODO fix
    x = max(x, 0)
    x = min(x, 16)
    y = max(y, 0)
    y = min(y, 8)
    
    return (y,x)


if __name__ == '__main__':
    hex_str = 'd4:33:fd:c5:64:d3:ee:9e:97:ca:54:21:3b:e4:ba:e9'
    steps = walk(hex_str)
    arr = insert_vals(steps, create_arr())

    print(hex_str)
    draw_board(arr)
