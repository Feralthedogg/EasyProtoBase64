from EasyProtoBase64 import EasyProtoBase64

if __name__ == "__main__":
    fields = {
        1: 150,
        2: "John Doe",
        3: 1
    }

    encoded_base64 = EasyProtoBase64.encode_to_base64(fields)
    print("Encoded to Base64:", encoded_base64)

    decoded_fields = EasyProtoBase64.decode_from_base64(encoded_base64)
    print("Decoded Fields:", decoded_fields)
