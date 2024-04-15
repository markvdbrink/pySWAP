from .utils.basemodel import PySWAPBaseModel
from typing import Optional


class Metadata(PySWAPBaseModel):
    """Metadata of a SWAP model."""

    author: str
    institution: str
    email: str
    project: str
    swap_ver: str
    comment: Optional[str] = None

    @property
    def include(self) -> set:
        return {'project'}
