# A dictionary of movie critics and their ratings of a small set of movies
from collections import defaultdict

critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5,
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
    },
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0},
}


def sim_distance(prefs, person1, person2):
    """
    Calcualate the similarity distance between two persons
    :param prefs:
    :param person1:
    :param person2:
    :return:
    """
    si = defaultdict()

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)


if __name__ == '__main__':
    score = sum(critics['Lisa Rose'][it] for it in critics['Lisa Rose'])
    sum_square = sum([pow(critics['Lisa Rose'][it], 2) for it in critics['Lisa Rose']])
    pSum = sum([critics['Lisa Rose'][it] * critics['Mick LaSalle'][it] for it in critics['Lisa Rose']])
    print(pSum)


def get_recommendations(prefs, person, similarity=sim_distance):
    """
    :param prefs:
    :param person:
    :param similarity:
    :return:
    """
    totals = defaultdict()
    sim_sums = defaultdict()

    for other in prefs:

        if other == person: continue

        sim = similarity(prefs, person, other)

        if sim <= 0: continue

        for item in prefs[other]:

            if item not in prefs[person] or prefs[person][item] == 0:
                totals[item] += prefs[other][item] * sim
                sim_sums[item] += sim

    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()

    return rankings