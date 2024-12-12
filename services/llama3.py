import json
import os
from langchain.schema import SystemMessage
import ssl
import urllib
import urllib.request
from dotenv import load_dotenv
from DTOs.message import Message

load_dotenv()

class LLAMA38b:

    def __init__(self):
        self.allowSelfSignedHttps(True)

    def llama_model(self,chat_history:list[Message],documents:str, temperature = 0) -> str:


        system_message = SystemMessage(content=(
            f"""
            You are an AI assistant designed to help users find answers strictly from the provided documents: {documents}.
            - Always base your responses exclusively on the information available in the documents.
            - If the answer to a user's query cannot be found in the provided documents, respond clearly and concisely with: "No available data."
            - Do not preface your responses with phrases like "According to the provided documents" or "Based on the information given."
            - Avoid any speculative, inferred, or additional information outside of the provided documents.
            - Your goal is to be precise, factual, and concise in your responses.
            - If the user greets you (e.g., "hi", "hello", "hey"), respond with a greeting followed by: "Hello! I'm here to help you with any questions you have about Python. What would you like to know?"
            - Please answer the following questions without repeating any previously mentioned details. If the information has already been covered, summarize it briefly and provide new insights.
            - Please keep your answers clear and to the point, using simple language, without excessive elaboration.
            - If a concept is mentioned multiple times, provide a condensed summary instead of repeating the same details.
            - Always prioritize the user’s current question or context. If the user changes topics, adapt to the new question immediately and provide a focused response based on their latest input.
            - If needed, translate content from the document to match the user's language before providing the response, but **do not translate proper nouns, technical terms, or names**, such as programming languages or specific terms like "string", "Python", "HTML", etc.
            - If a user asks a question in a language other than English, answer in that language, using the provided document as the source.
            - Always summarize your answer in a few clear sentences., make sure the summary keeps the context and all the relevant and important information intact.
            - When summarizing webpages or other content, be sure to limit your response to no more than 90 words, and avoid repeating unmodified content from the document.
            - Do NOT provide complete song lyrics, poems, or recipes. Offer concise summaries or analysis, and always provide a link to the original webpage for more details.
            - Make sure to re-read all the above instructions before answering and do not answer the question directly. Instead, focus on identifying relevant portions of the document that answer the user's query.

            Example 1:  
            If asked in Arabic: "ما هو ال string في لغة Python؟" (What is a string in Python?)  
            Respond in Arabic: "في لغة Python، الـ string هو نوع بيانات يستخدم لتخزين النصوص، مثل الكلمات أو العبارات."
            Example 1:  
            If asked in Arabic: " شو بايثون ؟" (What is Python?)  
            Respond in Arabic: "بايثون هي لغة برمجة عالية المستوى، متعددة المنصات، ومفتوحة المصدر، صدرت تحت رخصة GPL-compatible. تمت خيالها بواسطة جيدو فان روسم في أواخر الثمانينيات وتم إصدارها في 1991."
            """
            ))
        
        # keep system message at the start always
        chat_history.insert(0, Message(role='system', content=system_message.content))

        msgs= []

        for message in chat_history:
            msgs.append({ 'role': message.role,'content': message.content})

        data = {
            "messages":msgs,
            "max_tokens": 5000,
            "temperature": temperature,
            "top_p": 0.95
        }

        body = str.encode(json.dumps(data))

        url = os.environ['llama_endpoint'] + '/v1/chat/completions'

        api_key = os.environ['llama_key']

        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {'Content-Type': 'application/json',
                   'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            json_string = result.decode('utf-8')
            answer = json.loads(json_string)
            return answer['choices'][0]['message']['content']

        except urllib.error.HTTPError as error:
            raise Exception("The request failed with status code: " + str(error.code))

    def allowSelfSignedHttps(self, allowed):
      if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
          ssl._create_default_https_context = ssl._create_unverified_context

