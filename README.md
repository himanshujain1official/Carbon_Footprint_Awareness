# 🌍 Carbon Footprint Awareness Platform

> **A smart, dynamic, and context-aware AI assistant designed to help individuals understand, track, and reduce their carbon footprint through natural language.**

## 📖 Overview

Tracking daily carbon emissions shouldn't require filling out endless forms. This platform leverages Agentic AI to parse natural language—allowing users to simply chat about their day. The system extracts relevant data, computes the carbon footprint, and provides actionable, real-world advice to reduce emissions. 

Visually, the project steps away from traditional white-label dashboards, embracing a minimalist "deep and dark internet wisdom" aesthetic. It features high-contrast neon glowing buttons and interactive 3D text particles powered by Three.js, ensuring an immersive, focused user experience.

## ✨ Core Features

* **Smart Dynamic Assistant:** Powered by **Gemini 2.5 Flash**, the chat interface understands unstructured input (e.g., *"I drove 15km in a petrol car and left my AC on for 8 hours"*).
* **Logical Decision Making:** The AI doesn't just calculate numbers; it suggests highly personalized, context-aware alternatives (like carpooling or power-saving modes) along with the projected CO2 savings.
* **Interactive Tracking Dashboard:** Visualizes daily and weekly footprints against standard baselines using clean, responsive data charts.
* **Immersive Cyber-Forensic UI:** Built with custom injected CSS and a Three.js canvas for an accessible yet visually striking dark-mode experience.

## 🏗️ Architecture & Tech Stack

* **Frontend:** Streamlit with Custom HTML/CSS/JS (Three.js integration)
* **Backend & AI Agent:** Python 3.13, Google Generative AI (`gemini-2.5-flash`)
* **Mathematical Engine:** Custom Python modules validated via `pytest`
* **Containerization & Deployment:** Docker, Google Cloud Run

## 🚀 Getting Started (Local Development)

### Prerequisites
* **Python 3.13** (Recommended for library stability and optimal performance)
* Google Gemini API Key

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/carbon-footprint-platform.git](https://github.com/yourusername/carbon-footprint-platform.git)
    cd carbon-footprint-platform
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3.13 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API key:
    ```env
    GEMINI_API_KEY="your_actual_api_key_here"
    ```

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🧪 Testing

Ensuring the accuracy of carbon calculations is critical. We use `pytest` to validate the underlying mathematical logic.
To run the test suite:
```bash
pytest tests/test_calculations.py -v
```

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![AI Model](https://img.shields.io/badge/Gemini-2.5_Flash-8A2BE2.svg)
![Deployment](https://img.shields.io/badge/Google_Cloud-Run-4285F4.svg)
