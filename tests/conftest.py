from pytest import fixture

from auditor.audit_vote import (
    OpenedVote,
    Commitment,
    OpenedLeft,
    OpenedRight,
)
from auditor.audit_table import OpenedVoteTable, CommitmentTable


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
def left_opened_vote_2() -> OpenedVote:
    return OpenedVote(
        left=OpenedLeft(
            key="2ca784881aebaebc63b53bdc1e55422aefba7cb0536ba48c9d9425e4c5a22fb7",
            data="0-007629B808CD8C5E-085B43",
        ),
        middle=1,
    )


@fixture
def right_opened_vote_2() -> OpenedVote:
    return OpenedVote(
        middle=1,
        right=OpenedRight(
            key="cd9c6d4d31e512c3b3566660d4214d0a1b95410083c3bbf47c6c1e2918f6b13f",
            data="0-1",
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
def commitment_2() -> Commitment:
    return Commitment(
        left="e7cb17ba6162fd2ee95ccd0bc57115f7923b787d2de5382fc32cd6da87d2d4ec",
        middle=1,
        right="bbb07e948f14697d6d7edaab1743cf408d6e20413aa3a01cb2fdca9092733b62",
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


@fixture
def left_opened_vote_table(
    left_opened_vote: OpenedVote, left_opened_vote_2: OpenedVote
) -> OpenedVoteTable:
    return [left_opened_vote, left_opened_vote_2]


@fixture
def right_opened_vote_table(
    right_opened_vote: OpenedVote, right_opened_vote_2: OpenedVote
) -> OpenedVoteTable:
    return [right_opened_vote, right_opened_vote_2]


@fixture
def commitment_table(
    commitment: Commitment, commitment_2: Commitment
) -> CommitmentTable:
    return [commitment, commitment_2]


@fixture
def all_opened_vote_table(opened_vote: OpenedVote) -> OpenedVoteTable:
    return [opened_vote, opened_vote]


@fixture
def long_opened_vote_table(left_opened_vote: OpenedVote) -> OpenedVoteTable:
    return [left_opened_vote, left_opened_vote, left_opened_vote]


@fixture
def long_commitment_table(commitment: Commitment) -> CommitmentTable:
    return [commitment, commitment, commitment]


@fixture
def invalid_commitment_table(
    commitment: Commitment, invalid_commitment: Commitment
) -> CommitmentTable:
    return [commitment, invalid_commitment]
