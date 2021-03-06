# Math5800Spring2020
Github Page for Math 5800 Spring 2020 at UCONN

Taught by Professor Jeremy Teitelbaum, https://jeremy9959.net/

Group members Christopher Hayes, Evelyn Nitch-Griffin

Basic idea. We are interested in multi-agent games, most notably Hanabi, as opposed to zero-sum or adversarial games. Hanabi is a cooperative game that requires players to make choices and inferences based on the actions of others.

References

- [The Hanabi Challenge: A New Frontier for AI Research](https://arxiv.org/abs/1902.00506) {Chris: Introduces the game, includes an open source self-playing program, and compares results of learning-agent bots with rule-based bots, collaborations between such, et cetera. No large data sets seem to be involved - unsure how it relates to data science. Published 2020 in AI (Elsevier)}

- The associated platform for this article is found at: https://github.com/deepmind/hanabi-learning-environment

- [Simplified Action Decoder for Deep Multi-Agent Reinforcement Learning 2020](https://openreview.net/forum?id=B1xm3RVtwB)
- [With associated code](https://colab.research.google.com/drive/1Cvs4GuFvHEdvb7tVJQVvQOviAkRf97r7) {Chris: What does the code actually do?} 

- [Bayesian Action Decoder](https://explore.openaire.eu/search/publication?articleId=od________18::0e0aaae71c134766acf27427f97258be) This reference dicusses multi-agent learning models, and introduces a simple "two matrix game" as an example of a multi-agent game. The aforementioned code plays this game.

- [A Survey and Critique of Multiagent Deep Reinforcement Learning](https://arxiv.org/abs/1810.05587) This paper provides an overview of multi-agent learning techniques and algorithms in the literature. This is a helpful paper for exploring possibilities.


- [Reinforcement Learning by Sutton and Barto](https://mitpress.mit.edu/books/reinforcement-learning-second-edition) A fundamental book on reinforcement learning, the primary machine learning topic for teaching machines to learn games.

- Games and Decisions by Luce and Raiffa. 
      {Chris: This is an older text by Dover that Chris has read. It goes over the mathematical fundamentals of combinatorial game theory, includes definitions and descriptions for zero-sum games, imperfecti information, et cetera. A more modern reference incorporating algorithms and machine learning would be good.}
      
                        To Do List
- Split py file into several different files and make interaction very clear
- Clean up code and comment it
- Fix bug that happens when board is full
- Function to combine .csv files
- Function convert .csv files data to Evelyn version
- Learn pytorch Stuph
- Fit code into Pytorch
- Neural Network I guess
- Fix data-based apparoach AI
