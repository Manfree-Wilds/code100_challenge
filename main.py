import json
from geometries import Rectangle, Ring, Logo


class ProblemSolver():
    def __init__(self, points_filename: str):
        """
            The class thas solve the proble.
            The logo is a rectangle and is composed by a list of geometries.

            :param filename: The name of the file that contains the points.
        """
        with open(points_filename) as file_json:
            self.points = json.load(file_json)['coords']

        geometries = [
            Rectangle(up_left_point=[145, 75], dimensions=[20,150]),
            Ring(center=[250, 150], radius=55, width=20),
            Ring(center=[410, 150], radius=55, width=20)
        ]

        self.logo = Logo(geometries=geometries)

    def count_points(self) -> int:
        """"
            Counts the number of points inside the logo, by cycling all the points.

            return: n_points: the number of points inside the logo
        """
        n_points = 0
        for point in self.points:
            if self.logo.is_inside(point):
                n_points += 1
        return n_points
    

def main(points_filename: str):
    solver = ProblemSolver(points_filename=points_filename)
    n_points = solver.count_points()

    print(f"Number of points inside of the logo: {n_points}")
    

if __name__ == '__main__':
    main(points_filename="points.json")
