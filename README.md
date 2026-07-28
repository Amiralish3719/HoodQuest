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