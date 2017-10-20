#!/usr/bin/env python3

'''
vocab_test.py

main test logic

'''
### CONSTANTS ###
WRONG_ANSWERS = 4
MAX_SCORE = 10000
EASY_WRONG_PENALIZE = 1
HARD_WRONG_FAVOR = 0.685
#################

#### IMPORTS ####
from sys import argv
from ENGLISH import *
from leg import Leg
from random import randint, shuffle, choice
import string
from itertools import islice, chain
#################

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

class Choice:
    '''
    represents one choice
    '''
    def __init__(self, letter, word):
        self.letter = letter
        self.definition = word.definition

class Question:
    '''
    Question holds tuples: one correct word and some other incorrect definitions (which also have words attached to them)
    Attributes:
        word (Word): the question word
        choices (list of (Word, correct -> bool)): the choices and whether they are correct nor not
        
        
    '''
    def __init__(self, correct, *incorrect):
        '''
            correct: Word
            *incorrect: iterable of Word
        '''
        self.possibleletters = string.ascii_uppercase[0:WRONG_ANSWERS+1]
        self.query = correct.word
        self.responsemap = {c: i for i, c in enumerate(self.possibleletters)}
        self.choices = list( zip( (correct, *incorrect), (True, *([False]*WRONG_ANSWERS)) ) ) # keep track of the correct word by attaching a bool flag to the correct word
        shuffle(self.choices)
        # get the right answer
        for ii, cc in enumerate(self.choices):
            if(cc[1]):
                self.correct = ii
                break
        self.correct_word = self.choices[self.correct][0]
        self.score = correct.score
        self.response = None
        self.gotit = False
        
    def __repr__(self):
        choices = (" << %s >> " % (c) for c in self.choices)
        return "query: %s, score: %f, choices (%s)" % (self.query, self.score, choices)
    
    def __str__(self):
        question = self.prompt
        choices = ("\t%s. %s" % (l, c[0].definition) for l, c in zip(self.possibleletters, self.choices))
        correct = str(self.correct)
        return '\n'.join((question, *choices))

    def choicelist(self):
        '''
        individual choicelist for passing into a tpl
        '''
        return [c[0] for c in self.choices]

    def answer(self, response):
        response = response.upper()
        if response not in self.responsemap:
            return 0.0
        self.response = self.responsemap[response]
        self.gotit = self.response == self.correct
        return self.getscore()
        
    def getscore(self):
        return self.score if self.gotit else 0.0

def calculate_score(rawscore, testscore):
    '''
        10000   perfect
        9500    universe brain
        9000    word whiz
        8500    adult
        8000    16 yo
        7500    13 yo
        7000    11 yo
        6500    10 yo
        6000    9 yo
        5500    8 yo
        ...
        3000    toddler
        2000    baby
        1000    fetal
    '''
    return int(round((rawscore/testscore)**EASY_WRONG_PENALIZE * MAX_SCORE))

def makewords(lex, n, group='', rand=True):
    '''
    Word factory function from lex
    lex (list of str): lexical database stored as list
    n (int): number of words to generate
    group (str): group letter
    rand (bool): generate words randomly
    '''
    if rand:
        shuffle(lex)
    return [Word_fromrow(row, group) for row in islice(lex, 0, n)] 

def testgen(lex, leg, rand=True):
    '''
    generate questions from leg
    lex (list of str): lexical database stored as list
    leg (Leg): the leg to choose from
    rand (bool): generate the questions randomly
    '''
    lexsec = lex[leg.start:leg.stop]
    if rand:
        shuffle(lexsec)
    answers = [Word_fromrow(row, leg.group) for row in islice(lexsec, 0, leg.count)]
    remainder = lexsec[leg.count:]
    return [Question(answer, *makewords(remainder, WRONG_ANSWERS, leg.group, rand)) for answer in answers]

class Test:
    '''
    A Test contains Questions and keeps track of the user's score, and then presents them their final score. If rawscore == maxscore, that is a perfect score.

    Attributes:
        lex (list of str): filename of the lexical database
        legs (list of Leg):  the sections of the file based on difficulty
        questions (list of Question): the questions themselves
        current (int): the current question
        maxscore (float): the maximum test score
        userscore (float): the final user score
        rawscore (float): the user's current raw score
    '''
    def __init__(self, lexname, legs, debug=False):
        self.lex = []
        self.legs = legs
        self.finished = False
        self.questions = []
        self.current = 0      # current question
        self.maxscore = 0.0   # maximum test score
        self.userscore = 0.0  # the final user score
        self.rawscore = 0.0   # the user's raw score

        # generate the questions from lex

        with open(lexname, "r") as f:
            self.lex = list(f)
            self.questions = list(chain.from_iterable([testgen(self.lex, leg, not debug) for leg in self.legs]))

        # generate the individual user question scores and the max raw score for this test
        self.questionscores = [0.0 for i in range(len(self.questions))]
        self.maxscore = sum(q.correct_word.score for q in self.questions)
        self.totalquestions = len(self.questions)
    
    def show_words(self):
        return '\n'.join(str(q.correct_word) for q in self.questions)

    def show_words_with_scores(self):
        return '\n'.join(q.correct_word.__repr__() for q in self.questions)
    
    def show_curr_question(self, n=-1):
        if n == -1: n = self.current
        print("%s" % (self.questions[n].query))
    
    def get_curr_question(self):
        return self.questions[self.current]

    def next_question(self):
        self.current += 1
        if self.current >= self.totalquestions: 
            self.finished = True
    
    def prev_question(self):
        self.current -= 1
        self.finished = False
    
    def show_all_questions(self):
        for q in self.questions:
            print("%s\n-----" % (q))
    
    def answer_question(self, response):
        if not self.finished:
            self.questionscores[self.current] = self.questions[self.current].answer(response)
    
    def finish(self):
        self.rawscore = sum(self.questionscores)
        self.userscore = calculate_score(self.rawscore, self.maxscore)
        return self.userscore
    
# terminal interface test  
def terminal_test(test):
    print("how good are u at english vocab")
    for q in test.questions:
        test.show_curr_question()
        test.answer_question(input("whats ur answer: "))
        print("--------------")
    return test.finish()
    
if __name__ == "__main__":
    test = Test(LEX_EN, LEGS_EN)

    # generate a word list and store to the argument
    if len(argv) > 1:
        with open(argv[1], 'w') as fw:
            fw.write(test.show_words())
        with open(''.join((argv[1], "_scores.txt")), 'w') as fsc:
            fsc.write(test.show_words_with_scores())
    # execute a test
    else:
        print("You scored: %i" % terminal_test(test))
