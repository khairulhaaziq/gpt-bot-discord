import discord
import openai
import os

intents = discord.Intents.default()
intents.message_content = True

DISCORD_KEY = os.getenv("DISCORD_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
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

    if message.content.startswith('!chat total_tokens'):
        cost_per_1k_tokens = 0.002
        estimated_price = (total_tokens / 1000) * cost_per_1k_tokens
        estimated_price_in_rm = estimated_price * 4.46
        await message.channel.send(f'total_tokens: {total_tokens}, estimated price: RM{estimated_price_in_rm:.4f}')

    elif message.content.startswith('!chat'):
        split_text = message.content.split(" ", 1)
        response = split_text[1] if len(split_text) > 1 else ""

        if response:
            completion = openai_call(response)
            await message.channel.send(completion)


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
