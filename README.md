# flashcard-bot

A flashcard is one of the most tried and true study tools, helping anyone from medical students to language learners all approach their goal of memorizing facts and figures. Software like Anki or Memrise have provided countless features and robust settings that make digital flashcards increasingly useful. However, there are plenty of times where you might not be able to pull up one of the more robust applications and need something more lightweight to study with.

For example, when your cell signal is good enough for texting, but cannot load a full-featured web application. Or perhaps you’re in an airplane that doesn’t allow various websites, but does allow you to text phone numbers down on the ground.

This tutorial will show you how to make a basic flashcard bot for WhatsApp or SMS to get you started on your way to reviewing flashcards wherever you are.

## Tutorial Requirements
To follow this tutorial you need the following components:
- Python 3.6 or newer. If your operating system does not provide a Python interpreter, you can go to python.org to download an installer.
- Flask. We will create a web application that responds to incoming WhatsApp messages with it.
- SQLite. A very simple database that we will use to store flashcards.
- ngrok. We will use this handy utility to connect the Flask application running on your system to a public URL that Twilio can connect to. This is necessary for the development version of the chatbot because your computer is likely behind a router or firewall, so it isn’t directly reachable on the Internet. If you don’t have ngrok it installed, you can download a copy for Windows, MacOS or Linux.
- A smartphone with an active phone number and WhatsApp installed. This tutorial works with standard SMSes as well if you prefer that over WhatsApp.
- A Twilio account. If you are new to Twilio create a free account now. You can review the features and limitations of a free Twilio account.

## Configure the Twilio WhatsApp Sandbox
Twilio provides a WhatsApp sandbox where you can easily develop and test your application. Once your application is complete you can request production access for your Twilio phone number, which requires approval by WhatsApp.

Let’s connect your smartphone to the sandbox. From your Twilio Console, select Programmable SMS and then click on WhatsApp. The WhatsApp sandbox page will show you the sandbox number assigned to your account, and a join code.
To enable the WhatsApp sandbox for your smartphone send a WhatsApp message with the given code to the number assigned to your account. The code is going to begin with the word join, followed by a randomly generated two-word phrase. Shortly after you send the message you should receive a reply from Twilio indicating that your mobile number is connected to the sandbox and can start sending and receiving messages.

Note that this step needs to be repeated for any additional phones you’d like to have connected to your sandbox.

## Steps:
* Clone the repo with git clone
* Create a python3 virtualenv
* pip install -r requirements.txt
* Initialize the SQLite databse with these commands. After these are run you will see a new migrations folder and a new app.db SQLite database. Inside of the migrations/versions folder are the scripts used to create the database structure we defined in the models.py file above. As you grow and change this flashcard bot to fit your specific needs, you can run the migrate and upgrade commands to update your database’s structure.
  * flask db init
  * flask db migrate
  * flask db upgrade
* Run the command 'flask run' in your root folder to start the flask server
* Download the ngrok and go to that directory. Open a new terminal in that directory and run './ngrok http 5000'
* Now, copy the URL from ngrok (https) + '/webhook' (the webhook endpoint from routes.py) into the Twilio Sandbox Configuration section.
* That's it! You are all set to text and recieve messages from the whatsapp flashcard-bot you designed. Test it. 
* Kudos to you!
