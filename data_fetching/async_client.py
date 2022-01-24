import asyncio
import aiohttp
import requests
import json


class AiohttpClient:
    @staticmethod
    async def fetch_response(url: str, header, payload) -> str:
        """
        Fetch conenction for single page.
        :param url: page url
        :type url: str
        :return: webpage text
        :rtype: str
        """
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.post(url, data=payload) as response:
                if response.status == 200:
                    try:
                        res = await response.read()
                        print('Parsed!')
                        data = json.loads(res)
                        return data
                    except Exception as err:
                        print(f'Err: {err}, status: {response.status}')
                        pass
                print('Something went wrong...', response.status)
                return None

    @staticmethod
    async def fetch_all_pages(url: list[str], header, payloads) -> list[str]:
        """
        Fetching all requests.
        :param urls: list of pages urls
        :type urls: list
        :return: list of responce objects
        :rtype: list
        """
        tasks = [
            asyncio.create_task(
                AiohttpClient.fetch_response(url, header, payload)
                ) 
                for payload in payloads
            ]
        await asyncio.gather(*tasks)
        pages = [task.result() for task in tasks]
        return pages


async def fetch_response(url: str) -> str:
    """
    Fetch conenction for single page.
    :param url: page url
    :type url: str
    :return: webpage text
    :rtype: str
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    return await response.text()
                except ValueError:
                    pass
            return None
