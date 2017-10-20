from bottle import Bottle, route, run, debug, template, get, post, request
from vocab_test import Test
from functools import partial
from ENGLISH import *

### pages ###
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
    output = template("question.tpl", **params)
    return output

def get_results(test):
    test.finish()
    params = {
        "score"     : test.userscore
    }
    output = template("results.tpl", **params)
    return output

def submit_response(test):
    formdata = request.forms.get('answer')
    print("#######FORMDATA#########")
    print(formdata)
    print("#######END FORMDATA#######")
    test.answer_question(formdata)
    test.next_question()
    
    return get_results(test) if test.finished else get_question(test)

### load routes ###
pages = {
    "/test"     : (get_question, ['GET']),
    "/respond"  : (submit_response, ['POST']),
    "/results"  : (get_results, ['GET'])
}
def load_routes(pages, test):
    for p in pages:
        f = partial(pages[p][0], test=test)
        route(p, pages[p][1], f)

test = Test(LEX_EN, LEGS_EN)
show_question = partial(get_question, test=test)
load_routes(pages, test)
run(host="localhost", port=8080, debug=True)

