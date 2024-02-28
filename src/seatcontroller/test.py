import asyncio
import sys
import os
import pandas as pd

from kuksa_client.grpc import Datapoint
from kuksa_client.grpc.aio import Metadata, VSSClient

client = VSSClient("127.0.0.1", 55555)


async def changeValue(delta, data):
    if data[3] == "mm":
        delta = delta / 10
    current_obj = (await client.get_current_values([data[0]]))[data[0]]
    current_value = 0
    if current_obj is not None:
        current_value = current_obj.value
    print(current_value)
    new_value = current_value + delta
    print(new_value)
    if float(data[1]) > new_value or float(data[2]) < new_value:
        print("out of bounds")
        return
    await client.set_target_values(
        {
            data[0]: Datapoint(new_value),
        }
    )


async def main():
    await client.connect()
    home = os.environ["PWD"]
    data = pd.read_csv(home + "/ressources/datapoints.csv")
    data = data.set_index("key").T.to_dict("list")
    await changeValue(float(sys.argv[2]), data[sys.argv[1]])
    await client.disconnect()


asyncio.run(main())
