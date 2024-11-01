import json
import subprocess
import threading
from threading import Thread
import time
import zipfile
import gradio as gr
import requests
from tqdm import tqdm
import websocket
from pluginInterface import VtuberPluginInterface
import os
import random
from liveTextbox import LiveTextbox


class VtubeStudioSmileDefault(VtuberPluginInterface):#20241101_kpopmodder
    isAuthenticated = False
    token = ""
    current_module_directory = os.path.dirname(__file__)
    token_path = os.path.join(".", "plugins", "VtubeStudio", "token.txt")
    smile_value = 1
    stop_smile_value = 0
    smile = False

    def init(self):
        self.liveTextbox = LiveTextbox()
        self.ws = None

    def create_ui(self):
        with gr.Accordion("Vtube Studio Smile Default",open=False):
            with gr.Row():
                self.start_smile_button = gr.Button(
                    "Start Smile", self.start_smile)
                self.stop_smile_button = gr.Button(
                    "Stop Smile", self.stop_smile)
            # with gr.Accordion("Console"):
            #     self.liveTextbox.create_ui()

        self.start_smile_button.click(self.start_smile)
        self.stop_smile_button.click(self.stop_smile)

    def start_smile(self):
        if not os.path.exists(self.token_path) and self.isAuthenticated == False:
            gr.Info("Please Authenticate...")
            self.liveTextbox.print("Please Authenticate...")
            return

        if os.path.exists(self.token_path) and self.isAuthenticated == False:
            gr.Info("starting smiling...")
            self.smile = True
            self.authenticate()
            self.liveTextbox.print("Started smiling...")
            return

        if os.path.exists(self.token_path) and self.isAuthenticated == True:
            gr.Info("starting smiling...")
            self.smile = True
 #           self.start_smile_request()
            self.liveTextbox.print("Started smiling...")
            return

    def stop_smile(self):
        gr.Info("Stopping smiling...")
        self.smile = False
        self.stop_smile_request()
        self.liveTextbox.print("Stopped smiling...")

    def smile_thread(self):
        while True:
            
            if self.smile == True:
                #print(self.smile)
                self.start_smile_request()
            time.sleep(0.1)

    def start_smile_request(self):
        message = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "6",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "mode": "set",
                    "parameterValues": [
                        {
                            "id": "MouthSmile",
                            "value": self.smile_value
                        },
                    ]
                }
            }
        if self.ws is not None:
            self.ws.send(json.dumps(message))

    def stop_smile_request(self):
        message = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "6",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "mode": "set",
                "parameterValues": [
                    {
                        "id": "MouthSmile",
                        "value": self.stop_smile_value
                    },
                ]
            }
        }
        if self.ws is not None:
            self.ws.send(json.dumps(message))

    def authenticate(self):
        if not os.path.exists(self.token_path):
            gr.Info("Aquiring token, please continue in Vtube Studio...")
        else:
            gr.Info("Token Found, attempting to authenticate with token...")
        thread = threading.Thread(target=self.websocket_thread)
        thread.start()

    def getToken(self):
        token_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "123",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "LocalAIVtuberPlugin",
                "pluginDeveloper": "Xiaohei"
            }
        }
        self.ws.send(json.dumps(token_request))

    def on_open(self, ws):
        # Check if the file exists. If not, create an empty file.
        if not os.path.exists(self.token_path):
            with open(self.token_path, 'w') as file:
                file.write('')
            self.getToken()

        else:
            with open(self.token_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.token = content
            self.send_authentication_request()

    def on_message(self, ws, message):
        response = json.loads(message)
        if response['messageType'] == "InjectParameterDataResponse":
            return
        print("Received message:", message)
        if response['messageType'] == "AuthenticationTokenResponse":
            self.token = response['data']['authenticationToken']
            print("Authentication token received:", self.token)
            with open(self.token_path, 'w') as file:
                file.write(self.token)
            self.send_authentication_request()
            return
        if response['messageType'] == "AuthenticationResponse":
            self.token = response['data']['authenticated'] == True
            print(response['data']['reason'])
            self.isAuthenticated = True
            threading.Thread(target=self.smile_thread).start()
            return

    def send_authentication_request(self):
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "234",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "LocalAIVtuberPlugin",
                "pluginDeveloper": "Xiaohei",
                "authenticationToken": self.token
            }
        }

        self.ws.send(json.dumps(auth_request))

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### Connection closed ###")
        print("Failed to connect to vtube studio, if you want vtube studio functionalities, please start vtube studio and enable plugins.")

    def websocket_thread(self):
        self.ws = websocket.WebSocketApp("ws://localhost:8001",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()
