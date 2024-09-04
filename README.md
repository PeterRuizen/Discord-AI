## Discord AI

"!!! WIP !!! For now only the recording of a discord call is possible"

The idea of the app I'm trying to make is explained below. In short this should enable you to talk to an ai using speech in a Discord channel.

An app used to create a webhook for Discord that will send en recieve voice data, based on that data it will use OpenAi's Whisper to turn speech to text. The text will be fed into a local instance of Llama that will generate a response. The response will then be transformed to speech using TTS and send via the webhook to Discord.

## Setup:

1.)  This is written in python 3.12.1

2.)  Run pip install -r requirements.txt to install all the dependencies needed.

3.)  Fill out the env file with your details

4.)  Since this is running on a local instance of Llama, you'll need a beefy computer to run it.

5.)  Run the Main.py to start the application.


## Notice!!!

This all needs to be changed because it's not yet sure how I'm going to build it all. 
