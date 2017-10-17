#!/usr/bin/env python3

'''
wordpicker.py
    
    pick words from a lexical database
    The database must be in the following format
    
        word|difficulty|definition
        word|difficulty|definition
        word|difficulty|definition
        ...
    
'''

from sys import argv, stdout
from itertools import islice
from ENGLISH import *
import random

HARD_WRONG_FAVOR = 0.685

class Word:
    '''
    Word represents a single word with its difficulty and score.
    
    Attributes:
        word (str): the string containing the word itself
        diff (float): the difficulty of the word
        score (float): the score of the word, which is calculated from the diff (lower difficulty means a higher score, to reflect the fact that knowing the common, everyday words in a language is more beneficial than more obscure words)
        group (str): word "group". this is more intended for debugging purposes to indicate when this word was generated 
            - (english: Z=easy, A=regular, B=hard, C=rare)
            - (japanese: todo)
    
    '''
    def __init__(self, word, diff, definition, group=""):
        self.word = word
        self.diff = diff
        self.score = (1/(self.diff))**HARD_WRONG_FAVOR
        self.group = group
        self.definition = definition.strip()

    
    def __repr__(self):
        return "%s|%s|%s|%s|GROUP:%s" % (self.word, self.diff, self.score, self.definition,self.group)
        #return self.word
    
    def __str__(self):
        return self.word

def Word_fromrow(row, group=''):
    rr = row.split('|')
    return Word(rr[0], float(rr[1]), rr[2], group=group)    

class MakeWord:
    def __init__(self, words, lexsec):
        self.words = words
        self.lexsec = lexsec

def makewords(lex, n, start, stop, group):
    '''
    generate a list of Word from a leg without repeats
    lex (list containing lexical database): 
    n (int): how many words to generate
    start, stop (int): bounds of leg to grab from
    group (str): group label
    '''
    lexsec = lex[start:stop]
    words = []
    for c in range(n):
        i = random.randint(0, len(lexsec)-1)
        words.append(Word_fromrow(lexsec.pop(i),group))
    return MakeWord(words, lexsec)

def makewords_fromsec(lexsec, n, group):
    '''
    generate a list of Word from a section without repeats
    lex (list containing lexical database): 
    n (int): how many words to generate
    start, stop (int): bounds of leg to grab from
    group (str): group label
    '''
    return makewords(lexsec, n, 0, len(lexsec), group)
    
class WordPicker:
    '''
    WordPicker will choose a set of words from a word database. 
        
    where word is a str and difficulty is a float
    
    Attributes: 
        testscore (float): maximum raw score of selected words
        words (list of Word): the list of Words that have been chosen.
        legs (tuple of (start -> int, stop -> int, step -> int, group -> string)) the difficulty distribution groups
    '''
    def __init__(self, lex, legs, test=False):
        self.testscore = 0
        self.words = []
        self.legs = legs
        self.fsecs = {} # words grouped by group as specified by legs
        self.lexsecs = {} # lexical database sections with already used words deleted
        listgen = self.const_listgen if test else self.rand_listgen
        with open(lex,"r") as f:
            self.lex = list(f)
            for group in self.legs:
                listgen(self.lex, group, *self.legs[group])
    
    def __iter__(self):
        return iter(self.fsecs)
    
    def const_listgen(self, f, group, start, stop, step):
        '''
        use const_listgen only for testing purposes. the step size for grabbing words will be constant and the same list will be generated every time with the same parameters
        '''
        lexsec = f[start:stop:step]
        self.fsecs[group] = []
        for i, row in enumerate(lexsec):
            addthis = Word_fromrow(row, group)
            self.add_word(addthis)
            lexsec.pop(i)
            self.fsecs[group].append(addthis)
            
        self.lexsecs[group] = lexsec
    
    def add_word(self, word):
        self.testscore += word.score
        self.words.append(word)
    
    def rand_listgen(self, f, group, start, stop, step):
        '''
        this is the production run generator that generates a more randomized list, but still keeping in mind the difficulty distribution (self.legs)
        '''
        if start is None: start = 0
        if stop is None: stop = len(f)
        n = (stop-start)//step+1
        mw = makewords(f, n, start, stop, group)
        for w in mw.words:
            self.add_word(w)
        self.fsecs[group] = mw.words
        self.lexsecs[group] = mw.lexsec
           
    
    def edit_word(self, fsec, group):
        '''
        generate a new word in fsec at group (this would be used for changing erroneous questions)
        '''
        i = random.randint(0, len(fsec)-1)
        self.testscore -= self.words[index].score
        newword = Word_fromrow(fsec.pop(i), group)
        self.words[index] = newword
        self.testscore += newword.score
        
    
    def write(self, f=stdout, showscores=False):
        '''
        write to output. set showscores=True to also show the difficulty and scores of each word
        '''
        for w in self.words:
            if showscores:
                f.write("%r\n" % w)
            else:
                f.write("%s\n" % w)
                
    def __repr__(self):
        return '''
        ------------->>>WORDPICKER<<------------
        score: {}
        <<<<<<LEGS>>>>>>
        {}
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@WORDS@@@@@@@@@@@@@@@@@@@@@@@@@@
        {}
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@FSECS@@@@@@@@@@@@@@@@@@@@@@@@@@
        {}
        '''.format(self.testscore, self.legs, self.words, self.fsecs)
 
 
### main for testing WordPicker and generating sample word lists ###
if __name__ == "__main__":
    
    fn = "testlist_.txt" if len(argv) < 2 else argv[1]
    # the following matrix of constants is the line numbers to grab from LEX. this is to account for the fact that the difficulty values in LEX are exponentially increasing
    # (start, stop, skip, group)
    
    wp = WordPicker(LEX_EN, LEGS_EN, test="--test" in argv)
    print(wp)
    print(wp.testscore)
    with open(fn, "w") as fw, open(fn+"_scores.txt", "w") as fsc:
        wp.write(f=fw)
        wp.write(f=fsc, showscores=True)