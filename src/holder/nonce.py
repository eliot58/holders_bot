import hmac
import hashlib
import time
import secrets
import struct
import binascii

def generate_payload(secret: str, ttl: float) -> str:
    # Генерируем 16 байт: первые 8 байт - это случайный nonce, следующие 8 байт - это таймстамп с TTL
    payload = bytearray(16)
    payload[:8] = secrets.token_bytes(8)
    struct.pack_into('>Q', payload, 8, int(time.time() + ttl))
    
    # Создаем HMAC на основе SHA256
    h = hmac.new(secret.encode(), payload, hashlib.sha256)
    payload.extend(h.digest())
    
    # Возвращаем первые 32 байта в hex формате
    return binascii.hexlify(payload[:32]).decode()

def check_payload(payload: str, secret: str) -> None:
    # Декодируем hex строку в байты
    try:
        b = binascii.unhexlify(payload)
    except binascii.Error:
        raise ValueError("invalid hex string")
    
    if len(b) != 32:
        raise ValueError("invalid payload length")
    
    # Проверяем подпись
    h = hmac.new(secret.encode(), b[:16], hashlib.sha256)
    sign = h.digest()
    
    if not hmac.compare_digest(b[16:], sign[:16]):
        raise ValueError("invalid payload signature")
    
    # Проверяем истек ли срок действия
    timestamp = struct.unpack('>Q', b[8:16])[0]
    if time.time() > timestamp:
        raise ValueError("payload expired")

# Пример использования
secret = "mysecret"
ttl = 60  # время жизни токена в секундах

payload = generate_payload(secret, ttl)
print("Generated payload:", payload)

try:
    check_payload(payload, secret)
    print("Payload is valid")
except ValueError as e:
    print("Payload validation failed:", e)
