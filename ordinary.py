from reversi import *
from math import sqrt, log
import numpy as np
import copy


visits = set()  # where all of the nodes are stored
plays = []  # list of plays that are actually chosen


class Node():
    """
    A class to represent a node
    ...
    Attributes
        myBoard : list
            Reversi board with 'X' and 'O' tiles
        myTile : char
            X or O, max or min player
        a : list
            previous action that leads to current node
            contains x and y values of tile placement
        r : float
            the reward accumulated from simulated games
        t : int
            mount of times the node has been visited. 
            initialized to 0
        c : list<Node>
            list of children from existing node + action. 
            initialized to an empty list.
    """

    def __init__(self, myBoard, myTile, a):
        """Constructor for neccesarry attributes for the node object

        Args:
            myBoard (list): reversi board with 'X' and 'O' tiles
            myTile (char): X or O, max or min player
            a (list): previous action that leads to current node. x and 
                    y values of tile placement
        """
        self.myBoard = myBoard
        self.myTile = myTile
        self.a = a
        self.r = 0
        self.t = 0
        self.children = []


def UCT(x):
    """
    Expansion, Simulation, and Backpropogation phase of MCTS
        Parameter:
            x: node
        Returns:
            v (int): value for given node. Either 1 or 0 depending on terminal state
            a (list): associated action from node
    """
    if x not in visits:
        visits.add(x)
    if getValidMoves(x.myBoard, x.myTile) == []:     # terminal node
        tile2 = 'X' if x.myTile == 'O' else 'O'
        v = 1 if getScoreOfBoard(x.myBoard)[x.myTile] > getScoreOfBoard(x.myBoard)[
            tile2] else 0
        a = x.a
    else:
        y, a = UCBchoose(x)  # chooses an explore/exploit child node
        # from chosen child node run UCT recursively until term. node
        v, a2 = UCT(y)
    # backpropogate the reward/times up to the root
    x.r = (x.r*x.t + v)/(x.t + 1)
    x.t = x.t + 1
    return v, a


def generateChildren(x):
    """
    Generates the children (groundbreaking) given the parent node
        Parameter: 
            x (Node): node object
        Returns:
            nothing. The children are added to the node
    """
    if (len(x.children) == 0):
        newTile = 'X' if x.myTile == 'O' else 'O'
        for a in getValidMoves(x.myBoard, x.myTile):
            newBoard = getBoardCopy(x.myBoard)
            makeMove(newBoard, x.myTile, a[0], a[1])
            x.children.append(Node(newBoard, newTile, a))


def UCBchoose(x):
    """
    Chooses the best action/child with apropriate ratio of explore/exploit as determined by
    the UCB formula
        Parameter:
            x (Node): node object
        Returns:
            x (Node), a (List): child node object, and associated action
    """
    generateChildren(x)
    Y = list(set(x.children) - visits)

    # exploratory phase. All children of parent should be explored once
    if (len(Y) > 0):
        i = random.randint(0, len(Y) - 1)
        return Y[i], Y[i].a
    # after they all have been visited once:
    t = sum(list(map(lambda y: y.t, x.children)))
    if x.myTile == 'X':  # max
        Q = list(map(lambda y: y.r + sqrt((2 * log(t))/y.t), x.children))
        i = np.argmax(Q)
        return x.children[i], x.children[i].a
    else:  # min
        Q = list(map(lambda y: 1-y.r + sqrt((2 * log(t))/y.t), x.children))
        i = np.argmax(Q)
        return x.children[i], x.children[i].a


def mostVisited(x):
    """
    Finds child that has the most visits (highest t value) and returns its 
    action
        Parameter:
            x (obj): node object
        Returns:
            a (list): action from child node with highest visits
    """
    i = np.argmax(list(map(lambda node: node.t, x.children)))
    return x.children[i].a


def get_move(board, tile):
    """
    Gets the best move from given reversi board and the player
        Parameters:
            board (list):  
                Reversi board with 'X' and 'O' tiles
            tile (char): 

        Returns:
            a (list): 
                action with highest amount of visits
    """
    myBoard = copy.deepcopy(board)
    # player never played action before
    if ((len(plays) == 0) or (plays[-1].myBoard != myBoard)):
        state = Node(myBoard, tile, None)
        plays.append(state)
        UCT(state)
    else:
        state = plays[-1]
        UCT(state)

    return mostVisited(state)
