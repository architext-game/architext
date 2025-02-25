from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import DEFAULT

from regex import P
from architext.core.domain.primitives import Visibility


@dataclass
class MissionRequirement:
    complete_mission_with_id: str

@dataclass
class Mission:
    id: str
    name: str
    description: str
    requirements: List[MissionRequirement]

@dataclass
class MissionLog:
    mission_id: str
    user_id: str
    completed_at: date

# using a factory method because sqlalchemy does not like
# instances of entities being created before the mappers are registered
def default_missions():
    class MISSIONS:
        tutorial = Mission(
            id="tutorial",
            name="Play the tutorial",
            description="Learn the basics of Architext",
            requirements=[],
        )

        play_with_friends = Mission(
            id="play_with_friends",
            name="Play with friends",
            description="Architext is more fun with friends, invite them to join!",
            requirements=[MissionRequirement(complete_mission_with_id="tutorial")],
        )

        create_your_world = Mission(
            id="create_your_world",
            name="Create your first world",
            description="There you'll be able to create anything that you can imagine!",
            requirements=[MissionRequirement(complete_mission_with_id="tutorial")],
        )

        play_monks_riddle = Mission(
            id="play_monks_riddle",
            name="Play the Monk's Riddle",
            description="Can you find out what happened in this abandoned monastery?",
            requirements=[MissionRequirement(complete_mission_with_id="tutorial")],
        )

        invite_friends_to_your_world = Mission(
            id="invite_friends_to_your_world",
            name="Invite friends to your world",
            description="Give them the code to your world to show them!",
            requirements=[MissionRequirement(complete_mission_with_id="create_your_world")],
        )

        all = [
            tutorial,
            play_with_friends,
            create_your_world,
            play_monks_riddle,
            invite_friends_to_your_world,
        ]
    return MISSIONS
