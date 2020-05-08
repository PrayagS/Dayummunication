#!/bin/python3

import numpy as np


def number_to_binary_array(n, r):
    """
    input integer
    output binary representation of integer as values in an array that can hold numbers less than 2^r
    """
    res = [int(i) for i in bin(n)[2:]]
    while len(res) < r:
        res = [0] + res
    return res


def make_identity_matrix(n):
    """
    input n
    output list of lists, identity matrix I_n
    """
    return [number_to_binary_array(2**i, n) for i in reversed(range(n))]


def make_extended_Golay_generator():
    """
    returns the generator for the extended Golay code
    """
    B = [[1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]]
    for _ in range(10):
        next_line = B[-1][:]
        next_line = next_line + [next_line.pop(0)]
        B.append(next_line)
    j = [[1]*11]
    G_extended = np.concatenate((np.array(B), np.array(j)))
    j_0 = [[1]]*11 + [[0]]
    G_extended = np.concatenate((np.array(G_extended), np.array(j_0)), axis=1)
    Id_12 = make_identity_matrix(12)
    G_extended = np.concatenate((Id_12, np.array(G_extended)), axis=1)
    return G_extended


G_extended = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
                       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
                       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
                       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])

G = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])


def encode_extended_Golay(info):
    global G_extended

    if type(info) == str:
        info = [int(i) for i in info]
        res = info @ G_extended % 2
        return ''.join(str(i) for i in res)

    if type(info) == list:
        return list(info @ G_extended % 2)

    if type(info) == np.ndarray:
        return info @ G_extended % 2

def encode_Golay(info):
    global G

    if type(info) == str:
        info = [int(i) for i in info]
        res = info @ G % 2
        return ''.join(str(i) for i in res)

    if type(info) == list:
        return list(info @ G % 2)

    if type(info) == np.ndarray:
        return info @ G % 2
