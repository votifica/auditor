import json
import typer
import click_spinner

from auditor.audit_tables import audit_tables, AuditTables, TallyTables
from auditor.audit_vote import Commitment, OpenedVote, OpenedLeft, OpenedRight
from auditor.audit_pre_election_row import (
    PreElectionTables,
    PreElectionRow,
    audit_pre_election_tables,
)
from auditor.audit_bb import BulletinBoardEntry, BulletinBoard, audit_bb
from auditor.audit_tally import TallyResults, audit_tables_tally


app = typer.Typer()


def _load_tally_data(path: str) -> TallyTables:
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


def _load_opened_vote(opened_vote_json: str) -> OpenedVote:
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


def _load_opened_data(path: str) -> AuditTables:
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


def _load_pre_election(path: str) -> PreElectionTables:
    with open(path) as f:
        data = json.load(f)

    commitment_tables = {}

    for table_id in data:
        commitment_table = [
            PreElectionRow(
                left=commitment["left"],
                middle=commitment["middle"],
                right=commitment["right"],
            )
            for commitment in data[table_id]
        ]
        commitment_tables[table_id] = commitment_table

    return commitment_tables


def _load_bb(path: str) -> BulletinBoard:
    with open(path) as f:
        data = json.load(f)

    bb = {}

    for vote_id in data:
        bb_entry = BulletinBoardEntry(**data[vote_id])
        bb[vote_id] = bb_entry

    return bb


def _load_tally(path: str) -> TallyResults:
    with open(path) as f:
        data = json.load(f)

    return data


@app.command()
def audit_elections(
    data_opened: str, data_pre_election: str, data_tally: str, bb: str, tally_all: str
):
    data_pre_election = _load_pre_election(data_pre_election)
    data_tally = _load_tally_data(data_tally)

    print("Auditing pre_election - data_tally...")
    with click_spinner.spinner():
        valid = audit_pre_election_tables(data_pre_election, data_tally)
    print("valid" if valid else "not valid!")

    del data_pre_election
    data_opened = _load_opened_data(data_opened)

    print("Auditing data_tally - data_opened...")
    with click_spinner.spinner():
        valid = audit_tables(data_opened, data_tally)

    print("valid" if valid else "not valid")

    del data_tally

    bb = _load_bb(bb)

    print("Auditing data_opened - bb...")
    with click_spinner.spinner():
        valid = audit_bb(bb, data_opened)
    print("valid" if valid else "not valid")

    del bb

    tally_all = _load_tally(tally_all)

    print("Auditing data_opened - tally with all votes...")
    with click_spinner.spinner():
        valid = audit_tables_tally(tally_all, data_opened)
    print("valid" if valid else "not valid")


@app.command()
def audit_tally_all(data_opened: str, tally_all: str):
    data_opened = _load_opened_data(data_opened)
    tally = _load_tally(tally_all)

    print("Auditing data_opened - tally with all votes...")
    with click_spinner.spinner():
        valid = audit_tables_tally(tally, data_opened)
    print("valid" if valid else "not valid")


@app.command()
def audit_tally_dummies(data_opened: str, tally_dummies: str):
    data_opened = _load_opened_data(data_opened)
    tally = _load_tally(tally_dummies)

    print("Auditing data_opened - tally with dummy votes...")
    with click_spinner.spinner():
        valid = audit_tables_tally(tally, data_opened, False, True)
    print("valid" if valid else "not valid")


@app.command()
def audit_tally_final(data_opened: str, tally_final: str):
    data_opened = _load_opened_data(data_opened)
    tally = _load_tally(tally_final)

    print("Auditing data_opened - final tally...")
    with click_spinner.spinner():
        valid = audit_tables_tally(tally, data_opened, True, False)
    print("valid" if valid else "not valid")


if __name__ == "__main__":
    app()
