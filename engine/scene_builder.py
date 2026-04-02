from shapely.ops import unary_union
from engine.path_generator import PathGenerator


class SceneBuilder:

    def __init__(self, layout_data):
        self.layout = layout_data
        self.plot_width = layout_data["plot"]["width"]
        self.plot_height = layout_data["plot"]["height"]

        self.objects = layout_data["objects"]
        self.paths = []

    # -------------------------
    # EXTRACT OBJECTS
    # -------------------------

    def get_house(self):
        for obj in self.objects:
            if obj["type"] == "house":
                return obj["geometry"]
        return None

    def get_garden_objects(self):
        return [
            obj for obj in self.objects
            if obj["type"] in ["bed", "tree"]
        ]

    # -------------------------
    # PATH GENERATION
    # -------------------------

    def build_paths(self):

        house = self.get_house()
        garden = self.get_garden_objects()

        path_gen = PathGenerator(self.plot_width, self.plot_height)

        generated_paths = path_gen.generate_paths(house, garden)

        for path in generated_paths:
            self.paths.append({
                "type": "path",
                "geometry": path
            })

    # -------------------------
    # MERGE + CLEAN SCENE
    # -------------------------

    def merge_scene(self):

        all_geoms = []

        for obj in self.objects:
            all_geoms.append(obj["geometry"])

        for path in self.paths:
            all_geoms.append(path["geometry"])

        unified = unary_union(all_geoms)

        return unified

    # -------------------------
    # BUILD FINAL SCENE
    # -------------------------

    def build(self):

        self.build_paths()

        final_scene = {
            "plot": {
                "width": self.plot_width,
                "height": self.plot_height
            },
            "elements": []
        }

        # original objects
        for obj in self.objects:
            final_scene["elements"].append({
                "type": obj["type"],
                "geometry": obj["geometry"]
            })

        # add paths
        for path in self.paths:
            final_scene["elements"].append(path)

        return final_scene
