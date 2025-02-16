import unittest

from coinbase_advanced_trader.utils.float_range import (FloatRange,
                                                        generate_buy_ranges,
                                                        generate_sell_ranges)


class TestFloatRange(unittest.TestCase):

    def test_creation_valid_range(self):
        range_obj = FloatRange(0.0, 5.0)
        self.assertEqual(range_obj.start, 0.0)
        self.assertEqual(range_obj.end, 5.0)
        self.assertTrue(range_obj.start_inclusive)
        self.assertFalse(range_obj.end_inclusive)

    def test_creation_invalid_range(self):
        with self.assertRaises(ValueError):
            FloatRange(5.0, 0.0)

    def test_contains_behavior(self):
        range_obj = FloatRange(1.0, 5.0)
        self.assertTrue(range_obj.contains(3.0))
        self.assertFalse(range_obj.contains(0.5))
        self.assertFalse(range_obj.contains(5.0))  # end is exclusive by default
        inclusive_range = FloatRange(1.0, 5.0, end_inclusive=True)
        self.assertTrue(inclusive_range.contains(5.0))

    def test_repr(self):
        range_obj = FloatRange(0.1, 1.5, True, True)
        self.assertEqual(repr(range_obj), "[0.1 - 1.5]")
        exclusive_range = FloatRange(0.1, 1.5, False, False)
        self.assertEqual(repr(exclusive_range), "(0.1 - 1.5)")

    def test_edge_cases(self):
        range_obj = FloatRange(2.0, 2.0, True, True)
        self.assertTrue(range_obj.contains(2.0))
        single_inclusive = FloatRange(2.0, 2.0, True, False)
        self.assertTrue(single_inclusive.contains(2.0))
        single_exclusive = FloatRange(2.0, 2.0, False, False)
        self.assertFalse(single_exclusive.contains(2.0))

    def test_equality(self):
        """Test equality of FloatRange instances."""
        range1 = FloatRange(0.0, 1.0)
        range2 = FloatRange(0.0, 1.0)
        range3 = FloatRange(0.0, 1.0, start_inclusive=False)  # Different inclusion
        range4 = FloatRange(0.0, 2.0)  # Different end value

        self.assertEqual(range1, range2)
        self.assertNotEqual(range1, range3)
        self.assertNotEqual(range1, range4)

    def test_hash(self):
        """Test the hash behavior of FloatRange."""
        range1 = FloatRange(0.0, 1.0)
        range2 = FloatRange(0.0, 1.0)
        range3 = FloatRange(1.0, 2.0)

        self.assertEqual(hash(range1), hash(range2))  # Same hashes for equal ranges
        self.assertNotEqual(hash(range1), hash(range3))  # Different hashes for different ranges

        # Ensure FloatRange can be used as a key in a dictionary
        range_dict = {range1: "First range"}
        self.assertIn(range2, range_dict)  # Equal ranges should be treated as the same key
        self.assertNotIn(range3, range_dict)  # Different ranges should not be treated as the same key

    def test_generate_buy_ranges_1(self):
        input = {
            "risk_0": "103",
            "risk_5": "103",
            "risk_10": "103",
            "risk_15": "78",
            "risk_20": "78",
            "risk_25": "",
            "risk_30": "",
            "risk_35": "",
            "risk_40": "",
            "risk_45": "",
            "risk_50": "",
            "risk_55": "",
            "risk_60": "",
            "risk_65": "",
            "risk_70": "",
            "risk_75": "",
            "risk_80": "",
            "risk_85": "",
            "risk_90": "",
            "risk_95": "",
            "risk_100": ""
        }
        ranges = generate_buy_ranges(input)
        assert ranges == {
            FloatRange(0.0, 10.0): 103,
            FloatRange(10.0, 20.0, end_inclusive=True): 78,
        }

    def test_generate_buy_ranges_2(self):
        input = {
            "risk_0": "179",
            "risk_5": "179",
            "risk_10": "179",
            "risk_15": "134",
            "risk_20": "134",
            "risk_25": "89",
            "risk_30": "89",
            "risk_35": "45",
            "risk_40": "45",
            "risk_45": "0",
            "risk_50": "0",
            "risk_55": "0",
            "risk_60": "0",
            "risk_65": "",
            "risk_70": "",
            "risk_75": "",
            "risk_80": "",
            "risk_85": "",
            "risk_90": "",
            "risk_95": "",
            "risk_100": ""
        }
        ranges = generate_buy_ranges(input)
        assert ranges == {
            FloatRange(0.0, 10.0): 179.,
            FloatRange(10.0, 20.0): 134.,
            FloatRange(20.0, 30.0): 89.,
            FloatRange(30.0, 40.0, end_inclusive=True): 45
        }

    def test_generate_buy_ranges_3(self):
        input = {
            "risk_0": "160",
            "risk_5": "160",
            "risk_10": "160",
            "risk_15": "140",
            "risk_20": "140",
            "risk_25": "120",
            "risk_30": "120",
            "risk_35": "100",
            "risk_40": "100",
            "risk_45": "80",
            "risk_50": "80",
            "risk_55": "60",
            "risk_60": "60",
            "risk_65": "40",
            "risk_70": "40",
            "risk_75": "0",
            "risk_80": "",
            "risk_85": "",
            "risk_90": "",
            "risk_95": "",
            "risk_100": ""
        }

        ranges = generate_buy_ranges(input)
        assert ranges == {
            FloatRange(0.0, 10.0): 160.,
            FloatRange(10.0, 20.0): 140.,
            FloatRange(20.0, 30.0): 120.,
            FloatRange(30.0, 40.0): 100.,
            FloatRange(40.0, 50.0): 80.,
            FloatRange(50.0, 60.0): 60.,
            FloatRange(60.0, 70.0, end_inclusive=True): 40
        }

    def test_generate_sell_ranges_1(self):
        input = {
            "risk_0": "",
            "risk_5": "",
            "risk_10": "",
            "risk_15": "",
            "risk_20": "",
            "risk_25": "",
            "risk_30": "",
            "risk_35": "",
            "risk_40": "",
            "risk_45": "",
            "risk_50": "",
            "risk_55": "",
            "risk_60": "10",
            "risk_65": "",
            "risk_70": "20",
            "risk_75": "",
            "risk_80": "30",
            "risk_85": "",
            "risk_90": "40",
            "risk_95": "",
            "risk_100": ""
        }
        ranges = generate_sell_ranges(input)
        assert ranges == {
            FloatRange(60.0, 70.0): 10.,
            FloatRange(70.0, 80.0): 20.,
            FloatRange(80.0, 90.0): 30.,
            FloatRange(90.0, 100.0, end_inclusive=True): 40.
        }

    def test_generate_sell_ranges_1(self):
        input = {
            "risk_0": "",
            "risk_5": "",
            "risk_10": "",
            "risk_15": "",
            "risk_20": "",
            "risk_25": "",
            "risk_30": "",
            "risk_35": "",
            "risk_40": "",
            "risk_45": "",
            "risk_50": "",
            "risk_55": "",
            "risk_60": "",
            "risk_65": "",
            "risk_70": "",
            "risk_75": "",
            "risk_80": "30",
            "risk_85": "",
            "risk_90": "70",
            "risk_95": "",
            "risk_100": ""
        }
        ranges = generate_sell_ranges(input)
        assert ranges == {
            FloatRange(80.0, 90.0): 30.,
            FloatRange(90.0, 100.0, end_inclusive=True): 70.
    }

if __name__ == "__main__":
    unittest.main()
