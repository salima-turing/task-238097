import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from federated_data_queries import visualize_data

class TestVisualizeData(unittest.TestCase):

	@patch('federated_data_queries.fetch_data_from_federation')
	def test_visualize_data_correctly_plots_histogram(self, mock_fetch_data):
		# Dummy data
		dummy_data = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
		mock_fetch_data.return_value = dummy_data

		expected_histogram_b64 = self.get_expected_histogram_base64()

		with patch('matplotlib.pyplot.savefig') as mock_savefig:
			visualize_data()

			args, _ = mock_savefig.call_args
			buf = args[0]

			with BytesIO() as img_file:
				plt.savefig(img_file, format='png')
				img_file.seek(0)
				actual_histogram_b64 = base64.b64encode(img_file.read()).decode()

			self.assertAlmostEqual(expected_histogram_b64, actual_histogram_b64, places=5)

	def get_expected_histogram_base64(self):
		# Generate expected histogram data using dummy data and return its base64 representation
		dummy_data = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
		dummy_data['values'].hist()

		with BytesIO() as img_file:
			plt.savefig(img_file, format='png')
			img_file.seek(0)
			return base64.b64encode(img_file.read()).decode()

if __name__ == '__main__':
	unittest.main()
