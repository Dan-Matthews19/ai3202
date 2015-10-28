#Return conditional probability given an engine, input tuple and conditional tuple list
def conditionalProbability(engine, input, conditionals, printable = True):

  conditionalString = ""
  #Assign evidence for conditionals
  for conditional, truthy in conditionals:
    engine.evidence[conditional] = truthy
    if conditional.name == 'pollution':
      conditionalString += conditional.name + "=" + 'Low' + ", " if truthy else 'high' + ", "
    else:
      conditionalString += conditional.name + "=" + str(truthy) + ", "

  #Grab querynode and truthyness from input variable
  queryNode, truthy = input

  # change true/false to low/high for polution
  if queryNode.name == 'pollution':
    truthyName = 'low' if truthy else 'high'
  else:
    truthyName = 'true' if truthy else 'false'


  Q = engine.marginal(queryNode)[0]
  index = Q.generate_index([truthy],range(Q.nDims))
  if printable:
    print "The conditional probability of", queryNode.name + "=" + truthyName + " |", conditionalString + "is", Q[index]

  return Q[index]



#Function for parsing the string into tuples of node and truthyness
def determineConditionalTuple(cancerNet, letter):
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
    print "Conditinal variables must be in the set p, s, c, x, d, ~p, ~s, ~c, ~x, ~d"
    exit()

  return input