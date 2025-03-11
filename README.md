# Social Media Agent

## 📌 Project Overview

This project automates **social media post generation** using **CrewAI** and **Gemini LLM**. It:

- Conducts **automated research** on a given topic.
- Generates **platform-specific** posts for Instagram, Facebook, Twitter, and LinkedIn.
- Uses **a smart AI Manager** to assign tasks dynamically.

## 🚀 How It Works

1. **Researcher Agent** gathers relevant information, hashtags, and images.
2. **Manager Agent** assigns the correct platform-specific content creator.
3. **Social Media Agents** generate optimized posts for the given platform.
4. **Final output** includes the post, hashtags, and an image URL.

## Folder Structure

```
social_media_agent/
├── .venv/                      # Virtual environment (automatically gets created by running kickoff command)
├── src/social_media_agent/
│   ├── crews/post_crew/        # Crew definition
│   │   ├── config/agents.yaml  # Configuration files for agents
│   │   ├── config/tasks.yaml   # Configuration files for tasks
│   │   ├── post_crew.py        # Crew setup file
│   ├── tools/                  # Custom tools for search and AI interactions
│   │   ├── custom_tool.py      # LLM and search tool integration
│   ├── main.py                 # Main entry point for execution
├── .env                        # Environment variables
├── .gitignore                  # Ignore unnecessary files
├── post.md                     # Output generated post
├── pyproject.toml              # Dependencies and package config
├── README.md                   # Project documentation
├── social-media-agent.ipynb    # Jupyter Notebook (Testing)
├── uv.lock                     # uv package lock file
```

## 🔥 Key Features

✅ **Dynamic AI Agents** – Smart task delegation via the Manager.  
✅ **Platform-Specific Content** – Posts optimized for different social media platforms.  
✅ **Real-Time Research** – Uses Serper tool for up-to-date info.  
✅ **Intelligent Image Selection** – Picks the best image from Google Image search.  
✅ **Modular & Extensible** – Easily customizable agents and tasks.

## ⚡ Quickstart

If you have `uv` installed, you can **run the project instantly** without additional setup:

```bash
uv run kickoff
```

## 🏗️ Installation and Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/social-media-agent.git
cd social-media-agent
```

### 2️⃣ Install Dependencies

This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

```bash
uv sync  # Install dependencies (Optional)
```

Or, using CrewAI's installation (For this you should have crewai installed on your environment):

```bash
crewai install
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file and add your API keys:

```
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

## ▶️ Running the Flow

Run the project using one of the following methods:

```bash
uv run kickoff
```

Or using CrewAI Flow:

```bash
crewai flow kickoff
```

## 🔄 How It Works

1. **Manager Agent**: Oversees the entire process and assigns tasks.
2. **Researcher Agent**: Finds relevant content based on the given topic.
3. **Social Media Agents** (Instagram, Facebook, Twitter, LinkedIn): Generate platform-specific posts.
4. **Custom Tooling**: Uses LLMs and search tools to fetch images and refine content.

## 🔧 Configuration

You can **modify agents and tasks** in:

- **`config/agents.yaml`** → Define AI agents (researcher, manager, social media creators).
- **`config/tasks.yaml`** → Define research and content creation tasks.
- **`custom_tool.py`** → Implement custom LLM model and temperature settings.

## 🎯 Example Input & Output

`main`

```python
inputs={'topic': 'Kerala Tourism', 'platform': 'Instagram'}
```

**Generated Instagram Post:**

```plaintext
Experience the magic of Kerala's sunsets! ✨ Golden sands meet turquoise waters in this breathtaking scene from Kovalam Beach.

📍 Plan your unforgettable escape to God's Own Country today!

🌍 #Kerala #TravelPhotography #IncredibleIndia #BeachSunset
```

## 🔗 Future Improvements

- ✅ Add **more customization** for social media formats.
- ✅ Improve **content personalization** based on trends.
- ✅ Optimize **image search for better results**.

🚀 **Now, you're all set to automate social media posts!**

## 🤝 Contributions

Feel free to submit PRs or report issues! 🚀

## 📜 License

MIT License - Free to use and modify.
