from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_vote import (
    audit_vote,
    OpenedVote,
    Commitment,
    OpenedLeft,
    OpenedRight,
)


@fixture
def left_opened_vote():
    return OpenedVote(
        left=OpenedLeft(
            key="8e7dab35dc53194f871a9d35a1e014ec02854119f387347d92d7310712d7ec73",
            data="0-6C6AC7158C5F086E-853334",
        ),
        middle=1,
    )


@fixture
def right_opened_vote():
    return OpenedVote(
        middle=1,
        right=OpenedRight(
            key="4972061d4ae700aa12ed3727221aaa99d5e43a27f1cdfc2fc276ef9a8aae6c4f",
            data="0-0",
        ),
    )


@fixture
def opened_vote():
    return OpenedVote(
        left=OpenedLeft(
            key="8e7dab35dc53194f871a9d35a1e014ec02854119f387347d92d7310712d7ec73",
            data="0-6C6AC7158C5F086E-853334",
        ),
        middle=1,
        right=OpenedRight(
            key="4972061d4ae700aa12ed3727221aaa99d5e43a27f1cdfc2fc276ef9a8aae6c4f",
            data="0-0",
        ),
    )


@fixture
def commitment():
    return Commitment(
        left="e04b0dab3e3dfe11fc7a093429aa9788003623a49dd659b9ce2a22d94d84606a",
        middle=1,
        right="8b6c1b2fc99055bc3125ad885d961803982e1e29778514f48aae9f08e88f877a",
    )


@fixture
def invalid_commitment():
    return Commitment(
        left="xd4b0dab3e3dfe11fc7a093429aa9788003623a49dd659b9ce2a22d94d84606a",
        middle=1,
        right="xd55787f5d831a8c84b56b8af0fa6dcb2f631ff4ec9d3f54086998435e59cdc5",
    )


@fixture
def invalid_middle_commitment():
    return Commitment(
        left="e04b0dab3e3dfe11fc7a093429aa9788003623a49dd659b9ce2a22d94d84606a",
        middle=0,
        right="8b6c1b2fc99055bc3125ad885d961803982e1e29778514f48aae9f08e88f877a",
    )


@mark.parametrize(
    "opened", (lazy_fixture("left_opened_vote"), lazy_fixture("right_opened_vote"))
)
def test_success(opened: OpenedVote, commitment: Commitment):
    assert audit_vote(opened, commitment)


@mark.parametrize(
    "opened", (lazy_fixture("left_opened_vote"), lazy_fixture("right_opened_vote"))
)
def test_invalid_commitment(opened: OpenedVote, invalid_commitment: Commitment):
    assert not audit_vote(opened, invalid_commitment)


def test_opened_cannot_have_both_left_and_right(
    opened_vote: OpenedVote, commitment: Commitment
):
    assert not audit_vote(opened_vote, commitment)


@mark.parametrize(
    "opened", (lazy_fixture("left_opened_vote"), lazy_fixture("right_opened_vote"))
)
def test_invalid_middle_filed(
    opened: OpenedVote, invalid_middle_commitment: Commitment
):
    assert not audit_vote(opened, invalid_middle_commitment)
