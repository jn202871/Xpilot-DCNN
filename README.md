### Xpilot-DCNN
This project aims to replicate the behavior of Xpilot agents using a DCNN and the behavioral cloning process. The DCNN uses gathered agent data from various different pre-built agents (currently a fuzzy system and basic neural network) to learn how to emulate those bots.

Currently the DCNN is able to adequately emulate the behavior of the bots it is trained on and put up a decent fight when it is tested against the bots it is trained on. The validation loss of the DCNN varies greatly between training on different bots at this time. 

When trained on the fuzzyBot on the lifeless map, it is able to attain a validation loss of ~10%. When trained on the neuralNetBot on the simple map, it is unable to attain a vaidation loss under ~28%. Interestingly, these validation losses do not correlate to DCNN effectiveness in combat. 

The DCNN controlled bot is unable to effectively challenge the fuzzyBot however is able to beat the neuralNetBot. This is a very odd result that requires further investigation to determine the cause.

### Instructions
To run the DCNN, clone the repositiory and use the included bash scripts to run the agents.


"lifeless.sh":

This script will run a DCNN agent that was trained on data collected by fuzzyBot on the lifeless map. The DCNN agent will have that fuzzyBot agent as its opponent.


"simple.sh":

This script will run a DCNN agent that was trained on data collected by neuralNetBot on the simple map. The DCNN agent will have fuzzyBot as its opponent. Note that this is not the bot the agent was trained on.


"simple_NNvDCNN.sh":

This script will run a DCNN agent that was trained on data collected by neuralNetBot on the simple map. The DCNN agent will have that neuralNetBot as its opponent. This is a seperate script as neuralNetBot was written in java and requires some extra steps to run, therefore it has it's own testing script.
