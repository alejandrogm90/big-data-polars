import csv
import os
import tempfile
import unittest

import setup


class SetupExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.data_source = os.path.join(cls.temp_dir.name, "iris.csv")
        rows = [
            (5.1, 3.5, 1.4, 0.2, "Iris-setosa"),
            (6.0, 3.0, 4.0, 1.3, "Iris-setosa"),
            (7.2, 3.2, 6.0, 1.8, "Iris-versicolor"),
            (5.0, 3.3, 1.4, 0.2, "Iris-versicolor"),
            (8.0, 3.4, 6.4, 2.0, "Iris-virginica"),
            (4.9, 3.1, 1.5, 0.1, "Iris-virginica"),
        ]
        with open(cls.data_source, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    "sepal_length",
                    "sepal_width",
                    "petal_length",
                    "petal_width",
                    "species",
                ]
            )
            writer.writerows(rows)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_example_1_filters_and_calculates_mean_by_species(self):
        result = setup.build_example_1_query(self.data_source).collect()
        means = dict(
            zip(result["species"].to_list(), result["sepal_width"].to_list())
        )

        self.assertEqual(
            means,
            {
                "Iris-setosa": 3.25,
                "Iris-versicolor": 3.2,
                "Iris-virginica": 3.4,
            },
        )

    def test_example_2_selects_species_with_sepal_length_over_seven(self):
        result = setup.build_example_2_query(self.data_source).collect()

        self.assertCountEqual(
            result.rows(),
            [
                ("Iris-versicolor", 7.2),
                ("Iris-virginica", 8.0),
            ],
        )

    def test_example_3_returns_unique_species_and_total_count(self):
        result = setup.build_example_3_query(self.data_source).collect()
        totals = dict(zip(result["species"].to_list(), result["Total"].to_list()))

        self.assertEqual(
            totals,
            {
                "Iris-setosa": 6,
                "Iris-versicolor": 6,
                "Iris-virginica": 6,
            },
        )

    def test_example_4_sums_measurements_and_sorts_species_descending(self):
        result = setup.build_example_4_query(self.data_source).collect()

        self.assertEqual(
            result.rows(),
            [
                ("Iris-virginica", 12.9, 6.5, 7.9, 2.1),
                ("Iris-versicolor", 12.2, 6.5, 7.4, 2.0),
                ("Iris-setosa", 11.1, 6.5, 5.4, 1.5),
            ],
        )


if __name__ == "__main__":
    unittest.main()
