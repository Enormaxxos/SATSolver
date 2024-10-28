#!/usr/bin/env python3

# from Graph import Graph

# from tkinter import Canvas

# main = Canvas(width=800, height=800)
# main.pack()

# main.mainloop()

import sys
import os
import Visualizer
from Graph import Graph
from pysat.solvers import Glucose4


def printUsage():
    print("Usage: solver.py <input file>")

def createGraph():
    return Graph.fromFile(sys.argv[1])

def main():
    if len(sys.argv) != 2:
        print("Error: Incorrect number of arguments.")
        printUsage()
        return
    
    if not os.path.exists(sys.argv[1]):
        print(f"Error: File {sys.argv[1]} doesn't exist.")
        printUsage()
        return
    
    g = Graph.fromFile(sys.argv[1])
    cnf = g.createCNFFormula()
    # print(g.vertices)
    # print(g.edges)
    # print(cnf)
    
    solver = Glucose4()
    for clause in cnf:
        solver.add_clause(clause)
        
    if solver.solve():
        Visualizer.visualize(g, [ x > 0 for x in solver.get_model()])
    else:
        print("This graph has no solution.")

if __name__ == "__main__":
    main()