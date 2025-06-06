import streamlit as st
import random
import pandas as pd

# -------------------------------
# Setup
st.set_page_config(page_title="Speech Intelligibility Test", layout="centered")
st.title("Speech Intelligibility Assessment")

# Full word and sentence lists
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

# Randomly select 15 of each
if 'word_items' not in st.session_state:
    st.session_state.word_items = random.sample(words, 15)
    st.session_state.sentence_items = random.sample(sentences, 15)
    st.session_state.responses = []
    st.session_state.index = 0

# Function to reset
def restart():
    st.session_state.word_items = random.sample(words, 15)
    st.session_state.sentence_items = random.sample(sentences, 15)
    st.session_state.responses = []
    st.session_state.index = 0

# Combine words and sentences for display
all_items = st.session_state.word_items + st.session_state.sentence_items
total_items = len(all_items)

# Display one item at a time
if st.session_state.index < total_items:
    current_item = all_items[st.session_state.index]
    st.header(f"Item {st.session_state.index + 1} of {total_items}")
    st.subheader(current_item)

    transcription = st.text_input("Transcription:")
    correct = st.selectbox("Was it correct?", ["", "Yes", "No"])

    if st.button("Next"):
        if correct != "":
            st.session_state.responses.append({
                "Item": current_item,
                "Transcription": transcription,
                "Correct": correct
            })
            st.session_state.index += 1
        else:
            st.warning("Please mark the item as correct or incorrect.")
else:
    st.success("Test complete!")
    df = pd.DataFrame(st.session_state.responses)
    correct_count = df[df['Correct'] == "Yes"].shape[0]
    accuracy = round((correct_count / total_items) * 100, 2)
    st.subheader(f"Total Score: {correct_count}/{total_items} ({accuracy}%)")
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Results", data=csv, file_name="intelligibility_results.csv", mime="text/csv")

    # Restart button
    if st.button("Start New Test"):
        restart()
