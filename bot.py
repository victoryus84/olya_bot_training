import asyncio, django, logging, os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from tgbot.config import load_config
from tgbot.handlers import OT_user_begin, OT_user_feedback

logger = logging.getLogger(__name__)

def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "dj_ac.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    setup_django()
    config = load_config(".env")
    
    # redisdata = config.redis
    # storage = RedisStorage(config.redis.host, config.redis.port, db=5, pool_size=10, prefix='bot_fsm') \
    # if redisdata.use_redis: 
    #     storage = RedisStorage(Redis(host=redisdata.host, port=redisdata.port, db=5, password=redisdata.password)) 
    # else:
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # dp.message.middleware(CheckSubscription())
    # dp.message.middleware(AntiFloodMiddleware(5))
    
    # bot['config'] = config
    dp.include_routers(
        OT_user_begin.router,
        OT_user_feedback.router,
    )

    # start
    try:
        await dp.start_polling(bot)
        await bot.delete_webhook(drop_pending_updates=True)
    finally:
        bot.session.close()
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
