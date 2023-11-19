import random

import hydra
import pandas as pd
import requests
import streamlit as st

from annotated_text import annotated_text
from omegaconf import DictConfig


def show_about_page() -> None:
    st.title("About Our Web App")

    st.header("Overview")
    st.write(
        "Hello, fellow learners! Welcome to our exclusive web application, an embodiment of the hard work, insights, and skills acquired from our course on Sustainable and Scalable Machine Learning Project Development. This platform serves as a testament to what can be achieved when the principles of sustainability in machine learning meet the challenges of our digital age. Here, you can see a cutting-edge natural language processing (NLP) model designed to detect cyberbullying on Twitter in real-time."
    )

    st.header("Course Background")
    st.write(
        "Our course delved deep into creating machine learning solutions that are not only efficient for current scenarios but also scalable for future challenges. Through practical sessions, workshops, and hands-on assignments, we journeyed from understanding the intricacies of an NLP problem to framing, solving, and showcasing it via this web application."
    )

    st.header("The Challenge & Our Solution")
    st.write(
        "Cyberbullying is a silent but potent threat in the online universe. To tackle this issue, we trained a classifier with a rich dataset to identify and flag potential instances of cyberbullying on Twitter. Our model, powered by advanced NLP techniques, provides a nuanced understanding of digital communication, differentiating between casual banter and harmful intent."
    )

    st.header("Features of the Web App")
    st.markdown(
        "* Live Detection: Witness the efficiency of our model as it analyses tweets in real-time, fetched straight from Twitter."
    )
    st.markdown("* Test model with your own text")

    st.header("Feedback & Collaboration")
    st.write(
        "We believe in continuous learning and growth. As this platform is exclusively for our course attendees, we highly value your feedback and insights. Your experiences, suggestions, and critiques will help refine our project and lead us to new avenues of exploration. Let's work together to push the boundaries of what we've learned and create even more impactful solutions."
    )
    st.write(
        "Thank you for engaging with our web application. Through collaboration and feedback, we can pave the way for a safer online environment, ensuring that the digital spaces we love remain inclusive and welcoming for all."
    )


@st.cache_data
def read_dataset(dataset_path: str) -> pd.DataFrame:
    return pd.read_parquet(dataset_path)


def get_prediction_from_text(config: DictConfig, text: str) -> int:
    data_processing_response = requests.get(config.data_processing_service_url, params={"text": text})
    cleaned_text = data_processing_response.json()["cleaned_text"]
    model_prediction_response = requests.get(config.model_prediction_service_url, params={"text": cleaned_text})
    prediction = model_prediction_response.json()["is_cyberbullying"]
    return prediction


def display_results(config: DictConfig, text: str) -> None:
    prediction = get_prediction_from_text(config, text)
    gif = random.choice(config.harmless_gifs) if prediction == 0 else random.choice(config.cyberbullying_gifs)
    color = "#5ed938" if prediction == 0 else "#ed0c0c"
    prediction_text = "harmless" if prediction == 0 else "cyberbullying"

    col1, col2 = st.columns(2)
    with col1:
        st.image(gif, use_column_width="auto")
    with col2:
        st.write("Text:")
        st.markdown(
            f"""
```
{text}
```
"""
        )

        annotated_text("Prediction: ", (prediction_text, "", color))


def use_the_model_on_random_samples(config: DictConfig) -> None:
    df = read_dataset(config.dataset_path)
    sample_df = df.sample(n=10)

    texts = sample_df["text"].values.tolist()
    for text in texts:
        display_results(config, text)


def use_the_model_on_your_own_text(config: DictConfig) -> None:
    st.write("Text to input to the model:")
    text = st.text_input("input_text", value="", help="Please enter the text you want to input to the model")

    if text:
        display_results(config, text)


@hydra.main(config_path="./configs", config_name="config")
def build_streamlit_page(config: DictConfig) -> None:
    st.title("Cyberbullying Detection")
    selected_mode = st.sidebar.selectbox(
        "selected_mode",
        ["What is this page about?", "Use the model on random test dataset samples", "Use the model on your own text"],
    )

    if selected_mode == "What is this page about?":
        show_about_page()
    elif selected_mode == "Use the model on random test dataset samples":
        use_the_model_on_random_samples(config)
    else:
        use_the_model_on_your_own_text(config)


if __name__ == "__main__":
    build_streamlit_page()
