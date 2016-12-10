import pandas as pd


class RentsClient:

	def __init__(self, csv_pathname, metro):
		df = pd.read_csv(csv_pathname)
		self.rents = df[df["Metro"] == metro]
		self.DATE_STRING = "2016-10"


	def get_avg_rent(self, neighborhood):
		result = self.rents.loc[self.rents["RegionName"] == neighborhood]
		if not result.empty:
			return result.iloc[0][self.DATE_STRING]
		else:
			return None

if __name__ == "__main__":

	cli = RentsClient("data/MedianRentalPrice_1Bedroom.csv", "New York")

	print cli.get_avg_rent("Soho")