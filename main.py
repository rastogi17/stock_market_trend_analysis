import streamlit as st
# from home import home
# from aboutUs import about
from aboutUs import aboutUs
from PIL import Image
from chatbot import chat
from combined import dashboard
import base64

logo = Image.open('D:/Documents/Plaksha TLP/DataX Python/Group_Proj/RISE/Rise.ai logo.png')

PAGES = {
    "About Us": aboutUs,
    "Dashboard": dashboard,
    "Chatbot": chat
}

# Set the background image
def read_image(file_path):
    with open(file_path, "rb") as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode()

def main():

    # Display the logo at specific coordinates within the sidebar
    st.sidebar.markdown(
        f"""
        <div style="position: absolute; top: -100px; left: -58px;">
            <img src="data:image/png;base64,{image_to_base64(logo)}" style="width: 250px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar navigation
    st.sidebar.title("")
    selection = st.sidebar.radio("", list(PAGES.keys()))

    page = PAGES[selection]
    page()

    # # Add your custom CSS for the background image
    # custom_css = f"""
    # <style>
    # [data-testid="stAppViewContainer"] > .main {{
    #     background-image: url('data:image/jpeg;base64,{read_image("D:/Documents/Plaksha TLP/DataX Python/Group_Proj/RISE/rise_ai_photo.png")}');
    #     background-size: 100% 100%;
    #     background-position: top left;
    #     background-repeat: no-repeat;
    #     background-attachment: local;
    # }}
    # </style>
    # """

    # # Inject the custom CSS into the app
    # st.markdown(custom_css, unsafe_allow_html=True)

    # Disclaimer and copyright notice
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    
    st.sidebar.markdown("---")
    st.sidebar.write("© 2024 Your Company. All Rights Reserved.")
    st.sidebar.write("This is a disclaimer.")

def image_to_base64(image):
    import base64
    import io
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode()

if __name__ == "__main__":
    main()
