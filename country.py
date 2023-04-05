import random, requests

def get_covid_info():

    api_url = "https://api.covid19api.com/summary"
    response = requests.get(api_url)

    covid = dict()
    elem = dict()
    a = []

    get_json = response.json()
    covid = get_json.get('Countries')

    if covid:
        for key in covid:
            a.append(key)

        elem = random.choice(a)

        info = 'Country:' +  str(elem['Country']) + '    ' +  'TotalConfirmed:' + str(elem['TotalConfirmed']) + '    ' +  'NewConfirmed:' +  str(elem['NewConfirmed'])
        return info
    return ''