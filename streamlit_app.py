import streamlit as st
from PIL import Image, ImageEnhance
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

# Fungsi untuk mengonversi gambar ke format byte agar bisa di-download
def convert_image_to_bytes(img, format_type):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format_type)
    img_byte_arr.seek(0)
    return img_byte_arr

# Layout Streamlit
st.image("https://th.bing.com/th/id/OIP.5HriVYJ9IdpM-pGiZPSU6wHaEK?rs=1&pid=ImgDetMain", width=100)
st.title("Image Editor")
st.write("Upload an image and edit it with rotation, brightness, scaling, and RGB color adjustments.")

# Upload gambar
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load image
    img = load_image(uploaded_file)
    st.image(img, caption="Original Image", use_container_width=True)

    # Pengaturan rotasi
    st.subheader("Step 1: Rotate Image")
    rotation_mode = st.radio("Choose Rotation Mode", ("Manual", "Automatic"))
    if rotation_mode == "Manual":
        # Manual rotation
        rotation_angle = st.slider("Rotate Image (0-360 degrees)", 0, 360, 0)
        img_rotated = rotate_image(img, rotation_angle)
    else:
        # Automatic rotation
        rotation_angle = st.selectbox("Select Rotation Angle", [0, 45, 90, 135, 180, 225, 270, 315, 360])
        img_rotated = rotate_image(img, rotation_angle)

    st.image(img_rotated, caption="Rotated Image", use_container_width=True)

    # Pengaturan kecerahan
    st.subheader("Step 2: Adjust Brightness")
    brightness_factor = st.slider("Adjust Brightness (0.1 - 2.0)", 0.1, 2.0, 1.0)
    img_bright = adjust_brightness(img_rotated, brightness_factor)
    st.image(img_bright, caption="Brightness Adjusted Image", use_container_width=True)

    # Pengaturan scale
    st.subheader("Step 3: Scale Image")
    scale_factor = st.slider("Scale Image (0.1 - 3.0)", 0.1, 3.0, 1.0)
    img_scaled = scale_image(img_bright, scale_factor)
    st.image(img_scaled, caption="Scaled Image", use_container_width=True)

    # Pengaturan RGB
    st.subheader("Step 4: Adjust RGB Colors")
    red_factor = st.slider("Red Intensity", 0.0, 2.0, 1.0)
    green_factor = st.slider("Green Intensity", 0.0, 2.0, 1.0)
    blue_factor = st.slider("Blue Intensity", 0.0, 2.0, 1.0)

    img_rgb = img_scaled.convert("RGB")  # Ensure the image is in RGB mode
    r, g, b = img_rgb.split()
    r = r.point(lambda i: i * red_factor)
    g = g.point(lambda i: i * green_factor)
    b = b.point(lambda i: i * blue_factor)

    img_colored = Image.merge("RGB", (r, g, b))
    st.image(img_colored, caption="Final Edited Image", use_container_width=True)

    # Tombol download untuk setiap format
    st.subheader("Download the Edited Image")
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
