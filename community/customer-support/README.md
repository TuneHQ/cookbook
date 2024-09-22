# Customer Support AI

Customer Support AI is an intelligent application that leverages the power of AI to resolve customer queries about products or services efficiently. Instead of requiring customers to search through extensive website content, this application utilizes the Tune Studio API's threads and assistant capabilities to provide accurate and timely responses.

## Features

- AI-powered customer support assistant
- Customizable assistant prompts
- Updatable knowledge base
- Real-time query resolution
- Integration with Tune Studio API

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm (v6 or later)
- Tune Studio API key

### Installation

1. Clone the repository:

   ```
   git clone <repo-link>
   ```

2. Navigate to the project directory:

   ```
   cd customer-support
   ```

3. Install dependencies:

   ```
   npm install
   ```

4. Create a `.env` file in the root directory and add your Tune Studio API key:

   ```
   TUNE_STUDIO_API_KEY=your_api_key_here
   ```

5. Start the application:

   ```
   npm start
   ```

## Usage

1. **Assistant Prompt Editing**: Customize the AI assistant's behavior by editing its prompt through the admin interface.

2. **Knowledge Base Update**: Keep your AI assistant up-to-date by adding new information to its knowledge base. Currently supports text input, with URL and PDF support coming soon.

3. **Query Resolution**: Users can input their questions, and the AI assistant will provide relevant answers based on the current knowledge base and prompt settings.

## Upcoming Features

- URL input for knowledge base updates
- PDF document support for knowledge base expansion
