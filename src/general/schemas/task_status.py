import json
from datetime import datetime
from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
    uuid4,
)

from poetry.console.commands import self
from pydantic import (
    BaseModel,
    Field,
)

from src.base_settings import base_settings
from src.common.databases.redis import get_redis_client
from src.common.enums import TaskStatus


redis = get_redis_client()


class TaskStatusModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    status: TaskStatus = TaskStatus.IN_PROGRESS
    created_at: str = datetime.utcnow().strftime(base_settings.date_time_format)
    done_at: Optional[str] = None
    details: Optional[Any] = None

    @staticmethod
    def get_redis_key(uuid: str) -> str:
        return f'background_task__{uuid}'

    async def save_to_redis(self) -> 'TaskStatusModel':
        redis_key = self.get_redis_key(uuid=str(self.uuid))

        await redis.set(
            name=redis_key,
            value=self.model_dump_json(),
        )

        return self

    @classmethod
    async def get_from_redis(cls, uuid: UUID) -> Optional['TaskStatusModel']:
        redis_key = cls.get_redis_key(str(uuid))
        redis_response = await redis.get(redis_key)
        json_response = json.loads(redis_response)
        response = TaskStatusModel(**json_response)
        return response

        # if (redis_response := await redis.get(name=cls.get_redis_key(uuid=str(uuid)))) is not None:
        #     return TaskStatusModel(**json.loads(redis_response))
