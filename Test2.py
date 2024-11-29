import aiohttp
import asyncio
from typing import List, Dict

class VKVideoSearch:
    def __init__(self, access_token: str, version: str = '5.131'):
        self.base_url = 'https://api.vk.com/method/'
        self.token = access_token
        self.version = version

    async def search_clips(self, query: str, count: int = 10, sort: str = 'views', filters: Dict = None) -> List[Dict]:
        if filters is None:
            filters = {}

        params = {
            'access_token': self.token,
            'v': self.version,
            'q': query,
            'count': count,
            'sort': sort,
            'extended': 1,
            'filters': 'clips',  # Поиск только видеоклипов
            **filters
        }

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.get(self.base_url + 'video.search', params=params) as response:
                    response_data = await response.json()
                    if 'error' in response_data:
                        print(f"Error in API response: {response_data['error']}")
                        return []
                    return response_data.get('response', {}).get('items', [])
            except Exception as e:
                print(f"Error during API request: {e}")
                return []

async def main():
    # Пример: получаем видеоклипы с хештегом '#funnycats'
    token = input("Enter VK access token: ")
    vk_searcher = VKVideoSearch(access_token=token)
    
    query = '#funnycats'  # Пример поиска по хештегу
    count = 10  # Количество результатов
    filters = {
        'date': 'last_week',  # Пример фильтрации по дате (за последнюю неделю)
        'likes': '100',  # Пример фильтрации по количеству лайков (минимум 100 лайков)
        'views': '1000',  # Пример фильтрации по количеству просмотров (минимум 1000 просмотров)
        'reposts': '50',  # Пример фильтрации по количеству репостов (минимум 50 репостов)
        'comments': '10',  # Пример фильтрации по количеству комментариев (минимум 10 комментариев)
    }

    results = await vk_searcher.search_clips(query=query, count=count, filters=filters)
    
    if results:
        print(f"Found {len(results)} videos:")
        for video in results:
            print(f"Title: {video.get('title')}")
            print(f"Link: https://vk.com/video{video.get('owner_id')}_{video.get('id')}")
            print(f"Likes: {video.get('likes', {}).get('count')}")
            print(f"Views: {video.get('views')}")
            print(f"Reposts: {video.get('reposts', {}).get('count')}")
            print(f"Comments: {video.get('comments', {}).get('count')}")
            print('-' * 60)
    else:
        print("No videos found or an error occurred.")


if __name__ == "__main__":
    asyncio.run(main())
