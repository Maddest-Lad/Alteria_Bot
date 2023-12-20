import aiohttp

class AioHttpSessionHandler():
    """Parent class to manage API interactions with aiohttp."""

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def _make_post_request(self, data: dict, endpoint: str, headers: dict = None) -> dict:
        """
        Makes an HTTP POST request to the specified endpoint

        Args:
            data (dict): The request parameters
            endpoint (str): The API endpoint
            headers (dict): The request headers

        Returns:
            dict: The response from the API
        """
        try:
            async with self.session.post(url=endpoint, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"An aiohttp error has occurred: {e}")
            raise

    async def _make_get_request(self, data: dict, endpoint: str, headers:dict = None) -> dict:
        """
        Makes an HTTP GET request to the specified endpoint

        Args:
            data (dict): The request parameters
            endpoint (str): The API endpoint
            headers (dict): The request headers

        Returns:
            dict: The response from the API
        """
        try:
            async with self.session.get(url=endpoint, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"An aiohttp error has occurred: {e}")
            raise
