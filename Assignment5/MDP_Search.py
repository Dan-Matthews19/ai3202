#Dan Matthews, Collaborating with Dan Palmer 
#CSCI 3202 Assignment 5
#Markov Decision Processes
#import Node
import math
import sys


gama = 0.9
pr_success = 0.8
pr_fail = 0.1

dir_Up = "U"
dir_Down = "D"
dir_Left = "L"
dir_Right = "R"
dir_dest = "*"
dir_None = "none"


class Node(object):
	def __init__(self, position, block):
		self.position = position
		self.block = block
		
		if block == 50:
			self.utility = 50
			self.dir = dir_dest
			self.reward = 0
		else:
			self.utility = 0
			self.dir = None 

			if (block == 2):
				self.dir = "Wall"

			if (block == 1):
				self.reward = -1
			elif (block == 3):
				self.reward = -2
			elif (block == 4):
				self.reward = 1
			else:
				self.reward = 0

	def getPosition(self):
		return self.position

	def getDir(self):
		return self.dir

	def getReward(self):
		return self.reward

	def getUtility(self):
		return self.utility

	def getBlock(self):
		return self.block

	def setDir(self, direction):
		self.dir = direction

	def setUtility(self, utility):
		self.utility = utility	


	def __str__(self):
		if self.dir == dir_None:
			return (str(self.position) + " has utility:" + str(self.utility) + " and no direction.")
		return (str(self.position) + " has utility:" + str(self.utility) + " in direction:" + str(self.dir))

	def __cmp__(self,test):
		if self.utility is None:
			if test.getUtility() is None:
				return 0
			else:
				return -1
		if test.getUtility() is None:
			return 1
		if self.utility > test.getUtility():
			return 1
		elif self.utility < test.getUtility():
			return -1
		return 0


def buildWorld(fileName):
	worldMatix = []
	fn = open(fileName, "r").readlines()
	for line in reversed(fn):
		worldMatix.append(line.split(" "))
	
	nodeMatrix = []
	for i in range(len(worldMatix)):
		nodeMatrix.append([])
		for j in range(len(worldMatix[i])):
			nodeMatrix[i].append(Node((j, i), int(worldMatix[i][j])))

	return nodeMatrix	
	


def find_Optimal_Policy(world, epsilon):
	delta = float("inf")
	while(delta > epsilon * (1-gama)/gama):
		delta = 0
		for i in range(len(world)-1, -1, -1):
			for j in range(len(world[i])-1, -1, -1):
				test_delta = calculateUtility(i, j, world)
				if test_delta > delta:
					delta = test_delta
	print ("Policy calculating...\n")
		

def calculateUtility(i, j, world):
	cur_state = world[i][j]
	cell_block = cur_state.getBlock()

	#if wall: no utility, if destination: utility already defined
	if cell_block == 50 or cell_block == 2:
		return None

	excpectedUtility = []
	#calculate down, up, left, and right utilities
	if (i - 1) < 0:
		downUtility = 0
	else:
		downUtility = (world[i-1][j]).getUtility()

	if (i + 1) >= len(world):
		upUtility = 0
	else:
		upUtility = (world[i+1][j]).getUtility()

	if (j - 1) < 0:
		leftUtility = 0
	else:
		leftUtility = (world[i][j-1]).getUtility()

	if (j + 1) >= len(world[i]): #possibly change to world[i]
		rightUtility = 0
	else:
		rightUtility = (world[i][j+1]).getUtility()

	#add utilities for all directions into a list for expected utililty
	moveUp = ((pr_success * upUtility + pr_fail * leftUtility + pr_fail * rightUtility), dir_Up)
	excpectedUtility.append(moveUp)
	moveDown =((pr_success * downUtility + pr_fail * rightUtility + pr_fail * leftUtility), dir_Down)
	excpectedUtility.append(moveDown)
	moveRight = ((pr_success * rightUtility + pr_fail * downUtility + pr_fail * upUtility), dir_Right)
	excpectedUtility.append(moveRight)
	moveLeft = ((pr_success * leftUtility + pr_fail * upUtility + pr_fail * downUtility), dir_Left)
	excpectedUtility.append(moveLeft)

	currentUtility = cur_state.getUtility()
	maxEU = max(excpectedUtility)
	cur_state.setUtility(float(cur_state.getReward() + gama * maxEU[0]))
	cur_state.setDir(maxEU[1])

	return abs(currentUtility - cur_state.getUtility())

	
			
def find_Optimal_Path(matrix):
	print ("\nOptimal Path:")

	i = 0
	j = 0
	#self.world[x][y] = Node(x,y)
	currentState = matrix[i][j]
	while not (currentState.getDir() == '*'):	
		print currentState
		if currentState.getDir() == 'U':
			i += 1
		elif currentState.getDir() == 'D':
			i -= 1
		elif currentState.getDir() == 'L':
			j -= 1
		if currentState.getDir() == 'R':
			j += 1
		currentState = matrix[i][j]
	print currentState

def find_Optimal_Actions(matrix):
	print("Action Policy:")
	for i in reversed(matrix):
		action = [str(x.getDir()) for x in i]
		print " ".join(action)




if __name__ == "__main__":
	print("\n-----------------------------------------\n")
	if len(sys.argv) > 3:
		print("Too many arguments provided, expected: W <epsilon>")
		sys.exit()

	if len(sys.argv) == 3:
		if (sys.argv[1] == "W"):
			fileName = "World1MDP.txt"
		else:
			print "Must enter 'W' for a valid world."
			sys.exit()
		world = buildWorld(fileName)
		epsilon = float(sys.argv[2])

	if len(sys.argv) < 3:
		print ("Error: expected: W <epsilon>")
	find_Optimal_Policy(world, epsilon)
	print("\n-----------------------------------------\n")
	find_Optimal_Path(world)
	print("\n-----------------------------------------\n")
	find_Optimal_Actions(world)
	print("\n-----------------------------------------\n")
	print("Done")


