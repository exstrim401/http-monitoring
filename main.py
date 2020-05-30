import json
from email.message import EmailMessage
import asyncio
import aiosmtplib
import aiohttp

config = None


async def main():
    global config
    session = aiohttp.ClientSession()
    while True:
        with open("config.json") as f:
            config = json.loads(f.read())
        for url in config["urls"]:
            try:
                async with session.get(url) as resp:
                    print(f"{url} - {resp.status}")
                    if resp.status != 200:
                        await report_url(url, resp.status)
            except Exception as e:
                print(f"{url} - {str(e)}")
                await report_url(url, str(e))
        await asyncio.sleep(60*10)


async def report_url(url, resp):
    message = EmailMessage()
    message["From"] = config["mail_user"]
    message["Subject"] = config["mail_subject"]
    message.set_content(config["mail_content"].format(url, resp))
    for email in config["mail_to"]:
        message["To"] = email
        await aiosmtplib.send(message, hostname=config["mail_host"],
                              port=config["mail_port"],
                              use_tls=config["mail_tls"])


asyncio.run(main())
