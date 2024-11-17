import random
import time
import hmac
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 生成随机 UUID-like 字符串
def generate_uuid():
    chars = "0123456789abcdef"
    uuid = [random.choice(chars) for _ in range(36)]
    uuid[14] = "4"  # 固定第 14 位为 '4'
    uuid[19] = chars[(int(uuid[19], 16) & 0x3) | 0x8]  # 第 19 位按规则生成
    uuid[8] = uuid[13] = uuid[18] = uuid[23] = "-"  # 固定位置为 '-'
    return "".join(uuid)

# 解密 NUMCODE (模拟部分，实际解密需要实现)
def aes_decrypt(ciphertext, key, iv):
    """
    AES 解密函数
    :param ciphertext: 待解密的密文 (Base64 编码)
    :param key: 密钥 (字符串)
    :param iv: 初始化向量 (字符串)
    :return: 解密后的字符串
    """
    # 将密钥和 IV 转换为字节数组
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')

    # Base64 解码密文
    encrypted_data = base64.b64decode(ciphertext)

    # 创建 AES 解密器
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    # 解密并去除填充
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size, style='pkcs7')

    # 转换为字符串并返回
    return decrypted_data.decode('utf-8')

# HMAC-SHA256 计算
def calculate_hmac_sha256(data, key):
    hmac_result = hmac.new(key.encode(), data.encode(), hashlib.sha256)
    return hmac_result.hexdigest()

# 完整实现 h 函数
def getKey(e):
    t = generate_uuid()  # 生成 UUID
    n = int(time.time() * 1000)  # 获取当前时间戳（毫秒）

    # t = "2c34b7a8-2beb-4b4d-8afd-606e951c9e32"
    # n = 1731831262457
    r = f"seat::{t}::{n}::{e.upper()}"  # 构造请求字符串

    # 假定解密 NUMCODE 的值
    numcode_encrypted = "UmrX+lxhFE5neclEsBPing=="
    # o = aes_decrypt(numcode_encrypted, "server_date_time", "client_date_time")  # 解密密钥
    o = "ujnLIB2022tsg"
    request_key = calculate_hmac_sha256(r, o)  # 计算 HMAC-SHA256

    return {
        "id": t,
        "date": n,
        "requestKey": request_key
    }

# 测试函数
# result = h("get")
# print(result)
