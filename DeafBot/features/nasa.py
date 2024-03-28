import requests

class NASA:
   
    # Gets the Picture of NASA A Picture Of the Day
    @staticmethod
    async def get_apod(message, api_key):
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract APOD information
            title = data.get('title')
            explanation = data.get('explanation')
            url = data.get('url')
            copyright = data.get('copyright')

            # Send message to the channel
            await message.channel.send(f"**{title}**\n{explanation}\n{url}\n Copyright: {copyright}")

        else:
            await message.channel.send("Sorry, APOD request failed.")
