from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
import algorithms

# A polygon class that handles all obstacles
# added on screen
class Polygon(algorithms.Polygon):

    # Static variable to keep all edges
    # of all the polygons, this will be
    # to check line intersections
    polygonEdges = set()
    polygonPoints = set()

    def __init__(self, details):
        super().__init__(0, [])
        self.details = details

    def addPoint(self, point):
        if point in Polygon.polygonPoints:
            return False
        self.vertices.append(point)
        Polygon.polygonPoints.add(point)
        return True

    # Check if polygon is not a complex polygon
    # And number of vertices are >= 3
    def checkValid(self):

        flag = True
        for i,eachEdge in enumerate(self.edges):

            for anotherEdge in Polygon.polygonEdges:
                if algorithms.Polygon.intersect(eachEdge, anotherEdge):
                    flag = False

            for j in range(i+1, len(self.edges)):
                anotherEdge = self.edges[j]

                if algorithms.Polygon.commonVertex(eachEdge, anotherEdge):
                    continue
                if algorithms.Polygon.intersect(eachEdge, anotherEdge):
                    flag = False

        flag = flag and self.n>2
        if flag:
            Polygon.polygonEdges.update(self.edges)

        return flag

    def enhance(self):
        pass

    # if user is done adding the points
    # compile the polygon
    def doneAddingPoints(self):
        # self.vertices = [*self.vertices, self.vertices[0]]
        self.n = len(self.vertices)
        self.build()
        self.drawPolygon()
        return self.checkValid()

    # draw the polygon on screen
    def drawPolygon(self):
        self.line = Line(points = self.vertices, width = 2, joint = 'miter', close = True)
