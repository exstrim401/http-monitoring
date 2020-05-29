from email.message import EmailMessage
import asyncio
import aiosmtplib
import aiohttp

MAIL_HOST = ""
MAIL_PORT = 25
MAIL_HAS_TLS = False
MAIL_TO = ""
MAIL_FROM = ""
MAIL_USER = None
MAIL_PASSWORD = None
URLS = ["https://google.com"]


async def main():
    session = aiohttp.ClientSession()
    while True:
        for url in URLS:
            async with session.get(url) as resp:
                print(f"{url} - {resp.status}")
                if resp.status != 200:
                    await report_url(url, resp.status)
        await asyncio.sleep(60*10)


async def report_url(url, resp):
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = MAIL_TO
    message["Subject"] = "Ошибка сервера"
    message.set_content(f"Сервер по адресу {url} выдал {resp}")
    await aiosmtplib.send(message, hostname=MAIL_HOST, port=MAIL_PORT,
                          username=MAIL_USER, password=MAIL_PASSWORD,
                          use_tls=MAIL_HAS_TLS)


asyncio.run(main())
