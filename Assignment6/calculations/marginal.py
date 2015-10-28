def margninalProbability(engine, input, printable = True, returnable = True):
  #Compute the marginal probability of sprinkler given no evidence
  Q = engine.marginal(input)[0]

  trueName = 'true'
  falseName = 'false'

  # change true/false to low/high for polution
  if input.name == 'pollution':
    trueName = 'low'
    falseName = 'high'


  true = Q.generate_index([True], range(Q.nDims))
  if printable:
    print "The marginal probability of", input.name + "=" + trueName + ":", Q[true]
  false = Q.generate_index([False], range(Q.nDims))
  if printable:
    print "The marginal probability of", input.name + "=" + falseName + ":", Q[false]

  #always return true
  if returnable:
    return Q[true]
  else:
    return Q[false]