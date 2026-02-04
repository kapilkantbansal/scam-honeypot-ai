import streamlit as st
import requests

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Scam Honeypot AI",
    layout="centered"
)

st.title("🕵️ Scam Honeypot AI")
st.caption("AI-powered system to trap scammers and extract evidence")

# -----------------------------
# Input
# -----------------------------
user_input = st.text_area(
    "Enter scam message or call transcript",
    height=120
)

# -----------------------------
# Button action
# -----------------------------
if st.button("Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",   # 🔴 change if your endpoint name is different
                json={"message": user_input},
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)
            else:
                data = response.json()

                # -----------------------------
                # Honeypot reply
                # -----------------------------
                st.subheader("🗣 Honeypot Reply")
                st.write(data.get("reply", "No reply returned"))

                # -----------------------------
                # Extracted evidence
                # -----------------------------
                extracted = data.get("extracted")

                if extracted:
                    st.subheader("🔍 Extracted Evidence")
                    st.json(extracted)
                else:
                    st.info("No structured evidence extracted")

                # -----------------------------
                # Optional: raw debug view
                # -----------------------------
                with st.expander("🔧 Raw Backend Response"):
                    st.json(data)

        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Start FastAPI first.")
        except Exception as e:
            st.error("Unexpected error")
            st.exception(e)
