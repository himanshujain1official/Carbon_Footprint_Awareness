# 🌱 Carbon Zero: Intelligent Carbon Footprint Awareness Platform

> **A smart, dynamic, and context-aware AI assistant designed to help individuals understand, track, and reduce their carbon footprint through natural language.**

## 📖 Overview

**Carbon 0** was developed for **Challenge 3 of the Hack2Skill PromptWars Virtual Hackathon**.

Tracking daily carbon emissions shouldn't require filling out endless forms. This platform leverages Agentic AI to parse natural language—allowing users to simply chat about their day. The system extracts relevant data, computes the carbon footprint, and provides actionable, real-world advice to reduce emissions. 

Visually, the project steps away from traditional white-label dashboards, embracing a minimalist aesthetic. Traditional carbon trackers rely on tedious, multi-step forms. Carbon Zero revolutionizes this by utilizing an Agentic AI approach. Users can simply describe their daily activities in natural conversational language (e.g., *"I drove 20km to work in a petrol car and used my AC for 3 hours"*).

### 🔗 Live Links
* **Live Application:** [Carbon Zero on Google Cloud Run](https://carbon-footprint-platform-1037288381649.asia-south1.run.app)
* **LinkedIn Build-in-Public:** [View Submission Post](https://www.linkedin.com/posts/himanshu-jain-70hj_buildwithai-promptwarsvirtual-challenge3-ugcPost-7472896664685555712-xthP)
  
## ✨ Core Features

* **Smart Dynamic Assistant:** Powered by **Gemini 2.5 Flash**, the chat interface understands unstructured input (e.g., *"I drove 15km in a petrol car and left my AC on for 8 hours"*).
* **Logical Decision Making:** The AI doesn't just calculate numbers; it suggests highly personalized, context-aware alternatives (like carpooling or power-saving modes) along with the projected CO2 savings.
* **Interactive Tracking Dashboard:** Visualizes daily and weekly footprints against standard baselines using clean, responsive data charts.
* **Secure Architecture:** Complete separation of credentials. API keys are injected securely via Google Cloud Secret Manager and Streamlit environment variables.
* **Inclusive Design:** Built with a high-contrast Light Mode UI. Features comprehensive `aria-labels`, semantic HTML wrappers, keyboard-navigable focus states, and screen-reader-friendly tooltips.

## 🏗️ Architecture & Tech Stack

* **Core Language:** Python 3.13 (Chosen specifically for strict library stability and optimal runtime execution).
* **Frontend Framework:** Streamlit (with custom injected CSS and semantic HTML tags).
* **AI Engine:** Google Generative AI (`gemini-2.5-flash`).
* **Containerization:** Docker (`python:3.13-slim` base image).
* **Cloud Infrastructure:** Google Cloud Run.
* **Testing:** `pytest` for mathematical validation of emission formulas.

## 🚀 Getting Started (Local Development)

### Prerequisites
* **Python 3.13** installed on your system. (Recommended for library stability and optimal performance)
* Google Gemini API Key

### Installation Steps

1. **Clone the repository:**
   ```
   git clone [https://github.com/himanshujain1official/Carbon_Footprint_Awareness.git](https://github.com/himanshujain1official/Carbon_Footprint_Awareness.git)
   cd Carbon_Footprint_Awareness
   ```
2. **Create a virtual environment (Recommended for Python 3.13 stability):**
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. **Install Dependencies:**
```
pip install --no-cache-dir -r requirements.txt
```
4. **Environment Setup:**
Create a `.env` file or `.streamlit/secrets.toml` file in the root directory:
```
GEMINI_API_KEY="your_api_key_here"
```
5. **Run the Application:**
```
streamlit run app.py
```

### ☁️ Cloud Run Deployment Architecture
The application is built for serverless scalability. The included `Dockerfile` maps Streamlit's default ports to standard Cloud Run `$PORT` configurations.

**Deployment Command used:**
```
gcloud run deploy carbon-footprint-platform \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 8080 \
  --min-instances 0 \
  --max-instances 2
```
(**Note:** The Gemini API Key is injected dynamically as an environment variable in the Cloud Run service instance, completely isolated from the source code).

### 🔬 Testing
To ensure the integrity of the carbon footprint logic and AI parsing, the repository includes mathematical unit tests.
```
pytest tests/test_calculations.py -v
```

### 🧑‍💻 About the Developer
Developed by Himanshu Jain. As a BCA student with a foundational background in biological sciences, I have a deep appreciation for systems that bridge the gap between technology and the environment. This project replaces standard database implementations with a biology/environmental-oriented technical stack to deliver genuine, real-world impact through AI.

Built with ❤️ for #BuildWithAI and the #PromptWarsVirtual Initiative.

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![Framework](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)
![AI Model](https://img.shields.io/badge/Gemini-2.5_Flash-8A2BE2.svg)
![Accessibility](https://img.shields.io/badge/WCAG-AA_Compliant-brightgreen.svg)
![Deployment](https://img.shields.io/badge/Google_Cloud-Run-4285F4.svg)
