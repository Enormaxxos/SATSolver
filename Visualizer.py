from tkinter import Canvas
from Graph import Graph

vertexSize = 10

def convertToBoolList(modelText):
    if "UNSAT" in modelText:
        return None
    return [int(x) > 0 for x in filter(lambda x: int(x) != 0, modelText.split(" "))]

def drawLine(index, graph, color, canvas):
    fromIndex = int(index / graph.vertLen)
    toIndex = int(index % graph.vertLen)
    
    canvas.create_line(graph.vertices[fromIndex][0], graph.vertices[fromIndex][1],graph.vertices[toIndex][0],graph.vertices[toIndex][1], fill=color, width=5)

def visualize(graph, file):
    model = []
    with open(file, "r") as f:
        model = convertToBoolList(f.read())
        
    if not model:
        print("This graph has no solution.")
        return
    
    main = Canvas(width=800, height=800)
    main.pack()
    
    for vert in graph.vertices:
        main.create_oval(vert[0]-vertexSize, vert[1]-vertexSize, vert[0]+vertexSize, vert[1]+vertexSize, fill="BLACK")
        
    for index, value in enumerate(model):
        if value == False:
            continue
        
        if index < graph.vertLenSq:
            drawLine(index,graph, "BLACK", main)
            continue
        
        if index < graph.vertLenSq * 2:
            drawLine(index - graph.vertLenSq, graph, "RED", main)
            continue
        
        drawLine(index - (graph.vertLenSq * 2), graph, "BLUE", main)
    
    main.mainloop()
        