# TuneStudioClient

`TuneStudioClient` is a Python client for interacting with the Tune Studio API. It allows you to send messages to the Tune Studio service and receive responses, with support for both streaming and non-streaming responses.

## Sample
Try out the Dungeons and Dragons game (`sample_app_dnd.py`) made using this client. 

Despite being a complex adventure, the game looks neat and clean as the module hides all the unnecessary implementation.

## Features

- Easy-to-use class-based interface
- Configurable parameters for model, temperature, frequency penalty, and max tokens
- Support for streaming and non-streaming responses
- Error handling and logging
- Environment variable support for API key

## Installation

1. Clone the repository or download the `tune_studio_client.py` file.
2. Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

## Setup

1. Create an api key and add to  [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fpradumn.yadav%2F3_cookie%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2239533336-0da7-44e3-b949-9e3bb052ea3f%22%5D "/Users/pradumn.yadav/3_cookie/.env") file in the root directory of your project:

```env
TUNE_STUDIO_API_KEY=your_api_key_here
```

## Usage

Here's an example of how to use the `TuneStudioClient`:

```python
from tune_studio_client import TuneStudioClient

# Initialize the client
client = TuneStudioClient()

# Define the messages
messages = [
    {"role": "system", "content": "You are TuneStudio"},
    {"role": "user", "content": "Who are you"}
]

# Generate a response
response = client.generate_response(messages)

# Print the response
if response:
    print(response)
```

## Configuration

You can update the default configurations dynamically using the `update_config` method:

```python
client.update_config(model="new_model", temperature=0.7, max_tokens=150)
```

## Logging

The client uses Python's built-in logging module to log information and errors. You can configure the logging level as needed.

## Error Handling

The client includes error handling for network requests and JSON parsing errors. If an error occurs, it will be logged, and the method will return `None`.

## License

This project is licensed under the MIT License.
