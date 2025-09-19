from dataclasses import dataclass
import json
from aiokafka import AIOKafkaConsumer  # ← Исправить импорт

@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer  # ← Исправить тип
    email_callback_topic: str

    async def open_connection(self) -> None:
        await self.consumer.start()

    async def close_connection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:
        await self.open_connection()

        try:
            async for message in self.consumer:
                print(message.value)
        finally:
            await self.close_connection()