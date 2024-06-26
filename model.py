import os

import openai
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

class Model:
    def __init__(self, api_key=None):
        self.tclient = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.gclient = Groq(api_key=GROQ_API_KEY)

    def transcribe(self, filename):
        audio = open(filename, "rb")
        transcription = self.tclient.audio.transcriptions.create(
            model="whisper-1",
            file=(audio),
        ).text
        return transcription

    def generate(self, ins):
        lab = os.getenv("LAB")
        topics = os.getenv("TOPICS")
        prompt = (
            f"This question is based on the course - {lab}. This course contains topics like {topics}. Ensure that your answer is related and relevant to the lab and topic given.Imagine you're explaining this to a college professor in a straightforward way. List any relevant mathematical formulas, graphs or principles used in the experiment. \n"
            + ins
        )

        chat_completion = self.gclient.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gemma-7b-it",
        )

        text = chat_completion.choices[0].message.content
        return text
