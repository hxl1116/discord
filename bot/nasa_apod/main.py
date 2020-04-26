# Relative imports
import datetime
import json
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from services.apod_bot import APODThread
from services.apod_webhook import WebhookThread

threads = {}


@APODThread.client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client_thread.client))


@APODThread.client.event
async def on_message(message):
    if message.author == client_thread.client.user:
        return

    debug = False
    usage = False

    if message.content.startswith('/nasa'):
        params = message.content.split(' ')[1:]

        if len(params) == 0:
            apod, status = client_thread.get_apod(datetime.date.today())
        elif len(params) == 1:
            if params[0] in client_thread.flag_dict:
                (apod, status), debug = client_thread.get_apod(datetime.date.today()), True
            else:
                apod, status = client_thread.get_apod(params[0])
        elif len(params) == 2:
            if params[1] in client_thread.flag_dict:
                (apod, status), debug = client_thread.get_apod(params[0]), True
            else:
                apod, status, usage = None, False, True
        else:
            apod, status, usage = None, False, True

        if debug:
            apod_msg = client_thread.debug_format % json.dumps(apod)
        else:
            if status:
                apod_msg = client_thread.success_format % (apod['date'], apod['title'], apod['url'])
            elif usage:
                apod_msg = client_thread.usage_format
            else:
                apod_msg = client_thread.error_format % (client_thread.get_err_msg(), apod['msg'])

        await message.channel.send(apod_msg)


def main():
    with ThreadPoolExecutor() as executor:
        fn = partial(client_thread.run, webhook_thread.run)
        executor.map(fn, threads.values())
    # client_thread.run()
    # webhook_thread.run()


if __name__ == '__main__':
    client_thread = APODThread('Client Thread')
    webhook_thread = WebhookThread('Webhook Thread')
    threads['client'], threads['webhook'] = client_thread, webhook_thread

    main()

    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(main())
    # except KeyboardInterrupt:
    #     loop.close()
    # finally:
    #     loop.close()
