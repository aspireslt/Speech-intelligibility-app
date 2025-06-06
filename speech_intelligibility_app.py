import streamlit as st
import random
import pandas as pd

# -------------------------------
# Setup
st.set_page_config(page_title="Speech Intelligibility Test", layout="centered")
st.title("Speech Intelligibility Assessment")

# Word and sentence pools
words = [
    "cat", "dog", "fish", "shoe", "ball", "sun", "car", "book", "chair", "milk",
    "house", "tree", "phone", "watch", "glass", "train", "plane", "spoon", "clock", "door",
    "apple", "banana", "grape", "orange", "bread", "cheese", "plate", "fork", "cup", "pencil",
    "school", "bed", "lamp", "hat", "coat", "sock", "kite", "ring", "star", "cloud",
    "rain", "snow", "wind", "leaf", "flower", "river", "mountain", "beach", "island", "baby"
]

sentences = [
    "The cat is on the bed.", "She likes to eat apples.", "He runs fast every morning.",
    "The boy threw the ball.", "They went to the beach.", "The bird is in the tree.",
    "He opened the door slowly.", "She sings very well.", "I have a red kite.",
    "We saw a big train.", "The dog barked loudly.", "She wore a yellow dress.",
    "He reads a book daily.", "The sun is very bright.", "They jumped in the pool.",
    "My friend has a bike.", "The flower is pink.", "She found a gold ring.",
    "He drew a star on paper.", "We climbed the tall mountain."
]

# Random selection and session state initialization
if 'word_items' not in st.session_state:
    st.session_state.word_items = random.sample(words, 15)
    st.session_state.sentence_items = random.sample(sentences, 15)
    st.session_state.index = 0
    st.session_state.complete = False

# Combine test items
all_items = st.session_state.word_items + st.session_state.sentence_items
total_items = len(all_items)

# Patient-facing phase
if not st.session_state.complete:
    if st.session_state.index < total_items:
        current_item = all_items[st.session_state.index]
        st.markdown(
            f"<h1 style='text-align: center; font-size: 48px;'>{current_item}</h1>",
            unsafe_allow_html=True
        )
        if st.button("Next"):
            st.session_state.index += 1
    else:
        st.session_state.complete = True
        st.experimental_rerun()

# SLT input phase
if st.session_state.complete:
    st.subheader("Clinician Scoring Panel")
    responses = []

    with st.form("scoring_form"):
        for i, item in enumerate(all_items):
            st.markdown(f"**Item {i+1}: {item}**")
            col1, col2 = st.columns([1, 2])
            with col1:
                understood = st.radio(f"Was it understood?", ["Yes", "No"], key=f"understood_{i}")
            with col2:
                notes = ""
                if understood == "No":
                    notes = st.text_input("Enter notes/transcription:", key=f"notes_{i}")
            responses.append({
                "Item": item,
                "Understood": understood,
                "Notes": notes if understood == "No" else ""
            })
        submitted = st.form_submit_button("Calculate Score")

    if submitted:
        df = pd.DataFrame(responses)
        understood_count = df[df['Understood'] == "Yes"].shape[0]
        accuracy = round((understood_count / total_items) * 100, 2)
        st.success(f"Score: {understood_count}/{total_items} = {accuracy}% intelligibility")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", data=csv, file_name="manual_scoring_results.csv", mime="text/csv")
