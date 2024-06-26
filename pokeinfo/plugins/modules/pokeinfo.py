#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import requests

def get_pokemon_data(pokemon_name):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
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
        result['error'] = f"Pokemon '{pokemon_name}' not found"
        module.fail_json(msg="Failed to fetch Pokemon data", **result)

if __name__ == '__main__':
    main()
