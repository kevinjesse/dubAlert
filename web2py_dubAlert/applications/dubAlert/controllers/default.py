__author__ = 'kevinjesse'

#JSON lib
import json

#Scrapes NBA lib
from nba_py import team
from nba_py import game
import nba_py
from nba_py import constants

# Email libs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = 'warriorsvslakers@gmail.com'
login = 'warriorsvslakers@gmail.com'
password = 'dubnation7!'


gsw_id = team.TEAMS.get('GSW')['id']
lal_id = team.TEAMS.get('LAL')['id']

gsw_win = False
gsw_record = None

lal_lose = False
lal_record = None

gsw_opp_abb = None
lal_opp_abb = None

gsw_game_score = None
lal_game_score = None

opponent_abb = None
team_record = None
game_score = None


tester = "kjesse@ucsc.edu"

def index():

    alert()
    #game_id = '0021500962'
    #game.Boxscore(game_id).line_score().to_json()
    return dict(d=nba_py.Scoreboard().game_header().to_json())

def alert():
    set_alert()
    if gsw_win or lal_lose:
        send_email(tester)

def team_game(team_id):
    index = -1
    games_json = nba_py.Scoreboard().game_header().to_json()
    games_object = json.loads(games_json)
    for id, home_team in games_object["HOME_TEAM_ID"].iteritems():
        if home_team == int(team_id):
            index = id
            break;
    for id, away_team in games_object["VISITOR_TEAM_ID"].iteritems():
        if away_team == int(team_id):
            index = id
            break;
    if index != -1:
        return games_object["GAME_ID"][index]
    return index

def game_results(game_id, team_id):
    global opponent_abb
    global team_record
    global game_score
    game_json = game.Boxscore(game_id).line_score().to_json()
    game_object = json.loads(game_json)
    for id, team in game_object["TEAM_ID"].iteritems():
        if team == int(team_id):
            index = id
        else:
            opponent = id
            opponent_id = team
    team_record = game_object["TEAM_WINS_LOSSES"][index]
    opponent_abb = game_object["TEAM_ABBREVIATION"][opponent]
    game_score = str(game_object["PTS"][index]) + "-" + str(game_object["PTS"][opponent])
    if game_object["PTS"][index]>game_object["PTS"][opponent]:
        return constants.Outcome.Win
    return constants.Outcome.Loss



def set_alert():
    global gsw_win, lal_lose
    global gsw_opp_abb, lal_opp_abb
    global gsw_record, lal_record
    global gsw_game_score, lal_game_score

     #if gsw played today
    game_id = -1
    game_id = team_game(gsw_id)
    if game_id != -1:
        if game_results(game_id, gsw_id) == constants.Outcome.Win:
            gsw_win = True
            gsw_record = team_record
            gsw_opp_abb = opponent_abb
            gsw_game_score = game_score



    #if lal played today
    game_id = -1
    game_id = team_game(lal_id)

    # #TESTING
    #
    #game_id = '0021500962'
    #
    #
    # #TESTING

    if game_id != -1:
        if game_results(game_id, lal_id) == constants.Outcome.Loss:
            lal_lose = True
            lal_record = team_record
            lal_opp_abb = opponent_abb
            lal_game_score = game_score

def set_message():
    message = ""
    subject = ""
    message1 = "The Golden State Warriors beat the " + constants.TEAMS.get(str(gsw_opp_abb))["city"]  + " " + \
                  constants.TEAMS.get(str(gsw_opp_abb))["name"] + " " + str(gsw_game_score) + " to improve to " + str(gsw_record) +\
                  "!\n\n" if gsw_win else ""
    subject1 = "GSW vs " + str(gsw_opp_abb) if gsw_win else ""

    message2 = "Did you know that the Los Angeles Lakers lost to the " + constants.TEAMS.get(str(lal_opp_abb))["city"] + " " + \
             constants.TEAMS.get(str(lal_opp_abb))["name"] + " " + str(lal_game_score) + " tanking further to a " + str(lal_record) \
             + ".\n\n" if lal_lose else ""
    subject2 = "LAL vs " + str(lal_opp_abb) if lal_lose else ""

    if gsw_win and lal_lose:
        subject = subject1 + " and " + subject2 + " results"
        message = message1 + " " + message2
    elif gsw_win:
        subject = subject1 + " results"
        message = message1
    elif lal_lose:
        subject = subject2 + " results"
        message = message2
    else:
        return "",""
    message += "You should really reconsider and join Dub Nation!\n\n"
    return message, subject

def send_email(to):
    message = ""
    subject = ""
    message, subject = set_message()

    fromaddr = sender
    toaddr = to
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = ""+str(subject)

    html_sig = """\
        <html>
          <head></head>
          <body>
            <p>Curious about warriorsvslakers service? Check out our dedicated <a href="https://github.com/kevinjesse/dubAlert">Team</a> !
            </p>
          </body>
        </html>
        """


    body = ""+str(message)
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html_sig, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return

if __name__ == "__main__":
    alert()