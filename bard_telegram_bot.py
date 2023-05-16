import os
import logging
from Bard import Chatbot
from telegram import Update
from telegram.ext import (ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler)
import speech_recognition as sr
from helpers import download_audio, convert_audio_to_wav
from tts_polly_Matthew import TTS   # Change to tts_polly_Joanna for a female voice

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

telegram_token = 'YOUR_BOT_TOKEN'
token = "YOUR_BARD_API_TOKEN"

# Initialize Google Bard API
chatbot = Chatbot(token)
messages_list = []

def append_history(content, role):
    messages_list.append({"role": role, "content": content})

def clear_history():
    messages_list.clear()

async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    append_history(update.message.text, "user")
    thinking = await context.bot.send_message(chat_id=update.effective_chat.id, text="⏳")

    # Generate response
    response = await prompt_bard(update.message.text)
    
    # Send text message
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🤖 BARD: {response}")

    # Generate and send audio response
    tts = TTS()
    audio_file_path = 'response.mp3'
    tts.convert(response, audio_file_path)
    with open(audio_file_path, 'rb') as f:
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=f)
    
    # Remove audio file
    os.remove(audio_file_path)

    append_history(response, "assistant")
    await context.bot.delete_message(message_id=thinking.message_id, chat_id=update.message.chat_id)

async def process_audio_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    append_history("Voice message", "user")
    thinking = await context.bot.send_message(chat_id=update.effective_chat.id, text="⏳")
    transcript = await get_audio_transcription(update, context)

    # Send the transcribed voice message as the user message
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"👨🏾‍💻 User: {transcript}")

    # Generate BARD response
    response = await prompt_bard(transcript)
    append_history(response, "assistant")

    # Send text message
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🤖 BARD: {response}")

    # Generate audio response using TTS
    tts = TTS()
    audio_file_path = 'response.mp3'
    tts.convert(response, audio_file_path)

    # Send audio response
    with open(audio_file_path, 'rb') as f:
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=f)

    # Remove audio files
    os.remove(audio_file_path)
    os.remove(update.message.voice.file_id + ".wav")

    await context.bot.delete_message(message_id=thinking.message_id, chat_id=update.message.chat_id)

async def get_audio_transcription(update, context):
    new_file = await download_audio(update, context)
    voice = convert_audio_to_wav(new_file)
    recognizer = sr.Recognizer()
    with sr.AudioFile(voice) as source:
        audio = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio, language="en")
    except sr.UnknownValueError:
        transcript = "I couldn't understand what you said."
    except sr.RequestError as e:
        transcript = "Error: {}".format(e)
    return transcript


async def prompt_bard(transcript):
    response = chatbot.ask(transcript)
    return response['content']

async def reset_history(update, context):
    clear_history()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Messages history cleaned")

if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_token).build()
    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), process_text_message)
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("reset", reset_history))
    audio_handler = MessageHandler(filters.VOICE, process_audio_message)
    application.add_handler(audio_handler)
    application.run_polling()
