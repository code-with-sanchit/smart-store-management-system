import unittest

import pandas as pd

from data_analysis.sales_report import summarize_sales_by_day


class SalesReportTests(unittest.TestCase):
    def test_daily_summary_groups_orders_by_calendar_date(self):
        source = pd.DataFrame({
            "sale_datetime": ["2026-01-01 09:00", "2026-01-01 15:00", "2026-01-02 10:00"],
            "total_amount": [100, 200, 50],
        })
        summary = summarize_sales_by_day(source)
        self.assertEqual(len(summary), 2)
        first_day = summary.loc[summary["sale_date"].astype(str) == "2026-01-01"].iloc[0]
        self.assertEqual(first_day["orders"], 2)
        self.assertEqual(first_day["revenue"], 300)
