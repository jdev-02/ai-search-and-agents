# AI Search and Agent Architectures

Implementations of foundational AI concepts from Russell & Norvig's *Artificial Intelligence: A Modern Approach*, plus a formal system solver from Hofstadter's *Gödel, Escher, Bach*.

## Contents

### lab-1-agent-architectures
Four intelligent agent architectures implemented and benchmarked in a vacuum-world environment:

| Agent Type | Avg Score |
|------------|-----------|
| Random | -3 |
| Reflex | 17 |
| Table-Driven | ~17 |
| Model-Based | **38** |

The model-based agent maintains an internal world state, allowing it to avoid revisiting clean squares — producing significantly better performance.

### lab-2-search-algorithms
Uninformed search algorithms applied to classic AI problems:
- **BFS** and **DFS** — implemented from scratch with frontier/explored-set cycle detection
- **Eight Puzzle** — state-space search with tuple-based state representation
- **Maze Solver** — reads a maze from an Excel file, finds the shortest path using BFS

### lab-3-search-extended
Extended search work building on lab-2 implementations.

### formal-system-miu-solver
A BFS-based solver for the **MIU formal system** from Hofstadter's *GEB*. Starting from the axiom "MI", applies 4 transformation rules to derive a target string. Includes full path-tracking — prints each derivation step and which rule was applied. Terminates gracefully if no derivation is found within the search limit.

## Technologies

Python · Jupyter Notebooks · NumPy

## Background

Naval Postgraduate School · CS3310 AI Basics / CS3001 Discrete Math · 2024–2025
