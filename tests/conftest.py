from pytest import fixture

from auditor.audit_vote import (
    OpenedVote,
    Commitment,
    OpenedLeft,
    OpenedRight,
)


@fixture
def left_opened_vote() -> OpenedVote:
    return OpenedVote(
        left=OpenedLeft(
            key="8e7dab35dc53194f871a9d35a1e014ec02854119f387347d92d7310712d7ec73",
            data="0-6C6AC7158C5F086E-853334",
        ),
        middle=1,
    )


@fixture
def right_opened_vote() -> OpenedVote:
    return OpenedVote(
        middle=1,
        right=OpenedRight(
            key="4972061d4ae700aa12ed3727221aaa99d5e43a27f1cdfc2fc276ef9a8aae6c4f",
            data="0-0",
        ),
    )


@fixture
def opened_vote() -> OpenedVote:
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
def empty_opened_vote() -> OpenedVote:
    return OpenedVote(middle=0)


@fixture
def commitment() -> Commitment:
    return Commitment(
        left="e04b0dab3e3dfe11fc7a093429aa9788003623a49dd659b9ce2a22d94d84606a",
        middle=1,
        right="8b6c1b2fc99055bc3125ad885d961803982e1e29778514f48aae9f08e88f877a",
    )


@fixture
def invalid_commitment() -> Commitment:
    return Commitment(
        left="xd4b0dab3e3dfe11fc7a093429aa9788003623a49dd659b9ce2a22d94d84606a",
        middle=1,
        right="xd55787f5d831a8c84b56b8af0fa6dcb2f631ff4ec9d3f54086998435e59cdc5",
    )


@fixture
def invalid_middle_commitment() -> Commitment:
    return Commitment(
        left="e04b0dab3e3dfe11fc7a093429aa9788003623a49dd659b9ce2a22d94d84606a",
        middle=0,
        right="8b6c1b2fc99055bc3125ad885d961803982e1e29778514f48aae9f08e88f877a",
    )
