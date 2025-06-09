import streamlit as st
from docx import Document
import json
import os

st.title("Transition Triplet Extractor")

uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])
outputs = st.multiselect("Select output files to generate:", [
    "fewshot_examples.json",
    "fewshots_rejected.txt",
    "transitions_only.txt",
    "transitions_only_rejected.txt",
    "fewshot_examples.jsonl",
    "fewshots-fineTuning_rejected.txt"
])

if st.button("Generate Outputs"):
    if uploaded_file is None:
        st.error("Please upload a .docx file.")
    else:
        document = Document(uploaded_file)
        paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        transition_candidates = paragraphs[-3:]  # naive fallback logic
        narrative = paragraphs[-4]  # example only

        examples = []
        rejected = []

        for t in transition_candidates:
            if t in narrative:
                parts = narrative.split(t)
                if len(parts) >= 2:
                    example = {
                        "paragraph_a": parts[0].strip(),
                        "transition": t,
                        "paragraph_b": parts[1].strip()
                    }
                    examples.append(example)

        # Save selected outputs
        if "fewshot_examples.json" in outputs:
            with open("fewshot_examples.json", "w") as f:
                json.dump(examples, f, indent=2)

        if "transitions_only.txt" in outputs:
            with open("transitions_only.txt", "w") as f:
                for e in examples:
                    f.write(e["transition"] + "\n")

        st.success(f"Generated {len(examples)} few-shot examples!")
        st.write("Files saved in workspace directory.")
