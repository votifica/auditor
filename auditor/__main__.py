import argparse
import json

from auditor.audit_tables import audit_tables, AuditTables, TallyTables
from auditor.audit_table import CommitmentTable, OpenedVoteTable
from auditor.audit_vote import Commitment, OpenedVote, OpenedLeft, OpenedRight


def _load_tally(path) -> TallyTables:
    with open(path) as f:
        tally = json.load(f)

    commitment_tables = {}

    for table_id in tally:
        commitment_table = [
            Commitment(
                left=commitment["left"],
                middle=int(commitment["middle"]),
                right=commitment["right"],
            )
            for commitment in tally[table_id]
        ]
        commitment_tables[table_id] = commitment_table

    return commitment_tables


def _load_opened_vote(opened_vote_json) -> OpenedVote:
    left = None
    right = None
    middle = int(opened_vote_json["middle"])
    if isinstance(opened_vote_json["right"], dict):
        right = OpenedRight(
            key=opened_vote_json["right"]["key"], data=opened_vote_json["right"]["data"]
        )

    if isinstance(opened_vote_json["left"], dict):
        left = OpenedLeft(
            key=opened_vote_json["left"]["key"], data=opened_vote_json["left"]["data"]
        )

    return OpenedVote(left=left, middle=middle, right=right)


def _load_opened_data(path) -> AuditTables:
    with open(path) as f:
        opened_data = json.load(f)

    opened_tables = {}

    for table_id in opened_data:
        opened_table = [
            _load_opened_vote(opened_vote_json)
            for opened_vote_json in opened_data[table_id]
        ]
        opened_tables[table_id] = opened_table

    return opened_tables


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voting auditor.")
    parser.add_argument("tally", type=str, help="audit_data-tally.json file path")
    parser.add_argument("opened", type=str, help="audit_data-opened.json file path")

    args = parser.parse_args()

    tally = _load_tally(args.tally)
    opened = _load_opened_data(args.opened)

    print(f"Data {'is' if audit_tables(opened, tally) else 'is not'} valid")
