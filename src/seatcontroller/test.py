import asyncio
import sys

from kuksa_client.grpc import Datapoint
from kuksa_client.grpc.aio import VSSClient

client = VSSClient("127.0.0.1", 55555)


async def changeTilt(delta: float):
    current_values = await client.get_current_values(
        ["Vehicle.Cabin.Seat.Row1.DriverSide.Tilt"]
    )
    if current_values is None:
        return
    new_value = current_values["Vehicle.Cabin.Seat.Row1.DriverSide.Tilt"].value + delta
    print(new_value)
    await client.set_current_values(
        {
            "Vehicle.Cabin.Seat.Row1.DriverSide.Tilt": Datapoint(new_value),
        }
    )


async def main():
    await client.connect()
    target = sys.argv[1]
    print(target)
    if target == "tilt":
        await changeTilt(float(sys.argv[2]))


asyncio.run(main())
