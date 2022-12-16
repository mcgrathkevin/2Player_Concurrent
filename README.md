# 2Player_Concurrent

**How to Run Code:**
1. Clone repository https://github.com/mcgrathkevin/2Player_Concurrent.git
2. Pull and run docker environment with abhibp1993/ggsolver:latest
3. Run ```p1_reach_1_ex.py``` (top) or ```p2_reach_3_ex.py``` (bottom) which import the DTPCGame class from ```dtpc.py``` and calculate and display the almost-sure winning region states and policy for the two examples shown below.

*Note: Action **(-, E)** at State 5 (bottom example) was replaced with actions **(a, E)** and **(c, E)**.*


![examples](examples.png)

Below is a code snippet from ```p2_reach_3_ex.py```  and the corresponding output for calculating almost-sure reachability set for P1 for reachability objective F = {3}. Setting ```verbose=True``` will print the intermediate confinement and safety sets for the opponent and player, respectively.

**Run**

```python
win, pi = game.asw_reach(player=2, final={3}, verbose=True)
print('********** Almost-Sure Reachability **********')
print(f'States: {win}')
print(f'Policy: {pi}')
```

**Output**
```python
*** Iteration 1 ***
Player 1 Confinement Set: {2, 4, 5}
Player 2 Safe Set: {1, 3} 
Policy: {1: ['-'], 3: ['-']}

********** Almost-Sure Reachability **********
States: {1, 3}
Policy: {1: ['-'], 3: ['-']}
```
