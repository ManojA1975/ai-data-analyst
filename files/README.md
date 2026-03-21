# 🤖 AI Data Analyst

An intelligent, AI-powered data analysis web app built with **Streamlit** and **Claude (Anthropic)**. Upload any CSV or Excel file and get instant insights, beautiful visualizations, and the ability to chat with your data in natural language.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![Claude](https://img.shields.io/badge/Claude-AI-purple?logo=anthropic)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📁 **Multi-format Upload** | CSV, XLSX, XLS support |
| 📊 **Auto Visualizations** | Distributions, correlations, custom charts (Plotly) |
| 🔍 **Statistical Analysis** | Descriptive stats, outlier detection, missing values |
| 💬 **Chat with Data** | Natural language Q&A powered by Claude AI |
| 📄 **AI Report** | One-click comprehensive report with recommendations |
| 📥 **Export** | Download AI reports as Markdown |

---

## 🖼️ Screenshots

### Dashboard Overview
> Upload your dataset → instant summary with row count, column info, missing values

### Visualizations
> Auto-generated distribution plots, correlation heatmaps, and a drag-and-drop chart builder

### Chat Interface
> Ask anything: *"What are the top 3 factors influencing sales?"* → get structured AI answers

### AI Report
> Full analyst-grade report: trends, anomalies, business recommendations

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your Anthropic API key
Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Open in browser
The app will open automatically at `http://localhost:8501`

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Add your `ANTHROPIC_API_KEY` in Secrets settings
6. Deploy! 🎉

---

## 📁 Project Structure

```
ai-data-analyst/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── sample_data/
│   └── sample_sales.csv   # Demo dataset
├── .gitignore
└── README.md
```

---

## 🧠 How It Works

```
User uploads CSV/Excel
        ↓
Pandas reads & parses data
        ↓
Plotly generates auto visualizations
        ↓
User asks a question (or clicks Generate Report)
        ↓
Data summary sent to Claude API
        ↓
Claude returns structured insights
        ↓
Results displayed in beautiful UI
```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit, custom CSS
- **Visualization:** Plotly Express, Plotly Graph Objects
- **Data:** Pandas, NumPy
- **AI:** Anthropic Claude (claude-sonnet-4)
- **Language:** Python 3.10+

---

## 📊 Sample Datasets to Try

- [Kaggle Titanic Dataset](https://www.kaggle.com/c/titanic/data)
- [Iris Dataset](https://archive.ics.uci.edu/ml/datasets/iris)
- [Sales Data Sample](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

Built with ❤️ using Claude AI + Streamlit
