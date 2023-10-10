import requests

class Common:
    @staticmethod
    def http_get_as_json(url, params):
        try:
            resp = requests.get(
                endpoint=url,
                params=params
            )
            data = resp.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status != 200:
            return data
        else:
            return {}