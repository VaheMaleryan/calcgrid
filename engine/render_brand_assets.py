"""Rebuild the committed social preview from our locally licensed fonts (requires Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent / 'brand_assets'
FONTS = ASSETS / 'fonts'

def render():
    image = Image.new('RGB', (1200, 630), '#f7f8f5')
    draw = ImageDraw.Draw(image)
    serif = lambda size: ImageFont.truetype(str(FONTS / 'InstrumentSerif-Regular.ttf'), size)
    italic = lambda size: ImageFont.truetype(str(FONTS / 'InstrumentSerif-Italic.ttf'), size)
    def sans(size):
        font = ImageFont.truetype(str(FONTS / 'Manrope-Variable.ttf'), size)
        font.set_variation_by_axes([500])
        return font
    ink, muted, green = '#19211e', '#58625c', '#234c3f'
    draw.text((65, 36), 'PayoutFolio', font=serif(43), fill=ink)
    draw.rounded_rectangle((887, 48, 1135, 90), radius=21, outline='#c9d1c8')
    draw.text((913, 58), 'Independent income, clarified', font=sans(13), fill=muted)
    draw.line((65, 119, 1135, 119), fill='#dce1da')
    draw.text((65, 175), 'Know what you', font=serif(105), fill=ink)
    draw.text((65, 276), 'actually keep.', font=italic(109), fill=green)
    draw.text((69, 427), 'Compare payout routes. Work backwards.', font=sans(19), fill=muted)
    draw.text((69, 458), 'Check your fees, privately on your device.', font=sans(19), fill=muted)
    draw.rounded_rectangle((805, 189, 1135, 486), radius=25, fill=green)
    draw.text((833, 219), 'ILLUSTRATIVE PAYOUT', font=sans(12), fill='#bed0bf')
    draw.text((833, 264), '$1,000.00', font=serif(40), fill='#bed0bf')
    draw.line((833, 326, 1105, 326), fill='#65816e')
    draw.text((833, 348), 'What you keep', font=sans(14), fill='#c8dacd')
    draw.text((831, 371), '$862.04', font=serif(67), fill='#ffffff')
    draw.text((833, 457), 'Editable assumptions · Not a quote', font=sans(10), fill='#c8dacd')
    draw.line((65, 548, 1135, 548), fill='#dce1da')
    draw.text((68, 573), '32 FREE BROWSER TOOLS', font=sans(12), fill=green)
    draw.text((839, 573), 'NO ACCOUNT. NO UPLOADS.', font=sans(12), fill=muted)
    image.save(ASSETS / 'og-preview.png', optimize=True)

if __name__ == '__main__':
    render()
