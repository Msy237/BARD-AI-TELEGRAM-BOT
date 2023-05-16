# BARD-AI-TELEGRAM-BOT

BARD Telegram Bot is a simple and easy-to-use conversational AI-assistant running on BARD LaMDA language model. It provides the capability to interact with the bot through voice inputs by performing audio recognition on Telegram.

## Features
* Responds to user inputs in text format using [Google BARD Language Models]
* Voice recognition with speech recognition library to handle voice inputs.
* Generates .mp3 files as responses using AWS polly voices
* Reset mechanism for clearing the conversation history.

## Requirements
* Python 3.x installed
* Install necessary Python packages using the requirements.txt file.
  ```
  pip install -r requirements.txt
  ```

## Environment Variables
* `TELEGRAM_TOKEN`: Your Telegram Bot Token which can be obtained from [BotFather](https://core.telegram.org/bots#6-botfather).
* `TOKEN`: Your BARD TOKEN, which can be found on the [BARD Dashboard](https://bard.google.com). (Developpers mode, cookies, copy the __Secure-1PSID Value)
* `AWS_ACCESS_KEY_ID`: Your AWS access key 
* `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key (AWS: Amazon Web Services)

## Usage
1. Set your environment variables:
   ```
   export TELEGRAM_TOKEN=your_telegram_token
   export TOKEN=your_bard_token
   export AWS_ACCESS_KEY_ID= XXXXXXXXXXXXXXXXXXXX
   export AWS_SECRET_ACCESS_KEY= XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

2. Run the script:
   ```
   python3 bard_telegram_bot.py
   ```

3. Open the Telegram app and interact with the bot using text messages or voice inputs.

This work was inspired by @AI-Austin and @jf3tt 
