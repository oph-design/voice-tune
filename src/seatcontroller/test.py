import asyncio
import sys
import os
import pandas as pd

from kuksa_client.grpc import Datapoint
from kuksa_client.grpc.aio import VSSClient

client = VSSClient("127.0.0.1", 55555)


async def changeValue(target, delta):
    # if not 0 <= delta <= 65535:
    #     print("Delta must be within uint16 range (0-65535).")
    #      return
    current_obj = (await client.get_current_values([target]))[target]
    current_value = 0
    if current_obj is not None:
        current_value = current_obj.value
    new_value = current_value + delta
    print(new_value)
    await client.set_current_values(
        {
            target: Datapoint(new_value),
        }
    )


async def main():
    await client.connect()
    home = os.environ["PWD"]
    data = pd.read_csv(home + "/ressources/datapoints.csv")
    print(data.head())
    target = data.loc[data["key"] == sys.argv[1], "value"].values[0]
    print(target)
    await changeValue(target, float(sys.argv[2]))


asyncio.run(main())
