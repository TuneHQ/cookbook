# Project Setup and Configuration

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
SWIGGY_SESSION_ID=<session_id> # Obtain from https://www.swiggy.com/
```

### 3. Start the Server

Run the following command to start the server:

```bash
npm run dev
```

The server will start on port `3000`.

## How to Obtain Swiggy Session ID

1. Log in to [Swiggy](https://www.swiggy.com/).
2. Open the developer tools in your browser.
3. Copy the value of the cookie named `_session_tid`.

**Note:** This workaround is necessary as Swiggy does not provide developer APIs at this time.
