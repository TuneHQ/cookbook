
# Multilingual Video Translator: Initial Prototype for English to Indian Language Translation

**Tune AI PyCon India 2024 Contest Submission**  
*Made with ♥️ on [Tune.ai](https://tune.ai)*

## Project Overview

This project is a beginner-level prototype of a multilingual video translator designed to convert English-spoken content into multiple Indian languages. The solution leverages AI models, including [ai4bharat](https://ai4bharat.org/), to achieve text-to-speech translations in over 20+ local Indian languages. While the current focus is on translating videos into Hindi, the system is built with the flexibility to extend to other languages such as Telugu, Bengali, Gujarati, and more.

### Key Features
- **Multilingual Support**: Translates video content into several Indian languages.
- **Initial Testing**: Early-stage testing with Hindi translations.
- **AI Integration**: Uses [ai4bharat](https://ai4bharat.org/) for high-quality text-to-speech in Indian languages.
- **Continuous Improvements**: Plans for improving audio quality, expanding language support, and enhancing user experience.

## Demo
This prototype demonstrates how a short English video from Tune.ai can be translated into Hindi. While this is a work in progress, it highlights the potential for accurate, multilingual video translation.

⚠️ **Note**: You may experience some minor voice breaks or incomplete translations, as this is still in its early phase.

---

## Table of Contents
- [How to Install and Run](#how-to-install-and-run)
- [Features](#features)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## How to Install and Run

### Prerequisites
- Python 3.x
- pip (Python package manager)
- Access to YouTube API (optional for pulling videos directly)

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/multilingual-video-translator.git
   cd multilingual-video-translator
   ```

2. **Install Dependencies**:
   Run the following command to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Update YouTube Video URL**:
   You can add any English video from YouTube for translation. Update the `url` in the `download.py` file to use your chosen video:
   ```python
   video_url = "https://www.youtube.com/your-video-link"
   ```

4. **Run the Application**:
   Run the orchestrator file to start the translation:
   ```bash
   python orchestrator.py
   ```

### Usage
Once you run the app, the video will be processed, and the English audio will be translated into the target language (Hindi for this prototype). The translated video will be saved locally for review.

---

## Features

- **Multilingual Support**: 
   - Translates English videos into multiple Indian languages.
   - Current prototype supports Hindi, with plans to add Telugu, Bengali, Gujarati, and more.

- **AI-Powered**: 
   - Uses the [ai4bharat](https://ai4bharat.org/) platform for text-to-speech translation into Indian languages.

- **Beginner-Friendly**: 
   - This is an early-stage prototype, suitable for experimentation and future development.

- **Expandable Architecture**:
   - Designed to extend support for additional languages with minimal changes.

---

## Future Enhancements

1. **Improved Audio Quality**:
   - Address voice loss and breaks to ensure smooth, coherent translations.

2. **Expanded Language Support**:
   - Extend support to more Indian languages beyond Hindi.

3. **User Interface Improvements**:
   - Improve the graphical user interface (GUI) for a more intuitive and seamless user experience.

4. **Machine Learning Integration**:
   - Incorporate advanced machine learning algorithms to enhance the accuracy and efficiency of the translations.

