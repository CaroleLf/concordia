import unittest
from CONCORDIA.METIER.main import create_shop, add_colonists_to_initial
from CONCORDIA.TEST.data_factory import DataFactory


class TestMain(unittest.TestCase):
    def test_find_way_by_name(self):
        cards = DataFactory.create_default_cards()
        print(cards)
        shop = create_shop(cards)
        self.assertEqual(5, len(shop))
        self.assertNotEqual(shop['I'], None)
        self.assertNotEqual(shop['II'], None)
        self.assertNotEqual(shop['III'], None)
        self.assertNotEqual(shop['IV'], None)
        self.assertNotEqual(shop['V'], None)

    def test_add_colonists_to_initial(self):
        colons = []
        add_colonists_to_initial(initial_colon=colons, colonist_type="sea", color="blue", nb_turn=3)
        self.assertEqual(len(colons), 3)
        add_colonists_to_initial(initial_colon=colons, colonist_type="sea", color="blue", nb_turn=3)
        self.assertEqual(len(colons), 6)
        add_colonists_to_initial(initial_colon=colons, colonist_type="sea", color="blue", nb_turn=2)
        self.assertEqual(len(colons), 8)
