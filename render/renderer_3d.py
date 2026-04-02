import trimesh
import numpy as np
from shapely.geometry import Polygon, MultiPolygon


class Renderer3D:

    def __init__(self, scene):
        self.scene = scene
        self.meshes = []

    # -------------------------
    # MATERIAL HELPER
    # -------------------------

    def apply_color(self, mesh, color):
        mesh.visual.vertex_colors = np.tile(color, (len(mesh.vertices), 1))

    # -------------------------
    # EXTRUSION WITH MATERIAL
    # -------------------------

    def extrude(self, geom, height, color):

        meshes = []

        if isinstance(geom, Polygon):
            m = trimesh.creation.extrude_polygon(geom, height)
            self.apply_color(m, color)
            meshes.append(m)

        elif isinstance(geom, MultiPolygon):
            for g in geom.geoms:
                m = trimesh.creation.extrude_polygon(g, height)
                self.apply_color(m, color)
                meshes.append(m)

        return meshes

    # -------------------------
    # HOUSE (premium block)
    # -------------------------

    def build_house(self, geom):

        meshes = self.extrude(
            geom,
            height=8,
            color=[139, 90, 60, 255]  # brown
        )

        return meshes

    # -------------------------
    # BEDS (soil look)
    # -------------------------

    def build_bed(self, geom):

        return self.extrude(
            geom,
            height=1,
            color=[90, 62, 43, 255]
        )

    # -------------------------
    # PATH (gravel feel)
    # -------------------------

    def build_path(self, geom):

        return self.extrude(
            geom,
            height=0.2,
            color=[210, 200, 180, 255]
        )

    # -------------------------
    # TREE (better model)
    # -------------------------

    def build_tree(self, geom):

        meshes = []

        center = geom.centroid
        x, y = center.x, center.y

        # trunk
        trunk = trimesh.creation.cylinder(radius=0.2, height=2)
        trunk.apply_translation([x, y, 1])
        self.apply_color(trunk, [100, 70, 40, 255])
        meshes.append(trunk)

        # foliage (bigger + layered)
        for i in range(2):
            foliage = trimesh.creation.icosphere(radius=1.2 - i * 0.3)
            foliage.apply_translation([x, y, 3 + i])
            self.apply_color(foliage, [40, 120, 50, 255])
            meshes.append(foliage)

        return meshes

    # -------------------------
    # GROUND (grass)
    # -------------------------

    def build_ground(self):

        plot = self.scene["plot"]

        ground = trimesh.creation.box(extents=[
            plot["width"],
            plot["height"],
            0.2
        ])

        ground.apply_translation([
            plot["width"] / 2,
            plot["height"] / 2,
            -0.1
        ])

        self.apply_color(ground, [110, 170, 110, 255])

        return ground

    # -------------------------
    # FAKE SHADOW SYSTEM
    # -------------------------

    def add_shadow(self, geom, offset=(1.5, -1.5)):

        shadow_meshes = []

        if isinstance(geom, Polygon):
            shifted = trimesh.creation.extrude_polygon(geom, 0.05)
            shifted.apply_translation([offset[0], offset[1], 0.01])
            self.apply_color(shifted, [0, 0, 0, 60])
            shadow_meshes.append(shifted)

        elif isinstance(geom, MultiPolygon):
            for g in geom.geoms:
                shifted = trimesh.creation.extrude_polygon(g, 0.05)
                shifted.apply_translation([offset[0], offset[1], 0.01])
                self.apply_color(shifted, [0, 0, 0, 60])
                shadow_meshes.append(shifted)

        return shadow_meshes

    # -------------------------
    # BUILD FULL SCENE
    # -------------------------

    def build_scene(self):

        for el in self.scene["elements"]:

            geom = el["geometry"]
            typ = el["type"]

            if typ == "house":
                self.meshes.extend(self.build_house(geom))
                self.meshes.extend(self.add_shadow(geom))

            elif typ == "bed":
                self.meshes.extend(self.build_bed(geom))
                self.meshes.extend(self.add_shadow(geom))

            elif typ == "path":
                self.meshes.extend(self.build_path(geom))

            elif typ == "tree":
                tree_meshes = self.build_tree(geom)
                self.meshes.extend(tree_meshes)
                self.meshes.extend(self.add_shadow(geom))

        self.meshes.append(self.build_ground())

    # -------------------------
    # EXPORT
    # -------------------------

    def export(self, output_path="output/map_3d.glb"):

        self.build_scene()

        scene = trimesh.Scene()

        for m in self.meshes:
            scene.add_geometry(m)

        scene.export(output_path)

        return output_path
