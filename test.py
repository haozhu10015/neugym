import unittest
from neugym.environment.gridworld import GridWorld


class TestGridWorld(unittest.TestCase):
    # Test 'neugym.environment.GridWorld' object.
    def test_init(self):
        # Test default instantiation.
        w = GridWorld()
        self.assertEqual(w.world.number_of_nodes(), 1)
        self.assertTrue((0, 0, 0) in w.world.nodes)

        # Test manually set origin shape.
        w = GridWorld((3, 3))
        self.assertEqual(w.world.number_of_nodes(), 9)
        self.assertEqual(w.world.number_of_edges(), 12)

    def test_add_area(self):
        # Test 'add_area' function.
        # Test default parameters.
        w = GridWorld()
        w.add_area((2, 2))
        self.assertEqual(w.num_area, 1)
        self.assertTrue(((0, 0, 0), (1, 0, 0)) in w.world.edges)
        self.assertEqual(w.alias[(0, 1, 0)], (1, 0, 0))
        self.assertEqual(w.alias[(1, -1, 0)], (0, 0, 0))
        self.assertEqual(w.world.number_of_nodes(), 5)
        self.assertEqual(w.world.number_of_edges(), 5)

        # Test manually specify inter-area connections.
        with self.assertRaises(ValueError):
            w.add_area((2, 3), access_from=(1, 1, 1), access_to=(1, 2))
        self.assertEqual(w.num_area, 1)

        w.add_area((2, 3), access_from=(1, 1, 1), access_to=(1, 0), register_action=(0, 1))
        self.assertTrue(((1, 1, 1), (2, 1, 0)) in w.world.edges)
        self.assertEqual(w.alias[(1, 1, 2)], (2, 1, 0))
        self.assertEqual(w.alias[(2, 1, -1)], (1, 1, 1))
        self.assertEqual(len(w.alias), 4)
        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_from=(0, 0))
        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_from=(99, 0, 0))

        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_to=(0, 0, 0))
        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_to=(3, 3))
        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_to=(1, 1))
        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_from=(2, 1, 2), access_to=(1, 0), register_action=(1, 0))
        with self.assertRaises(ValueError):
            w.add_area((3, 3), access_from=(2, 1, 2), access_to=(1, 0), register_action=(3, 3))

    def test_remove_area(self):
        # Test 'remove_area' function.
        w = GridWorld()
        w.add_area((2, 2))
        w.add_area((3, 3))
        w.add_area((5, 5))
        w.add_object((1, 0, 0), 1, 0.5)
        w.add_object((2, 0, 0), 1, 0.6)
        w.add_object((3, 0, 0), 1, 0.7)
        self.assertEqual(w.world.number_of_edges(), 59)
        self.assertTrue(((0, 0, 0), (3, 0, 0)) in w.world.edges)

        w.remove_area(3)
        self.assertEqual(w.num_area, 2)
        self.assertEqual(w.world.number_of_nodes(), 14)
        self.assertEqual(w.world.number_of_edges(), 18)
        self.assertTrue(((0, 0, 0), (3, 0, 0)) not in w.world.edges)
        self.assertEqual(len(w.objects), 2)
        for obj in w.objects:
            self.assertTrue(obj.coord != (3, 0, 0))

        w.add_area((5, 5), access_to=(1, 1))
        w.add_object((3, 1, 1), 1, 0.7)
        w.remove_area(1)
        w.remove_area(1)
        self.assertEqual(w.num_area, 1)
        self.assertEqual(w.world.number_of_nodes(), 26)
        self.assertEqual(w.world.number_of_edges(), 41)
        self.assertTrue(((0, 0, 0), (1, 0, 0)) not in w.world.edges)
        self.assertTrue(((0, 0, 0), (1, 1, 1)) in w.world.edges)
        self.assertEqual(len(w.objects), 1)
        self.assertEqual((1, 1, 1), w.objects[0].coord)
        self.assertTrue((1, 1, 1) in w.world.nodes)

        # Test remove origin.
        with self.assertRaises(ValueError):
            w.remove_area(0)

    def test_add_object(self):
        # Test 'add_object' function.
        w = GridWorld()
        w.add_area((2, 2))
        w.add_area((4, 3))

        w.add_object((1, 1, 1), 1, 0.3)
        w.add_object((2, 2, 1), 1, 0.7, -1)
        self.assertEqual(len(w.objects), 2)
        self.assertEqual(w.objects[0].reward, 1)
        self.assertEqual(w.objects[0].prob, 0.3)
        self.assertEqual(w.objects[0].punish, 0)
        self.assertEqual(w.objects[0].coord, (1, 1, 1))
        self.assertEqual(w.objects[1].punish, -1)

        # Test add object with illegal coordinate.
        with self.assertRaises(ValueError):
            w.add_object((1, 1), 1, 0, 0.5)
        with self.assertRaises(ValueError):
            w.add_object((3, 1, 1), 1, 0, 0.5)

    def test_remove_object(self):
        # Test 'remove_object' function.
        w = GridWorld()
        w.add_area((4, 3))
        w.add_area((4, 3))
        w.add_area((4, 3))
        w.add_object((1, 2, 1), 1, 0.2)
        w.add_object((2, 2, 1), 1, 0.8)
        w.add_object((3, 2, 1), 1, 0.9)

        w.remove_object((3, 2, 1))
        self.assertEqual(len(w.objects), 2)
        for obj in w.objects:
            self.assertTrue(obj.coord != (3, 2, 1))

        # Test remove undefined object.
        with self.assertRaises(ValueError):
            w.remove_object((0, 0, 0))

    def test_update_object(self):
        # Test 'update_object' function.
        w = GridWorld()
        w.add_area((4, 3))
        w.add_area((4, 3))
        w.add_object((1, 2, 1), 1, 0.3)
        w.add_object((2, 2, 1), 1, 0.7)

        w.update_object((1, 2, 1), reward=10, prob=0.2, punish=-10)
        self.assertEqual(w.objects[0].reward, 10)
        self.assertEqual(w.objects[0].prob, 0.2)
        self.assertEqual(w.objects[0].punish, -10)

        # Test modify undefined object.
        with self.assertRaises(ValueError):
            w.update_object((0, 0, 0), reward=1)

        # Test modify illegal attribute.
        with self.assertRaises(AttributeError):
            w.update_object((1, 2, 1), undefined_attr=10)


if __name__ == '__main__':
    unittest.main()
