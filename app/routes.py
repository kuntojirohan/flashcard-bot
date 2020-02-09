from flask import request
from app import app, _update_db
from app.models import User, Flashcard
from twilio.twiml.messaging_response import MessagingResponse


def _send_message(output_lines):
    """It takes a list of lines, concatenates them with a newline, and sends them back to the user as a Twilio message.

    Returns:
        string : response message texts
    """
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(output_lines))
    return str(resp)


@app.route("/webhook", methods=["POST"])
def bot():
    """The webhook for creating the response messages to be sent on Whatsapp.
    """
    incoming_msg = request.values.get("Body", "").strip().lower()
    remote_number = request.values.get("From", "")
    output_lines = []
    # incoming From is "whatsapp:#######"
    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    if not remote_number:
        remote_number = "123"

    user = User.query.get(remote_number)

    # Help commands
    # - 'help'
    if incoming_msg == "help":
        output_lines.append("'create account' - create a new account")
        output_lines.append("'create flashcards' - start creating flashcards")
        output_lines.append(
            "'stop creating flashcards' - stop creating flashcards")
        output_lines.append("'start reviewing' - start reviewing flashcards")
        output_lines.append("'stop reviewing' - stop reviewing flashcards")
        return _send_message(output_lines)

    # User creation commands
    # - 'create account'
    if not user:
        if incoming_msg == "create account":
            new_user = User(remote_number)
            _update_db(new_user)
            output_lines.append(
                f"Account successfully created for number {remote_number}!"
            )
            output_lines.append(
                "To get started, text 'create flashcards' to start creating flashcards."
            )
            output_lines.append(
                "When you're finished, text 'stop creating flashcards'."
            )
            output_lines.append(
                "You can text 'start reviewing' to review the flashcards you've created."
            )
            output_lines.append(
                "Text 'help' at any time to see available commands."
            )
        else:
            output_lines.append(
                "Please register with 'create account', first!")

        return _send_message(output_lines)
    else:
        if incoming_msg == "create account":
            output_lines.append(
                f"You have already registered {remote_number}. Send 'help' for available options.")
            return _send_message(output_lines)

    # Flashcard commands
    # - 'create flashcards'
    #   - '{front} / {back}'
    #   - 'stop creating flashcards'
    # - 'start reviewing'
    #   - '{answer}'
    #   - 'stop reviewing'

    if not user.creating_flashcards and incoming_msg == "create flashcards":
        output_lines.append(
            "Create a new flashcard by texting in the form {front} / {back}."
        )
        output_lines.append(
            "For example 'hello / 你好' would create 'hello' on the front and '你好' on the back."
        )
        user.creating_flashcards = True
        user.current_review = None
        _update_db(user)
        return _send_message(output_lines)

    if user.creating_flashcards and incoming_msg == "stop creating flashcards":
        output_lines.append("Flashcard creation stopped.")
        user.creating_flashcards = False
        _update_db(user)
        return _send_message(output_lines)

    if user.creating_flashcards:
        if "/" not in incoming_msg:
            output_lines.append(
                "Please include a / in your text when creating flash cards."
            )
            output_lines.append("Text 'stop creating flashcards' to end.")
            return _send_message(output_lines)
        else:
            message_parts = incoming_msg.split("/")
            if len(message_parts) > 2:
                output_lines.append(
                    "More than one / was sent. Please use only one / in message.")
                return _send_message(output_lines)
            front = message_parts[0].strip()
            back = message_parts[1].strip()
            new_review = Flashcard(user.phone_number, front, back)
            _update_db(new_review)
            output_lines.append(
                f"Flashcard for '{front} / {back}' created successfully."
            )
            return _send_message(output_lines)

    if user.current_review is None and incoming_msg == "start reviewing":
        review = user.get_new_review()
        if not review:
            output_lines.append(
                "First create a flashcard with 'create flashcards'")
        else:
            output_lines.append("Respond with the back of the flashcard.")
            output_lines.append(review.front.title())
        return _send_message(output_lines)

    if user.current_review is not None:
        if incoming_msg == "stop reviewing":
            output_lines.append("Done reviewing!")
            user.stop_reviewing()
        else:
            if incoming_msg == user.current_review.back:
                output_lines.append("Correct!")
                new_review = user.get_new_review()
                output_lines.append(new_review.front.title())
            else:
                output_lines.append("Incorrect!")
        return _send_message(output_lines)

    output_lines.append(
        "Sorry, I don't understand, please try again or text 'help'.")
    return _send_message(output_lines)
