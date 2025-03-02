import base64
from io import BytesIO
from PIL import Image, ImageDraw

def get_icon():
    # Create a hosts file icon
    icon_data = (
        'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlz'
        'AAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAQFSURB'
        'VFiF7ZdbiJVVFMd/a+/vfOfMOTNnxhk1x5nxAqKoZIWXMaQosB6iC1QPUr0UEUGQD5FEYFJEPnQj'
        'oqineol6CbqZUkmUeUVLLLU0dUYdZ87MOd+3d9fDOWfmnJnRGSHoIRZsNt/e/7X/e+21115bWJQF'
        'Qe5bRvF/l/8cQKVhVYUwXCWwHLgBuAZYCrQBBtgPHAZ+Ar4XkW/D2B7pX/LzYKMxjQNUGlZVGNpH'
        'RGQ9cCtwKTDtJwKDwCHgK+BDhfeGlxw+Wg9iXgDlhlUTqN4vIvcCi+eYezoZAT4G3kpE3x1e8sux'
        '2QDmBCg3rLpGVZ8ArgIkz5xJVTNgEPgGeB94L4ztZ/1Lfj5RC2JWgErdqglVHwEeBhbn5oeAI8Bv'
        'wDhQADqBK4HLgOY8bgx4W0QeH1py+MhMEDMClOtWXaXqM8BtQAQcBD4FvgQOishwvQQisgS4Hrge'
        'uAu4JF8aAV5X1cdHlh4+XgtCpgMo160aUH0euA8oAe8BL4nIvlqJZpKKiKwEngLuBgzwJfBQf+eh'
        'fdNjpwGU61YNqL4E3A2cAJ4TkVcXmrxaKiLyIPAC0AZ8ADzQ33loqBo3BaBct2pA9WXgHuAk8LSI'
        'vNZI8iqIB4CXgXbgXRG5f6Dr0Eg5ZgJAuW7VgOorwD3ACeApEXmj0eRVEPcBrwKtwAci8kB/16Hh'
        'ybgJgHLdqkH1VeBu4DjwpIi82SzyKohNwGtAG/CeiNzX33VoZAKgXLdqUH0NuAs4BjwhIm81m7wK'
        '4l7gdaAdeF9ENvd3HRoFEADKdauG1JeBjcBR4DER+aBVyasg7gHeADqAD0Vk00DXoTEBKNWtGlJ9'
        'CdgAHAEeFZGPWk1eBXEX8CbQCXwsIpsHug6NC0CpbtWQ6ovARuAw8IiIfHK2yKsgbgfeAhYDn4jI'
        'XQNdh8YFoFS3alB9AdgEDAIPi8in54K8CuI24G1gCfCpiNw50HVoQgBKdauG1OeBe4FB4CER+fxc'
        'kldBbADeAZYCn4vIhoGuQxMCUKpbNag+B2wGBoAHReTLc01eBbEeeA/oAr4Qkdv7uw5lAqBUt2pI'
        'fRbYAgwA94vIV+eLvAriVmArsAzYJiK39ncdygSgVLdqSH0G2AocB+4Tke3nk7wKYh3wPrAc2C4i'
        't/R3HcoEoFS3alB9GtgKnADuFZEd55u8CmIt8AGwAtghIjf3dx3KBKBUt2pIfQrYBpwE7hGRnReK'
        'vApiDfAhsBLYKSI39XcdygSgVLdqUJ8EtgOngM0isuuCkU+KyGrgI+AyYJeI3NjfdSgTgFLdqiH1'
        'CeBz4DSwSUR2X2jyKohVwMfAlcBuEbmhv+tQJgCluv0H+Aa4QUR+uNDEVRArgZ3ANcAeEVnb33Uo'
        '+/svRRblb8u8f86/ASbWsoI3S4WGAAAAAElFTkSuQmCC'
    )
    
    # Decode the base64 data
    icon_bytes = base64.b64decode(icon_data)
    
    # Return the bytes for use with PhotoImage
    return icon_bytes

def create_icon_image():
    # For creating a PIL Image object from the icon data
    try:
        icon_bytes = get_icon()
        image = Image.open(BytesIO(icon_bytes))
        return image
    except Exception as e:
        # If there's an error with the image data, create a simple icon instead
        img = Image.new('RGBA', (64, 64), color=(0, 120, 212, 255))
        draw = ImageDraw.Draw(img)
        # Draw a simple hosts file icon
        draw.rectangle([10, 10, 54, 54], fill=(255, 255, 255))
        draw.rectangle([16, 20, 48, 22], fill=(0, 0, 0))
        draw.rectangle([16, 28, 48, 30], fill=(0, 0, 0))
        draw.rectangle([16, 36, 48, 38], fill=(0, 0, 0))
        draw.rectangle([16, 44, 48, 46], fill=(0, 0, 0))
        return img