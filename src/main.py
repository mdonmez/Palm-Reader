import streamlit as st
from PIL import Image
from litellm import completion
import instructor
import io
from pydantic import BaseModel, Field
from pathlib import Path
import base64
import logging

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 20 * 1024 * 1024

SUPPORTED_FORMATS = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png"}


class PalmResult(BaseModel):
    suitable: bool = Field(
        ..., description="Indicates if the image is suitable for palm reading"
    )
    english: str | None = Field(
        None, description="The palm reading explanation in English"
    )
    turkish: str | None = Field(
        None, description="The palm reading explanation in Turkish"
    )


@st.cache_resource
def get_client():
    return instructor.from_litellm(completion, mode=instructor.Mode.JSON)


@st.cache_data(show_spinner=False)
def load_prompt() -> str:
    return (Path(__file__).parent / "llm_instruction.md").read_text()


def load_secrets():
    try:
        api_key = st.secrets["LLM_API_KEY"]
        model = st.secrets["LLM_MODEL"]
        if not api_key or not model:
            raise ValueError("LLM_API_KEY and LLM_MODEL must not be empty")
        return api_key, model
    except KeyError as e:
        st.error(f"Missing secret: {e}. Check your .streamlit/secrets.toml file.")
        st.stop()


def detect_image_format(image_data: bytes) -> str:
    try:
        img = Image.open(io.BytesIO(image_data))
        fmt = img.format.lower() if img.format else "jpeg"
        return SUPPORTED_FORMATS.get(fmt, "jpeg")
    except Exception:
        return "jpeg"


def display_image(image_data: bytes):
    st.image(image_data, width=200)


def validate_file_size(image_data: bytes):
    if len(image_data) > MAX_FILE_SIZE:
        st.error(
            f"File exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB. Please upload a smaller image."
        )
        st.stop()


def get_reading(image_data: bytes, api_key: str, model: str, prompt: str) -> PalmResult:
    base64_image = base64.b64encode(image_data).decode("utf-8")
    fmt = detect_image_format(image_data)
    client = get_client()

    return client.chat.completions.create(
        api_key=api_key,
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{fmt};base64,{base64_image}",
                        },
                    },
                ],
            },
        ],
        response_model=PalmResult,
    )


def main():
    st.set_page_config(page_title="AI Palm Reader", page_icon="🔮")
    st.title("🔮 AI Palm Reader")
    st.caption(
        "Upload or capture a photo of your palm and receive a mystical AI reading ✋"
    )

    api_key, model = load_secrets()
    prompt = load_prompt()

    input_mode = st.radio("Choose input method", ["📸 Use Camera", "📁 Upload Image"])

    image_data: bytes | None = None

    match input_mode:
        case "📸 Use Camera":
            camera_image = st.camera_input("Take a picture of your palm")
            if camera_image:
                image_data = camera_image.getvalue()
                validate_file_size(image_data)
                display_image(image_data)

        case "📁 Upload Image":
            uploaded_file = st.file_uploader(
                "Upload an image of your palm", type=["jpg", "jpeg", "png"]
            )
            if uploaded_file:
                image_data = uploaded_file.read()
                validate_file_size(image_data)
                display_image(image_data)

    if image_data:
        with st.spinner("🔮 Reading your palm..."):
            try:
                response = get_reading(image_data, api_key, model, prompt)

                if response.suitable:
                    st.markdown("## 🧙‍♂️ Your Palm Explanation | Fal Açıklamanız")
                    st.markdown("### English Explanation")
                    st.write(response.english)
                    st.markdown("### Türkçe Açıklama")
                    st.write(response.turkish)
                else:
                    st.error(
                        "The AI couldn't detect a clear palm in the image. "
                        "Please make sure your hand is clearly visible with good lighting and try again."
                    )

            except Exception:
                logger.exception("Palm reading failed")
                st.error(
                    "An unexpected error occurred while generating your palm reading. "
                    "Please try again."
                )


if __name__ == "__main__":
    main()
