from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_vote import Commitment
from auditor.audit_table import CommitmentTable
from auditor.audit_tables import TallyTables
from auditor.audit_pre_election_row import (
    audit_pre_election_row,
    audit_pre_election_table,
    audit_pre_election_tables,
    PreElectionRow,
    PreElectionTable,
    PreElectionTables,
)


@fixture
def pre_election_row(commitment: Commitment) -> PreElectionRow:
    return PreElectionRow(left=commitment.left, middle="0", right=commitment.right)


@fixture
def pre_election_row_invalid_middle(commitment: Commitment) -> PreElectionRow:
    return PreElectionRow(left=commitment.left, middle="1", right=commitment.right)


@fixture
def pre_election_table(
    commitment: Commitment, commitment_2: Commitment
) -> PreElectionTable:
    return [
        PreElectionRow(left=commitment.left, middle="0", right=commitment.right),
        PreElectionRow(left=commitment_2.left, middle="0", right=commitment_2.right),
    ]


@fixture
def pre_election_table_invalid_middle(
    commitment: Commitment, commitment_2: Commitment
) -> PreElectionTable:
    return [
        PreElectionRow(left=commitment.left, middle="0", right=commitment.right),
        PreElectionRow(left=commitment_2.left, middle="1", right=commitment_2.right),
    ]


@fixture
def long_pre_election_table(
    commitment: Commitment, commitment_2: Commitment
) -> PreElectionTable:
    return [
        PreElectionRow(left=commitment.left, middle="0", right=commitment.right),
        PreElectionRow(left=commitment_2.left, middle="0", right=commitment_2.right),
        PreElectionRow(left=commitment_2.left, middle="0", right=commitment_2.right),
    ]


@fixture
def pre_election_tables(pre_election_table: PreElectionTable) -> PreElectionTables:
    return {"1": pre_election_table, "2": pre_election_table}


@fixture
def pre_election_tables_invalid_middle(
    pre_election_table: PreElectionTable,
    pre_election_table_invalid_middle: PreElectionTable,
) -> PreElectionTables:
    return {"1": pre_election_table, "2": pre_election_table_invalid_middle}


@fixture
def pre_election_tables_invalid_keys(
    pre_election_table: PreElectionTable,
) -> PreElectionTables:
    return {"1": pre_election_table, "X": pre_election_table}


@fixture
def pre_election_tables_too_many_keys(
    pre_election_table: PreElectionTable,
) -> PreElectionTables:
    return {"1": pre_election_table, "2": pre_election_table, "3": pre_election_table}


@fixture
def pre_election_tables_one_table_longer(
    pre_election_table: PreElectionTable, long_pre_election_table: PreElectionTable
) -> PreElectionTables:
    return {"1": pre_election_table, "2": long_pre_election_table}


def test_success_pre_election_row(
    pre_election_row: PreElectionRow, commitment: Commitment
):
    assert audit_pre_election_row(pre_election_row, commitment) is True


def test_invalid_pre_election_row(
    pre_election_row_invalid_middle: PreElectionRow, commitment: Commitment
):
    assert audit_pre_election_row(pre_election_row_invalid_middle, commitment) is False


def test_invalid_commitment(
    pre_election_row: PreElectionRow, invalid_commitment: Commitment
):
    assert audit_pre_election_row(pre_election_row, invalid_commitment) is False


def test_success_pre_election_table(
    pre_election_table: PreElectionTable, commitment_table: CommitmentTable
):
    assert audit_pre_election_table(pre_election_table, commitment_table) is True


@mark.parametrize(
    "commitment_",
    (lazy_fixture("invalid_commitment_table"), lazy_fixture("long_commitment_table")),
)
def test_pre_election_table_invalid_commitment(
    pre_election_table: PreElectionTable, commitment_: CommitmentTable
):
    assert audit_pre_election_table(pre_election_table, commitment_) is False


def test_invalid_pre_election_table(
    pre_election_table_invalid_middle: PreElectionTable,
    commitment_table: CommitmentTable,
):
    assert (
        audit_pre_election_table(pre_election_table_invalid_middle, commitment_table)
        is False
    )


def test_success_pre_election_tables(
    pre_election_tables: PreElectionTables, commitment_data: TallyTables
):
    assert audit_pre_election_tables(pre_election_tables, commitment_data) is True


@mark.parametrize(
    "pre_election_tables_",
    (
        lazy_fixture("pre_election_tables_invalid_middle"),
        lazy_fixture("pre_election_tables_invalid_keys"),
        lazy_fixture("pre_election_tables_too_many_keys"),
    ),
)
def test_invalid_pre_election_tables(
    pre_election_tables_: PreElectionTables, commitment_data: TallyTables
):
    assert audit_pre_election_tables(pre_election_tables_, commitment_data) is False


@mark.parametrize(
    "invalid_commitment_data",
    (
        lazy_fixture("invalid_commitment_data_invalid_table"),
        lazy_fixture("invalid_commitment_data_one_table_longer"),
        lazy_fixture("invalid_commitment_data_wrong_keys"),
        lazy_fixture("invalid_commitment_data_missing_keys"),
        lazy_fixture("invalid_commitment_data_too_many_keys"),
    ),
)
def test_invalid_pre_election_tables_invalid_commitment(
    pre_election_tables: PreElectionTables, invalid_commitment_data: TallyTables
):
    assert (
        audit_pre_election_tables(pre_election_tables, invalid_commitment_data) is False
    )


def test_tables_of_different_len(
    pre_election_tables_one_table_longer: PreElectionTables,
    invalid_commitment_data_one_table_longer: TallyTables,
):
    assert (
        audit_pre_election_tables(
            pre_election_tables_one_table_longer,
            invalid_commitment_data_one_table_longer,
        )
        is False
    )
