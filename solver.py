#!/usr/bin/env python3

# from Graph import Graph

# from tkinter import Canvas

# main = Canvas(width=800, height=800)
# main.pack()

# main.mainloop()

import sys
from Graph import Graph

g = Graph.fromFile(sys.argv[1])
print(g.vertices)
print(g.edges)
print(g.createCNFFormula())