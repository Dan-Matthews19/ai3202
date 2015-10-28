#Dan Matthews
#Bayes net 
#collaboration with Dan Palmer

#! /usr/bin/env python

import getopt, sys, copy, re
from numpy import *
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *
from calculations.model import *
from calculations.marginal import *
from calculations.conditional import *
from calculations.joint import *

try:
    from IPython import embed
except:
    pass

def main():
  try:
    optlist, remainder = getopt.getopt(sys.argv[1:], 'j:g:m:p:')
    if len(optlist) == 0:
      print "no arguments provided"
  except getopt.GetoptError as err:
    print str(err)

  #initializing bayes net via PBNT utilities
  cMap = BayesModel()
  for node in cMap.nodes:
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
      
  cEngine = JunctionTreeEngine(cMap)

  #********** Respond to Input***********
  for o, a in optlist:
	  
#marginal prob
    if o == "-m":
      if len(a) > 1:
        print "invalid input"
      if a == 'P':
        input = pollution
      elif a == 'S':
        input = smoker
      elif a == 'C':
        input = cancer
      elif a == 'X':
        input = xray
      elif a == 'D':
        input = dyspnoea
      else:
        print "invalid input"
	  
	  #calculations
      marginalEngine = copy.copy(cEngine)
      margninalProbability(marginalEngine, input)

#set prior
    elif o == "-p":
      if a[0] == 'P':
      	input = pollution
        pollutionLow = float(a[1:])
      elif a[0] == 'S':
        smokeTrue = float(a[1:])

#conditional prob
    elif o == "-g":
      splitInput = a.find('|')
      query = a[:splitInput]
      conditionals = a[splitInput+1:]

      #input tuple
      input = determineConditionalTuple(cMap, query)

      #Create conditionals list of tuples
      conditionalsplit = re.findall('~?[a-z]',conditionals)
      conditionalsList =[]
      for letter in conditionalsplit:
        conditionalsList.append(determineConditionalTuple(cMap, letter))

      #Return the conditional probability
      conditionalEngine = copy.copy(cEngine)
      conditionalProbability(cEngine, input, conditionalsList)

#joint prob
    elif o == "-j":
      # Return the joint probability
      jointEngine = copy.copy(cEngine)
      jointSplit = re.findall('[A-Z]',a)
      jointInput = []
      if len(jointSplit) > 0:
        for letter in jointSplit:
          jointInput.append(determineJointTuple(cMap, letter, True))
        jointProbabilityDistribution(jointEngine,jointInput)
      else:
        jointSplit = re.findall('~?[a-z]',a)
        for letter in jointSplit:
          jointInput.append(determineJointTuple(cMap, letter))
        probability = jointProbability(jointEngine, jointInput)
        jointString = ""
        for joint in jointInput:
          if joint[0].name == 'pollution':
            jointString += joint[0].name + "=" + ('Low' + ", " if joint[1] else 'High' + ", ")
          else:
            jointString += joint[0].name + "=" + str(joint[1]) + ", "

        print "The joint probability of " + jointString + "is", probability

if __name__ == "__main__":
    main()
