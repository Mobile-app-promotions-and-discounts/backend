# Перенести в проект
CITY_APPLICATIONS = ['Москва',]
MAIN_CATEGORY = ['Продукты',]

# URL
URL_GET_STORES = 'https://lenta.com/api/v1/stores/'
URL_GET_PRODACT = 'https://lenta.com/api/v1/stores/{}/skus/'


# КОНСТАНТЫ ДЛЯ ПАРСИНГА
NAME_STORE = 'Лента'
LENTA_VALUE = True
PRODUCTS_ON_PAGE = 24
PATH_FILE = 'scr/data/{}.json'
FILE_NAME = {
    'ALL_STORES': 'all_stores',
    'STORES_IN_SITY': 'stores_in_{}',
    'PRODUCTS_IN_CATEGORY': 'products_in_{}',
}

# Cловарь связи категории приложения и ключа категории на сайте
CATEGORY_LENTA = {
    # 'Алкогольные напитки': None,
    # 'Продукция собственного производства': None,
    'Фрукты и овощи': 'g6b6be260dbddd6da54dcc3ca020bf380',
    # 'Мясо, птица, колбаса': 'gd6dd9b5e854cf23f28aa622863dd6913',
    # 'Молоко, сыр, яйцо': 'g604e486481b04594c32002c67a2b459a',
    # 'Хлеб и хлебобулочные изделия': None,
    # 'Бакалея': 'g7cc5c7251a3e5503dc4122139d606465',
    # 'Рыба и морепродукты': 'g523853c00788bbb520b022c130d1ae92',
    # # 'Замороженная продукция': None,
    # 'Кондитерские изделия': 'g301007c55a37d7ff8539f1f169a4b8ae',
    # 'Чай, кофе, какао': 'g68552e15008531b8ae99799a1d9391df',
    # 'Безалкогольные напитки': 'g9290c81c23578165223ca2befe178b47',
    # 'Всё для дома': 'g6f4a2d852409e5804606d640dc97a2b1',
    # 'Посуда': None,
    # 'Товары для детей': None,
    # 'Лента Зоомаркет - профессиональный уход': None,
    # 'Товары для животных': None,
    # 'Здоровое питание': None,
    # 'Красота и здоровье': None,
    # 'Бытовая химия': None,
    # 'Бытовая техника и электроника': None,
    # 'Текстиль для дома': None,
    # 'Одежда и обувь': None,
    # 'Спорт и активный отдых': None,
    # 'Дача, сад': None,
    # 'Автотовары': None,
    # 'Цветы': None,
    # 'Канцелярия и печатная продукция': None,
}

CATEGORY = {
        'PRODUCTS': [CATEGORY_LENTA.get['Фрукты и овощи']],
        'Одежда и обувь': [],
        'Для дома и сада': [],
        'Косметика и гигиена': [],
        'Для детей': [],
        'Зоотовары': [],
        'Авто': [],
        'К празднику': [],
}

# requests headers
HEADERS = {
        'Accept': 'application/json',
        'Accept-Language': 'en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,uk;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://lenta.com',
        'Referer': 'https://lenta.com/promo/frukty-i-ovoshchi/frukty/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

# requests cookies
cookies = {
    'KFP_DID': 'cda1cfa9-63f0-931d-71f0-99caa85965f4',
    'oxxfgh': 'caa429fd-33a7-4dcf-b241-26cdf35bbf1f#0#5184000000#5000#1800000#44965',
    '_gid': 'GA1.2.433868370.1703450819',
    'splses.d58d': '*',
    '.ASPXANONYMOUS': 'IwzFt9mMQQX1bDam_1RPrXO37fW7XQ9pDywfvnRZPq6cDKKwRhxtE3pEWr_T9HVeqEys58bmbHNNSyROjzc8xlT88uXMeCeOaDYRWYfHrJIHPtYJjaleA68DzgecmXx2BExA2g2',
    'ASP.NET_SessionId': 'yyg0ywhb0emhs5uh1dp52qih',
    'cookiesession1': '678B286D68C34367DB0D4BEA1FC1E493',
    'qrator_ssid': '1703450819.710.maJA9ERPvYdlwII8-cpcg93tn2dmgpa4hbah7hr4u70o1cq85',
    'CustomerId': '46b8831c53db40969723899342bc8918',
    'CityCookie': 'msk',
    'LastUpdate': '2023-12-24',
    'StoreSubDomainCookie': '0601',
    'CitySubDomainCookie': 'msk',
    'Store': '0601',
    'IsNextSiteAvailable': 'False',
    'DeliveryOptions': 'Pickup',
    'ShouldSetDeliveryOptions': 'False',
    'qrator_jsid': '1703450824.923.pUTa0VmG58glIgTD-kbplu51t6sn0abd578kl9p5avs6g5csd',
    'ValidationToken': 'c40de6d01de8280c1d81ab1b6d3040c2',
    'GACustomerId': 'c086794b4be74c8d927ec39296ae0066',
    'DontShowCookieNotification': 'true',
    '_gcl_au': '1.1.1877955746.1703450827',
    '_ym_uid': '1703450827978779799',
    '_ym_d': '1703450827',
    '_ym_visorc': 'b',
    'tmr_lvid': '1d031272b36e00f721bfb1d1dbe628e6',
    'tmr_lvidTS': '1703450828746',
    '_ymab_param': '4V1J5CVKR6D5NUY5xAHB0TPhc3EhqkI_HVR9ftmjSZwfrDhHpAUuOIRMQCNVP93JEY1mDTEQlgMAPSvt9RrlrNventU',
    '_tm_lt_sid': '1703450830148.404920',
    '_a_d3t6sf': 'duMSjuF5KgnOuW98pJGflGSa',
    '_ym_isad': '2',
    'UnAuthorizedNavigationsCount': '4',
    '_utm_referrer': 'undefined',
    '_userID': 'undefined',
    '_selectedStoreID': '0601',
    'AuthorizationMotivationHidden': 'true',
    '_ga_VN3RKMJFLJ': 'GS1.1.1703453635.1.0.1703453635.0.0.0',
    '_ga_MDSCN4577L': 'GS1.1.1703453635.1.0.1703453636.0.0.0',
    '_ga_NHNYQN6D48': 'GS1.1.1703453635.1.0.1703453636.0.0.0',
    '_gat_UA-327775-1': '1',
    '_dc_gtm_UA-327775-44': '1',
    '_ga': 'GA1.2.2140699981.1703103881',
    'tmr_detect': '0%7C1703454278504',
    '_ga_R6J1ZT7WKM': 'GS1.2.1703450819.9.1.1703454304.0.0.0',
    'splid.d58d': '53e8ede6-f3fe-4ca3-9688-2d4b848d0889.1703450819.9.1703454305..26270234-2cf9-4dfc-bbd4-c97759feb5a9..f188ad02-d288-4e3b-990d-a7b9c1a4f30a.1703450819364.159',
    '_ga_QB4J0GGLM': 'GS1.1.1703450819.9.1.1703454304.0.0.0',
    '_ga_QB4J0GGLMG': 'GS1.1.1703450819.9.1.1703454304.0.0.0',
    '_ga_7T2BMDLJY8': 'GS1.1.1703450819.9.1.1703454304.0.0.0',
    '_ga_Z9D3HDRHYG': 'GS1.1.1703450819.9.1.1703454304.0.0.0',
}
