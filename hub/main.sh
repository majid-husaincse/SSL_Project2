#!/bin/bash
touch users.tsv
# --Authentication function--
authenticate_user() {
    while true; do
        read -p "Enter username for $1 : " user
        if [[ ! "$user" =~ ^[a-zA-Z0-9_]+$ ]]; then
        echo -e "\e[31mError: Username can only contain letters, numbers and underscores.\e[0m"
        continue
        fi
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
                if [[ -z "${user}" ]]; then
                    echo -e "\e[31mUsername cannot be empty. Please enter a valid username.\e[0m"
                    break
                fi

                read -p "Username '$user' not found, do you want to register? (Y/N): " a
                if [[ ${a} == "Y" || ${a} == "y" ]]; then
                    while true; do
                        read -s -p "Create Password: " new_pass; echo
                        if [[ ${#new_pass} -lt 8 || ! "$new_pass" =~ [A-Z] || ! "$new_pass" =~ [a-z] || ! "$new_pass" =~ [0-9] ]]; then
                            echo -e "\e[31mWeak Password! Requirements: 8+ chars, Uppercase, Lowercase, and Number.\e[0m"
                        else
                            break
                        fi
                    done
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
#Password change function
change_password() {
    read -p "Enter your username: " user
    if grep -q -P "^${user}\t" users.tsv; then
        stored_hash=$(grep -P "^${user}\t" users.tsv | awk '{print $2}')
        # Verify old password
        read -s -p "Enter current password: " old_pass; echo
        old_hash=$(echo -n "$old_pass" | sha256sum | awk '{print $1}')
        if [[ "$old_hash" != "$stored_hash" ]]; then
            echo -e "\e[31mIncorrect current password.\e[0m"
            return
        fi
        # Enter new password
        while true; do
            read -s -p "Enter new password: " new_pass; echo
            if [[ ${#new_pass} -lt 8 || ! "$new_pass" =~ [A-Z] || ! "$new_pass" =~ [a-z] || ! "$new_pass" =~ [0-9] ]]; then
                echo -e "\e[31mWeak Password! Requirements: 8+ chars, Uppercase, Lowercase, and Number.\e[0m"
            else
                break
            fi
        done
        new_hash=$(echo -n "$new_pass" | sha256sum | awk '{print $1}')
        # Replace old password in file
        sed -i "s/^${user}\t.*/${user}\t${new_hash}/" users.tsv
        echo -e "\e[32mPassword updated successfully.\e[0m"
    else
        echo -e "\e[31mUsername not found.\e[0m"
    fi
}
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
