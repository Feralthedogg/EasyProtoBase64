### EasyProtoBase64 Documentation (English & Korean)

---

## **Class Overview**
`EasyProtoBase64` provides a simple way to encode and decode protobuf-like data structures into Base64 format. It automatically determines wire types based on value types (e.g., integers as VARINT, strings as LENGTH_DELIMITED).

`EasyProtoBase64`는 protobuf 스타일의 데이터 구조를 Base64 형식으로 쉽게 인코딩하고 디코딩할 수 있는 간단한 클래스입니다. 값의 타입에 따라 wire type(정수 → VARINT, 문자열 → LENGTH_DELIMITED)을 자동으로 결정합니다.

---

## **Key Features | 주요 기능**
- **Automatic Wire Type Detection | 와이어 타입 자동 감지**: 
  Automatically detects wire types based on value types (`int` → VARINT, `str` → LENGTH_DELIMITED).  
  값의 타입에 따라 wire type을 자동으로 결정합니다 (`int` → VARINT, `str` → LENGTH_DELIMITED).
  
- **Minimal Interface | 간단한 인터페이스**: 
  Provides two key methods for encoding and decoding:
  - `encode_to_base64`: Encodes data to Base64
  - `decode_from_base64`: Decodes Base64 back to data  
  인코딩 및 디코딩을 위한 두 가지 주요 메서드를 제공합니다.
  - `encode_to_base64`: 데이터를 Base64로 인코딩
  - `decode_from_base64`: Base64를 데이터로 디코딩
  
- **Easy to Use | 사용하기 쉬움**: 
  Simply pass a dictionary of field numbers and values to encode or decode.  
  필드 번호와 값을 포함한 딕셔너리를 전달하여 쉽게 인코딩하거나 디코딩할 수 있습니다.

---

## **Methods | 메서드**

### `encode_to_base64(fields: dict[int, int | str]) -> str`
**Description**  
Encodes a dictionary of fields (`{field_number: value}`) into a Base64 string. Automatically determines the wire type based on the value type.  

딕셔너리 형태의 필드(`{field_number: value}`)를 Base64 문자열로 인코딩합니다. 값의 타입에 따라 wire type을 자동으로 결정합니다.

**Parameters | 매개변수**  
- `fields`: A dictionary where the key is the field number (int) and the value is either an `int` or `str`.  
  필드 번호(int)를 키로 하고 값은 `int` 또는 `str`인 딕셔너리.

**Returns | 반환값**  
- A Base64-encoded string.  
  Base64로 인코딩된 문자열.

**Example | 사용 예제**
```python
fields = {
    1: 150,      # int → VARINT
    2: "John Doe", # str → LENGTH_DELIMITED
    3: 1         # int → VARINT
}
encoded_base64 = EasyProtoBase64.encode_to_base64(fields)
print(encoded_base64)  # Outputs Base64 string
```

---

### `decode_from_base64(base64_data: str) -> dict[int, int | str]`
**Description**  
Decodes a Base64-encoded protobuf-like string back into a dictionary of fields (`{field_number: value}`).  

Base64로 인코딩된 protobuf 스타일 문자열을 디코딩하여 필드 딕셔너리(`{field_number: value}`)로 변환합니다.

**Parameters | 매개변수**  
- `base64_data`: A Base64-encoded protobuf-like string.  
  Base64로 인코딩된 protobuf 스타일 문자열.

**Returns | 반환값**  
- A dictionary of fields (`{field_number: value}`).  
  필드 딕셔너리(`{field_number: value}`).

**Example | 사용 예제**
```python
decoded_fields = EasyProtoBase64.decode_from_base64(encoded_base64)
print(decoded_fields)  # Outputs {1: 150, 2: "John Doe", 3: 1}
```

---

## **Supported Data Types | 지원 데이터 타입**
- **Integer (`int`)**: Automatically encoded as `VARINT`.  
  정수(`int`): `VARINT`로 자동 인코딩됩니다.
- **String (`str`)**: Automatically encoded as `LENGTH_DELIMITED`.  
  문자열(`str`): `LENGTH_DELIMITED`로 자동 인코딩됩니다.

---

## **Error Handling | 에러 처리**
- **Unsupported Value Types | 지원하지 않는 값 타입**:  
  Raises a `ValueError` if a value is neither an integer nor a string.  
  값이 정수나 문자열이 아닌 경우 `ValueError`가 발생합니다.
  
  ```python
  fields = {1: 3.14}  # float is unsupported
  encoded_base64 = EasyProtoBase64.encode_to_base64(fields)
  # Raises ValueError: Unsupported value type: <class 'float'>
  ```

---

## **Installation | 설치**
No external dependencies are required. The module uses standard Python libraries only.  
추가 설치가 필요 없습니다. 표준 Python 라이브러리만 사용합니다.

---

## **Full Example | 전체 예제**

```python
from easy_proto_base64 import EasyProtoBase64  # Import the class

# Define fields to encode
fields = {
    1: 150,         # Integer
    2: "존 도",      # Korean String
    3: 1            # Another Integer
}

# Encode fields to Base64
encoded = EasyProtoBase64.encode_to_base64(fields)
print("Encoded Base64:", encoded)

# Decode back to fields
decoded = EasyProtoBase64.decode_from_base64(encoded)
print("Decoded Fields:", decoded)
```

**Output | 출력**
```
Encoded Base64: [Base64 Encoded String]
Decoded Fields: {1: 150, 2: '존 도', 3: 1}
```

---
