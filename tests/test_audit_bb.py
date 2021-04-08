from pytest import fixture

from auditor.audit_vote import OpenedLeft, OpenedVote
from auditor.audit_table import OpenedVoteTable
from auditor.audit_bb import BulletinBoard, BulletinBoardEntry, audit_bb_table


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
def bb() -> BulletinBoard:
    return {
        "0": BulletinBoardEntry(
            cast_codes={"0": "704337551322485", "1": "141026018500926"},
            vote_codes={"0": ["416652537"], "1": ["414929953"]},
        )
    }


def test_audit_bb_table(bb: BulletinBoard, opened_left_table: OpenedVoteTable):
    assert audit_bb_table(bb, opened_left_table) is True


def test_audit_bb_invalid_table(bb: BulletinBoard, opened_left_table: OpenedVoteTable):
    opened_left_table[0].middle = 0
    assert audit_bb_table(bb, opened_left_table) is False
