#called by show_graphs saves plots
import csv
import os
import matplotlib.pyplot as plt
with open ('history.csv','r') as file:
    csv_reader = csv.reader(file,delimiter=',')
    players_won = []
    players_lost = []
    games = []
    next(csv_reader)
    for row in csv_reader:
        if row[0] != row[1]:
            players_won.append(row[0])
        games.append(row[3])
players_wins = {}
games_played = {}
for player in players_won:
    players_wins[player] = 0
for player in players_won:
    players_wins[player]+=1
players_names = []
wins_players = []
players_wins = sorted(players_wins.items(),key = lambda x: x[1],reverse = True)
for player, wins in players_wins:
    players_names.append(player)
    wins_players.append(wins)
x = min(len(players_names),5)
top_five_players_names = players_names[:x]
top_five_players_wins = wins_players[:x]
os.makedirs("charts", exist_ok = True)

plt.style.use('dark_background')
plt.bar(top_five_players_names,top_five_players_wins,color = ['b','b','b','b','b'])
plt.xlabel('Top players')
plt.ylabel('Wins')
plt.title('Our Top performers')
plt.savefig('charts/bar.png',dpi = 300,bbox_inches = 'tight', transparent = True)
plt.close()
for game in games:
    games_played[game] = 0
for game in games:
    games_played[game]+=1
game_names = []
times_played = []
for game, time_played in games_played.items():
    game_names.append(game)
    times_played.append(time_played)
plt.pie(times_played,labels = game_names,autopct='%1.1f%%',colors=['y','r','g'])
plt.tight_layout()
plt.savefig('charts/pie.png',dpi = 300,bbox_inches = 'tight',transparent = True)
plt.close()





        
