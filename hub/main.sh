#!/bin/bash
touch users.tsv
# Authentication function for both login and registration
# If it exists, it verifies the password by comparing the hash of the entered password with the stored hash. 
#If the username does not exist, it offers the option to register a new account by creating a new username and password, hashing the password, and storing it in the users.tsv file. The function also includes input validation for usernames and passwords to ensure they meet certain criteria.
authenticate_user() {
    while true; do
        read -p "Enter username for $1 : " user 
        # It prompts the user for a username and checks if it exists in the users.tsv file. 
        if [[ ! "$user" =~ ^[a-zA-Z0-9_]+$ ]]; then
        echo -e "\e[31mError: Username can only contain letters, numbers and underscores.\e[0m"
        continue
        fi
        if grep -q -E "^${user}[[:space:]]" users.tsv; then # check if the username exists in the users.tsv file
            pass_hash_1=$(grep -E "^${user}$(printf '\t')" users.tsv | awk '{print $2}') # hash entered passwd and compare to stored passwd in users.tsv
            while true; do 
                read -s -p "Enter Password for $user: " Pass1; echo
                pass_hash_2=$(echo -n "$Pass1" | sha256sum | awk '{print $1}') # hashing the entered password using sha256sum
                if [[ "${pass_hash_1}" == "${pass_hash_2}" ]]; then
                    echo -e "\e[32mWelcom back, $user\e[0m"
                    return 0
                else
                    echo -e "\e[31mPassword does not match. Please retry...\e[0m"
                fi
            done
        else
            while true; do
                if [[ -z "${user}" ]]; then
                    echo -e "\e[31mUsername cannot be empty. Please enter a valid username.\e[0m"
                    break
                fi

                read -p "Username '$user' not found, do you want to register? (Y/N): " a 
                # If the username does not exist, it offers the option to register a new account by creating a new username and password
                if [[ ${a} == "Y" || ${a} == "y" ]]; then
                    while true; do
                        
                        while true; do
                        read -s -p "Create Password: " new_pass; echo # conditions on password
                        if [[ ${#new_pass} -lt 8 || ! "$new_pass" =~ [A-Z] || ! "$new_pass" =~ [a-z] || ! "$new_pass" =~ [0-9] ]]; then
                            echo -e "\e[31mWeak Password! Requirements: 8 or more chars, Uppercase, Lowercase, and Number.\e[0m"
                        else 
                            break
                        fi
                        done
                        read -s -p "Confirm Password: " confirm_pass; echo
                        if [[ $new_pass == $confirm_pass ]]; then
                            pass_hash=$(echo -n "$new_pass" | sha256sum | awk '{print $1}')
                            echo -e "${user}\t${pass_hash}" >> users.tsv
            
                            echo -e "\e[32mUser '${user}' registered and logged in successfully.\e[0m"
                            return 0  
                         else
                            echo -e "\e[31mPasswords do not match! Please try again.\e[0m"
                        fi
                    done
                    
                    # Store only the hash part
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
#Password change function
change_password() {
    read -p "Enter your username: " user
    if grep -q -E "^${user}[[:space:]]" users.tsv; then
            # Works on most systems (using a literal tab via printf)
            stored_hash=$(grep -E "^${user}$(printf '\t')" users.tsv | awk '{print $2}')
        # Verify old password
        read -s -p "Enter current password: " old_pass; echo
        old_hash=$(echo -n "$old_pass" | sha256sum | awk '{print $1}')
        if [[ "$old_hash" != "$stored_hash" ]]; then
            echo -e "\e[31mIncorrect current password.\e[0m"
            return
        fi
        # Enter new password
        while true; do
            while true; do
            read -s -p "Enter new password: " new_pass; echo
            if [[ ${#new_pass} -lt 8 || ! "$new_pass" =~ [A-Z] || ! "$new_pass" =~ [a-z] || ! "$new_pass" =~ [0-9] ]]; then
                echo -e "\e[31mWeak Password! Requirements: 8 or more chars, Uppercase, Lowercase, and Number.\e[0m"
            else
                break
            fi
            done
            read -s -p "Confirm new password: " confirm_new_pass; echo
            if [[ $new_pass == $confirm_new_pass ]]; then
                new_hash=$(echo -n "$new_pass" | sha256sum | awk '{print $1}')
                # Replace old password in file
                sed -i "s/^${user}\t.*/${user}\t${new_hash}/" users.tsv
                echo -e "\e[32mPassword updated successfully.\e[0m"
                return 0
            else echo -e "\e[31mPasswords do not match! Please try again.\e[0m"
            fi
        done
        # new_hash=$(echo -n "$new_pass" | sha256sum | awk '{print $1}')
        # # Replace old password in file
        # sed -i "s/^${user}\t.*/${user}\t${new_hash}/" users.tsv
        # echo -e "\e[32mPassword updated successfully.\e[0m"
    else
        echo -e "\e[31mUsername not found.\e[0m"
    fi
}
#figlet "WELCOME TO FUNGRID" # used this to get this formatting and then copied and pasted
clear
echo -e "\e[31m"
echo -E '__        _______ _     ____ ___  __  __ _____   _____ ___'
echo -E '\ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \' 
echo -E ' \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | |'
echo -E '  \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| |'
echo -E '   \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/' 
                               echo -E                             
echo -E '         _____ _   _ _   _  ____ ____  ___ ____'  
echo -E '        |  ___| | | | \ | |/ ___|  _ \|_ _|  _ \' 
echo -E '        | |_  | | | |  \| | |  _| |_) || || | | |'
echo -E '        |  _| | |_| | |\  | |_| |  _ < | || |_| |'
echo -E '        |_|    \___/|_| \_|\____|_| \_\___|____/' 
echo -e "\e[0m"
echo
while true; do

    echo "1. Login / Register"
    echo "2. Change Password"
    echo "3. Exit"
    read -p "Choose an option: " choice
    if [[ $choice -eq 1 ]]; then
        break
    elif [[ $choice -eq 2 ]]; then
        change_password
    elif [[ $choice -eq 3 ]]; then
        exit 0
    else
        echo -e "\e[31mInvalid choice. Please select 1, 2, or 3.\e[0m"
    fi
done
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
python3 game.py "$Player1" "$Player2"