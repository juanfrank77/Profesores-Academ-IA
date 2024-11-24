import os
import streamlit as st
from openai import OpenAI  

client = OpenAI(
    base_url=os.getenv("LLAMA_BASE_URL"),
    api_key=os.getenv("LLAMA_API_KEY"),
)

system_prompt = """
You are a pedagogy expert tasked with helping teachers create effective class plans. 
You will be provided with questions and reference materials (when applicable) to craft a class plan.
Your advice should be practical, evidence-based, and adaptable to various teaching contexts
"""

# Function to generate the class plan
def get_class_plan(answers, uploaded_files):
    
    with st.status("Generating class plan..."):
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-8b-Instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please generate a class plan based using the following information as reference: Class topic: {answers[0]}, Number of students: {answers[1]}, Time available: {answers[2]}, Class level: {class_level}, Modality: {modality}, Purpose: {purpose}, Reference materials: {uploaded_files}"},
            ],
            temperature=0.7
        )

        response = completion.choices[0].message.content

        return response

# Set the page title and icon
st.set_page_config(page_title="Class Planning Chatbot", page_icon="🎓")

# Title and description
st.title("Class Planning Chatbot")
st.write("Welcome teacher! Answer a few questions and I'll help you create a class plan.")

# User input for questions
st.subheader("Please answer the following questions:")
answer_1 = st.text_input("What is the main topic of the class?")
answer_2 = st.text_input("What is the number of students?")
answer_3 = st.text_input("What is the time available for the class? (in minutes)")

# Selection of class options
st.sidebar.header("Select Class Options")
class_level = st.sidebar.selectbox("Class Level", ["Elementary", "Middle School", "High School"])
modality = st.sidebar.selectbox("Modality", ["Online", "In-Person"])
purpose = st.sidebar.selectbox("Class Purpose", ["Intro", "Review", "Evaluation"])

# File upload for reference materials
st.sidebar.header("Upload Reference Materials")
uploaded_files = st.sidebar.file_uploader(
    "Choose documents", type=["txt", "pdf"], accept_multiple_files=True)

# Generate class plan button
if st.button("Generate Class Plan"):
    if not answer_1 or not answer_2 or not answer_3:
        st.error("Please answer all the questions.")
    else:
        # Combine questions into a list
        answers = [answer_1, answer_2, answer_3]

        if uploaded_files:
            # If files are uploaded, pass them to the get_class_plan function
            class_plan = get_class_plan(answers, uploaded_files)
        else:
            # If no files are uploaded, pass an empty string
            class_plan = get_class_plan(answers, "")
        
        # Display the class plan
        st.subheader("Generated Class Plan:")
        st.write(class_plan)

# Footer
st.write("Powered by Llama-3.1")
