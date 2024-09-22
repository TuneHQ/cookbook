# Dell Chatbot - Laptop Buying Assistant

This project is a Dell laptop recommendation chatbot. Users can interact with the chatbot to receive recommendations based on laptop specifications, details, and pricing. The chatbot utilizes function calling to fetch laptop specs, provide details on available models, and retrieve price information for specific laptops. We're using meta/llama-3.1-70b-instruct model for this project due to its price (open source) and performance.


## Demo Video

https://github.com/user-attachments/assets/3dc4c8b7-a714-4ee7-821e-2d12c36f20fb

## Initial Setup

### 1. Install Dependencies
Run the following command to install the required npm packages:

```bash
npm install
```

### 2. Environment Variables
Create a `.env` file in the root directory and add the following environment variables:

```plaintext
TUNE_KEY=<key> # Obtain from https://studio.tune.app
STUDIO_MODEL=<model> # Obtain from https://studio.tune.app
```

### 3. Start the Server
Run the following command to start the server:

```bash
npm run dev
```

The server will start on port 3000.

## Available Features

- **Laptop Recommendations:** Users can request trending or specific Dell laptops based on screen size, RAM, and storage requirements.
- **Laptop Details:** The chatbot can provide detailed specs for particular models.
- **Pricing:** The chatbot can fetch and display the price of a specific Dell laptop in Indian Rupees.

## Example Interactions

- Get recommendations for laptops based on your preferences (e.g., "Show me laptops with 16GB RAM and 512GB SSD").
- Find the price of a specific laptop model.
- Ask for specs such as screen size, RAM, or storage for different models.

