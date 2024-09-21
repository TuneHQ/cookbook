import unittest
from unittest.mock import patch, MagicMock
from tools.llm.gemini import GeminiAI

class TestGeminiAI(unittest.TestCase):

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_initialization_default(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        ai = GeminiAI()
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_with('GEMINI_KEY')
        mock_GenerativeModel.assert_called_with(model_name="gemini-1.5-flash")

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_initialization_custom_model(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        ai = GeminiAI(model_name="custom-model")
        mock_GenerativeModel.assert_called_with(model_name="custom-model")

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_initialization_with_system_instruction(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        ai = GeminiAI(system_instruction="You are a cat.")
        mock_GenerativeModel.assert_called_with(model_name="gemini-1.5-flash", system_instruction="You are a cat.")

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_generate_content(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        mock_model_instance = mock_GenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = "Generated content"
        ai = GeminiAI()
        response = ai.generate_content("Test prompt")
        self.assertEqual(response, "Generated content")
        mock_model_instance.generate_content.assert_called_with("Test prompt")

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_generate_content_empty_prompt(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        mock_model_instance = mock_GenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = "Generated content"
        ai = GeminiAI()
        response = ai.generate_content("")
        self.assertEqual(response, "Generated content")
        mock_model_instance.generate_content.assert_called_with("")

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_generate_content_special_characters(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        mock_model_instance = mock_GenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = "Generated content"
        ai = GeminiAI()
        response = ai.generate_content("!@#$%^&*()")
        self.assertEqual(response, "Generated content")
        mock_model_instance.generate_content.assert_called_with("!@#$%^&*()")

    @patch('tools.llm.gemini.genai.GenerativeModel')
    @patch('tools.llm.gemini.os.getenv')
    @patch('tools.llm.gemini.load_dotenv')
    def test_generate_content_long_prompt(self, mock_load_dotenv, mock_getenv, mock_GenerativeModel):
        mock_getenv.return_value = 'fake_api_key'
        mock_model_instance = mock_GenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = "Generated content"
        ai = GeminiAI()
        long_prompt = "a" * 1000
        response = ai.generate_content(long_prompt)
        self.assertEqual(response, "Generated content")
        mock_model_instance.generate_content.assert_called_with(long_prompt)

if __name__ == '__main__':
    unittest.main()