from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_table import OpenedVoteTable, CommitmentTable
from auditor.audit_tables import audit_tables, CommitmentData, OpenedData


@fixture
def opened_data(
    left_opened_vote_table: OpenedVoteTable, right_opened_vote_table: OpenedVoteTable
) -> OpenedData:
    return {"1": left_opened_vote_table, "2": right_opened_vote_table}


@fixture
def invalid_opened_data_all_columns_opened(
    all_opened_vote_table: OpenedVoteTable,
) -> OpenedData:
    return {"1": all_opened_vote_table, "2": all_opened_vote_table}


@fixture
def invalid_opened_data_one_table_longer(
    left_opened_vote_table: OpenedVoteTable, long_opened_vote_table: OpenedVoteTable
) -> OpenedData:
    return {"1": left_opened_vote_table, "2": long_opened_vote_table}


@fixture
def invalid_opened_data_wrong_keys(
    left_opened_vote_table: OpenedVoteTable, right_opened_vote_table: OpenedVoteTable
) -> OpenedData:
    return {"X": left_opened_vote_table, "2": right_opened_vote_table}


@fixture
def invalid_opened_data_missing_keys(
    left_opened_vote_table: OpenedVoteTable,
) -> OpenedData:
    return {"1": left_opened_vote_table}


@fixture
def commitment_data(commitment_table: CommitmentTable) -> CommitmentData:
    return {"1": commitment_table, "2": commitment_table}


@fixture
def invalid_commitment_data_invalid_table(
    commitment_table: CommitmentTable, invalid_commitment_table: CommitmentTable
) -> CommitmentData:
    return {"1": commitment_table, "2": invalid_commitment_table}


@fixture
def invalid_commitment_data_one_table_longer(
    commitment_table: CommitmentTable, long_commitment_table: CommitmentTable
) -> CommitmentData:
    return {"1": commitment_table, "2": long_commitment_table}


@fixture
def invalid_commitment_data_wrong_keys(
    commitment_table: CommitmentTable,
) -> CommitmentData:
    return {"Y": commitment_table, "2": commitment_table}


@fixture
def invalid_commitment_data_missing_keys(
    commitment_table: CommitmentTable,
) -> CommitmentData:
    return {"1": commitment_table}


@fixture
def invalid_commitment_data_too_many_keys(
    commitment_table: CommitmentTable,
) -> CommitmentData:
    return {"1": commitment_table, "2": commitment_table, "3": commitment_table}


def test_successful_audit(opened_data: OpenedData, commitment_data: CommitmentData):
    assert audit_tables(opened_data, commitment_data) is True


@mark.parametrize(
    "invalid_opened_data",
    (
        lazy_fixture("invalid_opened_data_one_table_longer"),
        lazy_fixture("invalid_opened_data_all_columns_opened"),
        lazy_fixture("invalid_opened_data_wrong_keys"),
        lazy_fixture("invalid_opened_data_missing_keys"),
    ),
)
def test_invalid_data_audit(
    invalid_opened_data: OpenedData, commitment_data: CommitmentData
):
    assert audit_tables(invalid_opened_data, commitment_data) is False


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
def test_invalid_commitment_audit(
    opened_data: OpenedData, invalid_commitment_data: CommitmentData
):
    assert audit_tables(opened_data, invalid_commitment_data) is False


def test_tables_of_different_len(
    invalid_opened_data_one_table_longer: OpenedData,
    invalid_commitment_data_one_table_longer: CommitmentData,
):
    assert (
        audit_tables(
            invalid_opened_data_one_table_longer,
            invalid_commitment_data_one_table_longer,
        )
        is False
    )


def test_empty_data():
    assert audit_tables(dict(), dict()) is False
