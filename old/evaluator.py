from csc.conceptnet.models import Concept, Assertion
import views as v
import cPickle as pickle

questioner = v.StatelessReconstructedMixtureModelQuestioner(min_observations=20,
                                                            model_components=5,
                                                            model_iterations=100,
                                                            recompute=False,
                                                            memcache=v.mixture_model_cache)
aspace_questioner = v.StatelessAnalogySpaceQuestioner([], recompute=False, memcache=v.mixture_model_cache)

try:
    feature_cache = pickle.load(open('feature_cache'))
except:
    feature_cache = {}

def add_to_feature_cache(concept, feature, response):
    feature_cache[concept, feature] = response
    pickle.dump(feature_cache, open('feature_cache', 'wb'))

lim = 40

en = v.en

a = Assertion.objects.filter(language=en)

def does_concept_have_feature(concept, feature):
    relation, other, slot = v.from_feature(feature)
    if slot == 1:
        c1, c2 = concept, other
    else:
        c1, c2 = other, concept
    c1_obj = Concept.get_raw(c1, 'en')
    c2_obj = Concept.get_raw(c2, 'en')
    data = list(a.filter(concept1=c1_obj, relation__name=relation, concept2=c2_obj))
    if len(data) > 0:
        return data[0].score > 0

    if (concept, feature) not in feature_cache:
        ans = raw_input('%s %s? ' % (concept, feature))
        res = dict(y=True, n=False, m=None)[ans[0].lower()]
        add_to_feature_cache(concept, feature, res)
    return feature_cache[concept, feature]


def run_eval(concept):
    normalized_concept = Concept.get(concept, en).text
    yes = []
    no = []
    maybe = []
    n = 0
    while n < lim:
        n += 1
        feature = questioner.get_question_stateless(yes, no, maybe, threshold=.5)
        response = does_concept_have_feature(concept, feature)
        print '%s%s' % ({True: '+', False: '-', None: '?'}[response], feature)
        if response is True: yes.append(feature)
        elif response is False: no.append(feature)
        else: maybe.append(feature)

        if n % 5 == 0:
            # Make a guess
            #print yes, no, maybe
            concepts_weighted = aspace_questioner.get_likely_concepts(5, yes, no, maybe)
            concepts = [c[0] for c in concepts_weighted]
            print concepts
            if normalized_concept in concepts:
                print 'Got it in', n
                return n

    return False
