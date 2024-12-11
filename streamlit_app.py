import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import io

# Fungsi untuk memuat gambar
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Fungsi untuk merotasi gambar
def rotate_image(img, angle):
    return img.rotate(angle, expand=True)

# Fungsi untuk mengatur kecerahan gambar
def adjust_brightness(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

# Fungsi untuk memperbesar atau memperkecil gambar
def scale_image(img, scale_factor):
    width, height = img.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return img.resize((new_width, new_height))

# Fungsi untuk mengubah orientasi gambar menjadi potret atau lanskap
def change_orientation(img, orientation):
    if orientation == "Portrait" and img.width > img.height:
        return img.rotate(90, expand=True)
    elif orientation == "Landscape" and img.height > img.width:
        return img.rotate(90, expand=True)
    return img

# Fungsi untuk mengubah komposisi warna gambar dengan 7 warna
def adjust_color_seven(img, red_factor, green_factor, blue_factor, purple_factor, orange_factor, yellow_factor, indigo_factor):
    r, g, b = img.split()
    # Komponen dasar RGB
    r = r.point(lambda i: i * red_factor)
    g = g.point(lambda i: i * green_factor)
    b = b.point(lambda i: i * blue_factor)

    # Komponen warna tambahan (campuran)
    purple = ImageOps.colorize(r.convert("L"), black="black", white="purple").split()[1].point(lambda i: i * purple_factor)
    orange = ImageOps.colorize(g.convert("L"), black="black", white="orange").split()[1].point(lambda i: i * orange_factor)
    yellow = ImageOps.colorize(r.convert("L"), black="black", white="yellow").split()[1].point(lambda i: i * yellow_factor)
    indigo = ImageOps.colorize(b.convert("L"), black="black", white="indigo").split()[1].point(lambda i: i * indigo_factor)

    # Gabungkan semua komponen warna
    r = Image.blend(r, purple, purple_factor / 2)
    g = Image.blend(g, orange, orange_factor / 2)
    b = Image.blend(b, yellow, yellow_factor / 2)

    return Image.merge("RGB", (r, g, b))

# Fungsi untuk mengonversi gambar ke format byte agar bisa di-download
def convert_image_to_bytes(img, format_type):
    img_byte_arr = io.BytesIO()
    if format_type == "PNG":
        img.save(img_byte_arr, format='PNG')
    elif format_type == "JPEG":
        img.save(img_byte_arr, format='JPEG')
    elif format_type == "PDF":
        img.save(img_byte_arr, format='PDF')
    img_byte_arr.seek(0)
    return img_byte_arr

# Layout Streamlit
st.title("Image Editor")
st.write("Upload an image and edit it with rotation, scaling, brightness, orientation, and color adjustments.")

# Upload gambar
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load image
    img = load_image(uploaded_file)
    st.image(img, caption="Original Image", use_container_width=True)

    # Pengaturan rotasi
    rotation_angle = st.slider("Rotate Image", 0, 360, 0)
    img_rotated = rotate_image(img, rotation_angle)

    # Pengaturan kecerahan
    brightness_factor = st.slider("Adjust Brightness", 0.1, 2.0, 1.0)
    img_bright = adjust_brightness(img_rotated, brightness_factor)

    # Pengaturan scale
    scale_factor = st.slider("Scale Image", 0.1, 3.0, 1.0)
    img_scaled = scale_image(img_bright, scale_factor)

    # Pengaturan orientasi
    orientation = st.radio("Change Orientation", ("Original", "Portrait", "Landscape"))
    img_oriented = change_orientation(img_scaled, orientation) if orientation != "Original" else img_scaled

    # Pengaturan komposisi warna dengan 7 warna
    st.write("Adjust Color Composition (7 Colors):")
    red_factor = st.slider("Red Intensity", 0.0, 2.0, 1.0)
    green_factor = st.slider("Green Intensity", 0.0, 2.0, 1.0)
    blue_factor = st.slider("Blue Intensity", 0.0, 2.0, 1.0)
    purple_factor = st.slider("Purple Intensity", 0.0, 2.0, 0.0)
    orange_factor = st.slider("Orange Intensity", 0.0, 2.0, 0.0)
    yellow_factor = st.slider("Yellow Intensity", 0.0, 2.0, 0.0)
    indigo_factor = st.slider("Indigo Intensity", 0.0, 2.0, 0.0)
    img_colored = adjust_color_seven(img_oriented, red_factor, green_factor, blue_factor, purple_factor, orange_factor, yellow_factor, indigo_factor)

    st.image(img_colored, caption="Edited Image", use_container_width=True)

    # Tombol download untuk setiap format
    st.write("Download the edited image in your preferred format:")

    img_png = convert_image_to_bytes(img_colored, "PNG")
    st.download_button(
        label="Download as PNG",
        data=img_png,
        file_name="edited_image.png",
        mime="image/png"
    )

    img_jpeg = convert_image_to_bytes(img_colored, "JPEG")
    st.download_button(
        label="Download as JPEG",
        data=img_jpeg,
        file_name="edited_image.jpeg",
        mime="image/jpeg"
    )

    img_pdf = convert_image_to_bytes(img_colored, "PDF")
    st.download_button(
        label="Download as PDF",
        data=img_pdf,
        file_name="edited_image.pdf",
        mime="application/pdf"
    )