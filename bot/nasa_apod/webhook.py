import asyncio
import datetime
import json
import logging
import requests
from aiohttp import ClientSession
from discord import AsyncWebhookAdapter, Embed, Webhook

webhook_info = {'name': '', 'api_key': '', 'api_url': '', 'webhook_url': '', 'test_url': ''}
logging.basicConfig(level=logging.INFO)


async def hook_apod(date='', debug=False, test=False):
    async with ClientSession() as session:
        webhook = Webhook.from_url(url=webhook_info['test_url' if test else 'webhook_url'],
                                   adapter=AsyncWebhookAdapter(session))
        await webhook.send(username=webhook_info['name'],
                           embed=get_embed(datetime.datetime.today() if date == '' else date, debug, test))


def get_apod(date):
    res = requests.get(webhook_info['api_url'] % (webhook_info['api_key'], date)).json()
    logging.info(res)
    return res


def get_embed(date, debug, test):
    apod = get_apod(date)
    apod_embed = Embed.from_dict({
        'title': apod['title'],
        'description': '[Click for HD](%s)' % apod['hdurl']
    }) \
        .set_image(url=apod['url']) \
        .add_field(name='Date', value=apod['date'], inline=False) \
        .add_field(name='Explanation', value=apod['explanation'], inline=False) \
        .set_footer(text='copyright %s' % apod['copyright'])

    if debug or test:
        apod_embed.add_field(name='Response', value='```json\n%s\n```' % json.dumps({
            'date': apod['date'],
            'title': apod['title'],
            'media_type': apod['media_type'],
            'url': apod['url'],
            'service_version': apod['service_version'],
        }))

    return apod_embed


def get_info():
    with open('../../resources/nasa_apod/info.json') as info:
        for [key, info_value] in zip(webhook_info.keys(), json.load(info).values()):
            webhook_info[key] = info_value
        print(webhook_info)


async def main():
    get_info()
    await hook_apod(input('Enter a date: '), test=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        exit(0)
    finally:
        loop.close()
