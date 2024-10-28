import re

class Graph:
    def __init__(self):
        self.vertices = [] # list of tuples (X position, Y position)
        self.edges = [] # list of tuples (vertex1, vertex2) 

        self.vertLen = 0
        self.vertLenSq = 0

    def _indexInternal(self, k, i, j):
        if i < 0 or j < 0 or i >= self.vertLen or j >= self.vertLen:
            raise IndexError("Indices outside of bounds")
        
        return k * self.vertLenSq + i * self.vertLen + j + 1

    def _getEdgeConnectionIndex(self, i, j):
        return self._indexInternal(0,i,j)

    def _getEdgeRedColorIndex(self, i, j):
        return self._indexInternal(1,i,j)

    def _getEdgeBlueColorIndex(self, i, j):
        return self._indexInternal(2,i,j)

    def createCNFFormula(self):
        result = []
        
        # rule 0 (defining whether there's an edge between i and j)
        for i in range(self.vertLen):
            for j in range(self.vertLen):
                connIndex = -self._getEdgeConnectionIndex(i,j)
                if j in self.edges[i]:
                    connIndex *= -1
                    
                result.append([connIndex])
        
        # rule 1 (at least one color of an edge)
        for i in range(self.vertLen):
            for j in range(self.vertLen):
                connIndex = -self._getEdgeConnectionIndex(i,j)
                redIndex  = self._getEdgeRedColorIndex(i,j)
                blueIndex = self._getEdgeBlueColorIndex(i,j)
                
                result.append([connIndex, redIndex, blueIndex])
            
        # rule 2 (at least NOT one color of an edge)
        for i in range(self.vertLen):
            for j in range(self.vertLen):
                connIndex = -self._getEdgeConnectionIndex(i,j)
                redIndex  = -self._getEdgeRedColorIndex(i,j)
                blueIndex = -self._getEdgeBlueColorIndex(i,j)
                
                result.append([connIndex, redIndex, blueIndex])
                
        # rule 3 (no color if not connected)
        for i in range(self.vertLen):
            for j in range(self.vertLen):
                connIndex = self._getEdgeConnectionIndex(i,j)
                redIndex  = -self._getEdgeRedColorIndex(i,j)
                blueIndex = -self._getEdgeBlueColorIndex(i,j)
                
                result.append([connIndex, redIndex])
                result.append([connIndex, blueIndex])
                
        # rule 4 (if there's an triangle, it's not monochromatic)
        for i in range(self.vertLen):
            for j in range(self.vertLen):
                for k in range(self.vertLen):
                    if i == j or i == k or j == k:
                        continue
                    
                    ijConn = -self._getEdgeConnectionIndex(i,j)
                    ikConn = -self._getEdgeConnectionIndex(i,k)
                    jkConn = -self._getEdgeConnectionIndex(j,k)
                    
                    ijRed  = -self._getEdgeRedColorIndex(i,j)
                    ikRed  = -self._getEdgeRedColorIndex(i,k)
                    jkRed  = -self._getEdgeRedColorIndex(j,k)
                    
                    ijBlue = -self._getEdgeBlueColorIndex(i,j)
                    ikBlue = -self._getEdgeBlueColorIndex(i,k)
                    jkBlue = -self._getEdgeBlueColorIndex(j,k)
                    
                    result.append([ijConn, ikConn, jkConn, ijRed, ikRed, jkRed])
                    result.append([ijConn, ikConn, jkConn, ijBlue, ikBlue, jkBlue])
                            
        return result


    @staticmethod
    def fromFile(filename):
        result = Graph()
        tmpEdges = []

        with open(filename, "r") as f:
            lines = f.readlines()
            readingVertices = True
            
            for index, line in enumerate(lines):
                matchVertex  = re.match(r"^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)(\s*|\s*#.*)$", line)
                matchEdge    = re.match(r"^\s*(\d+)\s*-\s*(\d+)(\s*|\s*#.*)$", line)
                matchDivider = re.match(r"^=+(\s*|\s*#.*)$", line)
                
                if matchDivider and not readingVertices:
                    raise Exception(f"Line {index+1}: Divider can be only declared once.")
                
                if matchDivider:
                    result.vertLen = len(result.vertices)
                    
                    if(result.vertLen <= 2):
                        raise Exception(f"Line {index+1}: Think about it. Do you really want to test this problem if you have less than three vertices?")
                    
                    result.vertLenSq = len(result.vertices)**2
                    readingVertices = False
                    continue

                if matchVertex and not readingVertices:
                    raise Exception(f"Line {index+1}: Vertex can be only defined above divider.")

                if matchVertex:
                    result.vertices.append((int(matchVertex[1]), int(matchVertex[2])))
                    continue

                if matchEdge and readingVertices:
                    raise Exception(f"Line {index+1}: Edge can be only defined under divider.")

                if matchEdge:
                    newEdge = (int(matchEdge[1]), int(matchEdge[2]))
                    if newEdge[0] == 0 or newEdge[1] == 0 or newEdge[0] > result.vertLen or newEdge[1] > result.vertLen:
                        raise Exception(f"Line {index+1}: Edge has a bad index.")
                    
                    for e in tmpEdges:
                        if (newEdge[0] == e[0] and newEdge[1] == e[1]) or (newEdge[0] == e[1] and newEdge[1] == e[0]):
                            raise Exception(f"Line {index+1}: This edge has already been defined, parallel edges aren't allowed.")
                    tmpEdges.append(newEdge)
                    continue
                
                raise Exception(f"Line {index+1}: Unknown format")
        
        for i in range(result.vertLen):
            result.edges.append([])
            
        for tmpE in tmpEdges:
            result.edges[tmpE[0]-1].append(tmpE[1]-1)
            result.edges[tmpE[1]-1].append(tmpE[0]-1)

        return result
