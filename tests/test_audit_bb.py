from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_vote import OpenedLeft, OpenedRight, OpenedVote
from auditor.audit_table import OpenedVoteTable
from auditor.audit_tables import AuditTables
from auditor.audit_bb import (
    BulletinBoard,
    BulletinBoardEntry,
    audit_left_column_bb,
    audit_right_column_bb,
    audit_bb,
)


@fixture
def opened_left_table() -> OpenedVoteTable:
    opened_1 = OpenedLeft(
        key="463985511795ba149dc5d052bc0c0dee9d375c47b9c94ca374c262e4a5c38698",
        data="0-704337551322485-416652537",
    )
    opened_2 = OpenedLeft(
        key="cbd4fe7ac251760da913e4036dd16e44a0996ebd948df469c57e6ef86c5a1800",
        data="0-704337551322485-487491335",
    )
    opened_3 = OpenedLeft(
        key="c67bafd4d11fc0acb43be5bbea6276954c7c46afa46b43985b8563bb008cf294",
        data="1-141026018500926-992023560",
    )
    opened_4 = OpenedLeft(
        key="7e46c9468f1881beef0d3208306b9dbe78eaefeae505a67f1cb0221f1a85a9c8",
        data="1-141026018500926-414929953",
    )

    return [
        OpenedVote(left=opened_1, middle=1),
        OpenedVote(left=opened_2, middle=0),
        OpenedVote(left=opened_3, middle=0),
        OpenedVote(left=opened_4, middle=1),
    ]


@fixture
def invalid_opened_left_table(opened_left_table: OpenedVoteTable) -> OpenedVoteTable:
    opened_left_table[0].middle = 0
    opened_left_table[1].middle = 1
    opened_left_table[2].middle = 1
    opened_left_table[3].middle = 0

    return opened_left_table


@fixture
def opened_right_table() -> OpenedVoteTable:
    opened_right_table = OpenedRight(
        key="4972061d4ae700aa12ed3727221aaa99d5e43a27f1cdfc2fc276ef9a8aae6c4f",
        data="0-0",
    )

    return [
        OpenedVote(right=opened_right_table, middle=1),
        OpenedVote(right=opened_right_table, middle=1),
        OpenedVote(right=opened_right_table, middle=0),
        OpenedVote(right=opened_right_table, middle=0),
    ]


@fixture
def invalid_opened_right_table(opened_right_table: OpenedVoteTable) -> OpenedVoteTable:
    opened_right_table[0].middle = 0

    return opened_right_table


@fixture
def opened_data(
    opened_left_table: OpenedVoteTable, opened_right_table: OpenedVoteTable
) -> AuditTables:
    return {"0": opened_left_table, "1": opened_right_table}


@fixture
def invalid_left_opened_data(
    invalid_opened_left_table: OpenedVoteTable, opened_right_table: OpenedVoteTable
) -> AuditTables:
    return {"0": invalid_opened_left_table, "1": opened_right_table}


@fixture
def invalid_right_opened_data(
    opened_left_table: OpenedVoteTable, invalid_opened_right_table: OpenedVoteTable
) -> AuditTables:
    return {"0": opened_left_table, "1": invalid_opened_right_table}


@fixture
def bb() -> BulletinBoard:
    return {
        "0": BulletinBoardEntry(
            cast_codes={"0": "704337551322485", "1": "141026018500926"},
            vote_codes={"0": ["416652537"], "1": ["414929953"]},
        )
    }


@fixture
def bb_voted_twice() -> BulletinBoard:
    return {
        "0": BulletinBoardEntry(
            cast_codes={"0": "704337551322485", "1": "141026018500926"},
            vote_codes={"0": ["416652537"], "1": []},
        ),
        "1": BulletinBoardEntry(
            cast_codes={"0": "704337551322485", "1": "141026018500926"},
            vote_codes={"0": [], "1": ["414929953"]},
        ),
    }


@fixture
def invalid_bb_wrong_vote_code() -> BulletinBoard:
    return {
        "0": BulletinBoardEntry(
            cast_codes={"0": "704337551322485", "1": "141026018500926"},
            vote_codes={"0": ["1234566789"], "1": ["414929953"]},
        )
    }


@fixture
def invalid_bb_wrong_cast_code() -> BulletinBoard:
    return {
        "0": BulletinBoardEntry(
            cast_codes={"0": "111111111111111", "1": "141026018500926"},
            vote_codes={"0": ["416652537"], "1": ["414929953"]},
        )
    }


@fixture
def invalid_bb_missing_votes() -> BulletinBoard:
    return {
        "0": BulletinBoardEntry(
            cast_codes={"0": "704337551322485", "1": "141026018500926"},
            vote_codes={"0": [], "1": []},
        )
    }


@fixture
def invalid_bb_empty() -> BulletinBoard:
    return {}


def test_audit_left_column_bb_voted_twice_table(
    bb_voted_twice: BulletinBoard, opened_left_table: OpenedVoteTable
):
    assert audit_left_column_bb(bb_voted_twice, opened_left_table) is True


def test_audit_left_column_bb(bb: BulletinBoard, opened_left_table: OpenedVoteTable):
    assert audit_left_column_bb(bb, opened_left_table) is True


@mark.parametrize(
    "invalid_bb",
    (
        lazy_fixture("invalid_bb_missing_votes"),
        lazy_fixture("invalid_bb_empty"),
        lazy_fixture("invalid_bb_wrong_cast_code"),
        lazy_fixture("invalid_bb_wrong_vote_code"),
    ),
)
def test_audit_left_column_invalid_bb(
    invalid_bb: BulletinBoard, opened_left_table: OpenedVoteTable
):
    assert audit_left_column_bb(invalid_bb, opened_left_table) is False


def test_audit_invalid_left_column_bb(
    bb: BulletinBoard, invalid_opened_left_table: OpenedVoteTable
):
    assert audit_left_column_bb(bb, invalid_opened_left_table) is False


def test_audit_right_column_bb(bb: BulletinBoard, opened_right_table: OpenedVoteTable):
    assert audit_right_column_bb(bb, opened_right_table) is True


def test_audit_right_column_bb_voted_twice_table(
    bb_voted_twice: BulletinBoard, opened_right_table: OpenedVoteTable
):
    assert audit_right_column_bb(bb_voted_twice, opened_right_table) is True


def test_audit_right_column_empty_bb(invalid_bb_empty: BulletinBoard):
    assert audit_right_column_bb(invalid_bb_empty, []) is False


def test_audit_invalid_right_column_bb(
    bb: BulletinBoard, invalid_opened_right_table: OpenedVoteTable
):
    assert audit_right_column_bb(bb, invalid_opened_right_table) is False


@mark.parametrize(
    "invalid_bb",
    (
        lazy_fixture("invalid_bb_missing_votes"),
        lazy_fixture("invalid_bb_empty"),
    ),
)
def test_audit_right_column_invalid_bb(
    invalid_bb: BulletinBoard, opened_right_table: OpenedVoteTable
):
    assert audit_right_column_bb(invalid_bb, opened_right_table) is False


def test_audit_right_column_empty_bb(invalid_bb_empty: BulletinBoard):
    assert audit_right_column_bb(invalid_bb_empty, []) is False


def test_audit_bb(bb: BulletinBoard, opened_data: AuditTables):
    assert audit_bb(bb, opened_data) is True


def test_audit_bb_voted_twice(bb_voted_twice: BulletinBoard, opened_data: AuditTables):
    assert audit_bb(bb_voted_twice, opened_data) is True


@mark.parametrize(
    "invalid_bb",
    (
        lazy_fixture("invalid_bb_missing_votes"),
        lazy_fixture("invalid_bb_empty"),
        lazy_fixture("invalid_bb_wrong_cast_code"),
        lazy_fixture("invalid_bb_wrong_vote_code"),
    ),
)
def test_audit_invalid_bb(invalid_bb: BulletinBoard, opened_data: AuditTables):
    assert audit_bb(invalid_bb, opened_data) is False


def test_audit_empty_bb(invalid_bb_empty: BulletinBoard):
    assert audit_bb(invalid_bb_empty, {}) is False


@mark.parametrize(
    "invalid_opened_data",
    (
        lazy_fixture("invalid_left_opened_data"),
        lazy_fixture("invalid_right_opened_data"),
    ),
)
def test_audit_bb_invalid_opened_data(
    bb: BulletinBoard, invalid_opened_data: AuditTables
):
    assert audit_bb(bb, invalid_opened_data) is False
