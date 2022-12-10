import numpy as np
import cv2
import asyncio
import websockets
import base64


async def show_cam():
    uri = "ws://192.168.137.246:6000"
    async with websockets.connect(uri) as websocket:
        data = await websocket.recv()
        data = cv2.imdecode(np.frombuffer(base64.b64decode(data), dtype='uint8'), cv2.IMREAD_COLOR)
        cv2.imshow("2022_ESD", data)

asyncio.get_event_loop().run_until_complete(show_cam())