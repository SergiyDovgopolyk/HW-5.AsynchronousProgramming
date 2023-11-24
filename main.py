import platform
import aiohttp
import asyncio
import datetime
import json

async def fetch_currency_data(days):
    async with aiohttp.ClientSession() as session:
        currency_data = []
        for day in range(days):
            date = datetime.date.today() - datetime.timedelta(days=day)
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime("%d.%m.%Y")}'
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    currency_info = {
                        date.strftime("%d.%m.%Y"): {
                            'EUR': {
                                'sale': None,
                                'purchase': None
                            },
                            'USD': {
                                'sale': None,
                                'purchase': None
                            }
                        }
                    }
                    for currency in result['exchangeRate']:
                        if currency['currency'] == 'EUR':
                            currency_info[date.strftime("%d.%m.%Y")]['EUR']['sale'] = currency['saleRate']
                            currency_info[date.strftime("%d.%m.%Y")]['EUR']['purchase'] = currency['purchaseRate']
                        elif currency['currency'] == 'USD':
                            currency_info[date.strftime("%d.%m.%Y")]['USD']['sale'] = currency['saleRate']
                            currency_info[date.strftime("%d.%m.%Y")]['USD']['purchase'] = currency['purchaseRate']
                    currency_data.append(currency_info)
        return currency_data

async def get_user_input():
    loop = asyncio.get_event_loop()
    days = await loop.run_in_executor(None, input, "Введіть кількість днів: ")
    return int(days)

async def main():
    days = 10  # Максимальна кількість днів для отримання даних
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()

    if __name__ == "__main__":
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        days = await get_user_input()
        currency_data = await fetch_currency_data(min(days, 10))
        print(json.dumps(currency_data, indent=2))

asyncio.run(main())
