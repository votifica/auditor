from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_table import OpenedVoteTable, CommitmentTable
from auditor.audit_tables import audit_tables, TallyTables, AuditTables


@fixture
def opened_data(
    left_opened_vote_table: OpenedVoteTable, right_opened_vote_table: OpenedVoteTable
) -> AuditTables:
    return {"1": left_opened_vote_table, "2": right_opened_vote_table}


@fixture
def invalid_opened_data_all_columns_opened(
    all_opened_vote_table: OpenedVoteTable,
) -> AuditTables:
    return {"1": all_opened_vote_table, "2": all_opened_vote_table}


@fixture
def invalid_opened_data_one_table_longer(
    left_opened_vote_table: OpenedVoteTable, long_opened_vote_table: OpenedVoteTable
) -> AuditTables:
    return {"1": left_opened_vote_table, "2": long_opened_vote_table}


@fixture
def invalid_opened_data_wrong_keys(
    left_opened_vote_table: OpenedVoteTable, right_opened_vote_table: OpenedVoteTable
) -> AuditTables:
    return {"X": left_opened_vote_table, "2": right_opened_vote_table}


@fixture
def invalid_opened_data_missing_keys(
    left_opened_vote_table: OpenedVoteTable,
) -> AuditTables:
    return {"1": left_opened_vote_table}


def test_successful_audit(opened_data: AuditTables, commitment_data: TallyTables):
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
    invalid_opened_data: AuditTables, commitment_data: TallyTables
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
    opened_data: AuditTables, invalid_commitment_data: TallyTables
):
    assert audit_tables(opened_data, invalid_commitment_data) is False


def test_tables_of_different_len(
    invalid_opened_data_one_table_longer: AuditTables,
    invalid_commitment_data_one_table_longer: TallyTables,
):
    assert (
        audit_tables(
            invalid_opened_data_one_table_longer,
            invalid_commitment_data_one_table_longer,
        )
        is False
    )


def test_empty_data():
    assert audit_tables(dict(), dict()) is True
