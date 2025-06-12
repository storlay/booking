from typing import TypeVar

from pydantic import BaseModel

from src.db import Base


SchemaType = TypeVar(
    "SchemaType",
    bound=BaseModel,
)
ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseDataMapper:
    model: type[SchemaType] = None
    schema: type[ModelType] = None

    @classmethod
    def map_to_domain_entity(
        cls,
        model: Base,
    ) -> type[SchemaType]:
        return cls.schema.model_validate(
            model,
            from_attributes=True,
        )

    @classmethod
    def map_to_persistence_entity(
        cls,
        schema: BaseModel,
    ) -> type[ModelType]:
        return cls.model(**schema.model_dump())
