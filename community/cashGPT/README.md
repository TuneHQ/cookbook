# CashGPT

Tracking your UPI transactions is a hassle. CashGPT helps you analyze your transactions based on your Google Pay data. You can track your spending and much more.

## Table of Contents

- [Usage](#usage)
- [Example Prompts](#Example)
- [Technologies Used](#technologies-used)

## Usage

1. Download your Google Takeout data from [Google Takeout](https://takeout.google.com/) for Google Pay.
2. Find the `My Activity.html` file inside `Takeout/Google Pay/My Activity` and paste it inside the CashGPT folder.
3. Start the Python server: `python3 api.py`
4. Open `index.html` from the `client` folder: `client/index.html`

## Example Prompts

- How much did I overall spend last month?
- Where did I spend the most this month?
- My last 5 transactions

## Technologies Used

- **Backend:** Python
- **Frontend:** HTML, CSS, JavaScript
- **AI Model API:** proxy.tune.app

## Snippet of Working

![Working Demo](https://github.com/phaniankur/cookbook/blob/main/community/cashGPT/demo.gif)
