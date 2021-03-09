from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
import algorithms

class Polygon(algorithms.Polygon):

    polygonEdges = set()

    def __init__(self, details):
        super().__init__(0, [])
        self.details = details

    def addPoint(self, point):
        self.vertices.append(point)

    def checkValid(self):

        for i,eachEdge in enumerate(self.edges):

            for anotherEdge in Polygon.polygonEdges:
                if algorithms.Polygon.intersect(eachEdge, anotherEdge):
                    return False

            for j,anotherEdge in enumerate(self.edges):
                if i==j:
                    continue
                if algorithms.Polygon.intersect(eachEdge, anotherEdge):
                    return False
        return True

    def enhance(self):
        pass

    def doneAddingPoints(self):
        self.vertices = [*self.vertices, self.vertices[0]]
        self.n = len(self.vertices)
        self.build()
        self.drawPolygon()
        return self.checkValid


    def drawPolygon(self):
        self.line = Line(points = self.vertices, width = 2, joint = 'miter', close = True)
