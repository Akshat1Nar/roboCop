import math
import random

class Polygon():

    def __init__(self, n, points):
        self.n = n
        self.vertices = points
        self.edges = []
        self.build()

    def __EQ__(self, other):
        if self.n!=other.n or self.vertices!=other.vertices:
            return False
        return True

    def build(self):
        for i in range(self.n):
            self.edges.append((self.vertices[i], self.vertices[(i+1)%self.n]))

    def edgePresent(self, edge):
        return edge in self.edges

class Circle():

    def __init__(self, center, radii):
        self.center = center
        self.radii = radii

    def checkPointinCircle(self, point):
        x, y = point[0], point[1]
        dist = math.sqrt( (x-self.center[0])**2 + (y-self.center[1])**2 )
        if dist<=self.radii:
            return True
        return False

class Triangle(Polygon):
    i = 0
    # COLORS  = [(0.925, 0, 0.543, 0.682),
    #            (0, 0.276, 0.769, 0.133),
    #            (0, 0.632, 0.792, 0.113),
    #            (0, 0.035, 0.129, 0.121),
    #            (0.924, 0.122, 0, 0.325)
    #           ]
    COLORS = set()


    def __init__(self, points):
        super().__init__(3, points)
        self.getCircumcircle()
        # self.color = Triangle.COLORS[Triangle.i]
        # self.color = (random.randint(0, 256)/255.0,
        #               random.randint(0, 256)/255.0,
        #               random.randint(0, 256)/255.0
        #              )
        while len(Triangle.COLORS)==Triangle.i:
            self.color = (random.randint(0, 100)/100.0,
                          random.randint(0, 100)/100.0,
                          random.randint(0, 100)/100.0,
                         )
            Triangle.COLORS.add(self.color)
        Triangle.i+=1

    def checkInCircumcircle(self, point):
        # return self.circumcircle.checkPointinCircle(point)
        A = self.vertices[0]
        B = self.vertices[1]
        C = self.vertices[2]

        a = A[0] - point[0]
        b = B[0] - point[0]
        c = C[0] - point[0]
        d = A[1] - point[1]
        e = B[1] - point[1]
        f = C[1] - point[1]
        g = a**2 + d**2
        h = b**2 + e**2
        i = c**2 + f**2

        return ( (a*e*i + d*h*c + b*f*g - b*d*i - f*h*a - c*e*g)>0 )

    # Find the circum circle of given triangle
    # https://en.wikipedia.org/wiki/Circumscribed_circle
    # Bull shit
    def getCircumcircle(self):
        A = self.vertices[0]
        B = self.vertices[1]
        C = self.vertices[2]

        modAsq = A[0]**2+A[1]**2
        modBsq = B[0]**2+B[1]**2
        modCsq = C[0]**2+C[1]**2

        Sx = (
                (modAsq*B[1]) + (modCsq*A[1]) + (modBsq*C[1]) -
                (modCsq*B[1]) - (modBsq*A[1]) - (modAsq*C[1])
             ) /2.
        Sy = (
                (modAsq*B[0]) + (modCsq*A[0]) + (modBsq*C[0]) -
                (modCsq*B[0]) - (modBsq*A[0]) - (modAsq*C[0])
             ) /-2.
        a =  (
                A[0]*B[1] + A[1]*C[0] + B[0]*C[1] -
                C[0]*B[1] - B[0]*A[1] - C[1]*A[0]
             ) *1.
        b =  (
                A[0]*B[1]*modCsq + A[1]*C[0]*modBsq + B[0]*C[1]*modAsq -
                C[0]*B[1]*modAsq + B[0]*A[1]*modCsq + C[0]*A[1]*modBsq
             ) *1.

        modSsq = Sx**2 + Sy**2
        assert a!=0

        self.circumcircle = Circle((Sx/a,Sy/a),math.sqrt(abs(b/a + modSsq/a**2 )))



class Delanuay():
    flag = 0

    def __init__(self, superPoints):

        self.triangulation = []
        self.points = set()
        self.superTriangle = Triangle(superPoints)
        self.triangulation.append(self.superTriangle)
        # Add super triangle to triangulation

    def addPoint(self, point):
        if point in self.points:
            return

        badTriangles = set()
        self.points.add(point)

        # find bad triangles
        for eachTriangle in self.triangulation:
            # if point in circumcircle
            if (eachTriangle.checkInCircumcircle(point)):
                badTriangles.add(eachTriangle)


        polygon = set()

        # form a polygon of with bad triangles
        for i,eachTriangle in enumerate(badTriangles):
            for eachEdge in eachTriangle.edges:
                revEachEdge = (eachEdge[1], eachEdge[0])
                if eachEdge in polygon:
                    polygon.remove(eachEdge)
                elif revEachEdge in polygon:
                    polygon.remove(revEachEdge)
                else:
                    polygon.add(eachEdge)
        # print(point)
        # print(polygon)
        # print()
        # print()

        # Remove bad triangles
        for eachTriangle in badTriangles:
            self.triangulation.remove(eachTriangle)

        # Retriangulate the polygon
        for eachEdge in polygon:
            newTriangle = Triangle([eachEdge[0], eachEdge[1], point]) # edge to point
            self.triangulation.append(newTriangle)
        # if Delanuay.flag<3:
        #     for eachTriangle in self.triangulation:
        #         for eachEdge in eachTriangle.edges:
        #             if self.superTriangle.edgePresent(eachEdge):
        #                 self.triangulation.remove(eachTriangle)
        #                 break
        #     Delanuay.flag += 1
