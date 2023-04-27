import discord
import openai
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

DISCORD_KEY = os.environ['DISCORD_KEY']
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = discord.Client(intents=intents)

message_history = []

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!chat'):
    split_text = message.content.split(" ", 1)
    response = split_text[1] if len(split_text) > 1 else ""
    
    if response:
      completion = openai_call(response)
      await message.channel.send(completion)

keep_alive()

def openai_call(message):
  update_conversation(message_history, "user", message)
    
  try:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history,
      max_tokens=500
    )
    response = completion.choices[0].message.content
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