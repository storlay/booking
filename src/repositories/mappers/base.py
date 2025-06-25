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
    model: type[ModelType] = None
    schema: type[SchemaType] = None
    schema_with_rels: type[SchemaType] | None = None

    @classmethod
    def map_to_domain_entity(
        cls,
        model: Base,
        with_rels: bool = False,
    ) -> type[SchemaType]:
        schema = (
            cls.schema_with_rels if with_rels and cls.schema_with_rels else cls.schema
        )
        return schema.model_validate(
            model,
            from_attributes=True,
        )

    @classmethod
    def map_to_persistence_entity(
        cls,
        schema: BaseModel,
    ) -> type[ModelType]:
        return cls.model(**schema.model_dump())
