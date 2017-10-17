#!/usr/bin/env python3

'''
vocab_test.py

main test logic

'''
WRONG_ANSWERS = 4
MAX_SCORE = 10000
EASY_WRONG_PENALIZE = 1

import wordpicker
from ENGLISH import *
from random import randint, shuffle
import string

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
        self.choices = list( zip( (correct, *incorrect), (True, *([False]*WRONG_ANSWERS)) ) ) # keep track of the correct word by attaching a bool flag to the correct word
        shuffle(self.choices)
        # get the right answer
        for ii, cc in enumerate(self.choices):
            if(cc[1]):
                self.correct = ii
                break
        
        self.score = correct.score
        self.response = None
        self.gotit = False
        
    def __repr__(self):
        choices = (" << %s >> " % (c) for c in self.choices)
        return "query: %s, score: %f, choices (%s)" % (self.query, self.score, choices)
    
    def __str__(self):
        question = "Choose the closest description for the word %s." % self.query
        choices = ("\t%s. %s" % (l, c[0].definition) for l, c in zip(self.possibleletters, self.choices))
        correct = str(self.correct)
        return '\n'.join((question, correct, *choices))
        
    def answer(self, response):
        responsemap = {c: i for i, c in enumerate(self.possibleletters)}
        self.response = responsemap[response.upper()]
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
        
class Test:
    '''
    A Test contains Questions and keeps track of the user's score, and then presents them their final score
    '''
    def __init__(self, lex, legs, debug=False):
        self.lex = lex
        self.legs = legs
        self.wordpicker = wordpicker.WordPicker(lex, legs, test=debug)
        self.questions = []
        self.current = 0
        self.testscore = self.wordpicker.testscore
        self.userscore = 0
        self.rawscore = 0
        for group in self.wordpicker:
            for word in self.wordpicker.fsecs[group]:
                mw = wordpicker.makewords_fromsec(self.wordpicker.lexsecs[group], WRONG_ANSWERS, group).words
                self.questions.append(Question(word, *mw))
        
        self.questionscores = [0.0 for i in range(len(self.questions))]
        
    def show_curr_question(self, n=-1):
        if n == -1: n = self.current
        print("%i. %s" % (n+1, self.questions[n]))
    
    def next_question(self):
        self.current += 1
    
    def prev_question(self):
        self.current -= 1
    
    def show_all_questions(self):
        for q in self.questions:
            print("%s\n-----" % (q))
    
    def answer_question(self, response):
        self.questionscores[self.current] = self.questions[self.current].answer(response)
        self.next_question()
    
    def finish(self):
        self.rawscore = sum(self.questionscores)
        self.userscore = calculate_score(self.rawscore, self.testscore)
        return self.userscore
    
    
# terminal interface test  
def terminal_test(test):
    print("how good are u at english vocab")
    for q in test.questions:
        test.show_curr_question()
        test.answer_question(input("whats ur answer: "))
        print("")
    return test.finish()
    
if __name__ == "__main__":
    test = Test(LEX_EN, LEGS_EN)
    print("You scored: %i" % terminal_test(test))