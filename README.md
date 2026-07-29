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

## Moving around

You can only move to a node that's directly connected to where you are — no shortcuts through the graph. Two ways to pick where to go:

- follow Dijkstra's suggestion
- pick any other neighboring node manually

You can also Undo the last completed turn (this uses a Stack under the hood — we push a snapshot of the game state before every turn). Undo isn't available until you've actually finished at least one turn, since there's nothing on the stack yet.

The wolf only moves on an even die roll (six-sided die), and when it does move it uses BFS to find the shortest path to the player and takes exactly one step along it.

## Scoring

| What happened | Points |
|---|---|
| Followed Dijkstra's suggested path | +3 |
| Moved somewhere else valid | +1 |
| Used Undo | -2 |
| Reached Grandma's house | +5 |

A few things worth noting:
- Score resets to 0 at the start of every round.
- Dijkstra reruns after every move, so the suggested path can change from one turn to the next.
- If the wolf catches you before you reach the goal, you don't get the +5 bonus, but whatever you scored up to that point is still saved.
- Going back over a node you already visited is fine, it's scored like any normal move.
- Whatever you score in a round gets added to your total score once the game ends.

## Accounts / leaderboard

Signing up checks the username against a hash table so you can't register a duplicate name. Passwords are hashed (with a salt) before being saved — we never store them as plain text.

Logging in looks the username up in the same hash table and checks the password against the stored hash.

After logging in, you see the current top player (pulled from a MaxHeap). Your own score is looked up from a BST. Usernames are case-sensitive, so `Ali` and `ali` count as two different accounts.