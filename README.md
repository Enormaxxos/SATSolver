# Monochromatic triangle
- Created by **Petr Pelikan** as a project for course NAIL062 on 
Charles University, Faculty of Mathematics and Physics.

## Dependencies

This solution depends on two external libraries
- `tk` - to visualize results.
- `python-sat` - to import Glucose4 solver.

I recommend creating Python virtual environment and installing these libraries in this venv.

## Usage

- Run solver with `solver.py <filename1> <filename2> ...` to run as many graphs as you want.
    - Recommended:
        - `cd` to root of the project
        - `./solver.py ./tests/*`
- To understand input file format, look at [this file](./tests/testFirst.in).

## Problem

The monochromatic triangle problem takes as input an n-node undirected graph G(V,E) with node set V and edge set E. The output is a Boolean value, true if the edge set E of G can be partitioned into two disjoint sets E1 and E2, such that both of the two subgraphs G1(V,E1) and G2(V,E2) are triangle-free graphs, and false otherwise.

## Theory

### Definitions
- $x_{ij}$ - vertices $v_i, v_j$ are connected with an edge
- $y_{ij}^k$ - edge connecting $v_i$ and $v_j$ has color $k$

### Theory
1) $\forall i,j( x_{ij} \rightarrow (y_{ij}^1\ \lor\ y_{ij}^2))$
    - if $v_i$ and $v_j$ are connected with an edge, it has at least one color
    - Process to CNF:
        - $\forall i,j( x_{ij} \rightarrow (y_{ij}^1\ \lor\ y_{ij}^2))$
        - $\forall i,j( \lnot x_{ij}\ \lor\ (y_{ij}^1\ \lor\ y_{ij}^2) )$
        - $\textcolor{red}{\forall i,j( \lnot x_{ij}\ \lor\ y_{ij}^1\ \lor\ y_{ij}^2 )}$
2) $\forall i,j( x_{ij} \rightarrow (\lnot y_{ij}^1 \lor \lnot y_{ij}^2))$
    - if $v_i$ and $v_j$ are connected with an edge, it doesn't have at least one color
    - Process to CNF:
        - $\forall i,j( x_{ij} \rightarrow (\lnot y_{ij}^1\ \lor\ \lnot y_{ij}^2))$
        - $\forall i,j( \lnot x_{ij}\ \lor\ (\lnot y_{ij}^1\ \lor\ \lnot y_{ij}^2) )$
        - $\textcolor{red}{\forall i,j( \lnot x_{ij}\ \lor\ \lnot y_{ij}^1\ \lor\ \lnot y_{ij}^2 )}$
3) $\forall i,j(\lnot x_{ij} \rightarrow (\lnot y_{ij}^1\ \land\ \lnot y_{ij}^2))$
    - if $v_i$ and $v_j$ aren't connected with an edge, it does not have any color
    - Process to CNF:
        - $\forall i,j( \lnot x_{ij} \rightarrow (\lnot y_{ij}^1\ \land\ \lnot y_{ij}^2))$
        - $\forall i,j( x_{ij}\ \lor\ (\lnot y_{ij}^1\ \land\ \lnot y_{ij}^2))$
        - $\textcolor{red}{\forall i,j( (x_{ij}\ \lor\ \lnot y_{ij}^1)\ \land\ (x_{ij}\ \lor\ \lnot y_{ij}^2))}$
4) $\forall i,j,k; i \neq j; i \neq k; j \neq k((x_{ij}\ \land\ x_{ik}\ \land\ x_{jk}) \rightarrow (\lnot( y_{ij}^1\ \land\ y_{ik}^1\ \land\ y_{jk}^1) \land \lnot( y_{ij}^2\ \land\ y_{ik}^2\ \land\ y_{jk}^2)))$
    - if there's an edge between $v_{i}-v_{j}$, $v_{i}-v_{k}$ and $v_{j}-v_{k}$, they are not all the same color
    - Process to CNF:
        - $\forall i,j,k((x_{ij}\ \land\ x_{ik}\ \land\ x_{jk}) \rightarrow (\lnot( y_{ij}^1\ \land\ y_{ik}^1\ \land\ y_{jk}^1) \land \lnot( y_{ij}^2\ \land\ y_{ik}^2\ \land\ y_{jk}^2)))$
        - $\forall i,j,k(\lnot (x_{ij}\ \land\ x_{ik}\ \land\ x_{jk})\ \lor\ ((\lnot y_{ij}^1\ \lor\ \lnot y_{ik}^1\ \lor\ \lnot y_{jk}^1)\ \land\ (\lnot y_{ij}^2\ \lor\ \lnot y_{ik}^2)\ \lor\ \lnot y_{jk}^2))$
        - $\textcolor{red}{\forall i,j,k((\lnot x_{ij}\ \lor\ \lnot x_{ik}\ \lor\ \lnot x_{jk}\ \lor\ \lnot y_{ij}^1\ \lor\ \lnot y_{ik}^1\ \lor\ \lnot y_{jk}^1)\ \land\ (\lnot x_{ij}\ \lor\ \lnot x_{ik}\ \lor\ \lnot x_{jk}\ \lor\ \lnot y_{ij}^2\ \lor\ \lnot y_{ik}^2\ \lor\ \lnot y_{jk}^2))}$