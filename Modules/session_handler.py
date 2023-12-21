import aiohttp

class SessionHandler():
    """Parent class to manage API interactions with aiohttp.
       Each object inheriting from SessionHandler will have it's own Individual Session Pool
    """

    def __init__(self):
        self.session = None

    async def initialize_session(self):
        """Initialize the aiohttp Client Session if not already initialized"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def cleanup_session(self):
        """Close the aiohttp Client Session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def _make_post_request(self, endpoint: str, data: dict = None, headers: dict = None) -> aiohttp.ClientResponse:
        """
        Makes an HTTP POST request to the specified endpoint

        Args:
            data (dict): The request parameters
            endpoint (str): The API endpoint
            headers (dict): The request headers

        Returns:
            dict: The response from the API
        """
        if not self.session:
            self.initialize_session()

        try:
            async with self.session.post(url=endpoint, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response
        except aiohttp.ClientError as e:
            print(f"An aiohttp error has occurred: {e}")
            raise

    async def _make_get_request(self, endpoint: str, data: dict = None, headers: dict = None) -> aiohttp.ClientResponse:
        """
        Makes an HTTP GET request to the specified endpoint

        Args:
            data (dict): The request parameters
            endpoint (str): The API endpoint
            headers (dict): The request headers

        Returns:
            dict: The response from the API
        """
        if not self.session:
            self.initialize_session()

        try:
            async with self.session.get(url=endpoint, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response
        except aiohttp.ClientError as e:
            print(f"An aiohttp error has occurred: {e}")
            raise
