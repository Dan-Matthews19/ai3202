from marginal import *
from conditional import *
from itertools import *
import copy

try:
    from IPython import embed
except:
    pass


# Returns the joint probability for the given variables

def jointProbability(engine, jointArray):

  #Base case: if joint probability is only 2 vars, use
  # P(X=x and Y=y) = P(Y=y | X=x) * P(X=x)
  jointArrayCopy = copy.copy(jointArray)
  if len(jointArrayCopy) == 2:
    tupleA, tupleB = jointArrayCopy
    engine = copy.copy(engine)
    return  conditionalProbability(engine, tupleB, [tupleA], False) * margninalProbability(engine, tupleA[0], False, tupleA[1])

  #Call joint function recursively to break down the probaility
  # P(Z=z, X=x, Y=y) = joinProb(Z=z, JointProb(X=x,Y=y)))
  firstElement = jointArrayCopy.pop(0)
  return conditionalProbability(engine, firstElement, jointArrayCopy, False) * jointProbability(engine,jointArrayCopy)





#GET JOINT PROBABILITY DISTRIBUTIONS (FOR CAPITAL LETTERS)

# For each combination of true, false for each variable, get the joint probability

def jointProbabilityDistribution(engine, jointArray):

  n = len(jointArray)
  newArray = list([jointArray]*2**n)
  allorderings = list(product([False, True], repeat = n))

  permutedList = []
  for i in range(len(newArray)):
    templist = []
    for j in range(n):
      templist.append((newArray[i][j], allorderings[i][j]))
    permutedList.append(templist)


  for permutation in permutedList:
    permutationString = ""
    probability = jointProbability(engine, permutation)
    for permtuple in permutation:
      if permtuple[0].name == 'pollution':
        permutationString += permtuple[0].name + "=" + ('Low' + ", " if permtuple[1] else 'High' + ", ")
      else:
        permutationString += permtuple[0].name + "=" + str(permtuple[1]) + ", "
    print "The Joint probability of " + permutationString + "is " + str(probability)


def determineJointTuple(cancerNet, letter, truthyNotDeclared=False):
  for node in cancerNet.nodes:
    if node.id == 0:
      pollution = node
    if node.id == 1:
      smoker = node
    if node.id == 2:
      cancer = node
    if node.id == 3:
      xray = node
    if node.id == 4:
      dyspnoea = node
  if truthyNotDeclared:
    if letter == 'P':
      input = pollution
    elif letter == 'S':
      input = smoker
    elif letter == 'C':
      input = cancer
    elif letter == 'X':
      input = xray
    elif letter == 'D':
      input = dyspnoea
    else:
      print "Joint Probability variables must all be in the set P, S, C, X, D"
      exit()
  else:
    if letter == 'p':
      input = (pollution, True)
    elif letter == 's':
      input = (smoker, True)
    elif letter == 'c':
      input = (cancer, True)
    elif letter == 'x':
      input = (xray, True)
    elif letter == 'd':
      input = (dyspnoea, True)
    elif letter == '~p':
      input = (pollution, False)
    elif letter == '~s':
      input = (smoker, False)
    elif letter == '~c':
      input = (cancer, False)
    elif letter == '~x':
      input = (xray, False)
    elif letter == '~d':
      input = (dyspnoea, False)
    else:
      print "Joint Probability variables must be in the set p, s, c, x, d, ~p, ~s, ~c, ~x, ~d"
      exit()

  return input