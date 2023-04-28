import discord
import openai
import os
from chat_42 import send_request_to_endpoint,get_top_endpoint

DISCORD_KEY = os.getenv("DISCORD_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
TRIGGER = '!chat '
TOTAL_TOKENS_TRIGGER = '!chat total_tokens'
CHAT42_TRIGGER = '!chat42'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

message_history = []
total_tokens = 0


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(TOTAL_TOKENS_TRIGGER):
        cost_per_1k_tokens = 0.002
        estimated_price = (total_tokens / 1000) * cost_per_1k_tokens
        estimated_price_in_rm = estimated_price * 4.46
        await message.channel.send(f'total_tokens: {total_tokens}, estimated spent: RM{estimated_price_in_rm:.4f}')

    elif message.content.startswith(TRIGGER):
        split_text = message.content.split(" ", 1)
        response = split_text[1] if len(split_text) > 1 else ""

        if response:
            completion = openai_call(response)
            await message.channel.send(completion)

    elif message.content.startswith(CHAT42_TRIGGER):
        split_text = message.content.split(" ", 1)
        question = split_text[1] if len(split_text) > 1 else ""

        if question:
            completion = send_request_to_endpoint(question)
            total_tokens += completion.usage.total_tokens
            await message.channel.send(completion.choices[0].message.content)

def openai_call(message):
    global total_tokens
    update_conversation(message_history, "user", message)

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history,
            max_tokens=800
        )
        response = completion.choices[0].message.content
        total_tokens += completion.usage.total_tokens
        update_conversation(message_history, "assistant", response)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "Error: openai call failed"


def update_conversation(conversation, role, message):
    conversation.append({"role": role, "content": message})
    if len(conversation) > 10:
        conversation.pop(0)


def main():
    openai.api_key = OPENAI_KEY
    client.run(DISCORD_KEY)


if __name__ == '__main__':
    main()
