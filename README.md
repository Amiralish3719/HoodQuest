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

## Where each data structure is actually used

| Structure/Algorithm | Used for |
|---|---|
| Graph | the map itself |
| Stack | Undo |
| Queue | used inside BFS |
| HashTable | user accounts (sign up / login) |
| MaxHeap | leaderboard / top player |
| BST | looking up a specific user's score |
| Dijkstra | suggested shortest path for the player |
| BFS | wolf's movement |
| A* | alternative suggested path (extra credit part) |

## Extra credit stuff we added

- User scores are also kept in a BST so looking up one specific player's score is faster than scanning through everything.
- Besides Dijkstra, there's an A* option too — you can ask for an A* suggested path as an alternative.

## Notes from actually building this

A couple of things came up while we were building/testing this that are probably worth mentioning:

- We had a bug in the Undo logic where if you hit Undo in the middle of a turn (before finishing it), the snapshot that later got pushed to the stack was stale — so a second Undo could restore you to the wrong state. Fixed by re-grabbing the snapshot right after a successful Undo instead of only once at the start of the turn.
- At one point `push_completed_turn` ended up with wrong indentation and got nested inside `wolf_turn()` (after a `return`, so it never even ran) — that gave an `AttributeError` the first time we actually tried to finish a turn in the game. Moving it back out to be its own method on `HoodQuestGame` fixed it.

Both of these only showed up once we actually played through the game a bunch of times rather than just reading the code, so — test your stuff, even if it "looks right."

## Team

- ** Amin Mohammad Jabbari ** – worked on `user_system.py` and `game.py` and `main.py`
- ** Amirali Sheikh Hassani ** – worked on `data_structures.py` and `graph.py`