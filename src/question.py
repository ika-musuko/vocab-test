from bottle import Bottle, route, run, debug, template, get, post
from vocab_test import Test
from functools import partial
from ENGLISH import *

def get_question(test):
    question = test.get_curr_question()
    clist = question.choicelist()
    params = {
        "number"    : test.current+1,
        "total"     : test.totalquestions,
        "query"     : question.query,
        "letters"   : question.possibleletters,
        "choices"   : clist
    }
    output = template("question", **params)
    return output
test = Test(LEX_EN, LEGS_EN)
show_question = partial(get_question, test=test)
route("/test", ['GET'], show_question)
run(host="localhost", port=8080, debug=True)

