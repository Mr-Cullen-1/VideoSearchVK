import requests

def search_vk_videos(access_token, query, count=10, filters='clips', date_filter='last_week', likes=100, views=1000, reposts=50, comments=10, sort='views'):
    # Формирование URL и параметров запроса
    url = 'https://api.vk.com/method/video.search'
    params = {
        'q': query,  # Поисковая фраза (например, хештег)
        'count': count,  # Количество видео для возврата
        'filters': filters,  # Тип контента, например, клипы
        'date': date_filter,  # Фильтр по дате
        'likes': likes,  # Минимальное количество лайков
        'views': views,  # Минимальное количество просмотров
        'reposts': reposts,  # Минимальное количество репостов
        'comments': comments,  # Минимальное количество комментариев
        'sort': sort,  # Сортировка (по просмотрам или дате)
        'access_token': access_token,  # Токен доступа
        'v': '5.199'  # Версия API
    }

    # Отправка запроса
    response = requests.get(url, params=params)

    # Обработка ответа
    data = response.json()
    if 'response' in data:
        return data['response']['items']  # Возвращаем список найденных видео
    else:
        return f"Ошибка запроса: {data.get('error', 'Неизвестная ошибка')}"  # Выводим ошибку

if __name__ == '__main__':
    # Запрашиваем токен доступа
    access_token = input("Enter VK access token: ")

    # Задаем параметры поиска
    query = '#funnycats'  # Пример поискового запроса
    videos = search_vk_videos(access_token, query)

    # Выводим результаты
    if isinstance(videos, list) and videos:
        for video in videos:
            print(f"Название: {video['title']}")
            print(f"Ссылка: https://vk.com/video{video['owner_id']}_{video['id']}")
            print(f"Просмотры: {video['views']}, Лайки: {video['likes']}")
            print('-' * 30)
    else:
        print(videos)  # В случае ошибки выводим сообщение