from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_vote import OpenedVote
from auditor.audit_table import audit_table, OpenedVoteTable, CommitmentTable


@fixture
def mixed_opened_vote_table(
    left_opened_vote: OpenedVote, right_opened_vote: OpenedVote
) -> OpenedVoteTable:
    return [left_opened_vote, right_opened_vote]


@mark.parametrize(
    "opened_vote_table",
    (lazy_fixture("left_opened_vote_table"), lazy_fixture("right_opened_vote_table")),
)
def test_only_one_column_is_opened_for_the_table(
    opened_vote_table: OpenedVoteTable, commitment_table: CommitmentTable
):
    assert audit_table(opened_vote_table, commitment_table) is True


def test_mixed_columns_are_opened_for_the_table(
    mixed_opened_vote_table: OpenedVoteTable, commitment_table: CommitmentTable
):
    assert audit_table(mixed_opened_vote_table, commitment_table) is False


def test_all_columns_are_opened_for_the_table(
    all_opened_vote_table: OpenedVoteTable, commitment_table: CommitmentTable
):
    assert audit_table(all_opened_vote_table, commitment_table) is False


@mark.parametrize(
    "opened_vote_table, commitment_table_",
    (
        (lazy_fixture("left_opened_vote_table"), lazy_fixture("long_commitment_table")),
        (lazy_fixture("long_opened_vote_table"), lazy_fixture("commitment_table")),
    ),
)
def test_tables_are_different_length(
    opened_vote_table: OpenedVoteTable, commitment_table_: CommitmentTable
):
    assert audit_table(opened_vote_table, commitment_table_) is False


def test_one_row_is_invalid(
    left_opened_vote_table: OpenedVoteTable, invalid_commitment_table: CommitmentTable
):
    assert audit_table(left_opened_vote_table, invalid_commitment_table) is False


def test_empty_tables():
    assert audit_table([], []) is True
