samples = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28, 1.0, 0.95,
0.71, 0.14, 0.1, 1.0, 0.71, 0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97,
0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, 0.14, 0.13, 0.4, 0.94, 0.19, 0.6, 0.68, 0.36, 0.67,
0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85, 0.01, 0.55, 0.3, 0.3, 0.11, 0.83, 0.96, 0.41, 0.65,
0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97, 0.95, 0.01, 0.62, 0.32,
0.56, 0.68, 0.32, 0.27, 0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79, 0.21, 0.2, 0.43, 0.81,
0.9, 0.0, 0.91, 0.01]

############Prior Sampling############

class Node:
	def __init__(self, name, parents):
		self.name = name
		self.parents = parents
		self.children = []
		self.marginal = 0.0
		self.conditions = {}
		self.value = None

	def setValue(self, newValue):
		self.value = newValue

	def addChild(self, newChild):
		self.children.append(newChild)

	def __str__(self):
		return "%s marginal probability - %f" % (self.name, self.marginal)

class BayesNet:
	def __init__(self):
		cloudy = Node("cloudy", None)
		cloudy.marginal = 0.5

		sprinkler = Node("sprinkler", [cloudy])
		sprinkler.conditions["c"] = 0.1
		sprinkler.conditions["~c"] = 0.5

		rain = Node("rain", [cloudy])
		rain.conditions["c"] = 0.8
		rain.conditions["~c"] = 0.2

		cloudy.addChild(sprinkler)
		cloudy.addChild(rain)

		wet_grass = Node("wet_grass", [sprinkler, rain])
		wet_grass.conditions["sr"] = 0.99
		wet_grass.conditions["s~r"] = 0.9
		wet_grass.conditions["~sr"] = 0.9
		wet_grass.conditions["~s~r"] = 0.0

		sprinkler.addChild(wet_grass)
		rain.addChild(wet_grass)

		self.baye_nodes = {}
		self.baye_nodes["cloudy"] = cloudy
		self.baye_nodes["sprinkler"] = sprinkler
		self.baye_nodes["rain"] = rain
		self.baye_nodes["wet_grass"] = wet_grass

	def __str__(self):
		string = "BayesNet\n"
		for n in self.baye_nodes:
			node = self.baye_nodes[n]
			string = string + "{0} - {1}\n".format(n, node.value)

		return string

	def clearNet(self):
		for n in self.baye_nodes:
			n.value = None

	def traverse(self, iterator):
		cloudy = self.baye_nodes["cloudy"]
		sprinkler = self.baye_nodes["sprinkler"]
		rain = self.baye_nodes["rain"]
		wet_grass = self.baye_nodes["wet_grass"]

		test_samples = []

		for i in range(0,4):
			test_samples.append(iterator.next())

		if (cloudy.marginal >= test_samples[0]):
			cloudy.setValue(True)

			if (sprinkler.conditions["c"] >= test_samples[1]):
				sprinkler.setValue(True)
			else:
				sprinkler.setValue(False)

			if (rain.conditions["c"] >= test_samples[2]):
				rain.setValue(True)
			else:
				rain.setValue(False)
		else:
			cloudy.setValue(False)
			if (sprinkler.conditions["~c"] >= test_samples[1]):
				sprinkler.setValue(True)
			else:
				sprinkler.setValue(False)

			if (rain.conditions["~c"] >= test_samples[2]):
				rain.setValue(True)
			else:
				rain.setValue(False)
		if (sprinkler.value == True and rain.value == True):
			if(wet_grass.conditions["sr"] >= test_samples[3]):
				wet_grass.setValue(True)
		elif (sprinkler.value == False and rain.value == True):
			if (wet_grass.conditions["~sr"] >= test_samples[3]):
				wet_grass.setValue(True)
		elif (sprinkler.value == True and rain.value == False):
			if (wet_grass.conditions["s~r"] >= test_samples[3]):
				wet_grass.setValue(True)
		else:
				wet_grass.setValue(False)

def prior_c_true():
	match = []
	i = iter(samples)

	for j in range(0, 25):
		model = BayesNet()
		model.traverse(i)

		if model.baye_nodes["cloudy"].value:
			match.append(model)

	p = float(len(match)) / 25

	print "P(c = True) = %.2f" % p

def prior_c_given_r():
	matchR = []
	i = iter(samples)

	for j in range(0, 25):
		model = BayesNet()
		model.traverse(i)

		if model.baye_nodes["rain"].value:
			matchR.append(model)

	matchR_C = []
	for n in matchR:
		if n.baye_nodes["cloudy"].value:
			matchR_C.append(n)

	p = float(len(matchR_C)) / len(matchR)
	print "P(c = True | r = True) = %.2f" % p

def prior_s_given_w():
	matchS = []
	i = iter(samples)
	for j in range(0, 25):
		model = BayesNet()
		model.traverse(i)

		if model.baye_nodes["wet_grass"].value:
			matchS.append(model)
	matchS_W = []
	for n in matchS:
		if n.baye_nodes["sprinkler"].value:
			matchS_W.append(n)
	p = float(len(matchS_W)) / len(matchS)
	print "P(s = True | w = true) = %.2f" % p

def prior_s_given_cw():
	matchS = []
	i = iter(samples)
	for j in range(0, 25):
		model = BayesNet()
		model.traverse(i)
		if model.baye_nodes["sprinkler"].value:
			matchS.append(model)
	matchS_C = []
	for n in matchS:
		if n.baye_nodes["cloudy"].value:
			matchS_C.append(n)
	matchS_CW = []
	for m in matchS_C:
		if m.baye_nodes["wet_grass"].value:
			matchS_CW.append(m)
	p = float(len(matchS_CW)) / len(matchS)
	print "P(s = True | c = True, w = True) %.2f" % p

############Rejection Sampling############
prob = {}
rejec = []

c = 0
while c < 100:
	s = c + 1
	r = c + 2
	w = c + 3

	cloudy = False
	rain = False
	sprinkler = False
	wet_grass = False

	if samples[c] < 0.5:
		cloudy = True
		if samples[s] < 0.1 and samples[r] < 0.8: #rs|c
			sprinkler = True
			rain = True
			if samples[w] < 0.99: #w|rs
				wet_grass = True
				rejec.append([cloudy,sprinkler,rain,wet_grass])
			else:
				rejec.append([cloudy,sprinkler,rain,wet_grass])
		elif samples[s] >= 0.1 and samples[r] < 0.8: #r~s|c
			sprinkler = False
			rain = True
			if samples[w] < 0.9: #w|r~s
				wet_grass = True
				rejec.append([cloudy,sprinkler,rain,wet_grass])
			else:
				rejec.append([cloudy,sprinkler,rain,wet_grass])
		elif samples[s] < 0.1 and samples[r] >= 0.8: # ~rs|c
			sprinkler = True
			rain = False
			if samples[w] < 0.9: #w|~rs
				wet_grass = True
				rejec.append([cloudy,sprinkler,rain,wet_grass])
			else:
				rejec.append([cloudy,sprinkler,rain,wet_grass])
		elif samples[s] >= 0.1 and samples[r] >= 0.8:
			sprinkler = False
			rain = False
			wet_grass = False
			rejec.append([cloudy,sprinkler,rain,wet_grass])
	if samples[c] >= 0.5:
		cloudy = False
		if samples[s] < 0.5 and samples[r] < 0.2:
			sprinkler = True
			rain = True
			if samples[w] < 0.99:
				wet_grass = True
				rejec.append([cloudy,sprinkler,rain,wet_grass])
			else:
				rejec.append([cloudy,sprinkler,rain,wet_grass])
		elif samples[s] >= 0.5 and samples[r] < 0.2:
			sprinkler = False
			rain = True
			if samples[w] < 0.9:
				wet_grass = True
				rejec.append([cloudy,sprinkler,rain,wet_grass])
			else:
				rejec.append([cloudy,sprinkler,rain,wet_grass])
		elif samples[s] < 0.5 and samples[r] >= 0.2:
			sprinkler = True
			rain = False
			if samples[w] < 0.9:
				wet_grass = True
				rejec.append([cloudy,sprinkler,rain,wet_grass])
			else:
				rejec.append([cloudy,sprinkler,rain,wet_grass])
		elif samples[s] >= 0.5 and samples[s] >= 0.2:
			sprinkler = False
			rain = False
			wet_grass = False
			rejec.append([cloudy,sprinkler,rain,wet_grass])
	c = c + 4

c = 0
s = 1
r = 2
w = 3
def prior_c_true_R():
	i = 0.0
	for j in rejec:
		if j[c] == True:
			i += 1.0
	print "P(c = True) = " , i/25.0

def prior_c_given_r_R():
	i = 0.0
	for j in rejec:
		if j[c] == True and j[r] == True:
			i += 1.0
	print "P(c = True | r = True) = ", i/25.0

def prior_s_given_w_R():
	i = 0.0
	for j in rejec:
		if j[s] == True and j[w] == True:
			i += 1.0
	print "P(s = True | w = True) = ", i / 25.0

def prior_s_given_cw_R():
	i = 0.0
	for j in rejec:
		if j[s] == True and j[c] == True and j[w] == True:
			i += 1.0
	print "P(s = True | c = True, w = True) = ", i/25.0


if __name__ == "__main__":
	print "********Prior Sampling********"
	prior_c_true()
	prior_c_given_r()
	prior_s_given_w()
	prior_s_given_cw()
	print "********Rejection Sampling********"
	prior_c_true_R()
	prior_c_given_r_R()
	prior_s_given_w_R()
	prior_s_given_cw_R()
