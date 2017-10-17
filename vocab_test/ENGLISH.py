#!/usr/bin/env python3

'''
ENGLISH.py
constants for english word database
'''
ZBOUND, ZSTEP = 1500,   115
ABOUND, ASTEP = 35000,  2000
BBOUND, BSTEP = 36500,  160
CBOUND, CSTEP = None,   70
LEX_EN = "lexwords/lex_filter.txt"
LEGS_EN= {
            "Z":  (0,         ZBOUND,   ZSTEP),   # group Z
            "A":  (ZBOUND+1,  ABOUND,   ASTEP),   # group A
            "B":  (ABOUND+1,  BBOUND,   BSTEP),   # group B
            "C":  (BBOUND+1,  CBOUND,   CSTEP)    # group C
}
