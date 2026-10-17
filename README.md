# StreamHub 🎬🍿

StreamHub is a modern, responsive web application for exploring trending movies, popular TV series, genre-based catalogs, and detailed actor profiles. Built with a Django backend and styled using Tailwind CSS, it seamlessly integrates with the TMDB (The Movie Database) API to deliver continuous title browsing, dynamic multi-server streaming embed options, and a client-side watchlist.

---

## 🌟 Key Features

- **Dynamic Content Filtering:** Switch seamlessly between **All Content**, **Movies Only**, and **TV Series Only** directly from the home dashboard.
- **Genre & Search Browsing:** Filter content by genres (Action, Comedy, Sci-Fi, Horror, Animation, etc.) or search for specific titles using real-time query handling.
- **Hero Title Showcase:** Highlights top trending titles with high-resolution backdrops and direct watch access.
- **Continuous / Infinite Scrolling:** Dynamically loads additional title pages as the user scrolls without requiring manual page reloads.
- **Interactive Watch Page & Multi-Server Streaming:**
  - Multi-server embed selection for reliability.
  - Interactive Season & Episode selector for TV series.
  - Complete media overview and rating stats.
- **Actor & Crew Profiles:** Detailed actor biography, department information, and a grid of top-rated known works.
- **Local Watchlist:** Save favorite movies and TV shows directly to your browser's local storage for easy access later.
- **Modern Glassmorphic UI:** Clean, dark-mode design with smooth animations, ambient light accents, and responsive layout built with Tailwind CSS.

---

## 🖼️ Screenshots

> *Note: Place your screenshots inside a folder named `screenshots/` in your repository root.*

### 📍 Home Dashboard & Content Filter
![StreamHub Home Showcase](screenshots/home.png)

### 📍 Title Detail & Streaming Player
![StreamHub Watch Screen](screenshots/watch.png)

### 📍 Actor Profile & Filmography
![StreamHub Actor Page](screenshots/actor.png)

### 📍 Personal Watchlist
![StreamHub Watchlist Screen](screenshots/watchlist.png)

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, Tailwind CSS, JavaScript (ES6)
- **External API:** TMDB (The Movie Database) API
- **Database:** SQLite3 (Django Default)
- **State Management:** Client-Side Browser `localStorage` (Watchlist)

---

## 🚀 Step-by-Step Setup Instructions

Follow these steps to set up and run StreamHub locally on your machine.

### 1. Prerequisites
Ensure you have Python installed on your system:
- Python 3.10 or higher
- `pip` (Python package manager)

### 2. Clone the Repository
Clone this repository to your local machine:
```bash
git clone [https://github.com/MrNoBody0402/StreamHUB.git](https://github.com/MrNoBody0402/StreamHUB.git)
cd StreamHUB
