import os
import time

import openai
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class ChatGPT:
    def __init__(self, api_key=None):
        api_key = "sk-proj-DdWGNSE2trdNX50otbUAT3BlbkFJr3UMbl7EfRQezGWcNTgH"
        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, prompt):
        try:
            response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}], temperature=1, max_tokens=2048, top_p=0.95, frequency_penalty=0, presence_penalty=0, stop=None)

            res = response.model_dump(mode="python")["choices"][0]["message"]["content"]
            return res
        except openai.RateLimitError:
            return self.get_completion(prompt)
        except requests.exceptions.Timeout:
            # Handle the timeout error here
            print("The OpenAI API request timed out. Please try again later.")
            return None
        except openai.BadRequestError as e:
            # Handle the invalid request error here
            print(f"The OpenAI API request was invalid: {e}")
            return None
        except openai.APIError as e:
            print(f"The OpenAI API returned an error: {e}")
            return None

    def call_api(self, ins):
        success = False
        retry_count = 5
        ans = ""
        while not success and retry_count >= 0:
            retry_count -= 1
            try:
                ans = self.get_completion(ins)
                success = True
            except:
                time.sleep(5)
                print("retry for sample:", ins)
        return ans

    def transcribe(self, filename):
        audio = open(filename, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=(audio),
        ).text
        return transcription


class Gemma:
    def __init__(self):
        self.client = Groq(api_key="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")

    def call_api(self, ins):
        lab = os.getenv("LAB")
        topics = os.getenv("TOPICS")
        prompt = f"This question is based on the course - {lab}. This course contains topics like {topics}. Ensure that your answer is related and relevant to the lab and topic given. \n" + ins

        chat_completion = self.client.chat.completions.create(
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
