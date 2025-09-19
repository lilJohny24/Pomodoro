from dataclasses import dataclass
import json
import uuid
import aio_pika

from app.broker.consumer import BrokerConsumer
from app.broker.producer import BrokerProducer
from app.settings import Settings

@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer
    broker_consumer: BrokerConsumer

    async def send_welcome_email(self, to: str) -> None:
            # Формируем тело сообщения
            email_body = {
                'message': 'Welcome to pomodoro',
                'user_email': to,
                'subject': 'Welcome message',
                'correlation_id': str(uuid.uuid4())
            }
            
            
            await self.broker_producer.send_welcome_email(email_data=email_body)
            return