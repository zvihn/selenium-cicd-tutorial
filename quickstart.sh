#!/bin/bash

# Quick Start Script for Selenium CI/CD Tutorial
# This script helps you set up and run the project quickly

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   🚀 Selenium + CI/CD Tutorial - Quick Start           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3 using: brew install python3"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

# Check if Chrome is installed
if ! command -v /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome &> /dev/null; then
    echo -e "${YELLOW}⚠️  Google Chrome not found in Applications${NC}"
    echo "Please install Chrome from: https://www.google.com/chrome/"
    read -p "Press Enter once Chrome is installed..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Main menu
while true; do
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}   What would you like to do?${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo "  1) 🌐 Start the web application"
    echo "  2) 🧪 Run Selenium tests (visible browser)"
    echo "  3) 👻 Run Selenium tests (headless mode)"
    echo "  4) 🚀 Run both (app + tests)"
    echo "  5) 📖 View README"
    echo "  6) 🛑 Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice

    case $choice in
        1)
            echo -e "${GREEN}🌐 Starting Flask application...${NC}"
            echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
            echo -e "${BLUE}Open http://localhost:5000 in your browser${NC}"
            cd app
            python app.py
            cd ..
            ;;
        2)
            echo -e "${GREEN}🧪 Running Selenium tests (visible browser)...${NC}"
            echo ""
            python tests/test_selenium.py
            ;;
        3)
            echo -e "${GREEN}👻 Running Selenium tests (headless)...${NC}"
            echo ""
            export HEADLESS=true
            python tests/test_selenium.py
            unset HEADLESS
            ;;
        4)
            echo -e "${GREEN}🚀 Starting app and running tests...${NC}"
            cd app
            python app.py &
            APP_PID=$!
            cd ..
            
            echo "Waiting for app to start..."
            sleep 3
            
            echo "Running tests..."
            python tests/test_selenium.py
            
            echo "Stopping app..."
            kill $APP_PID
            ;;
        5)
            echo -e "${BLUE}📖 Opening README...${NC}"
            if command -v less &> /dev/null; then
                less README.md
            else
                cat README.md
            fi
            ;;
        6)
            echo -e "${GREEN}👋 Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid choice. Please enter 1-6.${NC}"
            ;;
    esac
done