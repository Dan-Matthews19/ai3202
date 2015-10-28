# Assignmnet 6 Bayes Net Calculator

## Usage:

### Options:
-g conditional probability
-j joint probability
-m marginal probability
-p set prior for either pollution or smoking

### Input
P pollution (p = low, ~p = high)
S smoker (s = true, ~s = false)
C cancer (c = true, ~s = false)
X xray (x = true, ~x = false)
D dyspnoea (d = true, ~d = false)

### Examples
conditional probability of cancer = true given smoker is false:
python Bayes_Net.py -g"c|~s"

joint probability of polution, smoker, cancer
python Bayes_Net.py -jPSC

joint probability of pollution = high, smoker = true, cancer = false
python Bayes_Net.py -j~ps~c

Set prior for pollution
python Bayes_Net.py -pP.30
