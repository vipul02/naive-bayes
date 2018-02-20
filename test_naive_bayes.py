import csv
import os
import unittest

import naive_bayes

test_data = [[6, 148, 72, 35, 0, 33.6, 0.627, 50, 1],
             [1, 85, 66, 29, 0, 26.6, 0.351, 31, 0],
             [8, 183, 64, 0, 0, 23.3, 0.672, 32, 1]]


class TestNaiveBayes(unittest.TestCase):
    filename = 'test.csv'

    @classmethod
    def setUpClass(cls):
        cls.create_csv(cls.filename)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)

    @classmethod
    def create_csv(cls, filename):
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            for row in test_data:
                writer.writerow(row)

    def test_load_csv_file(self):
        dataset = naive_bayes.load_csv(self.filename)

        self.assertEqual(len(dataset), len(test_data))

        self.assertEqual(dataset[-1], test_data[-1])

    def test_split_dataset(self):
        dataset = naive_bayes.load_csv(self.filename)

        split_ratio = 0.67
        train, test = naive_bayes.split_dataset(dataset, split_ratio)

        num_rows = len(dataset)
        train_size = int(num_rows * split_ratio)
        test_size = num_rows - train_size
        self.assertEqual(len(train), train_size)
        self.assertEqual(len(test), test_size)

    def test_separate_by_class(self):
        dataset = [[1, 20, 1], [2, 21, 0], [3, 22, 1]]

        separated = naive_bayes.separate_by_class(dataset)

        expected_separation = {
            0: [
                [2, 21, 0]
            ],
            1: [
                [1, 20, 1],
                [3, 22, 1]
            ]
        }
        self.assertEqual(separated, expected_separation)

    def test_mean(self):
        numbers = [1, 2, 3, 4, 5]

        avg = naive_bayes.mean(numbers)

        expected_mean = 3.0
        self.assertEqual(avg, expected_mean)

    def test_stdev(self):
        numbers = [1, 2, 3, 4, 5]

        stdev = naive_bayes.stdev(numbers)

        expected_stdev = 1.5811388300841898
        self.assertEqual(stdev, expected_stdev)

    def test_summarize(self):
        dataset = [[1, 20, 1], [2, 21, 0], [3, 22, 1]]

        summaries = naive_bayes.summarize(dataset)

        expected_summaries = [(2.0, 1.0), (21.0, 1.0)]
        self.assertEqual(summaries, expected_summaries)

    def test_summarize_by_class(self):
        dataset = [[1, 20, 1],
                   [2, 21, 0],
                   [3, 22, 1],
                   [4, 22, 0]]
        summary = naive_bayes.summarize_by_class(dataset)

        expected_summary = {
            0: [(3.0, 1.4142135623730951),
                (21.5, 0.7071067811865476)],
            1: [(2.0, 1.4142135623730951),
                (21.0, 1.4142135623730951)]
        }
        self.assertEqual(summary, expected_summary)

    def test_calculate_probability(self):
        expected_probability = 0.0624896575937
        x = 71.5
        mean = 73
        stdev = 6.2

        probability = naive_bayes.calculate_probability(x, mean, stdev)

        self.assertAlmostEqual(expected_probability, probability)

    def test_calculate_class_probabilities(self):
        expected_class_zero_probability = 0.7820853879509118
        expected_class_one_probability = 6.298736258150442e-05
        summaries = {0: [(1, 0.5)], 1: [(20, 5.0)]}
        input_vector = [1.1, '?']
        probabilities = naive_bayes.calculate_class_probabilities(summaries, input_vector)
        self.assertAlmostEqual(expected_class_zero_probability, probabilities[0])
        self.assertAlmostEqual(expected_class_one_probability, probabilities[1])

    def test_predict(self):
        expected_prediction = 'A'

        summaries = {
            'A': [(1, 0.5)],
            'B': [(20, 5.0)]
        }
        input_vector = [1.1, '?']

        prediction = naive_bayes.predict(summaries, input_vector)

        self.assertEqual(expected_prediction, prediction)


if __name__ == '__main__':
    unittest.main()
