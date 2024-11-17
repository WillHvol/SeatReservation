from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64


# 加密函数
def aes_encrypt(text, key, iv):
    # 将字符串转换为字节
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')

    # 创建 AES 加密对象
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    # PKCS7 填充并加密
    ciphertext = cipher.encrypt(pad(text_bytes, AES.block_size))

    # Base64 编码返回加密后的字符串
    return base64.b64encode(ciphertext).decode('utf-8')


# 示例数据
text = "hello world"
key = "1234567890123456"  # 16 字节密钥
iv = "abcdefghijklmnop"  # 16 字节 IV

# 执行加密
encrypted = aes_encrypt(text, key, iv)
print("加密结果:", encrypted)
