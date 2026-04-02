import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon


class Renderer2D:

    def __init__(self, scene):
        self.scene = scene
        self.width = scene["plot"]["width"]
        self.height = scene["plot"]["height"]

    # -------------------------
    # STYLE CONFIG (premium look)
    # -------------------------

    COLORS = {
        "grass": "#6FAF73",
        "house": "#8B5A3C",
        "bed": "#5A3E2B",
        "tree": "#2E7D32",
        "path": "#D8C3A5",
        "border": "#2f2f2f"
    }

    # -------------------------
    # DRAW SHAPES
    # -------------------------

    def draw_polygon(self, ax, geom, color, z=1, alpha=1.0):
        if isinstance(geom, Polygon):
            x, y = geom.exterior.xy
            ax.fill(x, y, color=color, alpha=alpha, zorder=z)

        elif isinstance(geom, MultiPolygon):
            for g in geom.geoms:
                x, y = g.exterior.xy
                ax.fill(x, y, color=color, alpha=alpha, zorder=z)

    def draw_tree(self, ax, geom):
        x, y = geom.centroid.x, geom.centroid.y
        ax.scatter(x, y, s=80, c=self.COLORS["tree"], zorder=4)

    # -------------------------
    # RENDER LAYERS
    # -------------------------

    def render_background(self, ax):
        ax.set_facecolor(self.COLORS["grass"])

    def render_paths(self, ax):
        for el in self.scene["elements"]:
            if el["type"] == "path":
                self.draw_polygon(ax, el["geometry"], self.COLORS["path"], z=2)

    def render_beds(self, ax):
        for el in self.scene["elements"]:
            if el["type"] == "bed":
                self.draw_polygon(ax, el["geometry"], self.COLORS["bed"], z=3)

    def render_house(self, ax):
        for el in self.scene["elements"]:
            if el["type"] == "house":
                self.draw_polygon(ax, el["geometry"], self.COLORS["house"], z=5)

    def render_trees(self, ax):
        for el in self.scene["elements"]:
            if el["type"] == "tree":
                self.draw_tree(ax, el["geometry"])

    # -------------------------
    # FINAL RENDER
    # -------------------------

    def render(self, output_path="output/map_2d.png"):

        fig, ax = plt.subplots(figsize=(8, 8))

        self.render_background(ax)
        self.render_paths(ax)
        self.render_beds(ax)
        self.render_house(ax)
        self.render_trees(ax)

        # border
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path
