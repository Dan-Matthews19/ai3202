#Dan Matthwes Assignment 8
#Constructs an HMM and runs viterbi algorithm on model given set of input data

#Viterbi reference: https://en.wikipedia.org/wiki/Viterbi_algorithm

import sys
import argparse
import math

states = []
output = []
d = {}
d1 = {}
d2 = {}

possibleStates = "abcdefghijklmnopqrstuvwxyz_"


#System arguments for different data file:
#typos20.data
#typos20Test.data
fn = sys.argv[1]
if len(sys.argv) < 2:
	print "Usage: python HMM.py <data_file>"

with open(fn, "r") as f:
	for line in f:
		l = line.split()
		states.append(l[0])
		output.append(l[1])


def transitionProb():
	for x in states:
		if x not in d:
			d[x] = {}
	for j in range(len(possibleStates)):
		for i in range(len(states) - 1):
			if states[i+1] not in d[states[i]]:
				d[states[i]][states[i+1]] = 1
			else:
				d[states[i]][states[i+1]] += 1
			if possibleStates[j] not in d[states[i]]:
				d[states[i]][possibleStates[j]] = 0
	total_states = 0.0
	for state in d:
		for t_state in d[state]:
			total_states += d[state][t_state]
		for t_state in d[state]:
			t_prob = float(d[state][t_state] + 1) / (total_states + 27)
			d[state][t_state] = t_prob
		total_states = 0.0
	text_file = open('Transition_output.txt', 'w')
	text_file.write('Transitoin Probabilities\n')
	for state in d:
		for t_state in d[state]:
			text_file.write('P(X_t+1)=' + t_state + ' | X_t=' + state + ') ' + str(d[state][t_state]) + '\n')
	text_file.close()
	

def emmisionProb():
	for x in states:
		if x not in d1:
			d1[x] = {}
	for j in range(len(possibleStates)):
		for i in range(len(states)):
			if output[i] not in d1[states[i]]:
				d1[states[i]][output[i]] = 1
			else:
				d1[states[i]][output[i]] += 1
			if possibleStates[j] not in d1[states[i]]:
				d1[states[i]][possibleStates[j]] = 0
	total_states = 0.0
	for state in d1:
		for e_state in d1[state]:
			total_states += d1[state][e_state]
		for e_state in d1[state]:
			e_prob = float(d1[state][e_state] + 1) / (total_states +27)
			d1[state][e_state] = e_prob
		total_states = 0.0
	text_file = open('Emission_output.txt', 'w')
	text_file.write('Emission Probabilities\n')
	for state in d1:
		for e_state in d1[state]:
			text_file.write('P(E_t)=' + e_state + ' | X_t = ' + state + ') ' + str(d1[state][e_state]) + '\n')
	text_file.close()

def initialProb():
	length = float(len(states))
	count = 0.0
	for x in states:
		if x not in d2:
			d2[x] = 1
		else:
			d2[x] += 1
	text_file = open('Base_Distribution_Ouput.txt', 'w')
	text_file.write('Initial Probability Distribution\n')
	for x in d2:
		numerator = float(d2[x])
		i_prob = numerator / length
		d2[x] = i_prob
		text_file.write('P(x= ' + x + ')' + str(d2[x]) + '\n')

def viterbi():
	T1 = [{}]
	path = {}
	res = []
	
	for state in possibleStates:
		T1[0][state] = math.log10(d2[state]) + math.log10(d1[state][output[0]])
		path[state] = [state]

	for t in range(1, len(output)):
		T1.append({})
		newPath = {}
		for c in possibleStates:
			(p, state) = max((T1[t-1][y0] + math.log10(d[y0][c]) + math.log10(d1[c][output[t]]), y0) for y0 in possibleStates)
			T1[t][c] = p
			newPath[c] = path[state] + [c]
		path = newPath
	(p, state) = max((T1[len(output) - 1][y], y) for y in possibleStates)

	return (p, path[state])



def main():
	transitionProb()
	emmisionProb()
	initialProb()
	V = viterbi()

	numCorrect = 0
	VT = V[1]
	print "State Sequence...\n"
	for element in VT:
		sys.stdout.write(element)

	for i in range(0, len(VT)):
		if VT[i] == states[i]:
			numCorrect += 1

	print '\n\nError Rate: ', 1 - numCorrect / float(len(states))

main()






