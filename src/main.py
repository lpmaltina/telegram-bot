import logging

from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp import web

from create_bot import BASE_URL, HOST, PORT, WEBHOOK_PATH, bot, dp
from handlers import router


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="get_text", description="Получить текст по id")
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup() -> None:
    await set_commands()
    logging.info(f"Webhook set to {BASE_URL}{WEBHOOK_PATH}")
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")


async def on_shutdown() -> None:
    logging.info("Shutting down bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


def main() -> None:
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    main()
