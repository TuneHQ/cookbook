import requests
import json
import base64

url = 'https://demo-api.models.ai4bharat.org/inference/tts'

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://models.ai4bharat.org',
    'priority': 'u=1, i',
    'referer': 'https://models.ai4bharat.org/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
}

payload = {
    "controlConfig": {"dataTracking": True},
    "input": [{"source": " नमस्ते सभी, इस प्रस्तावना में हम बात करेंगे F तunning LLMs और कुछ थोड़ा अनुबhavशील बात के बारे में जो माने गये कहलाते हैं मॉडल मर्जिंग का कथन करेंगे। इस प्रस्तावना के अंत में, आपको सभी मुख्य पहुँच को विस्तार से जानने का एक अच्छा सुरक्षा होगी जिसमें आपको फाइन टयनिंग के लिए किस प्रकार के इनपुट्स की अनुमति होगी, आपको क्या प्रकार के आउटपुट मिलेंगे और अपने मॉडल की गुणवत्ता को और उच्चतम करने के लिए म Games मर्जिंग के साथ होगा। हम कुछ प्राकृतिक उदाहरणों को देखेंगे जो आपको सुखद होगा। \n\nमुझे बताने के लिए, मैं लिक्विद AI का एक स्टाफ मशीन लॉरNING साइंसिस्ट हूँ। मैं भी GDE हूँ। मैं ब्लॉग पोस्ट लिखता हूँ। GitHub पर LLM को लिखा हुआ कोर्स है। मैंने कुछ फेसबुक पर LLM मॉडल और डेटा सेट भी प्रकाशित किए हैं। मैंने कुछ टूल्स भी लिखे हैं और Hands-On ग्राफ नेटवर्क का लेखक भी हूँ। लेकिन हमने कुछ दिन पहले ही एक नया बुक भी घोषित किया है जो LLM इंजीनियर्स हैं।"}],
    "config": {"gender": "male", "language": {"sourceLanguage": "hi"}}
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

response_json = response.json()
audio_content = response_json['audio'][0]['audioContent']

# Decode the base64 encoded audio content
audio_data = base64.b64decode(audio_content)

# Write the decoded audio content to a file
with open('output.wav', 'wb') as audio_file:
    audio_file.write(audio_data)

print("Audio file saved as output.wav")