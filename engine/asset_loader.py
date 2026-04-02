import os
import trimesh


class AssetLoader:

    def __init__(self, asset_dir="assets/models"):
        self.asset_dir = asset_dir
        self.cache = {}

    # -------------------------
    # LOAD MODEL
    # -------------------------

    def load_model(self, name):

        if name in self.cache:
            return self.cache[name].copy()

        path = os.path.join(self.asset_dir, f"{name}.glb")

        if not os.path.exists(path):
            return None

        mesh = trimesh.load(path)

        self.cache[name] = mesh
        return mesh.copy()

    # -------------------------
    # PLACE MODEL
    # -------------------------

    def place_model(self, mesh, x, y, z=0, scale=1):

        mesh = mesh.copy()

        mesh.apply_scale(scale)
        mesh.apply_translation([x, y, z])

        return mesh

    # -------------------------
    # HIGH LEVEL HELPERS
    # -------------------------

    def get_house(self, x, y):

        model = self.load_model("house")

        if model:
            return self.place_model(model, x, y, 0, scale=2)

        return None

    def get_tree(self, x, y):

        model = self.load_model("tree")

        if model:
            return self.place_model(model, x, y, 0, scale=1.5)

        return None

    def get_bed(self, x, y):

        model = self.load_model("bed")

        if model:
            return self.place_model(model, x, y, 0, scale=1)

        return None
