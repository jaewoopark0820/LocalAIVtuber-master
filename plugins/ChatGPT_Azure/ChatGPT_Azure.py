from operator import truediv
from re import T
import sys
from jinja2.utils import F
import requests
from pluginInterface import LLMPluginInterface
import gradio as gr
from openai import AzureOpenAI
import os
from configManager import config_manager
from openai import AzureOpenAI#20241102_kpopmodder
from azure.cognitiveservices.vision.computervision import ComputerVisionClient#20241102_kpopmodder
from msrest.authentication import CognitiveServicesCredentials#20241102_kpopmodder
import time#20241102_kpopmodder
import os#20241102_kpopmodder
import cv2#20241102_kpopmodder
import threading#20241102_kpopmodder
from threading import Thread#20241102_kpopmodder
from liveTextbox import LiveTextbox#20241102_kpopmodder
import mss#20241102_kpopmodder
from PIL import Image#20241102_kpopmodder


class ChatGPT_Azure(LLMPluginInterface):
    context_length = 4096
    temperature = 0.9

    plugin_config = config_manager.load_section("ChatGPT_Azure")
    api_key = plugin_config.get("api_key")
    api_version = plugin_config.get("api_version")
    azure_endpoint = plugin_config.get("azure_endpoint")
    model_name = plugin_config.get("model_name")

    # #20241102_kpopmodder# Computer Vision API 설정
    # plugin_config_computer_vision = config_manager.load_section("Computer_Vision")
    # vision_api_key = plugin_config_computer_vision.get("vision_api_key")#20241102_kpopmodder
    # vision_endpoint = plugin_config_computer_vision.get("vision_endpoint")#20241102_kpopmodder
    # isCaptureScreen = False#20241102_kpopmodder
    # isCaptureScreenThread = False#20241102_kpopmodder

    def init(self):
        self.client = None
        # self.liveTextbox = LiveTextbox()#20241102_kpopmodder

        # self.init_vision_client()#20241102_kpopmodder

    def create_ui(self):
        with gr.Accordion("ChatGPT_Azure settings", open=False):
            with gr.Row():
                self.api_key_Input = gr.Textbox(label="API key", value=self.api_key)
                self.api_key_Input.change(fn=self.update_api_key,inputs=self.api_key_Input)

                self.api_version_Input = gr.Textbox(label="API version", value=self.api_version)
                self.api_version_Input.change(fn=self.update_api_version,inputs=self.api_version_Input)

                self.azure_endpoint_Input = gr.Textbox(label="azure_endpoint", value=self.azure_endpoint)
                self.azure_endpoint_Input.change(fn=self.update_azure_endpoint,inputs=self.azure_endpoint_Input)

                self.model_name_Input = gr.Textbox(label="model_name", value=self.model_name)
                self.model_name_Input.change(fn=self.update_model_name,inputs=self.model_name_Input)

            # with gr.Row():#20241102_kpopmodder
            #     self.vision_api_key_Input = gr.Textbox(label="Computer Vision API key", value=self.vision_api_key)
            #     self.vision_api_key_Input.change(fn=self.update_vision_api_key,inputs=self.vision_api_key_Input)

            #     self.vision_endpoint_Input = gr.Textbox(label="Computer Vision endpoint", value=self.vision_endpoint)
            #     self.vision_endpoint_Input.change(fn=self.update_vision_endpoint,inputs=self.vision_endpoint_Input)

            #     self.start_ai_capture_screen_button = gr.Button(
            #         "Start AI Capture Screen", self.start_ai_capture_screen)
            #     self.stop_ai_capture_screen_button = gr.Button(
            #         "Stop AI Capture Screen", self.stop_ai_capture_screen)

        # self.start_ai_capture_screen_button.click(self.start_ai_capture_screen)
        # self.stop_ai_capture_screen_button.click(self.stop_ai_capture_screen)

    def update_api_key(self, value):
        self.api_key = value
        config_manager.save_config("ChatGPT_Azure", "api_key", value)

    def update_api_version(self, value):
        self.api_version = value
        config_manager.save_config("ChatGPT_Azure", "api_version", value)
    
    def update_azure_endpoint(self, value):
        self.azure_endpoint = value
        config_manager.save_config("ChatGPT_Azure", "azure_endpoint", value)

    def update_model_name(self, value):
        self.model_name = value
        config_manager.save_config("ChatGPT_Azure", "model_name", value)

    def predict(self, message, history, system_prompt):
        if self.client is None:
            self.client = AzureOpenAI(
                api_key=self.api_key,  
                api_version=self.api_version,
                azure_endpoint=self.azure_endpoint
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        for entry in history:
            user, ai = entry
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": ai})
        
        messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,  
            top_p=1.0,
            stream=True
        )

        output = ""
        for chunk in response:
            try:
                print(chunk.choices[0].delta.content  or "", end="")
                output += chunk.choices[0].delta.content
                yield output
            except Exception as e:
                print(f"Error: {e}")

    # def update_vision_api_key(self, value):#20241102_kpopmodder
    #     self.vision_api_key = value
    #     config_manager.save_config("Computer_Vision", "vision_api_key", value)

    # def update_vision_endpoint(self, value):#20241102_kpopmodder
    #     self.vision_endpoint = value
    #     config_manager.save_config("Computer_Vision", "vision_endpoint", value)

    # def start_ai_capture_screen(self):#20241102_kpopmodder
    #     gr.Info("starting AI Capture Screen...")
    #     self.isCaptureScreen = True
    #     self.liveTextbox.print("Started AI Capture Screen...")

    #     self.init_vision_client()

    #     if self.isCaptureScreenThread == False:
    #         threading.Thread(target=self.ai_capture_screen_thread).start()       

    # def stop_ai_capture_screen(self):#20241102_kpopmodder
    #     gr.Info("stoping AI Capture Screen...")
    #     self.isCaptureScreen = False
    #     self.liveTextbox.print("Stoped AI Capture Screen...")

    # def init_vision_client(self):#20241102_kpopmodder
    #     if self.vision_api_key and self.vision_endpoint:#20241102_kpopmodder
    #         self.vision_client = ComputerVisionClient(
    #             self.vision_endpoint,
    #             CognitiveServicesCredentials(self.vision_api_key)
            # )

    # def capture_and_analyze_screen(self):#20241102_kpopmodder
    #     #20241102_kpopmodder# 화면을 캡처하여 이미지를 저장
    #     cap = cv2.VideoCapture(0)
    #     ret, frame = cap.read()
    #     if not ret:
    #         print("Error: Unable to capture screen.")
    #         cap.release()
    #         return None

    #     #20241102_kpopmodder# 이미지 파일로 저장
    #     image_path = "captured_image.jpg"
    #     cv2.imwrite(image_path, frame)
    #     cap.release()
        
    #     #20241102_kpopmodder# 이미지 분석 수행
    #     with open(image_path, "rb") as image_stream:
    #         analysis = self.vision_client.analyze_image_in_stream(
    #             image_stream, visual_features=["Description", "Tags", "Objects"]
    #         )
        
    #     description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
    #     tags = [tag.name for tag in analysis.tags]
    #     objects = [obj.object_property for obj in analysis.objects]
        
    #     return {
    #         "description": description,
    #         "tags": tags,
    #         "objects": objects
    #     }

    # def ai_capture_screen_thread(self):#20241102_kpopmodder
    #     self.isCaptureScreenThread = True
    #     while True:
    #         #print("ai_capture_screen_thread")
    #         if self.isCaptureScreen == True:
    #             if self.client is None:
    #                 self.client = AzureOpenAI(
    #                     api_key=self.api_key,
    #                     api_version=self.api_version,
    #                     azure_endpoint=self.azure_endpoint
    #                 )

    #             # 실시간 이미지 캡처 및 분석
    #             image_analysis = self.capture_and_analyze_screen()
    #             if not image_analysis:
    #                 print("Image analysis failed.")
    #                 return

    #             messages = [
    #                 {"role": "system", "content": "Picture"},
    #                 {"role": "system", "content": f"Image Description: {image_analysis['description']}"},
    #                 {"role": "system", "content": f"Image Tags: {', '.join(image_analysis['tags'])}"},
    #                 {"role": "system", "content": f"Image Objects: {', '.join(image_analysis['objects'])}"}
    #             ]

    #             print(messages)
    #             #print("ai_capture_screen_thread")

    #             response = self.client.chat.completions.create(
    #                 model=self.model_name,
    #                 messages=messages,
    #                 temperature=self.temperature,
    #                 top_p=1.0,
    #                 stream=True
    #             )

    #             output = ""
    #             for chunk in response:
    #                 try:
    #                     print(chunk.choices[0].delta.content or "", end="")
    #                     output += chunk.choices[0].delta.content
    #                     #yield output
    #                 except Exception as e:
    #                     print(f"Error: {e}")

    #             print("\nResponse:", output)

    #         time.sleep(0.1)

    # def capture_screen(self):#20241102_kpopmodder
    #     # 바탕화면 전체 캡처
    #     with mss.mss() as sct:
    #         monitor = sct.monitors[1]  # 첫 번째 모니터 전체
    #         screenshot = sct.grab(monitor)
    #         img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    #         img.save("screenshot.png")  # 이미지를 파일로 저장
    #         return "screenshot.png"

    # def analyze_screen(self, image_path):#20241102_kpopmodder
    #     # 이미지 분석
    #     with open(image_path, "rb") as image_stream:
    #         analysis = self.vision_client.analyze_image_in_stream(
    #             image_stream,
    #             visual_features=["Description", "Tags", "Objects"]
    #         )
        
    #     description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
    #     tags = [tag.name for tag in analysis.tags]
    #     objects = [obj.object_property for obj in analysis.objects]
        
    #     return {
    #         "description": description,
    #         "tags": tags,
    #         "objects": objects
    #     }

    # def ai_capture_screen_thread(self):#20241102_kpopmodder
    #     while True:
    #         self.isCaptureScreenThread == True

    #         if self.isCaptureScreen == True:
    #             # 화면 캡처 및 분석
    #             image_path = self.capture_screen()
    #             image_analysis = self.analyze_screen(image_path)
    #             if not image_analysis:
    #                 print("Image analysis failed.")
    #                 return

    #             # Azure OpenAI와 통합
    #             messages = [
    #                 {"role": "system", "content": "Picture"},
    #                 {"role": "system", "content": f"Image Description: {image_analysis['description']}"},
    #                 {"role": "system", "content": f"Image Tags: {', '.join(image_analysis['tags'])}"},
    #                 {"role": "system", "content": f"Image Objects: {', '.join(image_analysis['objects'])}"}
    #             ]

    #             print(messages)

    #             if self.client is None:
    #                 self.client = AzureOpenAI(
    #                     api_key=self.api_key,
    #                     api_version=self.api_version,
    #                     azure_endpoint=self.azure_endpoint
    #                 )

    #             response = self.client.chat.completions.create(
    #                 model=self.model_name,
    #                 messages=messages,
    #                 temperature=self.temperature,
    #                 top_p=1.0,
    #                 stream=True
    #             )

    #             output = ""
    #             for chunk in response:
    #                 try:
    #                     print(chunk.choices[0].delta.content or "", end="")
    #                     output += chunk.choices[0].delta.content
    #                 except Exception as e:
    #                     print(f"Error: {e}")

    #             print("\nResponse:", output)

    #         time.sleep(3)  # 대기 시간(초) 후 다시 캡처 및 분석
