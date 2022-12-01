import networkx as nx
import pytest
import unittest

import numpy as np
import neugym as ng
from neugym.environment.gridworld import GridWorld


class TestGridWorldFunction(unittest.TestCase):
    """Test GridWorld environment."""
    def test_init(self):
        # Test default instantiation.
        W = GridWorld()
        self.assertEqual(W.get_area_altitude(0).all(), np.zeros((1, 1)).all())
        self.assertEqual(W.world.number_of_nodes(), 1)
        self.assertTrue((0, 0, 0) in W.world.nodes)
        self.assertTrue(True not in nx.get_node_attributes(W.world, 'blocked').values())

        # Test manually set origin shape.
        W = GridWorld((3, 3))
        self.assertEqual(W.get_area_altitude(0).all(), np.zeros((3, 3)).all())
        self.assertEqual(W.world.number_of_nodes(), 9)
        self.assertEqual(W.world.number_of_edges(), 12)
        self.assertEqual(9, len(nx.get_node_attributes(W.world, 'blocked')))
        self.assertTrue(True not in nx.get_node_attributes(W.world, 'blocked').values())

    def test_add_area(self):
        # Test 'add_area' function.
        # Test default parameters.
        W = GridWorld()
        W.add_area((2, 2))
        self.assertEqual(W.num_area, 1)
        self.assertEqual(W.world.number_of_nodes(), 5)
        self.assertEqual(W.get_area_altitude(1).all(), np.zeros((2, 2)).all())

        # Test add area with name.
        W = GridWorld()
        W.add_area((2, 2), name="Up")
        with self.assertRaises(RuntimeError):
            W.add_area((2, 2), name="Up")
        self.assertEqual(W.num_area, 1)
        self.assertEqual(W.get_area_name(1), "Up")

        # Test initial block.
        W = GridWorld()
        W.block((0, 0, 0))
        W.add_area((2, 2), name="Up")
        self.assertTrue(nx.get_node_attributes(W.world, 'blocked')[(0, 0, 0)])

    def test_remove_area(self):
        # Test 'remove_area' function.
        W = GridWorld()
        W.add_area((2, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((3, 3))
        W.add_path((1, 1, 1), (2, 0, 0))
        W.add_area((5, 5))
        W.add_path((0, 0, 0), (3, 0, 0))
        W.add_object((1, 0, 0), 1, 0.5)
        W.add_object((2, 0, 0), 1, 0.6)
        W.add_object((3, 1, 1), 1, 0.7)
        self.assertEqual(W.world.number_of_edges(), 59)
        self.assertTrue(((1, 1, 1), (2, 0, 0)) in W.world.edges)
        self.assertEqual(W._path_alias.get((1, 2, 1)), (2, 0, 0))
        self.assertTrue(((0, 0, 0), (3, 0, 0)) in W.world.edges)

        W.remove_area(2)
        self.assertEqual(W.num_area, 2)
        self.assertEqual(W.world.number_of_nodes(), 30)
        self.assertEqual(W.world.number_of_edges(), 46)
        self.assertTrue(((1, 1, 1), (2, 0, 0)) not in W.world.edges)
        self.assertTrue((2, -1, 0) not in W._path_alias.keys())
        self.assertEqual(W._path_alias.get((0, 0, 1)), (2, 0, 0))
        self.assertTrue(W._path_alias.get((2, 0, -1)), (0, 0, 0))
        self.assertEqual(len(W._path_alias), 4)
        self.assertEqual(len(W._objects), 2)
        for obj in W._objects:
            self.assertTrue(obj.coord != (2, 0, 0))

        W.add_area((5, 5))
        W.add_path((0, 0, 0), (3, 4, 4))
        W.add_object((3, 1, 1), 1, 0.7)
        W.remove_area(1)
        W.remove_area(1)
        self.assertEqual(W.num_area, 1)
        self.assertEqual(W.world.number_of_nodes(), 26)
        self.assertEqual(W.world.number_of_edges(), 41)
        self.assertTrue(((0, 0, 0), (1, 0, 0)) not in W.world.edges)
        self.assertTrue(((0, 0, 0), (1, 4, 4)) in W.world.edges)
        self.assertEqual(len(W._objects), 1)
        self.assertEqual((1, 1, 1), W._objects[0].coord)
        self.assertTrue((1, 1, 1) in W.world.nodes)
        self.assertEqual(len(W._path_alias), 2)
        self.assertEqual(W._path_alias.get((0, -1, 0)), (1, 4, 4))
        self.assertEqual(W._path_alias.get((1, 5, 4)), (0, 0, 0))

        # Test remove origin.
        with self.assertRaises(ng.NeuGymPermissionError):
            W.remove_area(0)

        # Test remove with area name.
        W = GridWorld()
        W.add_area((2, 2), name="First")
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((2, 2), name="Second")
        W.add_path((0, 0, 0), (2, 0, 0))
        W.add_area((2, 2), name="Third")
        W.add_path((0, 0, 0), (3, 1, 1))
        W.remove_area("Second")
        self.assertEqual(W.num_area, 2)
        self.assertEqual(W.get_area_name(2), "Third")
        self.assertEqual(W.get_area_name(1), "First")
        with self.assertRaises(ValueError):
            W.remove_area("test")

    def test_add_path(self):
        # Test 'add_path' function.
        W = GridWorld()

        # Test add self-loop at origin.
        with self.assertRaises(ng.NeuGymPermissionError):
            W.add_path((0, 0, 0), (0, 0, 0))

        W.add_area((2, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((3, 3))
        W.add_path((0, 0, 0), (2, 0, 0))
        W.add_area((2, 2))
        W.add_path((0, 0, 0), (3, 1, 1))
        with self.assertRaises(ValueError):
            W.add_path((1, 1, 1), (2, 0))
        with self.assertRaises(ng.NeuGymConnectivityError):
            W.add_path((1, 1, 1), (2, 2, 0), (-1, 0))
        with self.assertRaises(ng.NeuGymConnectivityError):
            W.add_path((1, 1, 1), (2, 1, 1))
        W.add_path((1, 1, 1), (2, 2, 0))
        self.assertEqual(W._path_alias.get((1, 1, 2)), (2, 2, 0))
        self.assertEqual(W._path_alias.get((2, 2, -1)), (1, 1, 1))
        self.assertTrue(((1, 1, 1), (2, 2, 0)) in W.world.edges)

        # Test add multiple paths between two positions.
        W.add_path((1, 1, 0), (2, 0, 2))
        with self.assertRaises(ng.NeuGymOverwriteError):
            W.add_path((1, 1, 0), (2, 0, 2))

    def test_remove_path(self):
        # Test 'remove_path' function.
        W = GridWorld()
        W.add_area((2, 4))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((3, 5))
        W.add_path((0, 0, 0), (2, 0, 0))
        W.add_path((1, 1, 0), (2, 0, 4))
        with self.assertRaises(ng.NeuGymOverwriteError):
            W.add_path((1, 1, 0), (2, 0, 4))
        self.assertEqual(len(W._path_alias), 6)
        with self.assertWarns(RuntimeWarning):
            W.remove_path((1, 1, 3), (0, 0, 0))
        with self.assertRaises(ValueError):
            W.remove_path((0, 0), (1, 1, 1))
        W.remove_path((1, 1, 0), (2, 0, 4))
        self.assertEqual(len(W._path_alias), 4)
        self.assertTrue(((1, 1, 0), (2, 0, 4)) not in W.world.edges)

        # Test remove path within an area.
        with self.assertRaises(ng.NeuGymPermissionError):
            W.remove_path((1, 0, 0), (1, 1, 0))

    def test_add_object(self):
        # Test 'add_object' function.
        W = GridWorld()
        W.add_area((2, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((4, 3))
        W.add_path((0, 0, 0), (2, 0, 0))

        W.add_object((1, 1, 1), 1, 0.3)
        W.add_object((2, 2, 1), 1, 0.7, -1)
        self.assertEqual(len(W._objects), 2)
        self.assertEqual(W._objects[0].reward, 1)
        self.assertEqual(W._objects[0].prob, 0.3)
        self.assertEqual(W._objects[0].punish, 0)
        self.assertEqual(W._objects[0].coord, (1, 1, 1))
        self.assertEqual(W._objects[1].punish, -1)

        # Test add object with illegal coordinate.
        with self.assertRaises(ValueError):
            W.add_object((1, 1), 1, 0, 0.5)
        with self.assertRaises(ValueError):
            W.add_object((3, 1, 1), 1, 0, 0.5)

    def test_remove_object(self):
        # Test 'remove_object' function.
        W = GridWorld()
        W.add_area((4, 3))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((4, 3))
        W.add_path((0, 0, 0), (2, 0, 0))
        W.add_area((4, 3))
        W.add_path((0, 0, 0), (3, 3, 1))
        W.add_object((1, 2, 1), 1, 0.2)
        W.add_object((2, 2, 1), 1, 0.8)
        W.add_object((3, 2, 1), 1, 0.9)

        W.remove_object((3, 2, 1))
        self.assertEqual(len(W._objects), 2)
        for obj in W._objects:
            self.assertTrue(obj.coord != (3, 2, 1))

        # Test remove undefined object.
        with self.assertRaises(ValueError):
            W.remove_object((0, 0, 0))

    def test_update_object(self):
        # Test 'update_object' function.
        W = GridWorld()
        W.add_area((4, 3))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((4, 3))
        W.add_path((0, 0, 0), (2, 0, 0))
        W.add_object((1, 2, 1), 1, 0.3)
        W.add_object((2, 2, 1), 1, 0.7)

        W.update_object((1, 2, 1), reward=10, prob=0.2, punish=-10)
        self.assertEqual(W._objects[0].reward, 10)
        self.assertEqual(W._objects[0].prob, 0.2)
        self.assertEqual(W._objects[0].punish, -10)

        # Test modify undefined object.
        with self.assertRaises(ValueError):
            W.update_object((0, 0, 0), reward=1)

        # Test modify illegal attribute.
        with self.assertWarns(RuntimeWarning):
            W.update_object((1, 2, 1), reward=1, prob=0.3, punish=0, undefined_attr=10)

    def test_get_object_attribute(self):
        # Test 'get_object_attribute' function.
        W = GridWorld()
        W.add_area((2, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_object((1, 0, 1), 10, 0.5)
        self.assertEqual(W.get_object_attribute((1, 0, 1), "reward"), 10)
        self.assertEqual(W.get_object_attribute((1, 0, 1), "prob"), 0.5)
        with self.assertRaises(ValueError):
            W.get_object_attribute((0, 0, 0), "prob")
        with self.assertRaises(ValueError):
            W.get_object_attribute((1, 0, 1), "undefined_attr")

    def test_set_altitude(self):
        # Test 'set_altitude' function.
        W = GridWorld()
        W.add_area((3, 4))
        W.add_path((0, 0, 0), (1, 0, 0))
        self.assertEqual(W.get_area_altitude(1).all(), np.zeros((3, 4)).all())
        altitude_mat = np.random.randn(3, 4)
        W.set_altitude(1, altitude_mat=altitude_mat)
        self.assertEqual(W.get_area_altitude(1).all(), altitude_mat.all())
        with self.assertRaises(ValueError):
            W.set_altitude(2, altitude_mat=altitude_mat)
        with self.assertRaises(ValueError):
            W.set_altitude(1, np.zeros((2, 2)))

        # Test set altitude with area name.
        W = GridWorld()
        W.add_area((3, 4), name="test")
        altitude_mat = np.random.randn(3, 4)
        W.set_altitude("test", altitude_mat=altitude_mat)
        self.assertEqual(W.get_area_altitude(1).all(), altitude_mat.all())
        with self.assertRaises(ValueError):
            W.set_altitude("undefined", altitude_mat=altitude_mat)
        with self.assertRaises(TypeError):
            W.set_altitude(1.0, altitude_mat=altitude_mat)

    def test_get_area_shape(self):
        # Test 'get_area_shape' function.
        W = GridWorld()
        W.add_area((4, 10))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((4, 3), name="Right")
        W.add_path((0, 0, 0), (2, 0, 0))

        self.assertEqual(W.get_area_shape(0), (1, 1))
        self.assertEqual(W.get_area_shape(2), (4, 3))
        self.assertEqual(W.get_area_shape("Right"), (4, 3))

        with self.assertRaises(ValueError):
            W.get_area_shape(3)

    def test_get_area_altitude(self):
        # Test 'get_area_altitude' function.
        W = GridWorld()
        altitude_mat = np.random.randn(5, 8)
        W.add_area((5, 8))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.set_altitude(1, altitude_mat)
        self.assertEqual(W.get_area_altitude(1).all(), altitude_mat.all())
        with self.assertRaises(ValueError):
            W.get_area_altitude(2)
        W.add_area((5, 8), name="Right")
        W.add_path((0, 0, 0), (2, 0, 0))
        W.set_altitude("Right", altitude_mat)
        self.assertEqual(W.get_area_altitude("Right").all(), altitude_mat.all())

    def test_init_agent(self):
        # Test 'add_agent' function.
        W = GridWorld()
        with self.assertRaises(ValueError):
            W.init_agent((2, 2, 2))
        W.init_agent()
        self.assertEqual(W.get_agent_state("init"), (0, 0, 0))
        with self.assertRaises(ng.NeuGymOverwriteError):
            W.init_agent()

        # Test initialize agent at other positions.
        W = GridWorld()
        W.add_area((2, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.init_agent((1, 1, 0))
        self.assertEqual(W.get_agent_state("init"), (1, 1, 0))
        W.init_agent((1, 1, 1), overwrite=True)
        self.assertEqual(W.get_agent_state("init"), (1, 1, 1))
        self.assertEqual(W.get_agent_state("current"), (1, 1, 1))

    def test_get_agent_state(self):
        # Test 'get_agent_state' function.
        W = GridWorld()
        W.add_area((1, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_object((1, 0, 1), 10, 1)
        W.init_agent()
        self.assertEqual(W.get_agent_state(), (0, 0, 0))
        W.step((1, 0))
        self.assertEqual(W.get_agent_state(), (1, 0, 0))
        self.assertEqual(W.get_agent_state(when="init"), (0, 0, 0))
        W.step((0, 1))
        self.assertEqual(W.get_agent_state(), (0, 0, 0))

    def test_step(self):
        # Test 'step' function.
        W = GridWorld()
        W.add_area((1, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.set_altitude(1, altitude_mat=np.array([[0.1, 0.2]]))
        W.add_object((1, 0, 1), 10, 1)
        W.init_agent()

        with self.assertRaises(ValueError):
            W.step((1, 1))

        ns, r, d = W.step((0, 0))
        self.assertEqual(ns, (0, 0, 0))
        self.assertEqual(r, 0)
        self.assertEqual(d, False)
        self.assertEqual(W.get_agent_state("current"), (0, 0, 0))

        ns, r, d = W.step((1, 0))
        self.assertEqual(ns, (1, 0, 0))
        self.assertEqual(r, -0.1)
        self.assertEqual(d, False)
        self.assertEqual(W.get_agent_state("current"), (1, 0, 0))

        ns, r, d = W.step((-1, 0))
        self.assertEqual(ns, (0, 0, 0))
        self.assertEqual(r, 0.1)
        self.assertEqual(d, False)
        self.assertEqual(W.get_agent_state("current"), (0, 0, 0))

        W.step((1, 0))
        ns, r, d = W.step((0, 1))
        self.assertEqual(ns, (1, 0, 1))
        self.assertEqual(r, 9.9)
        self.assertEqual(d, True)
        self.assertEqual(W.get_agent_state("current"), (0, 0, 0))

        self.assertEqual(W.time, 5)

    def test_set_reset_state(self):
        # Test 'set_reset_state' function.
        W = GridWorld()
        W.add_area((1, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.set_altitude(1, altitude_mat=np.array([[0.1, 0.2]]))
        W.add_object((1, 0, 1), 10, 1)
        W.init_agent((1, 0, 0))

        W.set_reset_checkpoint()
        W.step((0, 1))
        with self.assertRaises(ng.NeuGymOverwriteError):
            W.set_reset_checkpoint()
        W.set_reset_checkpoint(overwrite=True)
        self.assertEqual(W._reset_state["time"], 1)

    def test_reset(self):
        W = GridWorld()
        W.add_area((1, 3))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.set_altitude(1, altitude_mat=np.array([[0.1, 0.2, 0.3]]))
        W.add_object((1, 0, 2), 10, 1)
        W.init_agent((1, 0, 0))

        with self.assertRaises(ng.NeuGymCheckpointError):
            W.reset()
        W.set_reset_checkpoint()
        for _ in range(2):
            W.step((0, 1))
            W.add_path((1, 0, 2), (0, 0, 0), register_action=(0, 1))
            W.add_object((0, 0, 0), 1, 0.5)
            W.init_agent((0, 0, 0), overwrite=True)
            W.reset()
            self.assertFalse(W.world.has_edge((1, 0, 2), (0, 0, 0)))
            self.assertEqual(len(W._path_alias), 2)
            self.assertEqual(len(W._objects), 1)
            self.assertEqual(W.get_agent_state("current"), (1, 0, 0))
            self.assertEqual(W.get_agent_state("init"), (1, 0, 0))
            self.assertEqual(W.time, 0)

    def test_area_alias(self):
        # Tests on area alias name operations.
        W = GridWorld()
        W.add_area((2, 2), name="Up")
        W.add_path((0, 0, 0), (1, 0, 0))
        W.add_area((2, 2), name="Right")
        W.add_path((0, 0, 0), (2, 0, 0))
        with self.assertRaises(RuntimeError):
            W.add_area((2, 2), name="Right")
        # Test get area name.
        self.assertEqual(W.get_area_name(1), "Up")
        self.assertEqual(W.get_area_name(2), "Right")
        self.assertEqual(W.get_area_index("Up"), 1)
        self.assertEqual(W.get_area_index("Right"), 2)
        with self.assertRaises(ValueError):
            W.get_area_index("test")
        with self.assertRaises(ValueError):
            W.get_area_name(3)

        # Test set area name.
        with self.assertRaises(TypeError):
            W.set_area_name(1.0, "Origin")
        with self.assertRaises(ValueError):
            W.set_area_name(100, "Origin")
        W.set_area_name(0, "Origin")
        self.assertEqual(W.get_area_name(0), "Origin")
        W.set_area_name(1, "NewUp")
        self.assertEqual(W.get_area_name(1), "NewUp")
        self.assertEqual(W.get_area_index("NewUp"), 1)
        self.assertTrue("Up" not in W._area_alias.keys())
        W.set_area_name("Right", "NewRight")
        self.assertEqual(W.get_area_name(2), "NewRight")
        self.assertEqual(W.get_area_index("NewRight"), 2)
        self.assertTrue("Right" not in W._area_alias.keys())


    def test_block_state(self):
        # Test block and unblock state.
        W = GridWorld()
        W.add_area((2, 2))
        W.add_path((0, 0, 0), (1, 0, 0))
        with self.assertRaises(ValueError):
            W.block((3, 3, 3))
        with self.assertRaises(ValueError):
            W.unblock((3, 3, 3))
        test_coord = (1, 1, 1)
        W.block(test_coord)
        self.assertTrue(nx.get_node_attributes(W.world, 'blocked')[test_coord])
        W.unblock(test_coord)
        self.assertTrue(not nx.get_node_attributes(W.world, 'blocked')[test_coord])

        # Test agent behavior.
        W = GridWorld()
        W.add_area((1, 1))
        W.add_path((0, 0, 0), (1, 0, 0))
        W.block((0, 0, 0))
        with self.assertRaises(RuntimeError):
            W.init_agent()
        W.unblock((0, 0, 0))
        W.init_agent()
        with self.assertRaises(RuntimeError):
            W.block((0, 0, 0))
        W.block((1, 0, 0))
        next_state, *_ = W.step((1, 0))
        self.assertEqual(next_state, (0, 0, 0))
        W.unblock((1, 0, 0))
        next_state, *_ = W.step((1, 0))
        self.assertEqual(next_state, (1, 0, 0))
    

if __name__ == '__main__':
    unittest.main()
