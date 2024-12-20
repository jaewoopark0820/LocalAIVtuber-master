from socket import setdefaulttimeout
import requests
from tqdm import tqdm
from pluginInterface import LLMPluginInterface
import gradio as gr
from llama_cpp import Llama
import os
import json#20241031_kpopmodder
import threading#20241102_kpopmodder
from threading import Thread#20241102_kpopmodder
import time#20241102_kpopmodder


class Korean_Chat(LLMPluginInterface):
    context_length = 32768
    temperature = 0.9
#    memory_file = "memory.json"  #20241031_kpopmodder_Memory file path
#    memory_file = os.path.join(".", "plugins", "Korean_Chat", "memory.json")#20241031_kpopmodder_Memory file path

    # def __init__(self):
    #     self.memory = self.load_memory()  #20241101_kpopmodder_초기 메모리 로드

    # def load_memory(self):#20241102_kpopmodder
    #     try:
    #         with open(self.memory_file, "r", encoding='utf-8') as file:
    #             return json.load(file)
    #     except FileNotFoundError:
    #         return {}

    # def save_memory(self):#20241102_kpopmodder
    #     with open(self.memory_file, "w", encoding='utf-8') as file:
    #         json.dump(self.memory, file, indent=4)


    def init(self):
        # Directory where the module is located
        current_module_directory = os.path.dirname(__file__)
        model_filename = "llama-3-korean-bllossom-8b-q4_k_m.gguf"
        model_directory = os.path.join(current_module_directory, "models")
        model_path = os.path.join(model_directory, model_filename)

        # Check if the model file exists
        if not os.path.exists(model_path):
            # If not, create the models directory if it does not exist
            if not os.path.exists(model_directory):
                os.makedirs(model_directory)

            # URL to download the model
            url = "https://huggingface.co/Brian314/llama-3-Korean-Bllossom-8B-Q4_K_M-GGUF/resolve/main/llama-3-korean-bllossom-8b-q4_k_m.gguf?download=true"
            
             # Download the file with progress
            print(f"Downloading model from {url}...")
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                total_size_in_bytes = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 Kibibyte

                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
                with open(model_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                progress_bar.close()

                if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                    print("ERROR, something went wrong during download")
                else:
                    print("Model downloaded successfully.")
            else:
                print(f"Failed to download the model. Status code: {response.status_code}")
                return

        # Initialize the model
        self.llm = Llama(model_path=model_path, n_ctx=self.context_length, n_gpu_layers=-1, seed=-1)

    # def load_user_memory(self, user_id):#20241101_kpopmodder
    #     return self.memory.get(user_id, [])

    # def save_user_memory(self, user_id, messages):#20241101_kpopmodder
    #     self.memory[user_id] = messages

    def create_ui(self):
        with gr.Accordion("Korean Chat LLM settings", open=False):
            with gr.Row():
                self.temperature_slider = gr.Slider(minimum=0, maximum=1, value=self.temperature,label="temperature")
                
                self.temperature_slider.change(fn=self.update_temperature,inputs=self.temperature_slider)

    def update_temperature(self, t):
        self.temperature = t

    def predict(self, message, history, system_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        for entry in history:
            user, ai = entry
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": ai})

        messages.append({"role": "user", "content": message})

        # Function to count the number of tokens in the messages
        def count_tokens(msg_list):
            result = sum(len(self.llm.tokenize(
                str.encode(msg['content']))) for msg in msg_list)
            print(f"Tokens_in_context = {result}")
            return result

        # Trim oldest messages if context length in tokens is exceeded
        while count_tokens(messages) > self.context_length and len(messages) > 1:
            # Remove the oldest message (after the system prompt)
            messages.pop(1)

        print(f"message: {message}")
        print(f"history: {history}")
        print(f"messages: {messages}")
        print(f"---------------------------------")
        print(f"Generating with temperature {self.temperature}")

        completion_chunks = self.llm.create_chat_completion(
            messages, stream=True, temperature=self.temperature)
        output = ""
        for completion_chunk in completion_chunks:
            try:
                text = completion_chunk['choices'][0]['delta']['content']
                output += text
                yield output
            except:
                pass


    # def predict(self, message, history, system_prompt, user_id="default_user"):#20241031_kpopmodder
    #     #20241031_kpopmodder Load past conversation history for this user
    #     messages = self.load_user_memory(user_id)#20241101_kpopmodder

    #     #20241031_kpopmodder Add the system prompt
    #     if not messages:
    #         messages.append({"role": "system", "content": system_prompt})

    #     #20241031_kpopmodder Add user and AI messages from history
    #     for user_msg, ai_msg in history:
    #         messages.append({"role": "user", "content": user_msg})
    #         messages.append({"role": "assistant", "content": ai_msg})

    #     #20241031_kpopmodder Add the new user message
    #     messages.append({"role": "user", "content": message})

    #     #20241031_kpopmodder Count tokens to ensure context length is not exceeded
    #     def count_tokens(msg_list):
    #         result = sum(len(self.llm.tokenize(str.encode(msg['content']))) for msg in msg_list)
    #         print(f"Tokens_in_context = {result}")
    #         return result

    #     #20241031_kpopmodder Trim oldest messages if context length in tokens is exceeded
    #     while count_tokens(messages) > self.context_length and len(messages) > 1:
    #         messages.pop(1)  # Remove the oldest message after the system prompt

    #     print(f"message: {message}")
    #     print(f"history: {history}")
    #     print(f"messages: {messages}")
    #     print(f"---------------------------------")
    #     print(f"Generating with temperature {self.temperature}")

    #     #20241031_kpopmodder Generate response
    #     completion_chunks = self.llm.create_chat_completion(
    #         messages, stream=True, temperature=self.temperature
    #     )
    #     output = ""
    #     for completion_chunk in completion_chunks:
    #         try:
    #             text = completion_chunk['choices'][0]['delta']['content']
    #             output += text
    #             yield output
    #         except:
    #             pass

    #     #20241031_kpopmodder Save updated conversation history
    #     messages.append({"role": "assistant", "content": output})
    #     self.save_user_memory(user_id, messages)#20241101_kpopmodder
    #     self.save_memory()  #20241101_kpopmodder# 모든 사용자 메모리를 파일에 저장