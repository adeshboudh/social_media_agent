# Social Media Agent

## 📌 Project Overview

This project automates **social media post generation** using **CrewAI** and **Gemini LLM**. It:

- Conducts **automated research** on a given topic.
- Generates **platform-specific** posts for Instagram, Facebook, Twitter, and LinkedIn.
- Uses **a smart AI Manager** to assign tasks dynamically.

## 🚀 How It Works

1. **Research Crew**: Gathers relevant information, hashtags, and images for the given topic.
2. **Dynamic Platform Agent**: Based on the user's selected platform (e.g., Instagram, Facebook, Twitter, LinkedIn), a specialized content creator agent is instantiated for that platform only.
3. **Post Creation**: The platform agent generates an optimized post using the research results, following platform-specific best practices and formatting.
4. **Image & Hashtag Integration**: The post includes relevant images and hashtags tailored for the selected platform.
5. **Output**: The final, ready-to-publish post is saved to a file and/or returned to the user.

> **Note:** There is no manager agent. The system dynamically creates the correct platform agent at runtime based on user input.

## 📁 Folder Structure (Full)

```
project_root/
├── .env                       # Environment variables
├── .gitignore                 # Git ignore file
├── .venv/                     # Python virtual environment
├── src/
    └── social_media_agent/
        ├── __init__.py
        ├── main.py            # Main entry point
        ├── tools/
        │   ├── __init__.py
        │   └── custom_tool.py # Custom LLM/search tools
        └── crews/
            ├── evaluation_crew/
            │   ├── evaluation_crew.py
            │   └── config/
            │       ├── agents.yaml
            │       └── tasks.yaml
            ├── image_crew/
            │   ├── image_crew.py
            │   └── config/
            │       ├── agents.yaml
            │       └── tasks.yaml
            ├── modify_crew/
            │   ├── modify_crew.py
            │   └── config/
            │       ├── agents.yaml
            │       └── tasks.yaml
            ├── post_crew/
            │   ├── post_crew.py
            │   └── config/
            │       ├── agents.yaml
            │       └── tasks.yaml
            └── research_crew/
                ├── research_crew.py
                └── config/
                    ├── agents.yaml
                    └── tasks.yaml
├── crewai_flow.html           # CrewAI flow visualization
├── pyproject.toml             # Project dependencies/config
├── README.md                  # Project documentation
├── social-media-agent.ipynb   # Jupyter notebook for testing
└── uv.lock                    # Dependency lock file
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

## 🔧 Configuration

The project is highly configurable and modular. You can customize agents, tasks, and tools as follows:

- **Agent and Task Configuration:**

  - Each crew (e.g., research, post, image, evaluation, modify) has its own `config/agents.yaml` and `config/tasks.yaml` files under `src/social_media_agent/crews/<crew_name>/config/`.
  - Edit these YAML files to define agent roles, goals, and task descriptions for each step of the workflow.
  - The post agent is dynamically created for the selected platform (Instagram, Facebook, Twitter, LinkedIn) at runtime.

- **Custom Tools:**

  - Extend or modify LLM and search tool logic in `src/social_media_agent/tools/custom_tool.py`.
  - Add new tools or change model parameters as needed for your use case.

- **Environment Variables:**

  - API keys and other secrets are set in the `.env` file at the project root.
  - Required: `GEMINI_API_KEY`, `SERPER_API_KEY` (see Installation and Setup).

- **Dependencies:**
  - All dependencies are managed in `pyproject.toml`.
  - Use `uv` or `crewai` to install and sync dependencies.

> For advanced customization, you can add new crews, agents, or tasks by following the structure in the `src/social_media_agent/crews/` directory.

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

## 🐍 Requirements

- **Python**: >=3.10, <3.13
- **Dependencies**: CrewAI, Streamlit, and others (see `pyproject.toml`).
- **.env file**: Required for API keys (see setup instructions above).

## 🏛️ Architecture Overview

- **Backend**: CrewAI orchestrates multiple agents (Manager, Researcher, Social Media, Image, Evaluation, Modify) for post generation.
- **Frontend**: Streamlit app for user-friendly post creation.
- **Custom Tools**: Extendable via `src/social_media_agent/tools/custom_tool.py`.

## 🔗 Future Improvements

- ✅ Add **more customization** for social media formats.
- ✅ Improve **content personalization** based on trends.
- ✅ Optimize **image search for better results**.

🚀 **Now, you're all set to automate social media posts!**

## 🤝 Contributions

Feel free to submit PRs or report issues! 🚀

## 📜 License

MIT License - Free to use and modify.
