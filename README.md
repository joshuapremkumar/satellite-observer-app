# Satellite Observer Intelligence Assistant

This is a Streamlit-based web application that helps astronomers track and study man-made satellites in real time. It fetches orbital data from CelesTrak, computes live satellite positions, retrieves insights about ground locations using Tavily, and generates AI summaries using CopilotKit. Optional login/authentication is handled via Appwrite.

---

## 🌐 Live Demo
Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) by connecting this repo.

---

## 📁 Project Structure
```
📦 satellite-observer-app
├── app.py                   # Main Streamlit frontend app
├── satellite_utils.py       # CelesTrak data + satellite position calculator
├── tavily_utils.py          # Tavily search integration
├── copilotkit.py            # CopilotKit AI assistant
├── appwrite_config.py       # Appwrite login handler
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/satellite-observer-app.git
cd satellite-observer-app
```

### 2. Create a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
You need a Tavily API key to run the search feature.
```bash
export TAVILY_API_KEY="your_tavily_api_key"  # On Windows: set TAVILY_API_KEY=...
```

### 5. Run the App
```bash
streamlit run app.py
```

---

## 🔑 Optional: Setup Appwrite for Authentication
1. Create a free [Appwrite](https://appwrite.io/) project.
2. Create a user using the Authentication tab.
3. Get the **project ID** and **endpoint** from Appwrite dashboard.
4. Replace placeholders in `appwrite_config.py` with your actual values.

---

## 🔍 Features
- Search satellites by NORAD Catalog Number using [CelesTrak](https://celestrak.org/).
- Compute live position from orbital elements.
- Use [Tavily](https://www.tavily.com/) for context-aware location insights.
- Get AI-powered summaries from [CopilotKit](https://www.copilotkit.ai/).
- Login users via Appwrite.

---

## 📦 Deployment
### Streamlit Cloud
1. Push this repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and deploy it from GitHub.
3. Set the `TAVILY_API_KEY` in the app settings.

---

## 🤝 Contributions
PRs and suggestions welcome! Please open an issue first to discuss major changes.

---

## 📄 License
[MIT](LICENSE)

---

## 📫 Contact
For questions or collaboration, reach out to `your-email@example.com`.

> Powered by CelesTrak, Tavily, CopilotKit, Appwrite, and Streamlit 🌌
