import requests
import json
from config import cookies, headers, tablet_cookies, tablet_headers
import os
import math

#  118 - лэптопы
#  195 - планшеты


def get_data(category):
    s = requests.Session()
    if category == '118':
        params = {
            'categoryId': {category},
            'offset':
            '0',
            'limit':
            '24',
            'filterParams': [
                'WyJza2lka2EiLCIiLCJkYSJd',
                'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
            ],
            'doTranslit':
            'true',
        }
        response = s.get('https://www.mvideo.ru/bff/products/listing',
                         params=params,
                         cookies=cookies,
                         headers=headers).json()
    elif category == '195':
        params = {
            'categoryId':
            '195',
            'offset':
            '0',
            'limit':
            '24',
            'filterParams': [
                'WyJza2lka2EiLCIiLCJkYSJd',
                'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
            ],
            'doTranslit':
            'true',
        }
        response = s.get('https://www.mvideo.ru/bff/products/listing',
                         params=params,
                         cookies=tablet_cookies,
                         headers=tablet_headers).json()

    if not os.path.exists('data'):
        os.mkdir('data')

    s = requests.Session()

    response = s.get('https://www.mvideo.ru/bff/products/listing',
                     params=params,
                     cookies=cookies,
                     headers=headers).json()

    total_items = response.get('body').get('total')

    if total_items is None:
        return '[!] No items :-('

    page_count = math.ceil(total_items / 24)

    print(f'[INFO] Total positions: {total_items} | Total pages: {page_count}')

    products_ids = {}
    products_description = {}
    products_prices = {}

    for i in range(page_count):
        offset = f'{i * 24}'

        params = {
            'categoryId': {category},
            'offset':
            offset,
            'limit':
            '24',
            'filterParams': [
                'WyJza2lka2EiLCIiLCJkYSJd',
                'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
            ],
            'doTranslit':
            'true',
        }
        response = s.get('https://www.mvideo.ru/bff/products/listing',
                         params=params,
                         cookies=cookies,
                         headers=headers).json()

        products_ids_list = response.get('body').get('products')
        products_ids[i] = products_ids_list

        json_data = {
            'productIds': products_ids_list,
            'mediaTypes': [
                'images',
            ],
            'category': True,
            'status': True,
            'brand': True,
            'propertyTypes': [
                'KEY',
            ],
            'propertiesConfig': {
                'propertiesPortionSize': 5,
            },
            'multioffer': False,
        }

        response = requests.post(
            'https://www.mvideo.ru/bff/product-details/list',
            cookies=cookies,
            headers=headers,
            json=json_data).json()
        products_description[i] = response

        products_ids_str = ','.join(products_ids_list)
        params = {
            'productIds': products_ids_str,
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',
        }

        response = s.get('https://www.mvideo.ru/bff/products/prices',
                         params=params,
                         cookies=cookies,
                         headers=headers).json()

        material_prices = response.get('body').get('materialPrices')

        for item in material_prices:
            item_id = item.get('price').get('productId')
            item_base_price = item.get('price').get('basePrice')
            item_sale_price = item.get('price').get('salePrice')
            item_bonus = item.get('bonusRubles').get('total')

            products_prices[item_id] = {
                'item_base_price': item_base_price,
                'item_sale_price': item_sale_price,
                'item_bonus': item_bonus
            }

        print(f'[+] Finished {i+1} of the {page_count} pages')

    with open('data/1_product_ids.json', 'w') as file:
        json.dump(products_ids, file, indent=4)

    with open('data/2_product_description.json', 'w') as file:
        json.dump(products_description, file, indent=4)

    with open('data/3_product_prices.json', 'w') as file:
        json.dump(products_prices, file, indent=4)


def get_result():
    with open('data/2_product_description.json') as file:
        products_data = json.load(file)

    with open('data/3_product_prices.json') as file:
        products_prices = json.load(file)

    for item in products_data.values():
        products = item.get('body').get('products')

        for item in products:
            product_id = item.get('productId')

            if product_id in products_prices:
                prices = products_prices[product_id]

            item['item_basePrice'] = prices.get('item_base_price')
            item['item_salePrice'] = prices.get('item_sale_price')
            item['item_bonus'] = prices.get('item_bonus')
            item[
                'item_link'] = f'http://www.mvideo.ru/products/{item.get("nameTranslit")}-{product_id}'

    with open('data/4_result.json', 'w') as file:
        json.dump(products_data, file, indent=4)


def main():
    get_data()
    get_result()


if __name__ == '__main__':
    main()
