import json

FIN_BIT_MASK = MASK_BIT_MASK = 0x80
RSV_BIT_MASK = 0x70
OPC_BIT_MASK = 0x0F
SM_PAYLOAD_MASK = 0x7F
MASK_KEY_MASK = 0xFFFF


class WebsocketParser:
    BUFFERSIZE = 2048

    def __init__(self, request):
        self.request = request

    def read_websocket_frame(self):
        frame = self.request.recv(WebsocketParser.BUFFERSIZE)
        return WebsocketParser.parse_websocket_frame(frame)

    @staticmethod
    def parse_websocket_frame(frame):
        n_xor = 0  # number of bytes xor'd from the payload
        counter = 0  # keeps track of which byte we're on in the mask (0 - 3)
        json_payload = b""  # holds the payload after the mask has been applied

        if len(frame) == 0:
            raise WebSocketEmptyFrameError

        # parse the first byte
        byte_one = frame[0]
        fin_bit = int((byte_one & FIN_BIT_MASK) >> 7)
        rsv_bit = (byte_one & RSV_BIT_MASK) >> 4
        opcode  = (byte_one & OPC_BIT_MASK)
        if fin_bit == 0:  # TODO: Keep reading in frames if fin_bit is not set
            raise NotImplementedError("FIN bit not set")
        if opcode != b"0001":
            raise NotImplementedError(f"Unexpected Opcode: {opcode}")

        # parse the second byte
        byte_two = frame[1]
        mask_bit = int((byte_two & MASK_BIT_MASK) >> 7)
        payload_len = int((byte_two & SM_PAYLOAD_MASK))
        mask_start = 2

        # determine where the mask or payload starts
        if payload_len == 126:
            # The next 2 bytes are the length
            payload_len = int(frame[2:4])
            mask_start = 4
        elif payload_len == 127:
            # the next 6 bytes are the length
            payload_len = int(frame[2:10])
            mask_start = 10

        # Get the mask key if its there
        if mask_bit != 1:
            mask_key = frame[mask_start:mask_start+4]
            payload_start = mask_start + 4
        else:
            payload_start = mask_start
            n_xor = payload_len  # Dont let the while loop activate

        # Get the payload bytes from the frame
        byte_payload = frame[payload_start:payload_start+payload_len]

        # XOR the bytes with the mask
        while n_xor < payload_len:
            to_xor = byte_payload[n_xor]
            json_payload += to_xor ^ mask_key[counter]
            n_xor += 1
            counter = counter+1 if counter+1 < 4 else 0

        # When the mask bit is not set
        if json_payload == b"":
            json_payload = byte_payload

        print(f"{fin_bit} {rsv_bit} {opcode}")
        print(f"{mask_bit} {payload_len}")
        print(f"{mask_key}")
        print(f"{json_payload}")

        return json.loads(json_payload)


class WebSocketParserError(Exception):
    pass


class WebSocketEmptyFrameError(WebSocketParserError):
    pass
