import math
import sys

#matrix = [[], [], [], [], [], [], [], [], [], []]
#matrix = []
class Node(object):
	def __init__(self, xCor, yCor):
		self.x = xCor
		self.y = yCor
		self.distanceToStart = 0
		self.hueristic = None
		self.f = None
		self.parent = None

	def totalDistance(self, parent, value, h):
		width = 9
		height = 7
		self.parent = parent
		pDistance = abs(parent.x - self.x) + abs(parent.y - self.y)
		#Diagonal move onto empty square
		if(pDistance == 2):
			self.distanceToStart = parent.distanceToStart + 14
		#Diagonal move onto mountain square
		#if(pDistance ==2) and (matrix[self.x][self.y] == 1):
		#	self.distanceToStart = parent.distanceToStart + 24
		#Horizontal or verticle move onto empty square
		if(pDistance == 1):
			self.distanceToStart = parent.distanceToStart + 10
		#Horizontal or verticle move onto empty square
		#if(pDistance == 1) and (matrix[self.x][self.y] == 0):
		#	self.distanceToStart = parent.distanceToStart + 20
		#Manhattan distance
		if(huer == 'Manhattan'):
			self.hueristic = abs(width - self.x) + abs(height - self.y)
		#pythagorean hueristic
		elif(huer == "Pythagorean"):
			self.hueristic = math.sqrt(abs(width - self.x)**2 + abs(height - self.y)**2)
		self.f = self.distanceToStart + self.hueristic

	def compare(self, testParent, val):
		parentDist = abs(testParent.x - self.x) + abs(testParent.y - self.y)
		testDistance = 0
		if(parentDist == 2):
			testDistance = testParent.distanceToStart + 14
		elif(parentDist == 1):
			testDistance = testParent.distanceToStart + 10
		if (val == 1):
			testDistance += 10
		if(testDistance < self.distanceToStart):
			self.distanceToStart = testDistance
			self.parent = testParent
			self.f = self.distanceToStart + self.hueristic

	def equalz(self, check):
		return (self.x == check.x and self.y == check.y)


def AStar(world, heur):
	openQueue = []
	closed = [Node(-1,-1)]
	start = Node(0,0)

	openQueue.append(start)

	nodesVisited = 0
	while(closed[-1].equalz(Node(9,7)) != 1 and len(openQueue) > 0 ):
		openQueue.sort(key = lambda node: node.f)
		min_node = openQueue[0]
		openQueue.remove(min_node)
		closed.append(min_node)

		for i in range(-1,2):
			for j in range(-1,2):
					valid_x = min_node.x + i
					valid_y = min_node.y + j
					if(valid_x >= 0 and valid_x <= 9 and valid_y >= 0 and valid_y <= 7):
						nodesVisited += 1	
						n = Node(valid_x, valid_y)
						
						check1 = True
						for c in closed:
							if c.equalz(n):
								check1 = False
						if (world[valid_x][valid_y] is not 2 and check1):
							n = Node(valid_x, valid_y)
							check2 = True

							for d in openQueue:
								if d.equalz(n):
									check2 = False
								if check2:
									openQueue.append(n)
									n.totalDistance(min_node, world[valid_x][valid_y], huer)
								else:
									n.compare(min_node, world[valid_x][valid_y])

	track = closed[-1]
	print "Now we evaluate the total cost, number of nodes visited:"
	print("Total cost: ", track.distanceToStart, " Locations evaluated:" , nodesVisited)
	path = []

	while(track is not None):
		path.insert(0, track)
		track = track.parent

	print"Now evaluting the path followed"
	for i in path:
		print(i.x, i.y)

def main():

	wrld = ""
	h = ""

	if(sys.argv[1] == "W1"):
		wrld = "World1.txt"
	elif(sys.argv[1] == "W2"):
		wrld = "World2.txt"
	else:
		print "Not a valid world: must select W1 or W2"
		sys.exit(0)

	if(sys.argv[2] == "H1"):
		h = "Manhattan"
	elif(sys.argv[2] == "H2"):
		h = "Pythagorean"

	else:
		print "Invalid hueristic: must select H1 for Manhattan or H2 for Pythagorean"
		sys.exit(0)
		
	gameBoard = [[], [], [], [], [], [], [], [], [], []]

	with open(wrld) as f:
		for line in f:
			for i, val in enumerate(line.split()):
				gameBoard[i].append(int(val))

	AStar(gameBoard, h)	

main()
