# -*- coding: utf-8 -*-
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

#设备的Characteristic UUID
par_notification_characteristic="47442020-0f63-5b27-9122-728099603712"
#设备的MAC地址
# par_device_addr="D7EDCD0F-F756-43C9-4EC6-4ED3697A3ECA"

#监听回调函数，此处为打印消息
def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print("rev data:", data)

async def main():
    print("starting scan...")

    #基于name查找设备
    device = await BleakScanner.find_device_by_name(
        'e-AR2016', cb=dict(use_bdaddr=False)  #use_bdaddr判断是否是MOC系统
    )
    if device is None:
        print("could not find device with address '%s'")
        return

    print("connecting to device...")
    async with BleakClient(device) as client:
        print("Connected")
        await client.start_notify(par_notification_characteristic, notification_handler)
        await asyncio.sleep(10.0)   #程序监听的时间，此处为10秒
        await client.stop_notify(par_notification_characteristic)

asyncio.run(main())
