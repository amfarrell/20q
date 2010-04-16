from models import SurveyResult, SurveyResultLine
from csc.conceptnet4.models import *
from commons.app.json import PartialInference, fill_in_nums
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list

from twentyq.questioner import StatelessReconstructedMixtureModelQuestioner, OutOfQuestions, StatelessAnalogySpaceQuestioner
from twentyq.cnet_utils import NotCachedError
import string
import random
import time
from sys import maxint

# Ram cache for mixture models
mixture_model_cache = {}
# Guess a concept after obtaining the following amounts of knowledge
mm_guess_concept = set([12, 15, 18, 19, 20])
mm_question_limit = 20

activity = Activity.objects.get(name='20 Questions')

#goodframe_texts = [
#'{1} is {%}a kind of {2}.',
#'{1} is {%}used for {2}.',
#'{1} is {%}part of {2}.',
#'{1} is {%}created by {2}.',
#'{1} is {%}made of {2}.',
#'{1} {%}requires {2}.',
#'{1} wants {2}.',
#'You are {%}likely to find {1} in {2}.',
#'{1} would {%}make you want to {2}.',
#'One of the things you do when you {1} is {%}{2}.',
#'The effect of {1} is {%}{2}.',
#'You would {%}{1} because you want {2}',
#]
goodframe_ids = [1402, 1441, 1422, 1633, 1388, 1650, 16224, 5611, 1416, 1444,
1438, 1686]
goodframes = [Frame.objects.get(id=x) for x in goodframe_ids]

en = Language.get('en')
def make_question(relation, concept, slot):
    rel = RelationType.objects.get(name=relation)
    frame = rel.preferred_frame(en)
    concept = Concept.get_raw(concept, en)
    partial = PartialInference(en, rel, concept, slot)
    parts = partial.fill_in('it', question=True)
    return fill_in_nums(parts[1], parts[0], parts[2])

def respond_with(template, request, new_data):
    '''Respond to the request with the given template and data. Uses the data from
    _common_data as a base; new_data can override.'''
    template_data = RequestContext(request, new_data)
    return render_to_response(template, template_data)


def assertion_from_text_and_feature(text, feature, score, lang, user):
    partial = PartialInference.from_feature(lang=lang, feature=feature)
    left, frame, right, frame_id = partial.fill_in(text)
    frame = Frame.objects.get(id=frame_id)

    if score == 1: value = RatingValue.objects.get(id=2)
    elif score == -1: value = RatingValue.objects.get(id=5)
    else: raise ValueError("unexpected score: %d" % score)
    a = Assertion.from_frame(user, frame, left, right, activity,
    Batch.objects.get(id=157), value)
    return a

def assertion_from_text_and_frame(frame, text1, text2, lang, user):
    a = Assertion.from_frame(user, frame, text1, text2, activity, Batch.objects.get(id=157), RatingValue.objects.get(id=2))
    return a

def from_feature(featstring):
    parts = featstring.split('/')
    if parts[0][0] in string.uppercase:
        return (parts[0], parts[1], 1)
    else:
        return (parts[1], parts[0], 2)

def to_feature(relation, concept, slot):
    if slot == 1:
        return "%s/%s" % (relation, concept)
    else:
        return "%s/%s" % (concept, relation)

def reset(request, lang):
    request.session['answers'] = []
    return question(request, lang)

def cache(request, lang):
    global mixture_model_cache
    return HttpResponse(repr(mixture_model_cache))

def frame(request, lang, frame, slot):
    chosenframe = Frame.objects.get(id=frame)
    slot = int(slot)
    concept = request.session['concept']
    answer_list = request.session['statements']

    return respond_with('frame.html', request,
                            {'concept': concept,
                             'prev': answer_list,
                             'chosenframe': chosenframe,
                             'slot': slot})

class usertest_decorator(object):
    def __init__(self, username_prefix, password):
        self.username_prefix = username_prefix
        self.password = password

        from django.contrib.auth.models import Group
        self.group = Group.objects.get(name="UserTest")

    def __call__(self, func):
        def new_func(request, *a, **kw):
            if not request.user.is_authenticated():
                from django.db import IntegrityError
                success = False
                while not success:
                    try:
                        username = self.username_prefix + str(random.randint(0, maxint))
                        user = User.objects.create_user(username, '', self.password)
                        success = True
                    except IntegrityError:
                        pass

                from django.contrib.auth import authenticate, login
                user = authenticate(username=username, password=self.password)
                login(request, user)
                user.groups.add(self.group)
            return func(request, *a, **kw)
        return new_func

@login_required
def question(request, lang, model_components=5, model_iterations=100):
    ''' Displays a 20Q question'''
    if not 'answers' in request.session:
        request.session['answers'] = []
    answer_list = request.session['answers']

    if request.method == 'POST':
        ans = request.POST['answer']
        relation = request.POST['relation']
        concept = request.POST['concept']
        slot = int(request.POST['slot'])
        guess = bool(int(request.POST['guess']))

        # Special case: if we guessed a concept AND the answer was yes,
        # then the game is over.
        if guess and ans[0] == 'Y':
            return show_results(request, Concept.get_raw(concept, en).canonical_name, answer_list)

        answer_list.append( (relation, concept, slot, ans, guess) )


    yes_features = [to_feature(r, c, s) for (r, c, s, ans, g) in answer_list if ans[0] == 'Y']
    no_features = [to_feature(r, c, s) for (r, c, s, ans, g) in answer_list if
    ans[0] == 'N' or ans[0] == 'D']
    maybe_features = [to_feature(r, c, s) for (r, c, s, ans, g) in answer_list
    if ans[0] == 'M']+['IsA/way', 'UsedFor/sex', 'AtLocation/theatr',
    'AtLocation/home', 'human/AtLocation']

    prev_questions = [(make_question(r, c, s), ans, g, Concept.get_raw(c, en).canonical_name)
                      for (r, c, s, ans, g) in answer_list]

    global mixture_model_cache
    questioner = StatelessReconstructedMixtureModelQuestioner(min_observations=20,
                                                              model_components=model_components,
                                                              model_iterations=model_iterations,
                                                              recompute=False,
                                                              memcache=mixture_model_cache,
                                                              neg_weight_assertions= True,
                                                              beta_prior_probability=0.04,
                                                              beta_prior_weight=0.2)

    if model_components == 5: threshold=.5
    else: threshold=.8
    feature = questioner.get_question_stateless(yes_features, no_features,
    maybe_features, threshold=threshold)
    likelyrank = questioner.get_likely_concepts(20, yes_features, no_features, maybe_features)
    '''    try:
        feature = questioner.get_question_stateless(yes_features, no_features, maybe_features, threshold=.5)
        likelyrank = questioner.get_likely_concepts(20, yes_features, no_features, maybe_features)
    except NotCachedError, OutOfQuestions:
        # Fall back on AnalogySpace's ad-hoc categories
        questioner = StatelessAnalogySpaceQuestioner([], recompute=False, memcache=mixture_model_cache)
        feature = questioner.get_question_stateless(yes_features, no_features, maybe_features)
        likelyrank = questioner.get_likely_concepts(20, yes_features, no_features, maybe_features)'''
    relation, concept, slot = from_feature(feature)
    likely = [Concept.get_raw(x[0], en).canonical_name for x in likelyrank[:10]]
    quest = make_question(relation, concept, slot)
    canonical_concept = Concept.get_raw(concept, en).canonical_name

    aspace_questioner = StatelessAnalogySpaceQuestioner([], recompute=False, memcache=mixture_model_cache)
    aspace_rank = aspace_questioner.get_likely_concepts(20, yes_features, no_features, maybe_features)

    guess = 0
    global mm_guess_concept, mm_question_limit
    if len(yes_features) + len(no_features) in mm_guess_concept:
        # Start guessing concepts
        guess = 1
        relation = 'IsA'
        previous_guesses = set([c for (r, c, s, ans, g) in answer_list if g])
        concept = [c[0] for c in likelyrank if c[0] not in previous_guesses][0]
        canonical_concept = Concept.get_raw(concept, en).canonical_name
        slot = 1

    give_up = False
    if len(yes_features) + len(no_features) > mm_question_limit:
        give_up = True

    return respond_with('question.html', request,
                        {'guess' : guess,
                         'question': quest,
                         'relation': relation,
                         'concept': concept,
                         'canonical_concept' : canonical_concept,
                         'slot': slot,
                         'prev': prev_questions,
                         'likely': likely,
                         'guess_frame' : 'Is it ',
                         'give_up' : give_up})

get_new_question = question

@login_required
def tellme(request, lang):
    feature_list = request.session['answers']
    text = request.POST['text']
    return show_results(request, text, feature_list)

def show_results(request, text, feature_list):
    results = []
    for r, c, s, answer, g in feature_list:
        feature = to_feature(r, c, s)
        if answer[0] == 'Y':
            a = assertion_from_text_and_feature(text, feature, 1, en,
            request.user)
        elif answer[0] == 'N':
            a = assertion_from_text_and_feature(text, feature, -1, en,
            request.user)
        else: continue
#        a.save()
        if a.score > 0:
            results.append(a)

    return respond_with('survey.html', request,
                        {'added': results})
