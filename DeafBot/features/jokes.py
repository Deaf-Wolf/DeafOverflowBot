import requests

class Jokes:
    @staticmethod
    async def get_joke(message):
        url = f"https://geek-jokes.sameerkumar.website/api?format=json"
        response = requests.get(url)
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            # Extract APOD information
            joke = data.get('joke')
            # Send message to the channel
            await message.channel.send(f"**Geek Joke**\n\n{joke}")

        else:
            await message.channel.send("Sorry, Joke request failed.")