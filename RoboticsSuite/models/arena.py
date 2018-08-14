import numpy as np
import xml.etree.ElementTree as ET
from RoboticsSuite.models.base import MujocoXML
from RoboticsSuite.models.model_util import *
from RoboticsSuite.utils import XMLError


class Arena(MujocoXML):
    def set_origin(self, pos):
        pos = np.array(pos)
        for node in self.worldbody.findall("./*[@pos]"):
            cur_pos = string_to_array(node.get("pos"))
            new_pos = cur_pos + pos
            node.set("pos", array_to_string(new_pos))

    def add_pos_indicator(self):
        body = gen_body(name="pos_indicator")
        body.append(
            gen_geom(
                "sphere",
                [0.03],
                rgba=[1, 0, 0, 0.5],
                group=1,
                contype="0",
                conaffinity="0",
            )
        )
        body.append(joint(type="free", name="pos_indicator"))
        self.worldbody.append(body)


class TableArena(Arena):
    def __init__(self, full_size=(0.8, 0.8, 0.8), friction=(1, 0.005, 0.0001)):
        self.full_size = np.array(full_size)
        self.half_size = self.full_size / 2
        if friction is None:
            friction = np.array([1, 0.005, 0.0001])
        self.friction = friction

        super().__init__(xml_path_completion("arena/table_arena.xml"))
        self.floor = self.worldbody.find("./geom[@name='floor']")
        self.table_body = self.worldbody.find("./body[@name='table']")
        self.table_collision = self.table_body.find("./geom[@name='table_collision']")
        self.table_visual = self.table_body.find("./geom[@name='table_visual']")
        self.table_top = self.table_body.find("./site[@name='table_top']")

        self.configure_location()

    def configure_location(self):
        self.bottom_pos = np.array([0, 0, 0])
        self.floor.set("pos", array_to_string(self.bottom_pos))

        self.center_pos = self.bottom_pos + np.array([0, 0, self.half_size[2]])
        self.table_body.set("pos", array_to_string(self.center_pos))
        self.table_collision.set("size", array_to_string(self.half_size))
        self.table_collision.set("friction", array_to_string(self.friction))
        self.table_visual.set("size", array_to_string(self.half_size))

        self.table_top.set("pos", array_to_string(np.array([0, 0, self.half_size[2]])))

    @property
    def table_top_abs(self):
        """Returns the absolute position of table top"""
        return string_to_array(self.floor.get("pos")) + np.array(
            [0, 0, self.full_size[2]]
        )


class EmptyArena(Arena):
    def __init__(self):
        super().__init__(xml_path_completion("arena/empty_arena.xml"))
        self.floor = self.worldbody.find("./geom[@name='floor']")


class BinsArena(Arena):
    def __init__(self, full_size=(0.39, 0.49, 0.82), friction=(1, 0.005, 0.0001)):
        self.full_size = np.array(full_size)
        self.half_size = self.full_size / 2
        if friction is None:
            friction = np.array([1, 0.005, 0.0001])
        self.friction = friction

        super().__init__(xml_path_completion("arena/bins_arena.xml"))
        self.floor = self.worldbody.find("./geom[@name='floor']")
        self.bin1_body = self.worldbody.find("./body[@name='bin1']")
        self.bin2_body = self.worldbody.find("./body[@name='bin2']")
        self.table_collision = self.bin1_body.find("./geom[@name='bin1_collision']")

        self.configure_location()

    def configure_location(self):
        self.bottom_pos = np.array([0, 0, 0])
        self.floor.set("pos", array_to_string(self.bottom_pos))

    @property
    def bin_abs(self):
        """Returns the absolute position of table top"""
        return string_to_array(self.bin1_body.get("pos"))


class PegsArena(Arena):
    def __init__(self, full_size=(0.45, 0.69, 0.82), friction=(1, 0.005, 0.0001)):
        self.full_size = np.array(full_size)
        self.half_size = self.full_size / 2
        if friction is None:
            friction = np.array([1, 0.005, 0.0001])
        self.friction = friction

        super().__init__(xml_path_completion("arena/pegs_arena.xml"))
        self.floor = self.worldbody.find("./geom[@name='floor']")
        self.bin1_body = self.worldbody.find("./body[@name='bin1']")
        self.peg1_body = self.worldbody.find("./body[@name='peg1']")
        self.peg2_body = self.worldbody.find("./body[@name='peg2']")
        self.table_collision = self.bin1_body.find("./geom[@name='bin1_collision']")

        self.configure_location()

    def configure_location(self):
        self.bottom_pos = np.array([0, 0, 0])
        self.floor.set("pos", array_to_string(self.bottom_pos))

    @property
    def table_top_abs(self):
        """Returns the absolute position of table top"""
        return string_to_array(self.bin1_body.get("pos"))