from PIL import Image

src_png = "caixa-logo.png"  # use uma imagem de origem grande e nítida
dst_ico = "caixa-logo.ico"

sizes = [(256,256), (128,128), (64,64), (48,48), (32,32), (24,24), (16,16)]

img = Image.open(src_png).convert("RGBA")

# Reamostar com LANCZOS para preservar detalhes
icons = [img.resize(size, Image.LANCZOS) for size in sizes]

# Salvar .ico contendo TODAS as resoluções
icons[0].save(dst_ico, format="ICO", sizes=sizes)
print("Gerado:", dst_ico)