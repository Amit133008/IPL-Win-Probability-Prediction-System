# IPL Win Probability Prediction System

A Streamlit-based machine learning application that predicts the probability of a team winning an IPL match using live match conditions such as batting team, bowling team, venue, target, current score, overs completed, and wickets lost.

## Overview

This project is built to estimate the winning chances of a cricket team during an Indian Premier League (IPL) match. It uses a trained machine learning pipeline to analyze match context and return a probability score for the batting side.

The app is designed with a clean dashboard interface and is useful for cricket enthusiasts, students, and data science learners who want to understand how match parameters influence win probability.

## Features

- Predicts win probability for the batting team
- Lets users choose the batting and bowling teams
- Supports venue selection across IPL host cities
- Uses live match metrics such as:
  - target
  - current score
  - overs completed
  - wickets lost
- Displays the result with a visual probability comparison
- Uses a saved trained ML model for inference

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Pickle

## Project Structure

```text
IPL-Win-Probability-Prediction-System/
├── ipl-win-probability/
│   ├── app.py
│   ├── pipe.pkl
│   └── README.md
└── README.md
