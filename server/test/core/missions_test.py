from typing import List, cast
from architext.core.domain.entities.mission import default_missions
import pytest # type: ignore
from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.commands import CompleteMission
from architext.core import Architext
from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.queries.available_missions import AvailableMissions
from architext.core.services.complete_mission import MissionUnavailable

MISSIONS=default_missions()

def test_complete_mission_success(uow: FakeUnitOfWork, architext: Architext) -> None:
    architext.handle(CompleteMission(mission_id=MISSIONS.tutorial.id), 'oliver')

    with uow as transaction:
        mission_log = transaction.missions.get_mission_log(mission_id=MISSIONS.tutorial.id, user_id='oliver')
        assert mission_log is not None
        assert mission_log.completed_at is not None


def test_complete_unavailable_mission_fails(architext: Architext, uow: FakeUnitOfWork) -> None:
    with pytest.raises(MissionUnavailable):
        architext.handle(CompleteMission(mission_id=MISSIONS.play_with_friends.id), 'oliver')


def test_complete_mission_with_wrong_id_fails(architext: Architext, uow: FakeUnitOfWork) -> None:
    with pytest.raises(MissionUnavailable):
        architext.handle(CompleteMission(mission_id='this_mission_does_not_exist'), 'oliver')


def test_get_new_user_available_missions_query(architext: Architext, uow: FakeUnitOfWork) -> None:
    data = architext.query(AvailableMissions(), 'oliver')

    mission_names = [mission.name for mission in data.missions]

    assert len(data.missions) == 1
    assert MISSIONS.tutorial.name in mission_names


def test_get_available_missions_query_after_completing_tutorial(architext: Architext, uow: FakeUnitOfWork) -> None:
    data = architext.query(AvailableMissions(), 'alice')

    mission_names = [mission.name for mission in data.missions]

    assert len(data.missions) == 3
    assert MISSIONS.play_with_friends.name in mission_names
    assert MISSIONS.create_your_world.name in mission_names
    assert MISSIONS.play_monks_riddle.name in mission_names


def assert_available_mission_names(architext: Architext, user_id: str, names: List[str]):
    data = architext.query(AvailableMissions(), user_id)
    mission_names = [mission.name for mission in data.missions]

    for name in names:
        assert name in mission_names

    assert len(data.missions) == len(names)


def test_full_mission_path(architext: Architext, uow: FakeUnitOfWork) -> None:
    assert_available_mission_names(architext, 'oliver', [MISSIONS.tutorial.name])

    architext.handle(CompleteMission(mission_id=MISSIONS.tutorial.id), 'oliver')

    assert_available_mission_names(architext, 'oliver', [
        MISSIONS.play_with_friends.name,
        MISSIONS.create_your_world.name,
        MISSIONS.play_monks_riddle.name,
    ])

    architext.handle(CompleteMission(mission_id=MISSIONS.play_with_friends.id), 'oliver')

    assert_available_mission_names(architext, 'oliver', [
        MISSIONS.create_your_world.name,
        MISSIONS.play_monks_riddle.name,
    ])

    architext.handle(CompleteMission(mission_id=MISSIONS.create_your_world.id), 'oliver')

    assert_available_mission_names(architext, 'oliver', [
        MISSIONS.invite_friends_to_your_world.name,
        MISSIONS.play_monks_riddle.name,
    ])

    architext.handle(CompleteMission(mission_id=MISSIONS.invite_friends_to_your_world.id), 'oliver')

    assert_available_mission_names(architext, 'oliver', [
        MISSIONS.play_monks_riddle.name,
    ])

    architext.handle(CompleteMission(mission_id=MISSIONS.play_monks_riddle.id), 'oliver')

    assert_available_mission_names(architext, 'oliver', [])


