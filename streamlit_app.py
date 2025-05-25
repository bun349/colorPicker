import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans

# --- Setup halaman
st.set_page_config(page_title="Color Picker", layout="centered", page_icon="🎨")

st.markdown("""
    <style>
        .stApp {
            background-color: white;
            font-family: 'Segoe UI', sans-serif;
            color: black;
        }
        html, body, [class*="css"] {
            color: black;
        }
        .stButton button {
        border-radius: 8px;
        border: 2px solid #555;
        background-color: white;
        color: black;
        padding: 0.5em 1em;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 125px;
        }

        /* Saat mouse hover */
        .stButton button:hover {
            background-color: #f0f0f0;  /* warna latar saat hover */
            border-color: black;
            transform: scale(1.03);     /* efek membesar */
            color: #800000;  
        }

        .stButton button:active {
            background-color: #dcdcdc;  /* warna saat tombol ditekan */
            transform: scale(0.97);     /* efek mengecil */
            color: #333;
        }
            
        .color-box {
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            height: 90px;
            margin-top: 6px;
        }
        
        div[data-testid="stFileUploader"] label {
        color: black !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- Judul
st.markdown("<h1 style='text-align:center; color:black;'>Color Picker Interaktif</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:black;'>Unggah gambar, lalu klik salah satu warna dominan untuk melihat di mana warna itu muncul.</p>", unsafe_allow_html=True)
st.write("\n")  

# --- Upload gambar
uploaded_file = st.file_uploader("Unggah gambar kamu di sini", type=["jpg", "jpeg", "png"])

def extract_colors(image, num_colors=5):
    small_img = image.resize((200, 200))
    img_np = np.array(small_img).reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(img_np)
    colors = np.round(kmeans.cluster_centers_).astype(int)
    return colors

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(*color)

def highlight_color_area(image, target_color, threshold=50):
    img_np = np.array(image)
    mask = np.linalg.norm(img_np - target_color, axis=2) < threshold

    result = image.copy()
    draw = ImageDraw.Draw(result)

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x]:
                draw.ellipse((x-2, y-2, x+2, y+2), fill=(255, 255, 255)) 

    return result

# --- Jika ada file diupload
if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Gambar Asli")

    # Ekstrak warna dominan
    colors = extract_colors(image)
    st.subheader("Klik salah satu warna:")

    selected_color = None
    cols = st.columns(len(colors))
    for i, col in enumerate(cols):
        hex_code = rgb_to_hex(colors[i])
        with col:
            if st.button(f"{hex_code}", key=f"btn_{i}"):
                selected_color = colors[i]
            st.markdown(
                f"<div class='color-box' style='background-color:{hex_code};'></div>",
                unsafe_allow_html=True
            )

    if selected_color is not None:
        highlighted_image = highlight_color_area(image, selected_color)
        st.write("\n")  
        st.image(highlighted_image, caption="Area warna yang terdeteksi")
