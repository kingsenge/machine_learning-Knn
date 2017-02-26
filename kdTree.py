import math

class KdNode:
    def __init__(self,parent,*param):
        self.left = None
        self.right = None
        self.parent = parent
        
        self.dimen = []
        for i in param:
            self.dimen.append(i)

    def setLeft(self,LTree):
        self.left = LTree

    def setRight(self,rtree):
        self.right = rtree
        
    def leftTree(self):
        return self.left

    def rightTree(self):
        return self.right

    def getParent(self):
        return self.parent

    def calDistance(self,pos):
        total = 0
        x = self.dimen[0] - pos[0]
        y = self.dimen[1] - pos[1]
        total = math.sqrt(x*x + y*y)
        return total

    def compare(self,node):
        if(self.dimen[self.dimen[2]]>node[self.dimen[2]]):
            return 0
        else:
            return 1

    def IsCross(self, x, y):
        if (self.dimen[2] == 0):
            if (x[0] <= self.dimen[0] <= x[1]):
                return 1
        elif (y[0] <= self.dimen[1] <= y[1]):
            return 1

        return 0

def ConstructTree(T,Deep,parent):
    if(len(T) == 1):
        dimen = (Deep+1)%2
        node = T[0]
        return KdNode(parent,node[0],node[1],dimen)
    elif(len(T) == 0):
        return
    
    dimen = (Deep+1)%2
    T.sort(key = lambda x:x[dimen])

    partition = int(len(T)/2);
    root = T[partition]
    rootNode = KdNode(parent,root[0],root[1],dimen)
    rootNode.setLeft(ConstructTree(T[0:partition],Deep+1,rootNode))
    rootNode.setRight(ConstructTree(T[partition+1:],Deep+1,rootNode))
    
    return rootNode

def SearchTree(tree,node):
    preTree = tree
    while(tree != None):
        preTree = tree
        if(tree.compare(node)== 0):
            tree = tree.leftTree()
        else:
            tree = tree.rightTree()
    return preTree

def searchChildTree(tree,x,y,node,minLen):
    minNode = None
    while(tree!=None):
        if(tree.IsCross(x,y)==1):
            tmplen = tree.calDistance(node)
            if (tmplen < minLen):
                minLen = tmplen
                minNode = tree
                x[0] = (node[0] - minLen)
                x[1] = (node[0] + minLen)
                y[0] = (node[1] - minLen)
                y[1] = (node[1] + minLen)

        if (tree.dimen[2] == 0):
            if (tree.dimen[0] < x[0]):
                tree = tree.left
            else:
                tree = tree.right
        else:
            if (tree.dimen[1] < y[0]):
                tree = tree.left
            else:
                tree = tree.right

    return (minNode,minLen)

def GetMinNode(minNode,node):
    minLen = minNode.calDistance(node)
    backupNode = minNode
    x = [0,0]
    x[0] = (node[0]-minLen)
    x[1] = (node[0]+minLen)
    y = [0,0]
    y[0] = (node[1] - minLen)
    y[1] = (node[1] + minLen)

    while(backupNode != None):
        parent = backupNode.getParent()
        if(parent==None):
            return minNode

        if(parent.IsCross(x,y)==0):
            backupNode = parent
            continue

        tmplen = parent.calDistance(node)
        if(tmplen < minLen):
            minLen = tmplen
            minNode = parent
            x[0] = (node[0] - minLen)
            x[1] = (node[0] + minLen)
            y[0] = (node[1] - minLen)
            y[1] = (node[1] + minLen)

        result = None
        if(backupNode == parent.left):
            result = searchChildTree(parent.right,x,y,node,minLen)
        else:
            result = searchChildTree(parent.left,x,y,node,minLen)

        if(result[0]!=None):
            minNode = result[0]

        backupNode = parent

    return minNode


T = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]

tree = ConstructTree(T,1,None)

pox = (2,4.5)

minNode = SearchTree(tree,pox)

minNode = GetMinNode(minNode,pox)

print(minNode.dimen[0],minNode.dimen[1])
