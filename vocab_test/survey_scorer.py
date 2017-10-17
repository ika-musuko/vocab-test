#!/usr/bin/env python3

import wordpicker
from sys import argv
from ENGLISH import *
from vocab_test import calculate_score as cs

if __name__ == "__main__":
    # the following matrix of constants is the line numbers to grab from LEX. this is to account for the fact that the difficulty values in LEX are exponentially increasing
    # (start, stop, skip, group)
    
    lex = []
    words = []

    with open(argv[1], "r") as f:
        words = [row.split()[0] for row in f]
               
    with open(LEX_EN, "r") as lexf:
        for row in lexf:
            if(row.split("|")[0] in words):
                lex.append(wordpicker.Word_fromrow(row, 'SCORER'))
    
        
    rawscore = 0
    totalscore = sum(w.score for w in lex)
    
    with open(argv[1], "r") as f:
        for line, ww in zip(f, lex):
            if(line.split()[1] == 'y'):
                rawscore += ww.score
    
    #print("raw: %8s total: %8s" %(rawscore, totalscore), sep="")
    print(cs(rawscore, totalscore))