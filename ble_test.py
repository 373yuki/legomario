import asyncio
import platform
from bleak import discover
from bleak import BleakClient


address = "1137934F-A232-4C00-8478-5BEB12070423"
MARIO_CHARACTERISTIC_UUID = '00001624-1212-efde-1623-785feabcd123'
port_val = b'\x06\x00\x21\x01\x00\x01'  # color
port_val = b'\x06\x00\x21\x00\x00\x01'  # gyro
# port_val = b'\x06\x00\x21\x01\x00\x00'

# x06 \ x00 \ x21
# byte \    \ Port Value
# x01 \ x00 \ x01
# PortID(#1) \ Mode \ Mode Information Type


def gyro(data):
    print(*data)


def color_code(data):
    if data[2] != 255:
        if data[2] == 21:
            print("Red")
        if data[2] == 23:
            print("Blue")
        if data[2] == 24:
            print("Yellow")
        if data[2] == 26:
            print("Black")
        if data[2] == 37:
            print("Green")
        if data[2] == 106:
            print("Brown")
        if data[2] == 19:
            print("White")
    else:
        if data[0] == 2:
            print("### Kuribo")
        if data[0] == 3:
            print("### Heiho")
        if data[0] == 14:
            print("### Kaiten")
        if data[0] == 46:
            print("### Kumo")
        if data[0] == 41:
            print("### Hatena")
        if data[0] == 54:
            print("### NokoNoko")
        if data[0] == 99:
            print("### Kinoko")
        if data[0] == 153:
            print("### Kuppa JR")
        if data[0] == 183:
            print("### GOAL")
        if data[0] == 184:
            print("### START")


def notification_handler(sender, data):
    if data[0] != 0x0f:
        # print("MARIO {0}: {1}".format(sender, data))
        gyro(data[4:7])
        # color_code(data[4:7])
        # for i in range(len(data)):
        #     a = hex(data[i])
        #     b = bin(data[i])[2:].zfill(8)
        #     if i == 6:
        #         print(a, b)
        #         color_code(data[i])


async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        # x = await client.is_connected()
        while True:
            try:
                x = await client.is_connected()
                # print("Connected: {0}".format(x))
                await client.start_notify(MARIO_CHARACTERISTIC_UUID, notification_handler)
                write_value = bytearray(port_val)
                await client.write_gatt_char(MARIO_CHARACTERISTIC_UUID, write_value)
                # 10秒後に終了
                await asyncio.sleep(0.5, loop=loop)
                await client.stop_notify(MARIO_CHARACTERISTIC_UUID)
            except:
                print("Received exit, exiting")
                await client.stop_notify(MARIO_CHARACTERISTIC_UUID)
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop))
