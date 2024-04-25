#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import requests

def get_pokemon_data(pokemon_name):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            "name": data["name"],
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        }
        if fields:
            filtered_data = {field: pokemon_info.get(field) for field in fields}
            return filtered_data
        else:
            return pokemon_info
    else:
        return None

def main():
    module_args = dict(
        name=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        pokemon_data=None,
        error=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    pokemon_name = module.params['name']
    pokemon_data = get_pokemon_data(pokemon_name)

    if pokemon_data:
        result['pokemon_data'] = pokemon_data
        module.exit_json(**result)
    else:
        result['error'] = f"Pokemon with name: '{pokemon_name}' dont found."
        module.fail_json(msg="Failed to fetch Pokemon data", **result)

if __name__ == '__main__':
    main()
