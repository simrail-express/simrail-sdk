import logging

import pydantic

logger = logging.getLogger(__name__)


class Bookmark:
    pass


class BasePydanticModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    def __hash__(self) -> int:
        pk = ":".join([str(getattr(self, field)) for field in self.Config.pk_fields])
        return hash(pk)
