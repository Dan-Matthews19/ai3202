# Dan Matthews Assignment 5
## MDP Search

To run the program:
python MDP_Search.py W 'epsilon'

epsilon must be a float: Output shown for epsilon = 0.5

output:
-----------------------------------------

Policy calculating...


-----------------------------------------


Optimal Path:
(0, 0) has utility:0.792984681064 in direction:U
(0, 1) has utility:0.983170211162 in direction:U
(0, 2) has utility:1.51540129824 in direction:U
(0, 3) has utility:2.09308802252 in direction:R
(1, 3) has utility:2.71770959917 in direction:U
(1, 4) has utility:3.51304469172 in direction:U
(1, 5) has utility:3.49033984961 in direction:R
(2, 5) has utility:4.40862795591 in direction:R
(3, 5) has utility:5.57424345649 in direction:R
(4, 5) has utility:6.96637838652 in direction:U
(4, 6) has utility:8.36327516163 in direction:U
(4, 7) has utility:9.74680974852 in direction:R
(5, 7) has utility:13.8808198928 in direction:R
(6, 7) has utility:18.1856286505 in direction:R
(7, 7) has utility:26.646706459 in direction:R
(8, 7) has utility:36.0 in direction:R
(9, 7) has utility:50 in direction:*

-----------------------------------------

Action Policy:
R R R R R R R R R *
Wall Wall R R U U Wall U Wall U
R R R R U U Wall R R U
Wall U Wall Wall R R R U Wall U
R U Wall R U Wall U U R U
U U Wall R U Wall R U Wall U
U L Wall U U Wall U U Wall Wall
U R R R R R U U L L

-----------------------------------------

Done

## Change with different epsilong values:
I ran my program with epsilon values ranging from 0.5 to 20.5 incrementing by 0.5 at a time. I noticed that the optimal path to the goal did not change based on epsilon value change. The Action policy (the optimal direction for each cell in the matrix, not counting walls) did change as the values of epsilon got higher as did the utility which gave influence to the optimal direction. I believe the reason for this is because as the max allowable error of utility in any state grows larger, the true optimal path will be distorted. The max change of any utility of a state in an iteration goes up, and therefore the error goes up, so the optimal path gets less and less optimal with higher values of epsilon.