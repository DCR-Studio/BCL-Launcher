# Get offline player's uuid
#(c)2025 DCR Studio
import hashlib
import uuid

def get_offline_uuid(username: str) -> str:
    hash_input = f"OfflinePlayer:{username}".encode("utf-8")
    md5_hash = hashlib.md5(hash_input).digest()

    #md5_bytes = bytearray(md5_hash)
    #md5_bytes[6] = (md5_bytes[6] & 0x0F) | 0x30
    #md5_bytes[8] = (md5_bytes[8] & 0x3F) | 0x80
    #offline_uuid = uuid.UUID(bytes=bytes(md5_bytes))
    offline_uuid = uuid.UUID(bytes=md5_hash, version=3)
    return str(offline_uuid)

# example
username="Leo_Lee_Of"
offline_uuid = get_offline_uuid(username)
print(f"Username:{username}")
print(f"Offline UUID:{offline_uuid}")