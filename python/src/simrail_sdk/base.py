import logging
from typing import Set, List, Iterable, Dict, Any, Optional

import pydantic


logger = logging.getLogger(__name__)


class Bookmark:
    pass


class BasePydanticModel(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

    def __hash__(self) -> int:
        pk = ":".join([str(getattr(self, field)) for field in self.Config.pk_fields])
        return hash(pk)
