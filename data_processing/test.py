# import requests
# import aiohttp
# from aiohttp import web
# import asyncio
# import time
# from data_fetching.variables import HEADERS, CIAN_API_URL
# import os
# import sys
# from pprint import pprint
# pprint(sys.path)

# urls = ['https://qna.habr.com/q/1063624',
#         'https://github.com/encode/httpx/issues/914',
#         'https://docs.python.org/3/library/asyncio-task.html',
#         'https://github.com/encode/httpx/issues/914']

# payload = {
#             "jsonQuery": {
#                 "region": {"type": "terms", "value": [2]},
#                 "_type": "flatsale",
#                 "room": {"type": "terms", "value": [1, 2, 3, 4, 5, 6]},
#                 "engine_version": {"type": "term", "value": 2},
#                 "page": {"type": "term", "value": 1},
#             }
#         }

# async def fetch_response(url, header, payload):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, data=payload, headers=header) as response:
#             return await response.text()


# start_time = time.time()


# def foo():
#     print(__file__)
# r = asyncio.get_event_loop().run_until_complete(fetch_response(CIAN_API_URL, HEADERS, payload))
# print("--- %s seconds ---" % (time.time() - start_time))
# print(r)

import json
import os

print(os.getcwd())


# with open('test/cian_spb_filtered.json') as file:
#     data = json.load(file)
# print(data[0])

    