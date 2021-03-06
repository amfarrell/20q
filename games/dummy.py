# This is a dummy python file for getting the next question.

import random
import pdb
from csc.conceptnet.models import Concept, Relation

LANG = 'en'

import pdb
#pdb.set_trace()
DUMMIES = [(Relation.get("HasProperty"), Concept.get("fuzzy", LANG), True),
           (Relation.get("HasProperty"), Concept.get("shiny", LANG), True),
           (Relation.get("Causes"), Concept.get("weariness", LANG), True),
           (Relation.get("UsedFor"), Concept.get("battle", LANG), True),
           (Relation.get("IsA"), Concept.get("frog", LANG), True)]

DefaultQuestionBlob = (Relation.get("CausesDesire"), Concept.get("eat cake", LANG), True)
 
           
VALID = [True, False]

def get_question(state): # state is a dictionary of features to truth values
    next = DUMMIES[int(random.random() * len(DUMMIES))]
    if not next in state:
        return next
    else:
        return DEFAULT
