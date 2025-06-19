import json
from typing import TypeVar

import aiofiles
from pydantic import BaseModel


SchemaClassType = TypeVar(
    "SchemaClassType",
    bound=type[BaseModel],
)


async def get_mock_data_from_file(
    fp: str,
    schema: SchemaClassType,
) -> list[SchemaClassType]:
    async with aiofiles.open(fp, "r", encoding="utf-8") as file:
        content = await file.read()
        data = json.loads(content)
    # fmt: off
    return [
        schema(**item)
        for item in data
    ]
    # fmt: on
