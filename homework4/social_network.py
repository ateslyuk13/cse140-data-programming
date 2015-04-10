# Name: Hongjoo Lee
# CSE 140
# Homework 4

import networkx as nx
import matplotlib.pyplot as plt
import operator
import random


###
### Problem 1a
###

practice_graph = nx.Graph()

practice_graph.add_node("A")
practice_graph.add_node("B")
practice_graph.add_node("C")
practice_graph.add_node("D")
practice_graph.add_node("E")
practice_graph.add_node("F")

practice_graph.add_edge("A", "B")
practice_graph.add_edge("A", "C")
practice_graph.add_edge("B", "C")
practice_graph.add_edge("B", "D")
practice_graph.add_edge("C", "D")
practice_graph.add_edge("C", "F")
practice_graph.add_edge("D", "E")
practice_graph.add_edge("D", "F")

assert len(practice_graph.nodes()) == 6
assert len(practice_graph.edges()) == 8

def draw_practice_graph():
    """Draw practice_graph to the screen."""
    nx.draw_networkx(practice_graph)
    plt.show()

# Comment out this line after you have visually verified your practice graph.
# Otherwise, the picture will pop up every time that you run your program.
draw_practice_graph()


###
### Problem 1b
###

nodes = ['Nurse', 'Juliet', 'Tybalt', 'Capulet', 'Friar Laurence', 'Romeo', 'Benvolio', 'Montague', 'Escalus', 'Mercutio', 'Paris']

rj = nx.Graph()
rj.add_nodes_from(nodes)
rj.add_edge('Nurse', 'Juliet')
rj.add_edge('Juliet', 'Tybalt')
rj.add_edge('Juliet', 'Capulet')
rj.add_edge('Juliet', 'Friar Laurence')
rj.add_edge('Juliet', 'Romeo')
rj.add_edge('Tybalt', 'Capulet')
rj.add_edge('Capulet', 'Escalus')
rj.add_edge('Capulet', 'Paris')
rj.add_edge('Romeo', 'Friar Laurence')
rj.add_edge('Romeo', 'Benvolio')
rj.add_edge('Romeo', 'Montague')
rj.add_edge('Romeo', 'Mercutio')
rj.add_edge('Montague', 'Benvolio')
rj.add_edge('Montague', 'Escalus')
rj.add_edge('Escalus', 'Mercutio')
rj.add_edge('Escalus', 'Paris')
rj.add_edge('Paris', 'Mercutio')

assert len(rj.nodes()) == 11
assert len(rj.edges()) == 17

def draw_rj():
    """Draw the rj graph to the screen and to a file."""
    nx.draw_networkx(rj)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()

# Comment out this line after you have visually verified your rj graph and
# created your PDF file.
# Otherwise, the picture will pop up every time that you run your program.
draw_rj()


###
### Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    The parameter 'user' is the string name of a person in the graph.
    """
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Returns a set of friends of friends of the given user, in the given graph.
    The result does not include the given user nor any of that user's friends.
    """
    return {friend_of_friend for friend in friends(graph, user) for friend_of_friend in friends(graph, friend)} - friends(graph, user) - set([user])

assert friends_of_friends(rj, "Mercutio") == set(['Benvolio', 'Capulet', 'Friar Laurence', 'Juliet', 'Montague'])


def common_friends(graph, user1, user2):
    """Returns the set of friends that user1 and user2 have in common."""
    return friends(graph, user1) & friends(graph, user2)

assert common_friends(practice_graph,"A", "B") == set(['C'])
assert common_friends(practice_graph,"A", "D") == set(['B', 'C'])
assert common_friends(practice_graph,"A", "E") == set([])
assert common_friends(practice_graph,"A", "F") == set(['C'])

assert common_friends(rj, "Mercutio", "Nurse") == set()
assert common_friends(rj, "Mercutio", "Romeo") == set()
assert common_friends(rj, "Mercutio", "Juliet") == set(["Romeo"])
assert common_friends(rj, "Mercutio", "Capulet") == set(["Escalus", "Paris"])


def number_of_common_friends_map(graph, user):
    """Returns a map from each user U to the number of friends U has in common with the given user.
    The map keys are the users who have at least one friend in common with the
    given user, and are neither the given user nor one of the given user's friends.
    Take a graph G for example:
        - A and B have two friends in common
        - A and C have one friend in common
        - A and D have one friend in common
        - A and E have no friends in common
        - A is friends with D
    number_of_common_friends_map(G, "A")  =>   { 'B':2, 'C':1 }
    """
    candidates = {node for node in graph.nodes()} - friends(graph, user) - set([user])
    return {friend : len(common_friends(graph, user, friend)) for friend in candidates if 0 != len(common_friends(graph, user, friend))} 


assert number_of_common_friends_map(practice_graph, "A") == {'D': 2, 'F': 1}

assert number_of_common_friends_map(rj, "Mercutio") == { 'Benvolio': 1, 'Capulet': 2, 'Friar Laurence': 1, 'Juliet': 1, 'Montague': 2 }


def number_map_to_sorted_list(map):
    """Given a map whose values are numbers, return a list of the keys.
    The keys are sorted by the number they map to, from greatest to least.
    When two keys map to the same number, the keys are sorted by their
    natural sort order, from least to greatest."""
    from itertools import chain, groupby
    sorted_tuples = sorted(map.items(), key=lambda x:x[1], reverse=True)
    result = chain(
        *(sorted( (k for k,v in items) ) for k, items in groupby(sorted_tuples, key=lambda x:x[1]))
    )
    return list(result)

assert number_map_to_sorted_list({"a":5, "b":2, "c":7, "d":5, "e":5}) == ['c', 'a', 'd', 'e', 'b']


def recommend_by_number_of_common_friends(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the number of common friends.
    """
    map = number_of_common_friends_map(graph, user)
    return number_map_to_sorted_list(map)


assert recommend_by_number_of_common_friends(practice_graph,"A") == ['D', 'F']

assert recommend_by_number_of_common_friends(rj, "Mercutio") == ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


###
### Problem 3
###

def influence_map(graph, user):
    """Returns a map from each user U to the friend influence, with respect to the given user.
    The map only contains users who have at least one friend in common with U,
    and are neither U nor one of U's friends.
    See the assignment for the definition of friend influence.
    """
    from itertools import groupby
    number_of_friends = lambda x:len(friends(graph, x))
    # find people to recommend having common friends
    map = number_of_common_friends_map(graph, user)
    # list tuple of the people and their weight calculated by number of friends that the friend in common has
    result = ((k,1./number_of_friends(cf)) for k in map.iterkeys() for cf in common_friends(graph, k, user))
    # sum up the weights for each recommender
    result = {k: sum(weight for k, weight in items) for k, items in groupby(result, key=lambda x:x[0])}
    return result

assert influence_map(rj, "Mercutio") == { 'Benvolio': 0.2, 'Capulet': 0.5833333333333333, 'Friar Laurence': 0.2, 'Juliet': 0.2, 'Montague': 0.45 }


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the influence measurement.
    """
    map = influence_map(graph, user)
    return number_map_to_sorted_list(map)

assert recommend_by_influence(rj, "Mercutio") == ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


###
### Problem 4
###



###
### Problem 5
###

# (There is no code to write for this problem.)


###
### Problem 6
###

# (There is no code to write for this problem.)


###
### Problem 7
###


###
### Problem 8
###

# (Your code goes here.)

assert len(facebook.nodes()) == 63731
assert len(facebook.edges()) == 817090


###
### Problem 9
###


###
### Problem 10
###


###
### Problem 11
###


###
### Problem 12
###
