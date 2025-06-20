import streamlit as st
import requests
from datetime import datetime
from PIL import Image
import base64
from streamlit_autorefresh import st_autorefresh
from datetime import timedelta



def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"



# Page settings
st.set_page_config(page_title="SkyNow 🌤️", page_icon="☁️", layout="centered")
st_autorefresh(interval=60000, key="refresh")

bg_image = get_base64_encoded_image("background_converted.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

logo = Image.open("logo.png")
col_logo, _ = st.columns([1, 10])
with col_logo:
    st.image(logo, width=100)



st.title("🌤️ SkyNow Weather Tracker")
st.write("Get real-time weather updates for any city in the world 🌍")

# City input
city = st.text_input("Enter city:")

if city:
    # OpenWeather API URL (metric = Celsius)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e43a2cc360cb99a67d9635dd38a9f734&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        # If city is found
        if str(data.get("cod")) == "200":
            st.success(f"📍 {data['name']}, {data['sys']['country']}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
                st.markdown(f"**💧 Humidity:** {data['main']['humidity']}%")
                st.markdown(f"**☁️ Condition:** {data['weather'][0]['description'].title()}")

            with col2:
                st.markdown(f"**🌬️ Wind Speed:** {data['wind']['speed']} m/s")
                utc_dt = datetime.utcfromtimestamp(data["dt"])
                ist_dt = utc_dt + timedelta(hours=5, minutes=30)
                st.markdown(f"**🕓 Updated at:** {ist_dt.strftime('%I:%M %p')} (IST)")


            st.caption("SkyNow ⛅ Powered by OpenWeather API")

        else:
            st.error(f"❌ Error: {data.get('message', 'Unknown error')}")

    except Exception as e:
        st.error(f"🚨 Exception: {e}")
