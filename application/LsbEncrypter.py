from math import floor


# noinspection DuplicatedCode
class LsbEncrypter:
    @staticmethod
    def encrypt(img, text: str, bit_position: int):
        max_size: int = floor((img.shape[0] * img.shape[1]) / 8)
        text_bits: str = LsbEncrypter._text_to_bits(text, max_size)
        if len(img.shape) == 2:
            return LsbEncrypter._bit_encryption_grayscale(img, text_bits, bit_position)
        elif len(img.shape) == 3:
            return LsbEncrypter._bit_encryption_bgr(img, text_bits, bit_position)
        return None

    @staticmethod
    def decrypt(img, bit_position: int) -> str:
        text_bits: str = ''
        if len(img.shape) == 2:
            text_bits = LsbEncrypter._bit_decryption_grayscale(img, bit_position)
        elif len(img.shape) == 3:
            text_bits = LsbEncrypter._bit_decryption_bgr(img, bit_position)
        result: str = LsbEncrypter._bits_to_text(text_bits)
        return result

    @staticmethod
    def _bit_encryption_grayscale(img, text_bits: str, bit_position: int):
        result = img.copy()
        if 1 <= bit_position <= 8:
            bit_amount: int = len(text_bits)
            iterator: int = 0
            for row in result:
                pixel: int = 0
                while pixel < len(row):
                    row[pixel] |= 2 ** (bit_position - 1)
                    if int(text_bits[iterator]) == 0:
                        row[pixel] &= 255 - 2 ** (bit_position - 1)
                    iterator += 1
                    if iterator >= bit_amount:
                        return result
                    pixel += 1
        return result

    @staticmethod
    def _bit_encryption_bgr(img, text_bits: str, bit_position: int):
        result = img.copy()
        if 1 <= bit_position <= 8:
            bit_amount: int = len(text_bits)
            iterator: int = 0
            for row in result:
                for pixel in row:
                    channel: int = 0
                    while channel < len(pixel):
                        pixel[channel] |= 2 ** (bit_position - 1)
                        if int(text_bits[iterator]) == 0:
                            pixel[channel] &= 255 - 2 ** (bit_position - 1)
                        iterator += 1
                        if iterator >= bit_amount:
                            return result
                        channel += 1
        return result

    @staticmethod
    def _bit_decryption_grayscale(img, bit_position: int):
        result: str = ''
        for row in img:
            for pixel in row:
                pixel &= 2 ** (bit_position - 1)
                if pixel == 2 ** (bit_position - 1):
                    result += '1'
                else:
                    result += '0'
                if len(result) % 8 == 0 and result.endswith('00000011'):
                    return result
        return result

    @staticmethod
    def _bit_decryption_bgr(img, bit_position: int):
        result: str = ''
        for row in img:
            for pixel in row:
                for channel in pixel:
                    channel &= 2 ** (bit_position - 1)
                    if channel == 2 ** (bit_position - 1):
                        result += '1'
                    else:
                        result += '0'
                    if len(result) % 8 == 0 and result.endswith('00000011'):
                        return result
        return result

    @staticmethod
    def _text_to_bits(text: str, max_size: int) -> str:
        text_bytes: bytes = text.encode('utf-8')
        result: str = bin(int.from_bytes(text_bytes, 'big')).replace('0b', '')
        if len(result) % 2 == 1:
            result = '0' + result
        if len(result) >= max_size:
            result = result[0:len(result) - 8]
        result += '00000011'
        return result

    @staticmethod
    def _bits_to_text(bits: str) -> str:
        text_number: int = int(bits, 2)
        text_bytes: bytes = text_number.to_bytes((len(bits)) // 8, 'big')
        result: str = text_bytes.decode('utf-8').strip()
        return result[0:len(result) - 1]
