#!/bin/bash
touch users.tsv
# --Authentication function--

authenticate_user() {
    while true; do
        read -p "Enter username for $1 : " user
        if grep -q -P "^${user}\t" users.tsv; then
            pass_hash_1=$(grep -P "^${user}\t" users.tsv| awk '{print $2}')

            while true; do
                read -s -p "Enter Password for $user: " Pass1; echo
                pass_hash_2=$(echo -n "$Pass1" | sha256sum | awk '{print $1}')
                if [[ "${pass_hash_1}" == "${pass_hash_2}" ]]; then
                    echo -e "\e[32mLogin successful\e[0m"
                    return 0
                else
                    echo -e "\e[31mPassword does not match. Please retry...\e[0m"
                fi
            done
        else
            while true; do
                read -p "Username '$user' not found, do you want to register? (Y/N): " a
                if [[ ${a} == "Y" || ${a} == "y" ]]; then
                    read -s -p "Create Password: " new_pass; echo
                    # Store only the hash part
                    pass_hash=$(echo -n "$new_pass" | sha256sum | awk '{print $1}')
                    echo -e "${user}\t${pass_hash}" >> users.tsv
                    echo -e "\e[32mUser '${user}' registered and logged in successfully.\e[0m"
                    return 0
                elif [[ ${a} == "N" || ${a} == "n" ]]; then
                    echo "Returning back."
                    break
                else
                    echo -e "\e[31mUnknown input. Please input Y or N.\e[0m"
                fi
            done
        fi
    done
}

# --First authentication
authenticate_user "Player 1"
Player1=${user}

# --Second authentication
while true; do
    authenticate_user "Player 2"
    Player2=${user}

    if [[ "${Player1}" == "${Player2}" ]]; then
        echo -e "\e[31mBoth players cannot be the same ($Player1). Please use a different account.\e[0m"
    else
        break
    fi
done
