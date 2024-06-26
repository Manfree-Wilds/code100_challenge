class ImpossibleGeometry(Exception):
        def __init__(self, message="Impossible Geometry"):
            """
                The exception representing invalid geometry parameters.

                :param message: Optional. The error message to display.
            """
            super().__init__(message)


class Geometry():

    """
        A class representing a generic geometry.
        It is useful because contains the information about the circumbscribed rectangle aroud any geometry,
        allowing the fast calculation of a point being surey outside the geometry.

        :param up_left_point: A list representing the coordinates of the up-left point of the rectangle.
        :param dimensions: A list representing the dimensions of the rectangle.
    """

    def __init__(self, up_left_point: list[float], dimensions: list[float]):
        self.up_left_point = up_left_point
        self.dimensions = dimensions
        self.n_dimensions = len(dimensions)
        self.down_right_point = [up_left_point[i] + dimensions[i] for i in range(self.n_dimensions)]
        if self.n_dimensions != len(up_left_point):
            raise ImpossibleGeometry(message="Number of dimension of different points in the same geometry must be equal")
        for d in dimensions:
            if d <= 0:
                raise ImpossibleGeometry(message="All dimensions must be positive numbers")


    def is_outside(self, point):
        """
            Check if a given point is outside the geometry.
            It is sufficient that 1 point coordinate is outside the range given by the coordinate of the 2 "extreme" points.

            :param point: A list representing the coordinates of the point to check.
            :return: True if the point is inside the geometry, False otherwise.
        """
        for i, coord in enumerate(point):
            if coord < self.up_left_point[i]:
                return True
            if coord > self.down_right_point[i]:
                return True
        return False
    
    def is_inside(self):
        pass


class Rectangle(Geometry):
    def __init__(self, up_left_point: list[float], dimensions: list[float]):
        """
            The class corresponding to the rectangle shape

            :param up_left_point: A list representing the coordinates of the up-left point of the rectangle.
            :param dimensions: A list representing the dimensions of the rectangle.
        """
        self.up_left_point=up_left_point
        self.dimensions=dimensions
        super().__init__(up_left_point=up_left_point, dimensions=dimensions)

    def is_inside(self, point):
        """
            Check if a given point is inside the rectangle.
            In this case, it is sufficient that the point is not outside.

            :param point: A list representing the coordinates of the point to check.
            :return: True if the point is inside the geometry, False otherwise.
        """
        return not self.is_outside(point)


class Ring(Geometry):
    def __init__(self, center: list[float], radius: float, width: float):
        """
            The class corresponding to the ring shape.
            The frame of the ring is the square circumbscribed to the ring.

            :param center: A list representing the coordinates of the center of the ring.
            :param radius: The inner radius of the ring.
            :param width: The width of the ring, the difference between the outer and inner radius.
        """
        if radius <= 0 or width <= 0:
                raise ImpossibleGeometry(message="All dimensions must be positive numbers")
        self.center = center
        self.radius = radius
        self.width = width
        self.big_radius = self.radius + self.width
        up_left_point = [coord - self.big_radius for coord in center]
        dimensions = [2 * self.big_radius] * len(center)
        super().__init__(up_left_point=up_left_point, dimensions=dimensions)
        self.radius_squared = radius ** 2
        self.big_radius_squared = self.big_radius ** 2

    def is_inside(self, point):
        """
            Check if a given point is inside the circle.
            First, check if the point if outside the circumscribed square, 
            then calculate the radial polar coordinate of the point and check if inside the two squared radiuses.

            :param point: A list representing the coordinates of the point to check.
            :return: True if the point is inside the geometry, False otherwise.
        """
        if self.is_outside(point):
            return False
        rho = sum([(coord - self.center[i])**2 for i, coord in enumerate(point)])
        if rho < self.radius_squared:
            return False
        if rho > self.big_radius_squared:
            return False
        return True
    

class Logo(Geometry):
    def __init__(self, geometries: list):
        """
            The class corresponding to the geometry of the logo.
            The assumption is that a Logo in the union of more geometry.

            :param geometries_data: a list of geometries
            :return: True if the point is inside the logo, False otherwise.
        """
        self.geometries = geometries
    
        n_dimensions = self.geometries[0].n_dimensions
        for geometry in geometries:
            if n_dimensions != geometry.n_dimensions:
                raise ImpossibleGeometry(message="All logo's geometry must have the same number of dimensions")
            
        up_left_point = [min([geometry.up_left_point[index] for geometry in self.geometries]) for index in range(n_dimensions)]
        down_right_point = [max([geometry.up_left_point[index]+geometry.dimensions[index] for geometry in self.geometries]) for index in range(n_dimensions)]
        dimensions = [down_right_point[i] - up_left_point[i] for i in range(n_dimensions)]
        super().__init__(up_left_point=up_left_point, dimensions=dimensions)


    def is_inside(self, point: list[list[float]]) -> bool:
        """
            Check if a given point is inside any geometry of the logo.
            First, check if the point is inside the frame, to avoid useless calculation for point outside
            For each geometry, check if the point is inside the geometry.

            :param point: A list representing the coordinates of the point to check.
            :return: True if the point is inside the logo, False otherwise.
        """
        if self.is_outside(point):
            return False
        for geometry in self.geometries:
            if geometry.is_inside(point):
                return True
        return False