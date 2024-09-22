# Recipe Generator in Python using Notion and Tune Studio

## Project Description

In this project, enter the topic name to write an article about, later this can be integrated with web scrapper to get the trending topics and this will get fully automated.
And this article will be sent to your slack channel.

CLI command:

```sh
python main.py --topic='Write an article about trending AI Startups' \
  --page_id=<your-notion-page-id> \
  --model=rohan/mixtral-8x7b-inst-v0-1-32k
```

## Installation

To install the dependencies in the requirements.txt file run the following command:

```sh
pip install -r requirements.txt
```

## Environment variables

Set the environment variables in a `.env` file

```
NOTION_KEY = <your-notion-api-key>
TUNEAI_API_KEY = <your-tuneai-api-key>
SERPER_KEY = <your-serper-api-key>
```