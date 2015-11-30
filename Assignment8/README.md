# Hidden Markov Models

## To Run

python HMM.py [datafile] > [outputfile]
datafile options:
typos20.data, typos20Test.data


### Part 1
This will output all the transition probabilities to Transition_output.txt
This will output all the emissions probabilities to Emissions_ouput.txt
This will output the base dristribution probabilites Base_Distribution_Output.txt

### Part 2
This will ouput the reconstructed text, as well as the Error Rate to an output file.
Example included in zip:
python HMM.py typos20.data > Viterbi.txt
python HMM.py typose20Test.data > V2.txt

