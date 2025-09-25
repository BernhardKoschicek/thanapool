import requests


def get_thanados_data(entity_id: int):

    response = requests.get(
            f"https://thanados.openatlas.eu/api/entity_presentation_view/{entity_id}",
            params={
                'place_hierarchy': 'true',
                'remove_empty_values': 'true',
                'centroid': 'true'},
            proxies='',
            timeout=30)
    response.raise_for_status()
    return response.json()
