from dataclasses import dataclass
from typing import Union

@dataclass
class AMFResult:
    Content: Union[dict, str] = None
    StatusCode: int = -999
    Code: int = -1

@dataclass
class LoginResult:
    ActorId: int
    Ticket: str
    ProfileId: str
    AccessToken: str

@dataclass
class GetProfileSnapshot:
    id: str
    full: str
    face: str

@dataclass
class GetProfilesResult:
    name: str
    id: int
    culture: str
    avatar: GetProfileSnapshot


@dataclass
class SearchProfileResult:
    id: str

@dataclass
class Experience2:
    xp: int
    level: int
    currentLevelXpMin: int
    currentLevelXpMax: int


@dataclass
class AttributesAdditionalData:
    ProfilePopupCustomization: str
    Mood: str
    WelcomeVersion: str
    ChatRoomPositionData: str
    Gender: str
    DefaultMyHome: str
    WAYD: str


@dataclass
class Attributes:
    profileId: str
    gameId: str
    avatarId: str
    additionalData: AttributesAdditionalData
