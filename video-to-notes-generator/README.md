# YouTube Video to Markdown Notes Converter

This project allows you to take YouTube video links as input and automatically generate detailed notes in Markdown. It supports features like adding slides, creating transcripts, generating images for specific sections using Tune AI, and inserting timestamps linked directly to the YouTube video.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This tool extracts meaningful notes from a YouTube video, converts them to Markdown, and enriches the content with various additional features, such as:

- Time-stamped links to specific sections of the video.
- Integration with Tune AI to automatically generate images based on the context (examples, concepts, etc.).
- Support for code blocks, tables, graphs, and more.
- Optional inclusion of screenshots or PDF lecture slides along with the video.

We recently migrated from a custom version of Gemini to Tune AI to leverage their larger context length and faster processing.

## Features

- **Video-to-Markdown**: Generate structured notes from a YouTube video, with automatic time-stamped links to the video.
- **Tune AI Integration**: Automatically generate images based on examples or references in the video.
- **Support for Rich Media**: Handle code blocks, tables, graphs, and other complex structures in Markdown.
- **Slide Support**: Optionally include screenshots or PDFs containing lecture slides as input.
- **Transcript Generation**: Automatically create transcripts from the video.

## Installation

To set up this project, ensure you are using Python 3.9 and Poetry for environment and dependency management.

### Step 1: Install Python 3.9

Download and install Python 3.9 from the official [Python website](https://www.python.org/downloads/release/python-390/).

### Step 2: Install Dependencies

1. Clone the repository and navigate into the project directory:

    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. Set up your Poetry environment with Python 3.9:

    ```bash
    poetry env use "C:\Program Files\Python39\python.exe"   # Use your Python 3.9 path
    set PYTHONPATH=%PYTHONPATH%;%CD%    # Add current directory to PYTHONPATH
    ```

3. Activate the Poetry virtual environment:

    ```bash
    poetry shell
    ```

4. Install required dependencies:

    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    ```

5. Install all project dependencies using Poetry:

    ```bash
    poetry install
    ```

   > If the installation fails, you may need to adjust the `pyproject.toml` file to ensure compatibility with Python 3.9 and other dependencies.

## Usage

### Running the Tool

Once the environment is set up, you can run the tool by providing YouTube video links, optional screenshots, or PDFs as input:

```bash
python core/notes_generator/create_notes.py
```

### Generating Notes with Images

The tool will analyze the content of the video, generate notes, and timestamp links. It will also generate images in certain sections (such as examples) using Tune AI

## Configuration

If you encounter any issues with the environment, ensure your `pyproject.toml` file is set up correctly:

```toml
[tool.poetry]
name = "youtube-markdown-notes"
version = "0.1.0"
description = "Generate markdown notes from YouTube videos with images and timestamps."
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
torch = "^1.13"
torchvision = "^0.14"
torchaudio = "^0.13"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## Examples

Below are some examples of how the notes are structured:

```markdown
## Section 1: Introduction [00:02:30](https://www.youtube.com/watch?v=abc123&t=150s)

- Overview of the video
- Key points

![Generated Image](images/intro_example.png)

---

## Section 2: Main Topic [00:15:00](https://www.youtube.com/watch?v=abc123&t=900s)

- Explanation of key concepts
- Example:
  - Code snippet:
    ```python
    def example():
        print("Hello World")
    ```

![Generated Image](images/main_topic_example.png)
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
