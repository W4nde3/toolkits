# -*- coding: utf-8 -*-

import sys
import base36
import base58
from base62 import encodebytes as b62encode, decodebytes as b62decode
import base64
from merry import Merry
import click
import pyperclip

merry = Merry()
merry.logger.disabled = True


@click.command()
@click.option('--codec', prompt="请输入 --codec 参数 ", type=click.Choice(['base16', 'base32', 'base62', 'base64', 'base58', 'base85', 'base36']))
@click.option('--mode', prompt="请输入 encode[编码] or decode[解码]\n", type=click.Choice(['encode', 'decode']))
@click.option('--data', prompt="请输入执行编/解码的数据\n", type=click.STRING)
def core(codec, mode, data):
    try:
        if codec == 'base36' and mode == 'encode':
            data = int(data)
    except:
        print('Base36编码失败，仅支持数值类型')
        return 

    mode = 0 if mode == 'encode' else 1
    @merry._try
    def Base16(_mode=mode, _data=data): return base64.b16encode(_data.encode(
    )).decode() if mode == 0 else base64.b16decode(_data.encode()).decode()

    @merry._try
    def Base32(_mode=mode, _data=data): return base64.b32encode(_data.encode(
    )).decode() if mode == 0 else base64.b32decode(_data.encode()).decode()

    @merry._try
    def Base58(_mode=mode, _data=data): return base58.b58encode(_data.encode(
    )).decode() if mode == 0 else base58.b58decode(_data.encode()).decode()

    @merry._try
    def Base62(_mode=mode, _data=data): return b62encode(
        _data.encode()) if mode == 0 else b62decode(_data).decode()

    @merry._try
    def Base64(_mode=mode, _data=data): return base64.b64encode(_data.encode(
    )).decode() if mode == 0 else base64.b64decode(_data.encode()).decode()

    @merry._try
    def Base36(_mode=mode, _data=data): return base36.dumps(
        int(_data)) if mode == 0 else str(base36.loads(_data))

    @merry._try
    def Base85(_mode=mode, _data=data): return base64.b85encode(_data.encode(
    )).decode() if mode == 0 else base64.b85decode(_data.encode()).decode()

    @merry._except(ValueError)
    def demo(e):
        print("解码失败，不能正确理解该字串")
        return

    @merry._except(UnicodeDecodeError)
    def decode_fail(e):
        print('解码失败！不能正确解码该字串')
        return

    oper = {'base16': Base16, 'base32': Base32, 'base58': Base58,
            'base62': Base62, 'base64': Base64, 'base36': Base36, 'base85': Base85}

    @merry._try
    def show_res():
        result = oper.get(codec)(mode, data)
        pyperclip.copy(result)
        print(result, '\n【结果已复制到剪切板】')
        return result

    @merry._except(pyperclip.PyperclipException)
    def pyperclip_PyperclipException():
        pass
    return show_res()


if __name__ == "__main__":
    core()
