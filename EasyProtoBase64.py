import base64
import struct

class EasyProtoBase64:
    WIRE_TYPE_VARINT = 0
    WIRE_TYPE_64BIT = 1
    WIRE_TYPE_LENGTH_DELIMITED = 2
    WIRE_TYPE_32BIT = 5

    @staticmethod
    def _encode_varint(value: int) -> bytes:
        result = []
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                result.append(byte | 0x80)
            else:
                result.append(byte)
                break
        return bytes(result)

    @staticmethod
    def _encode_length_delimited(value_str: str) -> bytes:
        encoded_value = value_str.encode('utf-8')
        length = len(encoded_value)
        return EasyProtoBase64._encode_varint(length) + encoded_value

    @staticmethod
    def _guess_wire_type(value):
        if isinstance(value, int):
            return EasyProtoBase64.WIRE_TYPE_VARINT
        elif isinstance(value, str):
            return EasyProtoBase64.WIRE_TYPE_LENGTH_DELIMITED
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    @staticmethod
    def _encode_field(field_number: int, wire_type: int, value) -> bytes:
        key = (field_number << 3) | wire_type
        encoded_key = EasyProtoBase64._encode_varint(key)

        if wire_type == EasyProtoBase64.WIRE_TYPE_VARINT:
            return encoded_key + EasyProtoBase64._encode_varint(value)
        elif wire_type == EasyProtoBase64.WIRE_TYPE_64BIT:
            return encoded_key + struct.pack('<Q', value)
        elif wire_type == EasyProtoBase64.WIRE_TYPE_LENGTH_DELIMITED:
            return encoded_key + EasyProtoBase64._encode_length_delimited(value)
        elif wire_type == EasyProtoBase64.WIRE_TYPE_32BIT:
            return encoded_key + struct.pack('<I', value)
        else:
            raise ValueError("Unsupported wire type")

    @staticmethod
    def encode(fields: dict[int, int|str]) -> bytes:
        result = b""
        for field_number, value in fields.items():
            wire_type = EasyProtoBase64._guess_wire_type(value)
            result += EasyProtoBase64._encode_field(field_number, wire_type, value)
        return result

    @staticmethod
    def encode_to_base64(fields: dict[int, int|str]) -> str:
        protobuf_data = EasyProtoBase64.encode(fields)
        return base64.b64encode(protobuf_data).decode('utf-8')

    @staticmethod
    def _decode_varint(data: bytes, index: int) -> tuple[int, int]:
        result = 0
        shift = 0
        while True:
            byte = data[index]
            result |= (byte & 0x7F) << shift
            index += 1
            if not (byte & 0x80):
                break
            shift += 7
        return result, index

    @staticmethod
    def _decode_length_delimited(data: bytes, index: int) -> tuple[str, int]:
        length, index = EasyProtoBase64._decode_varint(data, index)
        value = data[index:index + length].decode('utf-8')
        return value, index + length

    @staticmethod
    def _decode_field(data: bytes, index: int) -> tuple[int, int, int|str, int]:
        key, index = EasyProtoBase64._decode_varint(data, index)
        field_number = key >> 3
        wire_type = key & 0x7

        if wire_type == EasyProtoBase64.WIRE_TYPE_VARINT:
            value, index = EasyProtoBase64._decode_varint(data, index)
        elif wire_type == EasyProtoBase64.WIRE_TYPE_64BIT:
            value = struct.unpack('<Q', data[index:index + 8])[0]
            index += 8
        elif wire_type == EasyProtoBase64.WIRE_TYPE_LENGTH_DELIMITED:
            value, index = EasyProtoBase64._decode_length_delimited(data, index)
        elif wire_type == EasyProtoBase64.WIRE_TYPE_32BIT:
            value = struct.unpack('<I', data[index:index + 4])[0]
            index += 4
        else:
            raise ValueError("Unsupported wire type")

        return field_number, wire_type, value, index

    @staticmethod
    def decode(protobuf_data: bytes) -> dict[int, int|str]:
        index = 0
        decoded_fields = {}
        while index < len(protobuf_data):
            field_number, wire_type, value, index = EasyProtoBase64._decode_field(protobuf_data, index)
            decoded_fields[field_number] = value
        return decoded_fields

    @staticmethod
    def decode_from_base64(base64_data: str) -> dict[int, int|str]:
        protobuf_data = base64.b64decode(base64_data)
        return EasyProtoBase64.decode(protobuf_data)
