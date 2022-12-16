# 2Player_Concurrent

**How to Run Code:**
1. Clone repository https://github.com/mcgrathkevin/2Player_Concurrent.git
2. Pull and run docker environment with abhibp1993/ggsolver:latest
3. Run ```p1_reach_1_ex.py``` or ```p2_reach_3_ex.py``` which import the DTPCGame class from ```dtpc.py``` and calculate and display the almost-sure winning region states and policy for the two examples shown below.

*Note: Action **(-, E)** at State 5 for P2 Reach({3}) (bottom image) was replaced with actions **(a, E)** and **(c, E)**.*


![examples](examples.png)

Below is a code snippet from ```p1_reach_1_ex.py```  and the corresponding output for calculating almost-sure reachability set for P1 for reachability objective F = {3}. Setting ```verbose=True``` will print the intermediate confinement and safety sets for the opponent and player, respectively.

**Run**

```python
win, pi = game.asw_reach(player=1, final={1}, verbose=True)
print('********** Almost-Sure Reachability **********')
print(f'States: {win}')
print(f'Policy: {pi}')
```

**Output**
```python
*** Iteration 1 ***
Player 2 Confinement Set: {2, 3, 4, 5}
Player 1 Safe Set: {0, 1} 
Policy: {0: ['c'], 1: ['-']}

********** Almost-Sure Reachability **********
States: {0, 1}
Policy: {0: ['c'], 1: ['-']}
```
