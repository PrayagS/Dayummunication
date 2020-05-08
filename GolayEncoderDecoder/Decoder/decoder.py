#!/bin/python3

import numpy as np


def make_extended_Golay_B():
    """
    returns B matrix for the extended Golay code
    """
    B = [[1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]]
    for _ in range(10):
        next_line = B[-1][:]
        next_line = next_line + [next_line.pop(0)]
        B.append(next_line)
    j = [[1]*11]
    B = np.concatenate((np.array(B), np.array(j)))
    j_0 = [[1]]*11 + [[0]]
    B = np.concatenate((B, np.array(j_0)), axis=1)
    return B


B = np.array([[1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
              [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
              [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
              [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
              [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
              [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
              [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
              [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
              [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
              [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])


H = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
              [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
              [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
              [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
              [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
              [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
              [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
              [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
              [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
              [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])


def find_weight(word):
    """
    input is bit vector
    output is Hamming weight
    """
    i = 0
    for letter in word:
        if letter != 0:
            i += 1
    return i


def decode_extended_Golay(word):
    if type(word) == str:
        word = [int(i) for i in word]

    global B
    global H

    s = list(word @ H % 2)
    if find_weight(s) <= 3:
        u = s + [0]*12
        # print(''.join(str(x) for x in u))
        sent_word = []
        for k in range(24):
            sent_word.append((word[k] + u[k]) % 2)
        # return ''.join(str(x) for x in sent_word[:12])
        return sent_word[:12]
    for i, row in enumerate(B):
        if find_weight([sum(z) % 2 for z in zip(s, list(row))]) <= 2:
            for j, value in enumerate(row):
                s[j] = (s[j] + value) % 2
            e_i = [0]*12
            e_i[i] = 1
            u = s + e_i
            # print(''.join(str(x) for x in u))
            sent_word = []
            for k in range(24):
                sent_word.append((word[k] + u[k]) % 2)
            # return ''.join(str(x) for x in sent_word[:12])
            return sent_word[:12]
    s = list(s @ B % 2)
    if find_weight(s) <= 3:
        u = [0]*12 + s
        # print(''.join(str(x) for x in u))
        sent_word = []
        for k in range(24):
            sent_word.append((word[k] + u[k]) % 2)
        # return ''.join(str(x) for x in sent_word[:12])
        return sent_word[:12]
    for i, row in enumerate(B):
        if find_weight([sum(z) % 2 for z in zip(s, list(row))]) <= 2:
            for j, value in enumerate(row):
                s[j] = (s[j] + value) % 2
            e_i = [0]*12
            e_i[i] = 1
            u = e_i + s
            # print(''.join(str(x) for x in u))
            sent_word = []
            for k in range(24):
                sent_word.append((word[k] + u[k]) % 2)
            # return ''.join(str(x) for x in sent_word[:12])
            return sent_word[:12]
    return 'request retransmission'

def decode_Golay(word):
    if type(word) == str:
        word = [int(i) for i in word]

    if find_weight(word) % 2 == 0:
        word += [1]
    else:
        word += [0]

    c = decode_extended_Golay(word)
    return ''.join(str(x) for x in c)
