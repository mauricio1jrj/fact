import httpx
from flask import current_app

class APIError(Exception):
        def __init__(self, message, status_code=400, errors=None):
            self.message = message
            self.status_code = status_code
            self.errors = errors
            super().__init__(message)

class APIClient:
    def __init__(self, token: str=None):
        self.base_url = current_app.config['API_BASE_URL']
        self.headers = {'content-type': 'application/json'}
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def _url(self, path: str) -> str:
        full_url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        print(f"APIClient: {full_url}")
        return full_url



    def handle(self, response: httpx.Response):
        if not response.content:
            raise APIError('El servidor retorno una respueta vacia', response.status_code)

        try:
            body = response.json()
        except Exception as e:
            raise APIError(
                f'Respuesta no es un JSON válido (status={response.status_code}):'
                f' {response.text[:200]}',
                response.status_code
            )

        if isinstance(body, list):
            return body

        if not isinstance(body, dict):
            raise APIError(
                f'Formato de respuesta inesperado: {type(body).__name__}', 
                response.status_code
            ) 

        if 'success'in body:
            if not body.get('success'):
                raise APIError(
                    body.get('message', f'Error desconocido'),
                    response.status_code,
                    body.get('errors')
                )
            return body.get('data')

        if response.status_code < 400:
            return body
        raise APIError(
            body.get('message',) or body.get('error') or 'Error desconocido',
            response.status_code

        )


    def get(self, path, params=None):
        print(path)
        r = httpx.get(self._url(path), params=params, headers=self.headers, timeout=10)
        print(r)
        return self.handle(r)


    def post(self, path, json=None):
        r = httpx.post(
            self._url(path),
            json=json,
            headers=self.headers,
            timeout=10
        )

        return self.handle(r)    

    def put(self, path, json=None):
        r = httpx.put(
            self._url(path),
            json=json,
            headers=self.headers,
            timeout=10
        )
        return self.handle(r)


    def delete(self, path):
        r = httpx.delete(
            self._url(path),
            headers=self.headers,
            timeout=10
        )
        return self.handle(r)    