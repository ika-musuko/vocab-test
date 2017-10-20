#!/usr/bin/env python3

'''
ENGLISH.py
constants for english word database
'''

from leg import Leg

ZBOUND, ZCOUNT = 1500,   2     
ABOUND, ACOUNT = 35000,  3 
BBOUND, BCOUNT = 36500,  3  
CBOUND, CCOUNT = None,   2
LEX_EN = "../resources/lexwords/lex_filter_2.txt"

LEGS_EN = (
            Leg(0,        ZBOUND,   ZCOUNT, "Z"),   # group Z
            Leg(ZBOUND,   ABOUND,   ACOUNT, "A"),   # group A
            Leg(ABOUND,   BBOUND,   BCOUNT, "B"),   # group B
            Leg(BBOUND,   CBOUND,   CCOUNT, "C")    # group C
)
