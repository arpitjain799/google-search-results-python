import random
import unittest
import os
import pprint
from serpapi import DuckDuckGoSearch

class TestDuckDuckGoSearch(unittest.TestCase):

		def setUp(self):
				DuckDuckGoSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")

		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
		def test_get_json(self):
				search = DuckDuckGoSearch({"q": "Coffee"})
				data = search.get_json()
				self.assertIsNone(data.get("error"))
				self.assertEqual(data["search_metadata"]["status"], "Success")
				self.assertIsNotNone(data["search_metadata"]["duckduckgo_url"])
				self.assertIsNotNone(data["search_metadata"]["id"])
				if "organic_results" in data:
					self.assertIsNotNone(data["organic_results"][1]["title"])
				# pp = pprint.PrettyPrinter(indent=2)
				# pp.pprint(data)
				self.assertTrue(len(data.keys()) > 3)

		@unittest.skipIf((os.getenv("API_KEY") == None), "no api_key provided")
		def test_paginate_page_size(self):
			start = 10
			limit = 3

			# use parameters in
			params = {
				"q": "coca cola",
				"api_key": os.getenv("API_KEY"),
				"start": start,
			}

			titles = []

			search = DuckDuckGoSearch(params)
			pages = search.pagination(limit=limit)

			page_count = 0
			count = 0

			for page in pages:
				page_count += 1

				for organic_results in page.get("organic_results", []):
					count += 1
					i = 0

					for t in titles:
						i += 1

						if t == organic_results.get('title'):
							print(f"{count} duplicated title: {t} at index: {i}")

					titles.append(organic_results['title'])

				self.assertEqual(count % 2, 0, f"page {page_count} does not contain 20 elements")

			# check number of pages match
			self.assertEqual(page_count, limit)


if __name__ == '__main__':
		unittest.main()
