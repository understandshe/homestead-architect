import numpy as np
from shapely.geometry import LineString
from shapely.geometry import Point


class PathGenerator:

    def __init__(self, plot_width, plot_height):
        self.plot_width = plot_width
        self.plot_height = plot_height

    # -------------------------
    # BEZIER CURVE
    # -------------------------

    def bezier_curve(self, p0, p1, p2, p3, num_points=50):
        """Cubic Bezier Curve"""
        t_values = np.linspace(0, 1, num_points)
        curve = []

        for t in t_values:
            x = (
                (1 - t) ** 3 * p0[0]
                + 3 * (1 - t) ** 2 * t * p1[0]
                + 3 * (1 - t) * t ** 2 * p2[0]
                + t ** 3 * p3[0]
            )
            y = (
                (1 - t) ** 3 * p0[1]
                + 3 * (1 - t) ** 2 * t * p1[1]
                + 3 * (1 - t) * t ** 2 * p2[1]
                + t ** 3 * p3[1]
            )
            curve.append((x, y))

        return curve

    # -------------------------
    # MAIN PATH (ENTRY → HOUSE)
    # -------------------------

    def generate_main_path(self, house_geom, width=2.5):

        centroid = house_geom.centroid

        start = (0, centroid.y)
        end = (centroid.x, centroid.y)

        # control points (curve shape)
        p0 = start
        p3 = end

        p1 = (centroid.x * 0.3, centroid.y + 15)
        p2 = (centroid.x * 0.7, centroid.y - 10)

        curve_points = self.bezier_curve(p0, p1, p2, p3)

        line = LineString(curve_points)

        path = line.buffer(width, cap_style=2, join_style=2)

        return path

    # -------------------------
    # SECONDARY PATHS (HOUSE → GARDEN)
    # -------------------------

    def generate_secondary_paths(self, house_geom, targets, width=1.8):

        paths = []

        house_center = house_geom.centroid

        for target in targets:

            target_center = target.centroid

            p0 = (house_center.x, house_center.y)
            p3 = (target_center.x, target_center.y)

            # natural curve randomness
            offset_x = np.random.uniform(-10, 10)
            offset_y = np.random.uniform(-10, 10)

            p1 = (house_center.x + offset_x, house_center.y + 10)
            p2 = (target_center.x - offset_x, target_center.y - 10)

            curve_points = self.bezier_curve(p0, p1, p2, p3)

            line = LineString(curve_points)

            path = line.buffer(width, cap_style=2, join_style=2)

            paths.append(path)

        return paths

    # -------------------------
    # FULL PATH SYSTEM
    # -------------------------

    def generate_paths(self, house_geom, garden_objects):

        all_paths = []

        # main entry path
        main_path = self.generate_main_path(house_geom)
        all_paths.append(main_path)

        # connect to beds
        bed_targets = [
            obj["geometry"] for obj in garden_objects if obj["type"] == "bed"
        ]

        secondary = self.generate_secondary_paths(house_geom, bed_targets)
        all_paths.extend(secondary)

        return all_paths
