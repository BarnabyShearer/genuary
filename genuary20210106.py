#!/usr/bin/env python3
# https://genuary2021.github.io/prompts
# Triangle subdivision.

import matplotlib.pyplot


class Point(tuple):
    def __new__(self, x=0, y=0, z=0):
        return tuple.__new__(Point, (x, y, z))

    def __add__(self, other):
        return Point(*(self[i] + other[i] for i in range(3)))

    def __mul__(self, other):
        return Point(*(self[i] * other for i in range(3)))

    def __truediv__(self, other):
        return Point(*(self[i] / other for i in range(3)))


CORNERS = (
    Point(-1.0, 1.0, 1.0),
    Point(-1.0, -1.0, 1.0),
    Point(1.0, -1.0, 1.0),
    Point(1.0, 1.0, 1.0),
    Point(1.0, -1.0, -1.0),
    Point(1.0, 1.0, -1.0),
    Point(-1.0, -1.0, -1.0),
    Point(-1.0, 1.0, -1.0),
)

CUBE = (
    (0, 1, 2),
    (0, 2, 3),
    (3, 2, 4),
    (3, 4, 5),
    (5, 4, 6),
    (5, 6, 7),
    (7, 0, 3),
    (7, 3, 5),
    (7, 6, 1),
    (7, 1, 0),
    (6, 1, 2),
    (6, 2, 4),
)


def avg(l):
    l = tuple(l)
    return sum(l, Point()) / len(l)


def avg_values(d):
    return tuple(avg(v) for _, v in sorted(d.items()))


def get_avg_face_points(faces, face_points):
    output = {}
    for face_point, face in zip(face_points, faces):
        for point in face:
            output.setdefault(point, []).append(face_point)
    return avg_values(output)


def get_avg_mid_edges(points, edges_faces):
    output = {}
    for edge_points in edges_faces.keys():
        for point in edge_points:
            output.setdefault(point, []).extend(points[point] for point in edge_points)
    return avg_values(output)


def get_points_faces(faces):
    output = {}
    for face in faces:
        for point in face:
            output.setdefault(point, 0)
            output[point] += 1
    return tuple(v for _, v in sorted(output.items()))


def catmull_clark(points, faces):
    face_points = tuple(avg(points[point] for point in face) for face in faces)
    edges_faces = {}
    for fi, face in enumerate(faces):
        for pi, point in enumerate(face):
            edges_faces.setdefault(
                tuple(sorted((point, face[(pi + 1) % len(face)]))), []
            ).append(fi)
    new_points = [
        point * (n - 3.0) / n + afp / n + ame * 2 / n
        for point, n, afp, ame in zip(
            points,
            get_points_faces(faces),
            get_avg_face_points(faces, face_points),
            get_avg_mid_edges(points, edges_faces),
        )
    ]
    face_point_idx = []
    for face_point in face_points:
        face_point_idx.append(len(new_points))
        new_points.append(face_point)
    edge_point_idx = {}
    for (p1, p2), (f1, f2) in edges_faces.items():
        edge_point_idx[(p1, p2)] = len(new_points)
        new_points.append(
            avg((points[p1], points[p2], face_points[f1], face_points[f2]))
        )
    new_faces = []
    for face, face_point in zip(faces, face_point_idx):
        edge_point_ab = edge_point_idx[tuple(sorted((face[0], face[1])))]
        edge_point_bc = edge_point_idx[tuple(sorted((face[1], face[2])))]
        edge_point_ca = edge_point_idx[tuple(sorted((face[2], face[0])))]
        new_faces.append((face[0], edge_point_ab, face_point))
        new_faces.append((face[1], edge_point_bc, face_point))
        new_faces.append((face[2], edge_point_ca, face_point))
        new_faces.append((face[0], face_point, edge_point_ca))
        new_faces.append((face[1], face_point, edge_point_ab))
        new_faces.append((face[2], face_point, edge_point_bc))
    return new_points, new_faces


def render(points, faces):
    plot = matplotlib.pyplot.figure().add_subplot(projection="3d")
    for face in faces:
        plot.plot_trisurf(
            *(tuple(points[point][i] for point in face) for i in range(3))
        )
    matplotlib.pyplot.show()


points, faces = CORNERS, CUBE
for _ in range(2):
    points, faces = catmull_clark(points, faces)
render(points, faces)
