import unittest

from src.ticket_workflow_seed import (
    DEFAULT_OWNER,
    UNKNOWN_SOURCE,
    delivery_summary,
    filter_delivery_records,
    normalize_delivery_owner,
)


class TicketWorkflowSeedTests(unittest.TestCase):
    def test_blank_owner_uses_default(self):
        self.assertEqual(normalize_delivery_owner(None), DEFAULT_OWNER)

    def test_owner_is_trimmed_and_lowercased(self):
        self.assertEqual(normalize_delivery_owner(" Billing-Ops "), "billing-ops")

    def test_repeated_owner_whitespace_is_collapsed(self):
        self.assertEqual(
            normalize_delivery_owner("  Billing\t \nOps  "),
            "billing ops",
        )

    def test_whitespace_only_owner_uses_default(self):
        self.assertEqual(normalize_delivery_owner(" \t\n "), DEFAULT_OWNER)

    def test_missing_owner_selection_preserves_all_records(self):
        records = [{"owner": "beta"}, {"owner": "alpha"}]
        self.assertEqual(filter_delivery_records(records), records)

    def test_empty_owner_selection_returns_no_records(self):
        self.assertEqual(filter_delivery_records([{"owner": "alpha"}], []), [])

    def test_owner_filter_uses_canonical_values_and_preserves_order(self):
        records = [
            {"id": 1, "owner": " Billing  Ops "},
            {"id": 2, "owner": "platform"},
            {"id": 3, "owner": "billing ops"},
        ]
        self.assertEqual(
            filter_delivery_records(records, ["BILLING\tOPS"]),
            [records[0], records[2]],
        )

    def test_owner_filter_matches_blank_owner_to_default(self):
        records = [{"owner": None}, {"owner": "platform"}]
        self.assertEqual(
            filter_delivery_records(records, [DEFAULT_OWNER]),
            [records[0]],
        )

    def test_summary_contains_existing_fields(self):
        self.assertEqual(
            delivery_summary(
                {"owner": " Billing-Ops ", "status": "queued", "source": "API"}
            ),
            {"owner": "billing-ops", "status": "queued"},
        )

    def test_summary_can_include_normalized_source(self):
        self.assertEqual(
            delivery_summary(
                {"owner": "billing", "status": "queued", "source": " CSV Import "},
                include_source=True,
            ),
            {"owner": "billing", "status": "queued", "source": "csv import"},
        )

    def test_summary_uses_unknown_for_missing_or_blank_source(self):
        for record in (
            {"owner": "billing", "status": "queued"},
            {"owner": "billing", "status": "queued", "source": "   "},
        ):
            with self.subTest(record=record):
                self.assertEqual(
                    delivery_summary(record, include_source=True)["source"],
                    UNKNOWN_SOURCE,
                )


if __name__ == "__main__":
    unittest.main()
