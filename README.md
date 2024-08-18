# Edita Bot
Edita Bot is a Discord bot designed for use in cybersecurity Capture The Flag (CTF) events. It manages team functionalities, questions, and scores, and interacts with users through various commands.

## Features
**Announcements**: Post important messages to the server.
**Questions Management**: Add, delete, display, and manage CTF questions and their flags.
**Teams Management**: Create, join, leave, and delete teams. Manage team roles and display team members.
**Scores Tracking**: Submit flags, check scores, and view leaderboards for users and teams.
**Events Management**: Schedule and manage server events based on CTFtime data.
**Base64 Encoding/Decoding**: Encode and decode messages in Base64 format.
**AI Interaction**: Ask questions to the Gemini AI model for assistance and get brief summaries of conversations.
Setup
Prerequisites
```
Python 3.8 or later
discord.py library
google.generativeai library
requests library
```
Installation
Clone the repository:
```sh
git clone https://github.com/yourusername/edita-bot.git
cd edita-bot
```
Install dependencies:

```sh
pip install -r requirements.txt
```
Setup environment variables:
Fill in the API keys in main.py with the following content:

```env
DISCORD_TOKEN=your-discord-bot-token
GEMINI_API_KEY=your-gemini-api-key
```
Run the bot:

```sh
python bot.py
```
Usage
```
/announce [message]: Announce important messages (Admin use only).
/add_question [question_number] [question] [flag]: Add a new CTF question.
/delete_question [question_number]: Delete an existing question.
/display_question [question_number]: Display details of a specific question.
/flag [task] [flag]: Submit a flag for verification.
/score [username]: Check the score of a specific user.
/ping: Check the bot's latency.
/create_team [team_name] [password]: Create a new team with a specified password.
/join_team [team_name] [password]: Join an existing team with the correct password.
/leave_team [team_name]: Leave your current team.
/delete_team [team_name]: Delete an existing team (Admin use only).
/display_team_members [team_name]: Display members of a specific team.
/display_all_teams: Display a list of all existing teams.
/team_score [team_name]: Display the total score for a specific team.
/display_all_questions: Display all available questions.
/team_leaderboard: Display the team leaderboard.
/leaderboard: Display the user leaderboard.
/b64 [message] [encode|decode]: Encode or decode a message in Base64.
/askai [message]: Ask a question to Gemini AI.
/create_event [weeks]: Schedule a server event based on CTFtime data.
```
## Contributing
Contributions are welcome! Please open an issue or a pull request to suggest improvements or report bugs.


Feel free to adjust the details according to your specific needs and preferences.



