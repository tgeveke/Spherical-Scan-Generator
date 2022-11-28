import matplotlib.pyplot as plt
import numpy as np
import math

def getrotx(angle):
    rad = math.radians(angle)
    return [[1, 0,              0],
            [0, math.cos(rad), -math.sin(rad)],
            [0, math.sin(rad),  math.cos(rad)]]

def getroty(angle):
    rad = math.radians(angle)
    return [[math.cos(rad), 0, math.sin(rad)],
            [0,              1, -math.sin(rad)],
            [-math.sin(rad), 0,  math.cos(rad)]]

def getrotz(angle):
    rad = math.radians(angle)
    return [[math.cos(rad), -math.sin(rad),0],
            [math.sin(rad), math.cos(rad), 0],
            [0,             0,             1]]

def transMatrix(x, y, z):
        return [[x, 0, 0],
                [0, y, 0],
                [0, 0, z]]

def fullMatrix():
    full_matrix = np.zeros((4, 4))
    rotation_matrix = getrotx()
    full_matrix[0:rotation_matrix.shape[0], 0:rotation_matrix.shape[1]] = rotation_matrix
    full_matrix[0:3, 3] = transMatrix()
    full_matrix[3, 3] = 1
    return full_matrix

def createPoints(radius = 1, degreesToScan = 90, numCurves = 8, pointsPerCurve = 20, h = 0, k = 0, j = 0, plot = True):
    # (h, k , j): (x, y, z) location for center of circle to scan

    points = []

    if plot:
        fig = plt.figure()
        plot = fig.add_subplot(projection = '3d')
        plot.scatter(h, k, j)
        plot.set_xlabel('X')
        plot.set_ylabel('Y')
        plot.set_zlabel('Z')

    radiansToScan = math.radians(degreesToScan) # Degrees -> radians
    xlimit = h + (radius * math.cos(radiansToScan / 2))

    for i in range(-numCurves // 2, numCurves // 2 + 1):
        x = np.linspace(-xlimit, xlimit, pointsPerCurve)
        y = i * (radius / numCurves)

        rotx = getrotx(15 * i)
        transMat = transMatrix(1, 1, 1)
        for ii in range(0, pointsPerCurve):
            z = math.sqrt(radius**2 - (x[ii] - h)**2)
            oldx = [x[ii], y, z]
            otherx = np.matmul(rotx, oldx)
            newx = np.matmul(transMat, otherx)

            pos_x = newx[0] + h
            pos_y = newx[1] + k
            pos_z = newx[2] + j
            
            magx = math.sqrt(newx[0]**2 + newx[1]**2 + newx[2]**2)
            xangle = math.acos(np.dot([1, 0, 0], newx) / magx)
            yangle = math.acos(np.dot([0, 1, 0], newx) / magx)
            zangle = math.acos(np.dot([0, 0, 1], newx) / magx)

            points.append([pos_x, pos_y, pos_z, xangle, yangle, zangle])

            if plot:
                plot.scatter(pos_x, pos_y, pos_z)
                plot.plot3D(np.linspace(pos_x, h, pointsPerCurve), np.linspace(pos_y, k, pointsPerCurve), np.linspace(pos_z, j, pointsPerCurve))
            
            '''
            if ii == pointsPerCurve - 1:
                if i != numCurves:
                    if i % 2 == 0:
                        xcon = np.linspace(x[0], x[0], 10)
                        ycon = np.linspace(pos_y, (i+1) * (radius / numCurves), 10)
                    else:
                        xcon = np.linspace(x[ii], x[-1], 10)
                        ycon = np.linspace((i+1) * (radius / numCurves), pos_y, 10)
                    zcon = np.linspace(z, math.sqrt(radius**2 - x[0]**2), 10)
                    plot.plot3D(xcon, ycon, zcon)
            '''
    if plot: plt.show()
    return points

if __name__ == '__main__':
    points = createPoints()
    print(points[0])