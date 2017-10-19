#!/usr/bin/env python3

'''
ENGLISH.py
constants for english word database
'''

from leg import Leg

ZBOUND, ZCOUNT = 1500,   5     
ABOUND, ACOUNT = 35000,  8 
BBOUND, BCOUNT = 36500,  4  
CBOUND, CCOUNT = None,   3
LEX_EN = "../resources/lexwords/lex_filter_2.txt"

LEGS_EN = (
            Leg(0,        ZBOUND,   ZCOUNT, "Z"),   # group Z
            Leg(ZBOUND,   ABOUND,   ACOUNT, "A"),   # group A
            Leg(ABOUND,   BBOUND,   BCOUNT, "B"),   # group B
            Leg(BBOUND,   CBOUND,   CCOUNT, "C")    # group C
)
