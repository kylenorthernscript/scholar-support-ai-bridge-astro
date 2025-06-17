#!/bin/bash

echo "GitHub Push Helper for Claude Code"
echo "=================================="
echo ""
echo "Choose authentication method:"
echo "1) GitHub CLI (recommended)"
echo "2) Personal Access Token"
echo "3) Exit"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting GitHub CLI authentication..."
        gh auth login --web
        if [ $? -eq 0 ]; then
            echo "Authentication successful! Pushing changes..."
            git push
        else
            echo "Authentication failed. Please try again."
        fi
        ;;
    2)
        echo ""
        echo "Please create a Personal Access Token at:"
        echo "https://github.com/settings/tokens"
        echo ""
        echo "Required scopes: repo (full control)"
        echo ""
        read -p "Enter your GitHub username: " username
        read -sp "Enter your Personal Access Token: " token
        echo ""
        echo "Pushing changes..."
        git push https://$username:$token@github.com/kylenorthernscript/scholar-support-ai-bridge-astro.git main
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        ;;
esac