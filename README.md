# Local AI Vtuber (A tool for hosting AI vtubers that runs fully locally and offline)

Full demo and setup guide: https://youtu.be/Yl-T3YgePmw?si=n-vaZzClw0Q833E5

- Chatbot, Translation and Text-to-Speech, all completely free and running locally.
- Support voice output in Japanese, English, German, Spanish, French, Russian and more, powered by RVC, silero and voicevox.
- Includes custom finetuned model to avoid generic chatbot responses and breaking character.
- Gradio UI web interface.
- plugin support for easily adding other providers.



<table>
  <tr>
    <td><img src="https://github.com/0Xiaohei0/VtuberChess/assets/24196833/6433bc1f-cdec-423f-b190-b7330497d28e" /></td>
    <td><img src="https://github.com/0Xiaohei0/VtuberChess/assets/24196833/5521eff5-4b36-4b13-9961-f4d7af8daded" /></td>
  </tr>
</table>


## Installation
### Manual setup (Tutorial video: [Full demo and setup guide](https://youtu.be/Yl-T3YgePmw?si=n-vaZzClw0Q833E5))
install python 3.10
https://www.python.org/downloads/release/python-3100/

install CUDA toolkit 12.4
https://developer.nvidia.com/cuda-12-4-0-download-archive

install visual studio and add desktop development with C++ component
https://visualstudio.microsoft.com/downloads/

![Screenshot 2024-10-03 100032](https://github.com/user-attachments/assets/11e56864-00ab-4c2d-931a-d9cc9422b52b)


#### 1. Download the project from [releases](https://github.com/0Xiaohei0/LocalAIVtuber/releases)
#### 2. open command prompt in project folder.
  
#### 3. Create environment
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
  (If you encounter an error that says “cannot be loaded because the execution of scripts is disabled on this system. Open powershell with admin privilage and run ```Set-ExecutionPolicy RemoteSigned```)
  
#### 4. Install packages
  ```
  pip install -r requirements.txt
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  pip install llama-cpp-python

  pip install nltk
  python -m nltk.downloader -d C:\nltk_data all
  ```

#### 5. Start Program
   ```
   python main.py
   ```
    When you see this message, go to http://localhost:7860 to see web UI 
    ```
    Running on local URL:  http://127.0.0.1:7860
    To create a public link, set `share=True` in `launch()`.
    ```

### Notes: 

#### restarting program

To start the program again, run:
  ```
  .\venv\Scripts\activate
   python main.py
   ```
#### run llm on gpu
If you have a decent GPU, You can install the GPU version of llama-cpp-python:
```
$env:CMAKE_ARGS ="-DGGML_CUDA=ON"
 pip install llama-cpp-python --force-reinstall --no-cache-dir --verbose --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/124
```
This can improve latency further.

Just a reminder for someone using Command Prompt instead of Power Shell
Change this
```
$env:CMAKE_ARGS ="-DGGML_CUDA=ON"
```
To this
```
set CMAKE_ARGS=-DGGML_CUDA=ON
```
or it will show error 
```
$env:CMAKE_ARGS ="-DGGML_CUDA=ON"
The filename, directory name, or volume label syntax is incorrect.
```

### One click setup (Outdated and may not work)
1. Download the project from [releases](https://github.com/0Xiaohei0/LocalAIVtuber/releases)
2. Extract and double click run.bat
3. When you see this message, go to http://localhost:7860 to see web UI 
```
Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
```

## TODO (This project is still under development and more features are planned)
- Fetch chat input from streaming platforms (Finished)
- Improve local LLM (Finetuned model avaliable https://huggingface.co/xiaoheiqaq/Aya-7b-gguf)
- Write plugins for cloud providers(Azure tts, elevenlabs, chatgpt, whisper...)
- GPU support (Finished)
- Vtube studio integration (Finished)
- Let AI play games and provide commentary. (can currently play chess and keep talking nobody explode)
- AI singing



## FAQ:

- NameError: name '_in_projection' is not defined

You cannot enable gpt sovits and rvc at the same time, some of their modules have conflict. 

- UnboundLocalError: local variable 'response' referenced before assignment

  If you cloned this repo, you maybe missing model files for gpt-sovits, which will be in the zip folder in the [releases](https://github.com/0Xiaohei0/LocalAIVtuber/releases) section. 
  replace plugins\gpt_sovits\models with the one from the zip.
- To fetch chat from Youtube, copy the youtube_video_id from the stream url like this:
  
 ![image](https://github.com/0Xiaohei0/LocalAIVtuber/assets/24196833/942b9811-46bc-40f9-a7df-7938d0070513)

Then press start fetching chat

![image](https://github.com/0Xiaohei0/LocalAIVtuber/assets/24196833/96b8a971-00e8-4930-a9b4-897b3ddf27bf)


## 한국어 설명:

- 원본 링크(출처): https://github.com/0Xiaohei0/LocalAIVtuber

- window power shell 관리자 권한으로 열어서 설치
  ```
  python -m venv venv
  .\venv\Scripts\activate
   ```
   
- 프로그램을 다시 시작하려면 다음을 실행하세요.
  ```
  .\venv\Scripts\activate
   python main.py
   ```
   
- packages 설치
  ```
  .\venv\Scripts\pip install --upgrade --force-reinstall -r requirements.txt

  .\venv\Scripts\pip install -r requirements.txt
  .\venv\Scripts\pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  .\venv\Scripts\pip install llama-cpp-python

  pip install nltk
  .\venv\Scripts\pip install nltk
  python -m nltk.downloader -d C:\nltk_data all
   ```
   
  - 프로그램을 다시 시작할 때 주의사항<-이거 사실상 visual studio에서 F5 로 컴파일 시키는 것만 먹힙니다.
  ```
  .\venv\Scripts\activate
   python main.py
   ```
 ![image](https://github.com/user-attachments/assets/b321c9e5-cdff-4e24-9bbd-624231dd8cdd)

- gpt_sovits 와 rvc 동시 사용 안 됨.

LocalAIVtuber-master\modules.json
  ```
{
  "Aya_LLM_GGUF": true,
  "Chess": false,
  "Local_EN_to_JA": true,
  "Idle_think": false,
  "vitsTTS": false,
  "gpt_sovits": false,
  "Local_LLM": false,
  "No_Translate": true,
  "Rana_LLM_gguf": false,
  "ChatGPT_Azure": true,
  "rvc": true,
  "silero": false,
  "TwitchChatFetch": true,
  "VoiceInput": true,
  "voicevox": false,
  "VtubeStudio": true,
  "YoutubeChatFetch": true
}
   ```

gpt_sovits 와 rvc 동시 사용 안 됨.


Rvc 에서 TTS 이름 잘봐야 합니다.
이름 보고 여자성별이면, rvc 모델 여자걸로
남자 성별이면, rvc 모델 남자걸로 맞춰줘야 합니다.


- LocalAIVtuber-master\plugins\VoiceInput\voiceInput.py 에서
  아래와 같이 소스코드 수정해야 다국어 모드가 활성화 됩니다.
  ```
  #        self.model = whisper.load_model("small.en")#20241024_kpopmodder
        self.model = whisper.load_model("small")#20241024_kpopmodder
   ```	


- LocalAIVtuber-master\modules.json

  뭔가 파이썬 디렉터리 추가하고 싶으면, 아래처럼 추가해서, true로 넣어줘야 합니다.
  안 넣으면, 에러 납니다.
  ``` 
  {
  "Aya_LLM_GGUF": true,
  "Korean_Chat": true,
  "Chess": false,
  "Local_EN_to_JA": true,
  "Idle_think": false,
  "vitsTTS": false,
  "gpt_sovits": false,
  "Local_LLM": false,
  "No_Translate": true,
  "Rana_LLM_gguf": false,
  "ChatGPT_Azure": true,
  "rvc": true,
  "silero": false,
  "TwitchChatFetch": true,
  "VoiceInput": true,
  "voicevox": false,
  "VtubeStudio": true,
  "YoutubeChatFetch": true
  }
   ```
 ![image](https://github.com/user-attachments/assets/9f6a1022-ac1c-412f-9dfc-dc98a649ec33)
 





- 이렇게 vtube studio API 시작되어 있어야 가능합니다.

![image](https://github.com/user-attachments/assets/d518f877-74d9-478b-bee0-82da2a04a7df)

![image](https://github.com/user-attachments/assets/8cb24c4f-fa7d-40cc-84c0-89894a99da33)

- Azure 관련해서 api version은 Azure OpenAI Studio => 배포 => AI 클릭 하면 나옵니다.

![image](https://github.com/user-attachments/assets/7d387c4f-e301-4ad9-b2c5-3af3460c98ab)


![image](https://github.com/user-attachments/assets/fdfadebf-e9fb-4680-9a90-4ce72b61ee44)

- azure key, end point url 은 아래와 같이 확인 가능합니다.

![image](https://github.com/user-attachments/assets/f2781cfb-9e25-4a15-8228-f602c6fe8d06)

![image](https://github.com/user-attachments/assets/74a5ae4f-09ad-445d-8800-4d7a802e1cc8)

- vtube studio 모델 링크 : https://drive.google.com/file/d/1IjzhfiLzeYDOgN_1KOOXe_wUUhPyP4HO/view?usp=drive_link

- 영어로된 내용은 번역기 돌려보시면 됩니다. 한국어 설명은 참고만 해주시면 감사하겠습니다.