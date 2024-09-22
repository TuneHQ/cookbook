import json
import requests
from tools.llm.tune import TuneAI

class ImageGenerator:
    def __init__(self, api_key, model="Legedith/image-gen", temperature=0.8, stream=False, frequency_penalty=0):
        self.url = "https://proxy.tune.app/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.frequency_penalty = frequency_penalty

    def generate_image(self, prompt):
        data = {
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model,
            "stream": self.stream,
            "frequency_penalty": self.frequency_penalty,
        }
        print(f"Sending request to generate image for prompt: {prompt}")
        response = requests.post(self.url, headers=self.headers, json=data)
        return response

    def handle_response(self, response):
        if self.stream:
            for line in response.iter_lines():
                if line:
                    l = line[6:]
                    if l != b'[DONE]':
                        print(json.loads(l))
        else:
            response_json = response.json()
            print(f"Received response: {response_json}")
            image_url = response_json['choices'][0]['message']['content'].split('![image-alt]')[1]
            image_url = image_url[1:-1].strip()  # remove any leading/trailing whitespace
            return image_url

    def download_image(self, image_url, save_path):
        print(f"Downloading image from URL: {image_url}")
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded successfully and saved to {save_path}!")
        else:
            print("Failed to download image. Status code:", response.status_code)

def read_markdown_file(file_path):
    print(f"Reading markdown file: {file_path}")
    with open(file_path, "r") as file:
        return file.readlines()

def write_markdown_file(file_path, lines):
    print(f"Writing updated markdown file: {file_path}")
    with open(file_path, "w") as file:
        file.writelines(lines)

def create_line_number_to_prompt_map(lines):
    # Initialize TuneAI
    tune_ai = TuneAI()
    line_number_to_prompt = {}

    for i, line in enumerate(lines):
        if line.startswith("#"):  # Assuming sections start with '#'
            section_title = line.strip("# ").strip()
            prompt_query = f"Generate an image prompt for the following section title: {section_title}"
            response = tune_ai.generate_content(prompt_query)
            generated_prompt = response.strip()
            line_number_to_prompt[i] = generated_prompt
            print(f"Generated prompt for line {i}: {generated_prompt}")

    return line_number_to_prompt

def main():
    api_key = "sk-tune-jSxbKCXcqYZleGRO288qYCT51f3Jp7LZIUm"
    markdown_file_path = "output.md"
    image_generator = ImageGenerator(api_key)

    # Step 1: Read the markdown file
    lines = read_markdown_file(markdown_file_path)

    # Step 2: Create line number to image prompt map
    line_number_to_prompt = create_line_number_to_prompt_map(lines)

    # Step 3: Generate images for each prompt
    for line_number, prompt in line_number_to_prompt.items():
        response = image_generator.generate_image(prompt)
        image_url = image_generator.handle_response(response)
        if image_url:
            image_path = f"downloads/{line_number}.png"
            image_generator.download_image(image_url, image_path)
            # Step 4: Insert image link into markdown file
            lines.insert(line_number + 1, f"![{prompt}]({image_path})\n")

    # Step 5: Write the updated markdown file
    write_markdown_file(markdown_file_path, lines)

if __name__ == "__main__":
    main()