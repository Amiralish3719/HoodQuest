# HoodQuest: The Algorithm Forest

**Final Project — Data Structures and Algorithms Course**

> *"In the forest of data, choose the right path, and every algorithm leads you home."*

---

## Introduction

Little Red Riding Hood is a kind girl who lives with her family near a forest. Her grandmother has fallen ill, and as usual, her mother has prepared a few cookies for her to bring to Grandma's house. But crossing the forest isn't simple: a hungry wolf roams the paths, and at any moment it may change course toward Little Red Riding Hood.

In this game, the player must guide Little Red Riding Hood through the forest — modeled as a **weighted, undirected graph** — by choosing the right paths, and reach Grandma's house (the safe node) before the wolf catches her. Every decision can either bring her closer to safety or one step closer to danger.

This project was built to design and implement a simulation game grounded in the core concepts of the Data Structures and Algorithms course. Concepts such as **graphs, stacks, queues, hash tables, binary search trees (BST), heaps**, and pathfinding algorithms like **Dijkstra, BFS, and A\*** are all put to practical use within one cohesive game.

---

Final project for our Data Structures and Algorithms course.

The idea is simple: Little Red Riding Hood has to cross a forest (modeled as a graph) and reach Grandma's house before the wolf gets to her. Along the way we had to use a bunch of the stuff we learned this semester — graphs, stacks, queues, hash tables, a BST, a heap, and pathfinding with Dijkstra/BFS/A*.

## Files

- `main.py` – the menus and the main game loop (this is what you run)
- `game.py` – the actual game logic: player/wolf movement, Undo, scoring
- `graph.py` – the Graph class, Dijkstra, BFS, A*, and the map itself
- `data_structures.py` – our own Stack, Queue, HashTable, MaxHeap and BST
- `user_system.py` – sign up / login / password hashing / saving scores to disk

None of the data structures or the Dijkstra/BFS implementations use Python's built-in stuff (no `heapq`, no `collections.deque`) — we wrote all of that ourselves, since that was one of the requirements.

## How to run it

You just need Python 3, nothing else to install.

```bash
python3 main.py
```

It'll ask you to sign up or log in first, then you get a dashboard where you can start a game, check the leaderboard, or read the instructions.

## The map

The forest is a weighted, undirected graph. Node `V` is Grandma's house. When a game starts, the player and the wolf both get random starting positions, the only rule being that neither of them starts on `V` and they don't start on the same node as each other.

Once the game starts, we run Dijkstra from the player's position to `V` and show that as the suggested path.

## Turn order

Every turn goes through the same sequence:

1. Run Dijkstra from the player to V
2. Show the suggested path / next node
3. Player either moves or hits Undo
4. Move gets applied, score gets updated
5. Check if the player reached V (win)
6. Check if the player walked into the wolf (instant loss)
7. Roll a die for the wolf
8. If the roll is even, the wolf moves one step using BFS
9. Check if the wolf landed on the player (loss)
10. Next turn

Game ends either when the player reaches `V` (win) or the player and the wolf end up on the same node (loss). If you walk straight into the wolf's cell, you lose right away — you don't wait around for its turn.