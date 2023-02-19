import requests, json, re
input_file = 'input.json'
output_file = 'output.txt'
store = 'expenseAccounts'
url = 'http://localhost:9091/api/v1/lookup/action/expenseAccounts/add-key'
cache_file = 'cache2.json'

def add_key(key, value):
    response = requests.post(url, json={
        "key": key,
        "value": value
    })

    return response

def clear_log():
    with open(output_file, 'w') as f:
        pass

def log_error(msg):
    with open(output_file, 'a') as f:
        f.write(msg + "\n")

def save_cache(ts):
    cache = load_cache()

    for kvp in ts:
        cache[kvp[0]] = kvp[1]
    with open(cache_file, 'w') as f:
        f.write(json.dumps(cache, indent=4))

def load_cache():
    cache = {}
    with open(cache_file) as f:
        cache = json.loads(f.read())
    return cache

#print(add_key("FOO", "Foo").json())

# load nodes
def load_nodes():
    clear_log()
    inp = {}
    with open(input_file) as f:
        j =  json.loads(f.read())
        for o in j:
            inp[o['id']] = o

    switch_nodes = [inp[i] for i in inp if inp[i]['type'] == 'switch']
    kvps = []

    for sn in switch_nodes:
        for (i, wire) in enumerate(sn['wires']):
            if (len(wire) != 1):
                log_error(f"Unexpected number of wires in node {sn['name']}")

            rule = sn['rules'][i]
            if rule['t'] == 'regex':
                log_error(f"Unable to run on regex. Node: {sn['name']}, rule: {rule['v']}")
                continue
            elif rule['t'] == 'else':
                continue
            elif rule['t'] != 'eq':
                log_error(f"Unrecognized rule type in switch node: {rule['t']}. Node: {sn['name']}")

            nxt = inp[wire[0]]
            if nxt['type'] == 'function':
                m = re.match(r'^msg\.regex\.output = (".*");\nreturn msg;$', nxt['func'])
                if m:
                    kvps.append((rule['v'], json.loads(m.group(1))))
                else:
                    log_error(f"Unrecognized format in function node. Node: {nxt['name']}")

    save_cache(kvps)

def build_kvp():
    cache = load_cache()
    for k in cache:
        response = add_key(k, cache[k])
        if (response.status_code != 200):
            print(f"Error adding kvp {k}={cache[k]}: {response.json()}")
        else:
            print(f"Added kvp {k}={cache[k]}")

build_kvp()



