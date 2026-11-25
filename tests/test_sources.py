"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'shots.csv': ['shot', 'project', 'variant', 'parent', 'segment_start', 'segment_end', 'method', 'final_state'], 'deliveries.csv': ['event', 'shot', 'variant', 'date', 'kind', 'review_until', 'hours'], 'work_logs.csv': ['log', 'shot', 'variant', 'block', 'date', 'activity', 'hours', 'cost'], 'bookings.csv': ['block', 'resource', 'start', 'stop', 'min_bill', 'projects', 'status'], 'invoices.csv': ['entry', 'block', 'booked', 'amount', 'state', 'original_entry'], 'promises.csv': ['project', 'deadline', 'requires', 'basis', 'committed'], 'prerequisites.csv': ['shot', 'variant', 'previous_shot', 'previous_variant', 'shared_resource'], 'revisions.csv': ['revision', 'project', 'shot', 'from_variant', 'to_variant', 'requested_on', 'start_second', 'end_second']}
REFERENCES = [('deliveries.csv', 'shot', 'shots.csv', 'shot'), ('work_logs.csv', 'block', 'bookings.csv', 'block'), ('work_logs.csv', 'shot', 'shots.csv', 'shot'), ('invoices.csv', 'block', 'bookings.csv', 'block'), ('invoices.csv', 'original_entry', 'invoices.csv', 'entry')]
OBSERVED_VALUES = [('shots.csv', 'shot', 'S1', 2), ('bookings.csv', 'block', 'B1', 1), ('work_logs.csv', 'block', 'B0', 3)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
