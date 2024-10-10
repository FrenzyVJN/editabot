import os
import re
import typing
import discord
from keep_alive import keep_alive
from discord.ext import commands
from discord import Interaction
from discord import app_commands
import json
import google.generativeai as genai
import base64 
import wikipedia
from astrapy.db import AstraDB
import datetime
import time
import requests
# db = AstraDB(
#   token="AstraCS:pDdyrHqxZsOJzbgTRQCnFeih:692aaa848f9de9a3c3d260da84f379b59cf9e13070433978b755fd9b71446ce6",
#   api_endpoint="https://5088dd79-ba17-4009-b3b2-4de79a6aa1f3-centralindia.apps.astra.datastax.com",
#   )
# #collection = db.create_collection("discordchat", dimension=5, metric="cosine")
# print(f"Connected to Astra DB: {db.get_collections()}")

# # print(collection)
# collection = db.collection("discordchat")

json_file_path = "data.json"

def load_data():
        try:
                with open(json_file_path, "r") as file:
                        return json.load(file)
        except FileNotFoundError:
                return {}

def save_data():
        with open(json_file_path, "w") as file:
                json.dump(db, file, indent = 2)


intents = discord.Intents.default()
intents.message_content = True


# Initialize the required keys in the database
db = load_data()

if "user_details" not in db:
    db["user_details"] = {}
    save_data()

if "teams" not in db:
    db["teams"] = {}
    save_data()
print(db["teams"])
print(db["user_details"])
print(db["question"])
#print(db["user_details"])
#print(db["teams"])

client = commands.Bot(command_prefix="$", intents=intents)
#bot = commands.Bot(command_prefix="$", intents=intents)

keys = db.keys()
print(keys) 
#del db["user_details"]["frenzyvjn"]



@client.event
async def on_ready():
    await client.tree.sync()
    print('We have logged in as {0.user}'.format(client))

    genai.configure(api_key="AIzaSyDREJlYov_T2kaZ3si1nS77sJH7FHrEzHA")
    generation_config = {"temperature":0.9, "top_p":1, "top_k":1, "max_output_tokens":2048}
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
    #a = "You are Edita bot. You are here to assist us with our queries. '"+input()+"' answer in less than 100 words"
    global chat
    chat = model.start_chat(history=[])
    response = chat.send_message('''You are Edita bot. You are here to assist us with our queries in field of cyberesecurity. 
                                 You are in a cyber security discord server. Edita bot can do the following!

        Available Commands:
        1. `/announce [message]`: Announce important messages.
2. `/add_question [question_number] [question] [flag]`: Add a new question with a flag.
3. `/delete_question [question_number]`: Delete an existing question.
4. `/display_question [question_number]`: Display details of a specific question.
5. `/flag [task] [flag]`: Submit your flag for verification.
6. `/score [username]`: Check your current score.
7. `/ping`: Check the bot's latency.
8. `/create_team [team_name] [password]`: Create a new team with a specified password.
9. `/join_team [team_name] [password]`: Join an existing team with the correct password.
10. `/leave_team [team_name]`: Leave your current team.
11. `/delete_team [team_name]`: Admin use only - Delete an existing team.
12. `/display_team_members [team_name]`: Display the members of a specific team.
13. `/display_all_teams`: Display a list of all existing teams.
14. `/team_score [team_name]`: Display the total score for a specific team.
15. `/display_all_questions`: Display all available questions.
16. `/team_leaderboard`: Display the team leaderboard.
17. `/leaderboard`: Display the user leaderboard.
18. `?[message]`: Ask Edita bot a question.

Note: Some commands may have admin restrictions. Please follow the guidelines and enjoy your CTF experience!''')
    
    ##response = chat.send_message('who are you?')
    ##print(response.text)
    print("ready")


@client.tree.command(name="announce",description="Admin use only")
async def announce(interaction: Interaction, message: str):
    await interaction.response.send_message(message)

@client.command()
async def edita(ctx):
    print("Hello world")
    await ctx.send(ctx)

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content != "tldr":
            player = message.author
            message_db = {str(player): message.content}
            documents = [
            {"user": str(player), "message": message.content},
            ]
            # res = collection.insert_many(documents)
    if message.author == "frenzyvjn" or message.author == "drunkencloud" or message.author == "hotaru_hspr" or message.author == "aditya20.0" or message.author == "aathish04":
        if message.content.startswith("tldr"):
            print("tldr entered")
            # temp = collection.find()["data"]['documents']
            text = str(temp)
            response = chat.send_message(text + "OUTPUT : can u brief me on the above conversation pls. very shortly. and who were part of this convo",safety_settings = [
                {"category":'HARM_CATEGORY_HARASSMENT',
                "threshold":'block_none'},
                {"category":'HARM_CATEGORY_DANGEROUS_CONTENT',
                "threshold":'block_none'},
                {"category":'HARM_CATEGORY_HATE_SPEECH',
                "threshold":'block_none'},
                {"category":'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                "threshold":'block_none'}
                ])
            text = response.text
            messages = []
            current = 0
            if len(text)>2000:
                for i in range(2000,0,-1):
                    if(text[i]=='\n'):
                        sub_message = text[current:current+i]
                        messages.append(sub_message)
                        current += i
                        break
            elif len(text)<=2000:
                sub_message = text[current:]
                messages.append(sub_message)

            # Send each part as a separate message
            for string in messages:
                await message.reply(string)

    if message.author != client.user:
        author = message.author
    if message.author == client.user:
        return
    if message.author.bot: return
    if message.content.startswith("!"):
            await message.reply("Edita is thinking...")
            response = chat.send_message(message.content[1:], safety_settings = [
                {"category":'HARM_CATEGORY_HARASSMENT',
                "threshold":'block_none'},
                {"category":'HARM_CATEGORY_DANGEROUS_CONTENT',
                "threshold":'block_none'},
                {"category":'HARM_CATEGORY_HATE_SPEECH',
                "threshold":'block_none'},
                {"category":'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                "threshold":'block_none'}
                ])
            messages = []
            text = response.text
            doc = [{"user": "aibot", "message": text}]
            # res = collection.insert_many(doc)
            current = 0
            while(len(text)>current):
                #print(chat.history)
                #print(len(chat.history))
                if len(chat.history)>4:
                    del chat.history[2:]
                if len(text)>2000:
                    for i in range(2000,0,-1):
                        if(text[i]=='\n'):
                            sub_message = text[current:current+i]
                            messages.append(sub_message)
                            current += i
                            break
                elif len(text)<=2000:
                    sub_message = text[current:]
                    messages.append(sub_message)
                    break

                # Send each part as a separate message
            for string in messages:
                await message.reply(string)
#            await message.channel.send(response.text)
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    if message.content == ('bot'):
      await message.channel.send('Greetings! I am a bot designed to assist you in team management. Currently, I am undergoing beta testing, so please be aware that there may be instances of data loss during this phase. I will be updated with more features in the future.')
    if message.content == ('bot help'):
      await message.channel.send(
        """
        Welcome to the CTF Bot Help Center!

        Available Commands:
        1. `/announce [message]`: Announce important messages.
2. `/add_question [question_number] [question] [flag]`: Add a new question with a flag.
3. `/delete_question [question_number]`: Delete an existing question.
4. `/display_question [question_number]`: Display details of a specific question.
5. `/flag [task] [flag]`: Submit your flag for verification.
6. `/score [username]`: Check your current score.
7. `/ping`: Check the bot's latency.
8. `/create_team [team_name] [password]`: Create a new team with a specified password.
9. `/join_team [team_name] [password]`: Join an existing team with the correct password.
10. `/leave_team [team_name]`: Leave your current team.
11. `/delete_team [team_name]`: Admin use only - Delete an existing team.
12. `/display_team_members [team_name]`: Display the members of a specific team.
13. `/display_all_teams`: Display a list of all existing teams.
14. `/team_score [team_name]`: Display the total score for a specific team.
15. `/display_all_questions`: Display all available questions.

Note: Some commands may have admin restrictions. Please follow the guidelines and enjoy your CTF experience!
        """

      )
      

@client.tree.command(name="b64", description="Encode (1) and decode (2) base64")
async def b64(interaction: Interaction, message:str, option:typing.Literal["encode", "decode"]):
    if option == "encode":
        message = base64.b64encode(message.encode()).decode()
        await interaction.response.send_message(message)
    elif option == "decode":
        message = base64.b64decode(message.encode()).decode()
        await interaction.response.send_message(message)

@client.tree.command(name="askai", description="Ask gemini ai from discord")
async def askai(interaction:Interaction, message:str):
    message = "!"+message
    await interaction.response.send_message(message)
allowed_role_name = "Team Edita"
@client.tree.command(name="add_question", description="Admin use only")
async def add_question(interaction: Interaction, question_number: str, *, question: str, flag: str):
    author = str(interaction.user)
    if question_number not in db["question"]:
      db["question"][question_number] = {"question": question, "author": author, "flag":[flag]}
      save_data()
      embed = discord.Embed(title=f"Question {question_number}", description=question, color=discord.Color.blue())
      embed.set_footer(text=f"Author: {author}")
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      await interaction.response.send_message("Question already exists")

@client.tree.command(name="display_all_questions", description="Displays all question numbers available")
async def display_all_questions(interaction: Interaction):
          question_numbers = list(db["question"])
          if not question_numbers:
              await interaction.response.send_message("No questions found.")
              return

          # Create an embed to display question numbers
          embed = discord.Embed(title="All Question Numbers", color=discord.Color.blue())

          # Add question numbers to the embed

          question_list = "\n".join(question_numbers)
          embed.add_field(name="Question Numbers", value=question_list)
          # Send the embed as a response
          await interaction.response.send_message(embed=embed)


@client.tree.command(name="delete_question", description="Admin use only")
async def delete_question(interaction: Interaction, question_number: str):
    username = str(interaction.user)
    if question_number in db["question"]:
          del db["question"][question_number]
          save_data()
    await interaction.response.send_message(f"Question {question_number} deleted")
    for username, user_data in db["user_details"].items():
      if "qs" in user_data and question_number in user_data["qs"]:
          user_data["qs"].remove(question_number)
          user_data["score"] -= 1
          save_data()
    # Remove the deleted question from team scores
    for team_name, team_data in db["teams"].items():
      if "qs" in team_data and question_number in team_data["qs"]:
          team_data["qs"].remove(question_number)
          team_data["score"] -= 1
          save_data()



@client.tree.command(name="create_event", description="Schedule a server event")
async def create_event(interaction: discord.Interaction, weeks: int):
    def get_events(weeks_time = 1):
        current_time = datetime.datetime.now()
        one_week_later = current_time + datetime.timedelta(weeks=weeks_time)

        start_timestamp = int(time.mktime(current_time.timetuple()))
        finish_timestamp = int(time.mktime(one_week_later.timetuple()))

        url = f"https://ctftime.org/api/v1/events/?limit=20&start={start_timestamp}&finish={finish_timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = response.json()
            return events
        else:
            return None
    # if interaction.guild.id != ALLOWED_GUILD_ID:
    #     await interaction.response.send_message("This bot only works in the designated server.", ephemeral=True)
    #     return

    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild

    events = get_events(weeks)

    if events:
        existing_events = await guild.fetch_scheduled_events()
        existing_event_titles = {event.name: event for event in existing_events}
        
        created_events = []
        updated_events = []
        
        for event in events:
            if event['onsite'] and "India" not in event['location']:
                continue

            description = (
                "CTFtime URL: " + event['ctftime_url'] + "\n\n" +
                "Format: " + event['format'] + "\n\n" +
                "Weight: " + str(event['weight']) + "\n\n" 
                )
            # if event['restrictions'] != "Open":
            #     description = "Restriction: " + event['restrictions'] + "\n\n" + description
            print(description)
            print(len(description))
            start_time = datetime.datetime.strptime(str(event['start']).replace('T', ' '), "%Y-%m-%d %H:%M:%S%z")
            finish_time = datetime.datetime.strptime(str(event['finish']).replace('T', ' '), "%Y-%m-%d %H:%M:%S%z")
            if event['title'] in existing_event_titles:
                scheduled_event = existing_event_titles[event['title']]
                await scheduled_event.edit(
                    description=description,
                    start_time=start_time,
                    end_time=finish_time,
                    entity_type=discord.EntityType.external,
                    location=event['url']
                )
                updated_events.append(event['title'])
            else:
                new_event = await guild.create_scheduled_event(
                    name=event['title'],
                    description=description,
                    start_time=start_time,
                    end_time=finish_time,
                    privacy_level=discord.PrivacyLevel.guild_only,
                    entity_type=discord.EntityType.external,
                    location=event['url']
                )
                created_events.append(event['title'])

        summary_message = "Event update summary:\n"
        if created_events:
            summary_message += f"Created events: {', '.join(created_events)}\n"
        if updated_events:
            summary_message += f"Updated events: {', '.join(updated_events)}\n"
        if not created_events and not updated_events:
            summary_message += "No events were created or updated."

        await interaction.followup.send(summary_message, ephemeral=True)
    else:
        await interaction.followup.send("Error! No events found using API", ephemeral=True)

@client.tree.command(name="display_question", description="Displays question")
async def display_question(interaction: Interaction, question_number: str):
    question_dict = db["question"]
    if question_number in question_dict:
      question = question_dict[question_number]["question"]
      author = question_dict[question_number]["author"]
      save_data()
      embed = discord.Embed(title=f"Question {question_number}", description=question, color=discord.Color.blue())
      embed.set_footer(text=f"Author: {author}")
      await interaction.response.send_message(embed=embed)
    else:
      await interaction.response.send_message(f"Question {question_number} not found")

@client.tree.command(name="team_leaderboard_beta", description="Displays team leaderboard")
async def team_leaderboard_beta(interaction: Interaction):
      teams = db["teams"]

      if not teams:
          await interaction.response.send_message("No teams found.")
          return

      # Calculate team scores
      team_scores = []
      for team_name, team_data in teams.items():
          team_members = team_data["members"]
          total_team_score = 0
          counted_questions = set()

          for member in team_members:
              if member in db["user_details"]:
                  member_scores = db["user_details"][member]["qs"]
                  for question in member_scores:
                      if question not in counted_questions:
                          total_team_score += 1
                          counted_questions.add(question)

          team_scores.append({"team_name": team_name, "score": total_team_score})

      # Sort teams based on scores in descending order
      sorted_teams = sorted(team_scores, key=lambda x: x["score"], reverse=True)

      # Generate leaderboard text
      leaderboard_text = "Team Leaderboard:\n"
      for team in sorted_teams:
          leaderboard_text += f"{team['team_name']}: {team['score']} points\n"

      await interaction.response.send_message(leaderboard_text)


@client.tree.command(name="flag", description="Submit your flag")
async def flag(interaction, task: str, flag: str):
    if flag.startswith("flag{") and flag.endswith("}"):
        # Extract the flag content between "flag{" and "}"
        username = str(interaction.user)
        team_name = db["user_details"][username]["team"]
        if team_name == []:
           await interaction.response.send_message("You are not in a team",ephemeral=True)
           return
        flag_content = flag
        question = task
        if flag == db["question"][question]["flag"][0]:
            await interaction.response.send_message("Your flag is correct!", ephemeral=True)
            if task not in db["user_details"][username]["qs"]:
                db["user_details"][username]["qs"].append(task)
                db["user_details"][username]["score"] += 1
                team_name = db["user_details"][username]["team"][0]
                team_members = db["teams"][team_name]["members"]
                total_team_score = db["teams"][team_name]["score"]
                counted_questions = db["teams"][team_name]["qs"]
                save_data()
                for member in team_members:
                    if member in db["user_details"]:
                        member_scores = db["user_details"][member]["qs"]
                        for question in member_scores:
                            if question not in counted_questions:
                                total_team_score += 1
                                counted_questions.append(question)
                                print(total_team_score)
                                print(counted_questions)
                                save_data()
        else:
            await interaction.response.send_message("Incorrect flag. Try again!", ephemeral=True)
    else:
        await interaction.response.send_message("Invalid flag format. Make sure it starts with 'flag{' and ends with '}'.", ephemeral=True)

@client.tree.command(name="score", description="Check your score")
async def score(interaction, username: str):
    if username in db["user_details"]:
        user_score = db["user_details"][username]["score"]
        await interaction.response.send_message(f"Your score is {user_score}")
    else:
        await interaction.response.send_message("User not found. Please make sure you have submitted at least one flag.")

@client.tree.command(name="ping", description="Shows the ping!")
async def ping(interaction: Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! ... {bot_latency}ms")

@client.tree.command(name="create_team", description="To create team")
async def create_team(interaction: Interaction, team_name: str, password: str):
    data = load_data()
    username = str(interaction.user)
    teams = db["teams"]
    if username not in db["user_details"]:
      db["user_details"][username] = {"score": 0, "qs": [], "team": [], "cash": 0}

    if team_name not in teams:
      if db["user_details"][username]["team"] == []:
        guild = interaction.guild
        team_role = await guild.create_role(name=team_name)
        await team_role.edit(mentionable=True)
        teams[team_name] = {"members": [username], "password": [password], "score": 0, "qs": [],"role_id":team_role.id, "team_cash": 0}
        db["user_details"][username]["team"].append(team_name)
        user = interaction.user
        await user.add_roles(team_role)
        save_data()
        await interaction.response.send_message(f"Team {team_name} created successfully", ephemeral=True)
        return
      elif db["user_details"][username]["team"] != []:
        await interaction.response.send_message("You are already in a team", ephemeral=True)
    else:
        await interaction.response.send_message(f"Team {team_name} already exists")

team_list = list(db["teams"].keys())
@client.tree.command(name="join_team", description="To join team")
async def join_team(interaction: Interaction, team_name: str, password: str):
    username = str(interaction.user)
    teams = db["teams"]
    if username not in db["user_details"]:
      db["user_details"][username] = {"score": 0, "qs": [], "team": [], "cash": 0}
      save_data()
    if team_name in teams:
      if db["user_details"][username]["team"] == []:
        team_members = teams[team_name]["members"]
        cpassword = teams[team_name]["password"][0]
        team_role_id = teams[team_name]["role_id"]
        save_data()
        if username not in team_members:
          if cpassword == password:
            guild = interaction.guild
            user = interaction.user
            try:
                team_role = guild.get_role(team_role_id)
                await user.add_roles(team_role)
            except AttributeError:
                pass
            team_members.append(username)
            await interaction.response.send_message(f"You have joined team {team_name}")
            # Update user's team information
            db["user_details"][username]["team"].append(team_name)
            save_data()
          elif cpassword != password:
            await interaction.response.send_message("Incorrect password. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message("User already exists in the team")
      elif db["user_details"][username]["team"] != []:
        await interaction.response.send_message("You are already in a team", ephemeral=True)
    else:
        await interaction.response.send_message(f"Team {team_name} not found")

@client.tree.command(name="leave_team", description="To leave team")
async def leave_team(interaction: Interaction, team_name: str):
    username = str(interaction.user)
    teams = db["teams"]
    if team_name in teams:
        team_members = teams[team_name]["members"]
        save_data()
        if username in team_members:
            guild = interaction.guild

            # Get the team role
            team_role_id = teams[team_name]["role_id"]
            team_role = guild.get_role(team_role_id)
            if team_role:
                # Remove the team role from the user
                await interaction.user.remove_roles(team_role)

            team_members.remove(username)
            await interaction.response.send_message(f"You have left team {team_name}")
            # Update user's team information
            db["user_details"][username]["team"].remove(team_name)
            save_data()
        else:
            await interaction.response.send_message(f"User not found in team {team_name}")
    else:
        await interaction.response.send_message(f"Team {team_name} not found")


@client.tree.command(name="delete_team", description="To delete team")
async def delete_team(interaction: Interaction, team_name: str):
        username = str(interaction.user)
        teams = db["teams"]
        if username == "frenzyvjn" or username == "drunkencloud" or username == "hotaru_hspr":
          if team_name in teams:
              # Get the members of the team to be deleted
              team_members = teams[team_name]["members"]
              save_data()
              # Update team information for each member
              for member in team_members:
                  if member in db["user_details"] and team_name in db["user_details"][member]["team"]:
                      db["user_details"][member]["team"].remove(team_name)
                      save_data()
              guild = interaction.guild

              # Get the team role
              team_role_id = teams[team_name]["role_id"]
              team_role = guild.get_role(team_role_id)
              save_data()
              if team_role:
                  # Delete the team role
                  await team_role.delete()

              # Delete the team from the teams dictionary
              del teams[team_name]
              save_data()
              await interaction.response.send_message(f"Team {team_name} deleted successfully")
          else:
              await interaction.response.send_message(f"Team {team_name} not found")


@client.tree.command(name="display_team_members", description="To display team members name")
async def display_team_members(interaction: Interaction, team_name: str):
    teams = db["teams"]
    if team_name in teams:
        team_members = teams[team_name]["members"]
        members_text = "\n".join(team_members)
        await interaction.response.send_message(f"Team {team_name} members are:\n{members_text}")
    else:
        await interaction.response.send_message(f"Team {team_name} not found")

@client.tree.command(name="display_all_teams", description="To display all teams")
async def display_all_teams(interaction: Interaction):
    teams = db["teams"]
    if not teams:
        await interaction.response.send_message("No teams found.")
        return

    team_names = list(teams.keys())
    teams_text = "\n".join(team_names)
    await interaction.response.send_message(f"Teams:\n{teams_text}")

@client.tree.command(name="leaderboard", description="To display leaderboard")
async def leaderboard(interaction: Interaction):
  users = db["user_details"]
  if not users:
      await interaction.response.send_message("No users found.")
      return

  leaderboard_text = "User Leaderboard:\n"

  # Sort users by their scores in descending order
  sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)

  for user_name, user_data in sorted_users:
      user_score = user_data["score"]
      leaderboard_text += f"{user_name}: {user_score} points\n"

  await interaction.response.send_message(leaderboard_text)
@client.tree.command(name="data", description="For admin use only")
async def data(interaction: Interaction):
   username = str(interaction.user)
   if username == "frenzyvjn" or username == "drunkencloud":
       await interaction.response.send_message(db)
       return
@client.tree.command(name="team_leaderboard", description="To display team leaderboard")
async def team_leaderboard(interaction: Interaction):
    teams = db["teams"]

    if not teams:
        await interaction.response.send_message("No teams found.")
        return

    leaderboard_text = "Team Leaderboard:\n"

    for team_name, team_data in teams.items():
        team_members = team_data["members"]
        total_team_score = 0
        counted_questions = set()

        for member in team_members:
            if member in db["user_details"]:
                member_scores = db["user_details"][member]["qs"]
                for question in member_scores:
                    if question not in counted_questions:
                        total_team_score += 1
                        db["teams"][team_name]["score"] += 1
                        counted_questions.add(question)

        leaderboard_text += f"{team_name}: {total_team_score} points\n"

    await interaction.response.send_message(leaderboard_text)

keep_alive()

async def on_disconnect():
        save_data()

try:
    token = '<ADD YOUR DISCORD BOT TOKEN HERE>' #main bot
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
