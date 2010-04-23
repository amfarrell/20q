from twentyq.games.models import Game
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from dummy import get_question, DefaultQuestionBlob
#from django.template.loader import get_template
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse
debug = True
if debug:
    import pdb



def first(request):
    return render_to_response("./testing.html", 
            {'foo':'socks','tasty':
                ['cucumbers','hummus','Irish baby back ribs'] })
    
def acceptAnswer(request):
    """
    Takes the answer from the user, saves it in the state, gets a new
    question and renders that.
    """
    if debug:
        assert request.POST
    state = request.session['state']
    answerBlob = dehumanize(request.POST['userAnswer'],request.session['unanswered_question'])
    request.session['state'].append(answerBlob)
    new_questionBlob = get_question(state)
    if debug:
        assert type(new_questionBlob) is tuple
        assert len(new_questionBlob) == 3
        assert str(new_questionBlob[0].__class__) == "<class 'csc.conceptnet.models.Relation'>"
        assert str(new_questionBlob[1].__class__) == "<class 'csc.conceptnet.models.Concept'>"
        assert type(new_questionBlob[2]) is bool
    questionString = humanize(new_questionBlob) 
    request.session['unanswered_question'] = new_questionBlob
    return HttpResponse(questionString)

def dehumanize(answerString,questionBlob):
    """
    turn a response from a user into a boolean
    """
    return (questionBlob,answerString in ('true','True','1','yes',True))

def humanize(questionBlob):
    """
    A questionBlob is a tuple of the form (Relation,Concept,bool)
    the bool indicates the order of the relation and concept.
    examples:
    (HasProperty,Fuzzy,True) represents 
    "Does it have the property fuzzy?"
    while 
    (HasProperty,Fuzzy,False) represents
    "Does fuzzy have it as a property?

    This function just produces that natural language representation.
    this could be improved alot.
    """
    if questionBlob[2] :
        return "does it %s to %s?" %\
    (str(questionBlob[0]),str(questionBlob[1].text))
    else:
        return "does %s %s to it?" %\
    (str(questionBlob[0]),str(questionBlob[1].text))

def postQuestion(request, questionString=None):
    if questionString is None:
        request.session['state'] = []
        questionString = humanize(DefaultQuestionBlob)
        request.session['unanswered_question'] = DefaultQuestionBlob
    return render_to_response('hackedupIO.html',{'questionString' : questionString})
    
