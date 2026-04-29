#!/bin/bash
# Read history.csv and make leaderboard on terminal
# sort_metric: "wins" | "losses" | "ratio" (default: wins)

clear

# Check if history file exists and has data
if [ ! -f history.csv ]; then
    echo "No history file found."
    exit 0
fi
SORT_BY=$1

# Skip header, count lines
DATA_LINES="tail -n +2 history.csv"

echo -e "\n=============================================="
echo "           FUNGRID LEADERBOARD                     "
echo -e "==============================================\n"

# Print per-game per-user stats
# history.csv format: Winner,Loser,Date,Game
# We loop over each unique game name

GAMES=` $DATA_LINES | cut -d',' -f4 | sort -u`

for GAME in $GAMES; do
    echo "----------------------------------------------"
    echo "  Game: $GAME"
    echo "----------------------------------------------"
    echo -e "  Player              Wins     Losses     W/L"
    echo "----------------------------------------------"

    # Get all unique players for this game
    PLAYERS=` $DATA_LINES | grep -v "Draw" | grep -v . | awk -F',' -v game="$GAME" 'BEGIN{ OFS = "\n"} $4==game {print $1,$2}' | sort -u`

    # Build temp data: player wins losses ratio
    TEMP_DATA=""
    for PLAYER in $PLAYERS; do
        WINS=` $DATA_LINES | awk -F',' -v p="$PLAYER" -v game="$GAME" '$1==p && $4==game' | wc -l | tr -d ' '`
        LOSSES=` $DATA_LINES | awk -F',' -v p="$PLAYER" -v game="$GAME" '$2==p && $4==game' | wc -l | tr -d ' '`

        # Compute ratio: wins/losses, handle division by zero
        if [ "$LOSSES" -eq 0 ]; then
                RATIO="INF"
        else
            RATIO=`awk "BEGIN {printf \"%.2f\", $WINS/$LOSSES}"`
        fi

        TEMP_DATA+="$PLAYER,$WINS,$LOSSES,$RATIO\n"
    done

    # Sort the temp data based on sort metric
    SORTED_DATA=""
    if [ "$SORT_BY" = "wins" ]; then
        # Sort by wins (field 2) descending
        SORTED_DATA=`echo -e "$TEMP_DATA" | sort -t',' -k2 -rg`
    elif [ "$SORT_BY" = "losses" ]; then
        # Sort by losses (field 3) descending
        SORTED_DATA=`echo -e "$TEMP_DATA" | sort -t',' -k3 -rg`
    elif [ "$SORT_BY" = "ratio" ]; then
        # Sort by ratio (field 4) descending; put "INF" on top
        SORTED_DATA=`echo -e "$TEMP_DATA" | sort -t',' -k4 -rg`
    fi

    # Print sorted data
    while IFS=',' read -r PLAYER WINS LOSSES RATIO; do
        printf " %-20s %-8s %-8s %-10s\n" "$PLAYER" "$WINS" "$LOSSES" "$RATIO"
    done <<< "$SORTED_DATA"

    echo ""
done

echo -e "\n==============================================\n"
echo "  Sorted by: $SORT_BY"
echo -e "\n==============================================\n"
                                