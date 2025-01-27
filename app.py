import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from a .env file
load_dotenv() 

# Configure the Google Generative AI API with the API key from the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# prompt for summarization
prompt = """You are tasked with summarizing YouTube video transcripts.
Condense the transcript into key points, ensuring the summary is concise,
clear, and within 300 words. Provide the summary of the following text: """

# Function to extract transcript details from a YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        # Extract the video ID from the YouTube URL
        video_id = youtube_video_url.split("=")[1]  # Assuming the format is 'https://www.youtube.com/watch?v=VIDEO_ID'

        # Retrieve the transcript data as a list of dictionaries
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

        # Concatenate the text from the transcript into a single string
        transcript = ""
        for entry in transcript_data:
            transcript += " " + entry["text"]

        return transcript

    except Exception as e:
        # Raise an exception if there is an issue with retrieving the transcript
        raise e

# Function to generate a summary using Google Gemini Pro
# Accepts the transcript text and a prompt as inputs
def generate_gemini_content(transcript_text, prompt):
    # Use the Gemini Pro generative model
    model = genai.GenerativeModel("gemini-pro")
    
    # Generate content based on the given prompt and transcript
    response = model.generate_content(prompt + transcript_text)
    
    return response.text

# Streamlit App Title
st.title("YouTube Transcript to Insightful Notes Generator")

# Input field for the YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

# Display the thumbnail of the video if a link is provided
if youtube_link:
    video_id = youtube_link.split("=")[1]  # Extract video ID
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)  # Display thumbnail

# Button to trigger the summarization process
if st.button("Generate Detailed Notes"):
    # Extract the transcript text from the video link
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Generate summaries using both prompts
        summary = generate_gemini_content(transcript_text, prompt)
        alternative_summary = generate_gemini_content(transcript_text, prompt)

        # Display the primary summary
        st.markdown("## Detailed Notes:")
        st.write(summary)

        # Display the alternative summary
        st.markdown("## Alternative Notes:")
        st.write(alternative_summary)
