<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>README</title>
  <style>
    code{white-space: pre-wrap;}
    span.smallcaps{font-variant: small-caps;}
    span.underline{text-decoration: underline;}
    div.column{display: inline-block; vertical-align: top; width: 50%;}
    div.hanging-indent{margin-left: 1.5em; text-indent: -1.5em;}
    ul.task-list{list-style: none;}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" type="text/javascript"></script>
  <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv-printshiv.min.js"></script>
  <![endif]-->
</head>
<body>
<h1 id="math5800-spring-2020-mathematical-aspects-of-machine-learning">Math5800 Spring 2020: Mathematical Aspects of Machine Learning</h1>
<p>This is the Github Page for Math 5800 Spring 2020 at UCONN, taught by Professor <a href="https://jeremy9959.net/">Jeremy Teitelbaum</a></p>
<p>Group members Christopher Hayes, Evelyn Nitch-Griffin</p>
<p>We are interested in reinforcment learning problems in games. In this project, we focused on Connect Four, a zero-sum game between two players. The goal was to create a functioning reinforcment learning model in Python.</p>
<h2 id="reinforcement-learning">Reinforcement Learning</h2>
<p>Reinforcment learning is a machine learning problem where an agent (such as a person, program, or robot) is attempting a maximize a reward output. For Connect Four, our agent is the player, and our reward output is winning or losing the game. The agent interacts with its environment and receives rewards and penalties based on its actions. In an attempt to maximine rewards, it learns the optimal behavior overtime. A famous example of this being applied recently is <a href="https://deepmind.com/research/case-studies/alphago-the-story-so-far">AlphaGo</a>, a computer program developed by Deepmind which consistently beat top human Go players.</p>
<h4 id="exploration-vs-exploitation">Exploration vs Exploitation</h4>
<p>One of the most fundamental problems in machine learning is the tradeoff between exploration vs exploitation. Explorating is when an agent takes actions that may not always be optimal, but help it determine the possible best actions. Exploitation is when an agent takes the <strong>currently perceived</strong> best action. An agent that explores too much might take too long (and waste posible resources) to find the optimal solution. An agent that explots too much may move towards a suboptimal solution. Operationalizing this and finding the correct balance is an important task for all reinforcment learning problems</p>
<h2 id="finite-markhov-decision-processes">Finite Markhov Decision Processes</h2>
<p>A Markhov Decision Process (MDP) is determined by 4 things: an agent, a environment (or a set of possible states), a set of actions, and a reward. Over a series of time steps <span class="math inline">\((t=0,1, ...)\)</span>, the agent interacts with the environment by taking an action, and then receives a reward. This yields a sequences of states, actions, and rewards.</p>
<p><span class="math display">\[
S_0, A_0, R_0, \rightarrow S_1, A_1, R_1 \rightarrow ...
\]</span></p>
<p>This is often notationally represented in the following way.</p>
<p><span class="math display">\[
(S, A, \{P_{sa}\}, \gamma, R)
\]</span> for the states, actions, state transition distribution, discount factor, and rewards. The state transition distribution determines the probabilities for moving into a state after taking a certain action, and gamma is a discounting factor that weights earlier rewards over later rewards <span class="math inline">\((0 &lt; \gamma \leq 1)\)</span>.</p>
<p>In the FMDP, there are a finite amount of states, actions, and rewards. In our Connect Four problem, our states would be the possible board configurations, our actions would be placing a piece in a (non-full) column, and our rewards are +1 for winning, 0 for ties, and -1 for losing. Here the state transition probability represents our opponent’s move. We choose <span class="math inline">\(\gamma\)</span> to be 1, which means we don’t discount; we only care about winning in the long term.</p>
<p>When we are in a state, we have a selection of actions that we can take. Each action is followed by an action of our opponent, which presents a new state before us. If our opponent is predictable, we could operationalize a state transition probability.</p>
<p><span class="math display">\[
p(s^{&#39;},r|s,a) = Pr\{S_{t} = s^{&#39;}, R_{t} = r| S_{t-1}=s, A_{t-l} = a\}
\]</span> which is the probability of the state <span class="math inline">\(s^{&#39;}\)</span> and reward <span class="math inline">\(r\)</span> happening after we take the action <span class="math inline">\(a\)</span> in the current state <span class="math inline">\(s\)</span>. In the Connect Four problem, this represents likely following board states that is are presented to us after we and our opponent make our moves. The probabilities would represent the likelyhood our opponent takes which actions. Although perhaps counterintuitive, our state space only represents the board states that are <strong>presented to the agent</strong>.</p>
<p>In a general problem, the state transition probability could repreent many things, such as the likely outcomes of a slot machine. The flexible nature of the Markhov Decision Process allows it to be applied to many different problems.</p>
<h5 id="the-markhov-property">The Markhov Property</h5>
<p>In the MDP the state transition probabilities completely characterize the dynamics of the environment. The state is said to have the Markhov property if the probabilites of future states depends only on the <em>current state</em>, irrelevant of the sequence of events that led to the state. This is sometimes called the memoryless property, because what determines the best action depends only of the current state. Connect Four has the Markhov property, as do almost all other board games, because in order to make the best move you only need to know the current board state. The actions that led up to that state are irrelevant to winning.</p>
<h5 id="policies-and-values">Policies and Values</h5>
<p>A policy <span class="math inline">\(\pi\)</span> is the agent’s methods for selecting its actions. It can be viewed as a probability distributirepresenting the likelyhood of certain actions given a state. We can also think about the <strong>value</strong> of a state given a policy <span class="math inline">\(\pi\)</span>. This is represented by <span class="math inline">\(V_{\pi}\)</span>, and is the expected <em>total</em> payoff starting in a state <span class="math inline">\(s\)</span> and following the policy <span class="math inline">\(\pi\)</span>. Because we are in a Markhov decision process, we can utilize Bellman’s equation.</p>
<p><span class="math display">\[
V_{\pi}(s) = R(s) + \gamma\sum_{s&#39;}p(s&#39;|s,\pi(s))V_{\pi}(s&#39;)
\]</span></p>
<p>Essentially, Bellman’s equation states that the expected payoff of a state given a policy <span class="math inline">\(\pi\)</span> is determined by its successor states. In a Finite MDP, if the state transition probabilities are known, this gives a series of linear equations, which could be solved to calculate the state value. However, things usually aren’t that simple.</p>
<p>Generally, many reinforcment learning problems are oriented towards estimating state values. By knows which states are higher valued, you can change your policy to favor high valued states. Over time, you should eventually move towards a optimal policy.</p>
<h3 id="our-code">Our Code</h3>
<p>Our python defines a Connect Four board, and allows us to simulate games. To begin, we implemented a rudimentary Monte Carlo AI. Given a board state, it looks at the possible moves and plays out a certain number of random games. Then, it picks the move that led to the most number of random wins. Essentially, this is a basic value estimation method.</p>
<p>We also implement a beginning Monte Carlo value estimation method. First, we generated a state database using the Monte Carlo AI. The value of the state was determined by averaging Bellman equation above. <span class="math display">\[
V(s) = \frac{\sum wins -\sum losses}{visits}
\]</span> Then, the policy is to make the move that generates the best value, with a small chance to take a random move to continue exploring different actions. This is often called a <span class="math inline">\(\epsilon\)</span> greedy policy, because it takes the currently best perceived action with an <span class="math inline">\(\epsilon\)</span> chance to explore.</p>
<p>Finally, we have yet to implement a neural network. The plan is to use pytorch or a self created network that trains on the database above. Then, it outputs a probability distribution for the possible moves, where each move is assigned a non-zero probability. This is so that we always have a chance to exploore to update the network.</p>
<h3 id="references">References</h3>
<ul>
<li><p><a href="https://arxiv.org/abs/1902.00506">The Hanabi Challenge: A New Frontier for AI Research</a> {Chris: Introduces the game, includes an open source self-playing program, and compares results of learning-agent bots with rule-based bots, collaborations between such, et cetera. No large data sets seem to be involved - unsure how it relates to data science. Published 2020 in AI (Elsevier)}</p></li>
<li><p>The associated platform for this article is found at: https://github.com/deepmind/hanabi-learning-environment</p></li>
<li><p><a href="https://openreview.net/forum?id=B1xm3RVtwB">Simplified Action Decoder for Deep Multi-Agent Reinforcement Learning 2020</a></p></li>
<li><p><a href="https://colab.research.google.com/drive/1Cvs4GuFvHEdvb7tVJQVvQOviAkRf97r7">With associated code</a> {Chris: What does the code actually do?}</p></li>
<li><p><a href="https://explore.openaire.eu/search/publication?articleId=od________18::0e0aaae71c134766acf27427f97258be">Bayesian Action Decoder</a> This reference dicusses multi-agent learning models, and introduces a simple “two matrix game” as an example of a multi-agent game. The aforementioned code plays this game.</p></li>
<li><p><a href="https://arxiv.org/abs/1810.05587">A Survey and Critique of Multiagent Deep Reinforcement Learning</a> This paper provides an overview of multi-agent learning techniques and algorithms in the literature. This is a helpful paper for exploring possibilities.</p></li>
<li><p><a href="https://mitpress.mit.edu/books/reinforcement-learning-second-edition">Reinforcement Learning by Sutton and Barto</a> A fundamental book on reinforcement learning, the primary machine learning topic for teaching machines to learn games.</p></li>
<li><p>Games and Decisions by Luce and Raiffa. {Chris: This is an older text by Dover that Chris has read. It goes over the mathematical fundamentals of combinatorial game theory, includes definitions and descriptions for zero-sum games, imperfecti information, et cetera. A more modern reference incorporating algorithms and machine learning would be good.}</p></li>
</ul>
</body>
</html>
