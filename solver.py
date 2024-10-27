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
    
    if os.path.exists("./tmp.in"):
        os.remove("./tmp.in") # remove cnf file if it exists somehow
    
    with open("./tmp.in", "x") as f:
        f.write(cnf) # write cnf formula to input file
        
    os.system("./glucose_static ./tmp.in ./tmp.out >/dev/null") # run glucose solver
    os.remove("./tmp.in") # remove input file
    
    Visualizer.visualize(g, "./tmp.out")

if __name__ == "__main__":
    main()