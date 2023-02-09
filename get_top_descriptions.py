import requests
import json
import re
def pull(cache_file_name):
    baseUrl = "http://docker-selfhosted:8080/api/v1/search/transactions"
    page = 1
    query="destination_account_is%3A\"(no+name)\""
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiOTA0ZGMwZTI5MjM2OTUwNTIwNjBiMjQxZWY5YjM2OTU1NmE3YjMzNDAwNTMyOWRiMDEyYjcxMDJjYmZjZGY1Y2FhMWI0ODFjZmEzNTdiYzciLCJpYXQiOjE2NzI1OTM3MzIuNTA2MjgzLCJuYmYiOjE2NzI1OTM3MzIuNTA2Mjg2LCJleHAiOjE3MDQxMjk3MzIuMzYyNTU0LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.z0nDGtZhhlYdOpyUtklj7nX1xXm1uMybJlp3GSJIu37zhowXmRN2_PlBsPdjfLA2HVDnSHC6vsU4-rmGef6r3WuzrZIM9xGg6C7OfaphrSiuSR7rAW7dlEblzhMnSaYAV-Aczb-pE1LMSrg1EsCz6GxWLwP8akMIcnPSS0jVUzwkx_i6RJ4sUL8GE_wx_xaIuknQ3uIk7WNOto2TL4lkOeDyx9J4eR4nCiJJnYKrBiToC15N_Qhamdzaa9Ox_gGUFNODLmfNJrtTqVCKxRkpzFimvIgTEeUp6NOPUPwnVsQ17A3a3hXMLCGeTnEi3tJbtCeur1_Dobu9oFGXqFYCB0u6yUk1KXvetFwfPStuqUcUPRxoAxN86n3usECObGYNlLFxEbD0YIlnosf9Pi0aAEjQ1D_p9Mmf4IcETUj_jkIC44hBuw2ptkdyTvpTa4JsFFu8X1vKZ-BkFaQmqv8sBH3F0SLw2GsDT1u0MStEB1RMqyWyCxy2IqYxYxFI_VgFLMcaXP1lKGI3xCBk_KIctYurs2TlSerndbFChpidbkQLLMzJgrr_euGD27OgTPWG6RZXglMoz_DnO9oOgRFlE0ITwkolHyAu7fWa1Iw-WsrYA0iLDvog7Jk3muXknPucv2hYVce7n_kKwX98rGiJT65gy_5ZOjkkLILa4_noVWc"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    req  = baseUrl + f"?page={page}&query={query}"
    res = requests.get(req, headers=headers).json()
    transactions = [i['attributes']['transactions'][0] for i in res['data']]

    while ('next' in res['links']):
        page += 1
        req  = baseUrl + f"?page={page}&query={query}"
        res = requests.get(req, headers=headers).json()
        transactions += [i['attributes']['transactions'][0] for i in res['data']]

    with (open(cache_file_name, 'w') as f):
        f.write(json.dumps(transactions))

def stat(cache_file_name):
    with(open(cache_file_name) as f):
        l = json.loads(f.read())
    d = {}
    for t in l:
        desc = t['description']
        desc = re.sub(r'[0-9]+', '', desc)
        if desc not in d:
            d[desc] = 0
        d[desc] += 1


    d = [(k, d[k]) for k in d]
    d = sorted(d, key=lambda t: t[1], reverse=True)
    print('\n'.join([str(i) for i in d[:10]]))

def main():
    cache_file_name = 'cache.json'
    #pull(cache_file_name)
    stat(cache_file_name)

main()