import asyncio

from tapo import ApiClient


class TapoClient:

    def __init__(self, username: str, password: str):
        self._client = ApiClient(username, password)

    async def read_p110_info(self, ip_address: str) -> None:
        device = await self._client.p110(ip_address)

        while True:
            print(await device.get_device_info_json())
            await asyncio.sleep(1)

    async def read_p110_power(self, ip_address: str) -> None:
        device = await self._client.p110(ip_address)

        while True:
            result = await device.get_current_power()
            print(result.to_dict())
            await asyncio.sleep(1)

    async def switch(self, ip_address: str, state: bool) -> None:
        """Turn the device on or off

        Args:
            ip_address (str): address of the device
            state (bool): true for on, false for off
        """
        device = await self._client.p110(ip_address)

        if state:
            await device.on()
        else:
            await device.off()
