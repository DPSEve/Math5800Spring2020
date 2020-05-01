# Math5800 Spring 2020: Mathematical Aspects of Machine Learning
This is the Github Page for Math 5800 Spring 2020 at UCONN, taught by Professor [Jeremy Teitelbaum](https://jeremy9959.net/)

Group members Christopher Hayes, Evelyn Nitch-Griffin

We are interested in reinforcment learning problems in games. In this project, we focused on Connect Four, a zero-sum game between two players. The goal was to create a functioning reinforcment learning model in Python.

## Reinforcement Learning

Reinforcment learning is a machine learning problem where an agent (such as a person, program, or robot) is attempting a maximize a reward output. For Connect Four, our agent is the player, and our reward output is winning or losing the game. The agent interacts with its environment and receives rewards and penalties based on its actions. In an attempt to maximine rewards, it learns the optimal behavior overtime. A famous example of this being applied recently is [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far), a computer program developed by Deepmind which consistently beat top human Go players.

#### Exploration vs Exploitation

One of the most fundamental problems in machine learning is the tradeoff between exploration vs exploitation. Explorating is when an agent takes actions that may not always be optimal, but help it determine the possible best actions. Exploitation is when an agent takes the **currently perceived** best action. An agent that explores too much might take too long (and waste posible resources) to find the optimal solution. An agent that explots too much may move towards a suboptimal solution. Operationalizing this and finding the correct balance is an important task for all reinforcment learning problems

## Finite Markhov Decision Processes

A Markhov Decision Process (MDP) is determined by 4 things: an agent, a environment (or a set of possible states), a set of actions, and a reward. Over a series of time steps $(t=0,1, ...)$, the agent interacts with the environment by taking an action, and then receives a reward. This yields a sequences of states, actions, and rewards.

$$
S_0, A_0, R_0, \rightarrow S_1, A_1, R_1 \rightarrow ...
$$

 This is often notationally represented in the following way. 
 
$$
(S, A, \{P_{sa}\}, \gamma, R)
$$
for the states, actions, state transition distribution, discount factor, and rewards. The state transition distribution determines the probabilities for moving into a state after taking a certain action, and gamma is a discounting factor that weights earlier rewards over later rewards $(0 < \gamma \leq 1)$.

In the FMDP, there are a finite amount of states, actions, and rewards. In our Connect Four problem, our states would be the possible board configurations, our actions would be placing a piece in a (non-full) column, and our rewards are +1 for winning, 0 for ties, and -1 for losing. Here the state transition probability represents our opponent's move. We choose $\gamma$ to be 1, which means we don't discount; we only care about winning in the long term.

When we are in a state, we have a selection of actions that we can take. Each action is followed by an action of our opponent, which presents a new state before us. If our opponent is predictable, we could operationalize a state transition probability.

$$
p(s^{'},r|s,a) = Pr\{S_{t} = s^{'}, R_{t} = r| S_{t-1}=s, A_{t-l} = a\}
$$
which is the probability of the state $s^{'}$ and reward $r$ happening after we take the action $a$ in the current state $s$. In the Connect Four problem, this represents likely following board states that is are presented to us after we and our opponent make our moves. The probabilities would represent the likelyhood our opponent takes which actions. Although perhaps counterintuitive, our state space only represents the board states that are **presented to the agent**.

In a general problem, the state transition probability could repreent many things, such as the likely outcomes of a slot machine. The flexible nature of the Markhov Decision Process allows it to be applied to many different problems.

##### The Markhov Property

In the MDP the state transition probabilities completely characterize the dynamics of the environment. The state is said to have the Markhov property if the probabilites of future states depends only on the *current state*, irrelevant of the sequence of events that led to the state. This is sometimes called the memoryless property, because what determines the best action depends only of the current state. Connect Four has the Markhov property, as do almost all other board games, because in order to make the best move you only need to know the current board state. The actions that led up to that state are irrelevant to winning.

##### Policies and Values

A policy $\pi$ is the agent's methods for selecting its actions. It can be viewed as a probability distributirepresenting the likelyhood of certain actions given a state. We can also think about the **value** of a state given a policy $\pi$. This is represented by $V_{\pi}$, and is the expected *total* payoff starting in a state $s$ and following the policy $\pi$. Because we are in a Markhov decision process, we can utilize Bellman's equation.

$$
V_{\pi}(s) = R(s) + \gamma\sum_{s'}p(s'|s,\pi(s))V_{\pi}(s')
$$

Essentially, Bellman's equation states that the expected payoff of a state given a policy $\pi$ is determined by its successor states. In a Finite MDP, if the state transition probabilities are known, this gives a series of linear equations, which could be solved to calculate the state value. However, things usually aren't that simple.

Generally, many reinforcment learning problems are oriented towards estimating state values. By knows which states are higher valued, you can change your policy to favor high valued states. Over time, you should eventually move towards a optimal policy.

### Our Code
Our python defines a Connect Four board, and allows us to simulate games. To begin, we implemented a rudimentary Monte Carlo AI. Given a board state, it looks at the possible moves and plays out a certain number of random games. Then, it picks the move that led to the most number of random wins. Essentially, this is a basic value estimation method.

We also implement a beginning Monte Carlo value estimation method. First, we generated a state database using the Monte Carlo AI. The value of the state was determined by averaging Bellman equation above. 
$$
V(s) = \frac{\sum wins -\sum losses}{visits}
$$
Then, the policy is to make the move that generates the best value, with a small chance to take a random move to continue exploring different actions. This is often called a $\epsilon$ greedy policy, because it takes the currently best perceived action with an $\epsilon$ chance to explore.

Finally, we have yet to implement a neural network. The plan is to use pytorch or a self created network that trains on the database above. Then, it outputs a probability distribution for the possible moves, where each move is assigned a non-zero probability. This is so that we always have a chance to exploore to update the network.


### References

- [The Hanabi Challenge: A New Frontier for AI Research](https://arxiv.org/abs/1902.00506) {Chris: Introduces the game, includes an open source self-playing program, and compares results of learning-agent bots with rule-based bots, collaborations between such, et cetera. No large data sets seem to be involved - unsure how it relates to data science. Published 2020 in AI (Elsevier)}

- The associated platform for this article is found at: https://github.com/deepmind/hanabi-learning-environment

- [Simplified Action Decoder for Deep Multi-Agent Reinforcement Learning 2020](https://openreview.net/forum?id=B1xm3RVtwB)
- [With associated code](https://colab.research.google.com/drive/1Cvs4GuFvHEdvb7tVJQVvQOviAkRf97r7) {Chris: What does the code actually do?} 

- [Bayesian Action Decoder](https://explore.openaire.eu/search/publication?articleId=od________18::0e0aaae71c134766acf27427f97258be) This reference dicusses multi-agent learning models, and introduces a simple "two matrix game" as an example of a multi-agent game. The aforementioned code plays this game.

- [A Survey and Critique of Multiagent Deep Reinforcement Learning](https://arxiv.org/abs/1810.05587) This paper provides an overview of multi-agent learning techniques and algorithms in the literature. This is a helpful paper for exploring possibilities.


- [Reinforcement Learning by Sutton and Barto](https://mitpress.mit.edu/books/reinforcement-learning-second-edition) A fundamental book on reinforcement learning, the primary machine learning topic for teaching machines to learn games.

- Games and Decisions by Luce and Raiffa. 
      {Chris: This is an older text by Dover that Chris has read. It goes over the mathematical fundamentals of combinatorial game theory, includes definitions and descriptions for zero-sum games, imperfecti information, et cetera. A more modern reference incorporating algorithms and machine learning would be good.}
      
                      