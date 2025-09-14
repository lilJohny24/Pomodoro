from dataclasses import dataclass
import json
import uuid
import aio_pika

from app.settings import Settings

@dataclass
class MailClient:
    settings = Settings()

    async def send_welcome_email(self, to: str) -> None:
        # Устанавливаем соединение
        connection = await aio_pika.connect_robust(self.settings.AMQP_URL)
        
        # Создаем канал и работаем внутри его контекста
        async with connection:
            channel = await connection.channel()
            # Объявляем очередь. Это ОЧЕНЬ важный шаг.
            await channel.declare_queue("email_queue", durable=True)
            
            # Формируем тело сообщения
            email_body = {
                'message': 'Welcome to pomodoro',
                'user_email': to,
                'subject': 'Welcome message'
            }
            # Создаем объект сообщения
            message = aio_pika.Message(
                body=json.dumps(email_body).encode(),
                correlation_id=str(uuid.uuid4()),
                reply_to='callback_mail_queue'
            )
            
            # Публикуем сообщение
            await channel.default_exchange.publish(
                message=message,
                routing_key='mail_queue' # routing_key должен совпадать с именем очереди
            )
        return