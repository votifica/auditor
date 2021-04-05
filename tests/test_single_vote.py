from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture

from auditor.audit_vote import (
    audit_vote,
    OpenedVote,
    Commitment,
)


@mark.parametrize(
    "opened", (lazy_fixture("left_opened_vote"), lazy_fixture("right_opened_vote"))
)
def test_success(opened: OpenedVote, commitment: Commitment):
    assert audit_vote(opened, commitment) is True


@mark.parametrize(
    "opened", (lazy_fixture("left_opened_vote"), lazy_fixture("right_opened_vote"))
)
def test_invalid_commitment(opened: OpenedVote, invalid_commitment: Commitment):
    assert audit_vote(opened, invalid_commitment) is False


def test_opened_cannot_have_both_left_and_right(
    opened_vote: OpenedVote, commitment: Commitment
):
    assert audit_vote(opened_vote, commitment) is False


@mark.parametrize(
    "opened", (lazy_fixture("left_opened_vote"), lazy_fixture("right_opened_vote"))
)
def test_invalid_middle_filed(
    opened: OpenedVote, invalid_middle_commitment: Commitment
):
    assert audit_vote(opened, invalid_middle_commitment) is False


def test_empty_opened_vote(empty_opened_vote: OpenedVote, commitment: Commitment):
    assert audit_vote(empty_opened_vote, commitment) is False
