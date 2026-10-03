# TripsNTips

### AI-Powered Travel Itinerary Optimizer | Hackathon Project

TripsNTips is a travel itinerary optimization application designed to help users plan trips efficiently. It aims to organize travel destinations into practical itineraries based on user preferences and travel requirements.

## Problem Statement

Planning a trip across multiple destinations can be time-consuming. Travelers need to organize locations, decide the order of visits, and manage their available time.

## Our Solution

TripsNTips provides a platform for organizing destinations and generating optimized travel itineraries using route-planning and optimization techniques.

## Key Features

- Travel itinerary planning
- Destination and route organization
- Route optimization
- Interactive route and itinerary display
- React-based frontend
- Python Flask backend

*Note: Features depend on the functionality implemented in the current version.*

## Technology Stack

**Frontend**
- React
- TypeScript
- Vite
- CSS

**Backend**
- Python
- Flask

## Project Structure

```text
TripsNTips/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── data/
│   ├── optimizer/
│   └── tests/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── main.tsx
│   └── styles.css
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Getting Started

### Prerequisites

Install Python and Node.js on your computer.

### Run the Backend

Open a terminal in the project directory:

```bash
cd backend
py -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies and start the Flask server:

```bash
python -m pip install -r requirements.txt
python app.py
```

### Run the Frontend

Open a second terminal in the project directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in your browser.

*If your downloaded project has `src/` and `package.json` directly in the root, run the frontend commands from the root directory instead of `frontend/`.*

## Project Status

Hackathon project — functionality and optimization algorithms should be tested against the current implementation.

## Repository

Source code: https://github.com/vamshi5272/TripsNTTips
