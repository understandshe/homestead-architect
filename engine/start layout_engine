import random
from shapely.geometry import box, Point
from shapely.ops import unary_union


class LayoutEngine:

    def __init__(self, plot_width, plot_height):
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.objects = []
        self.occupied = []

    # -------------------------
    # BASIC HELPERS
    # -------------------------

    def is_valid(self, geom):
        """Check if geometry is inside plot and not colliding"""
        plot_boundary = box(0, 0, self.plot_width, self.plot_height)

        if not plot_boundary.contains(geom):
            return False

        for obj in self.occupied:
            if geom.intersects(obj):
                return False

        return True

    def add_object(self, geom, obj_type, meta=None):
        self.occupied.append(geom)
        self.objects.append({
            "type": obj_type,
            "geometry": geom,
            "meta": meta or {}
        })

    # -------------------------
    # HOUSE (ANCHOR)
    # -------------------------

    def place_house(self, width=20, height=15):
        x = (self.plot_width - width) / 2
        y = (self.plot_height - height) / 2

        house = box(x, y, x + width, y + height)

        self.add_object(house, "house", {
            "width": width,
            "height": height
        })

        return house

    # -------------------------
    # GARDEN BEDS (GRID SYSTEM)
    # -------------------------

    def place_beds(self, count, bed_w=3, bed_h=1.5, spacing=2):

        cols = max(2, int(count ** 0.5))
        rows = (count // cols) + 1

        start_x = 5
        start_y = 5

        placed = 0

        for r in range(rows):
            for c in range(cols):

                if placed >= count:
                    return

                x = start_x + c * (bed_w + spacing)
                y = start_y + r * (bed_h + spacing)

                bed = box(x, y, x + bed_w, y + bed_h)

                if self.is_valid(bed):
                    self.add_object(bed, "bed")
                    placed += 1

    # -------------------------
    # TREES (SMART RANDOM)
    # -------------------------

    def place_trees(self, count, radius=1.2, min_distance=3):

        attempts = 0
        placed = 0

        while placed < count and attempts < count * 20:
            attempts += 1

            x = random.uniform(2, self.plot_width - 2)
            y = random.uniform(2, self.plot_height - 2)

            tree = Point(x, y).buffer(radius)

            if not self.is_valid(tree):
                continue

            # spacing check
            too_close = False
            for obj in self.occupied:
                if tree.distance(obj) < min_distance:
                    too_close = True
                    break

            if too_close:
                continue

            self.add_object(tree, "tree")
            placed += 1

    # -------------------------
    # PATH SYSTEM (MAIN AXIS)
    # -------------------------

    def create_main_path(self, house_geom, width=2.5):

        centroid = house_geom.centroid

        start = Point(0, centroid.y)
        end = Point(centroid.x, centroid.y)

        path_line = start.buffer(width / 2).union(end.buffer(width / 2))

        self.add_object(path_line, "path")

    # -------------------------
    # FULL GENERATION
    # -------------------------

    def generate(self, beds=10, trees=10):

        house = self.place_house()

        self.place_beds(beds)
        self.place_trees(trees)
        self.create_main_path(house)

        return {
            "plot": {
                "width": self.plot_width,
                "height": self.plot_height
            },
            "objects": self.objects
        }
