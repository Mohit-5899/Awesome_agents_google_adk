# 🤖 AI Agents Collection

> A collection of production-ready AI agents built with Google Agent Development Kit (ADK) and Gemini

[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?logo=google)](https://github.com/google/adk-python)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20%7C%202.5-8E75B2)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)

## 📁 Repository Structure

This repository contains a collection of AI agent projects, each in its own directory with complete documentation and setup instructions.

```
ai-agents/
│
├── ai-news-podcast-agent/     # 🎙️ AI News Podcast Generator
│   ├── agent.py
│   ├── README.md
│   └── ...
│
└── [future-agent-projects]/    # More agents coming soon...
```

## 🎙️ Current Projects

### [AI News Podcast Agent](./ai-news-podcast-agent/)

A comprehensive multi-agent system that researches AI news, analyzes financial data, and generates professional podcasts with audio output.

**Features:**
- 🔍 Real-time news research with source filtering
- 📊 Live stock market data integration
- 📝 Structured markdown report generation
- 🎤 Two-person conversational podcast creation
- 🔊 Multi-speaker audio output (Gemini TTS)
- 🛡️ Production-ready with callbacks & guardrails

**Tech Stack:**
- Google ADK
- Gemini 2.0 Flash Live (voice)
- Gemini 2.5 Flash (text)
- Gemini TTS (audio generation)
- yfinance (financial data)
- Pydantic (structured output)

**[→ View Project Details](./ai-news-podcast-agent/README.md)**

---

## 🚀 Getting Started

Each agent project is self-contained with its own:
- ✅ Complete implementation (`agent.py`)
- ✅ Dependencies (`requirements.txt`)
- ✅ Setup instructions (project `README.md`)
- ✅ Configuration templates (`.env.example`)
- ✅ Automated setup scripts

### Quick Start (Any Agent)

```bash
# Navigate to the agent directory
cd [agent-name]

# Run setup script
chmod +x setup.sh
./setup.sh

# Configure API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start with ADK Web UI
adk web --host 0.0.0.0 --port 8000
```

## 📚 Prerequisites

All agents require:
- **Python 3.10+**
- **Google Gemini API Key** - [Get one here](https://ai.google.dev/)
- **Terminal/Command Line** access

## 🛠️ Technologies Used

- **[Google ADK](https://github.com/google/adk-python)** - Agent Development Kit
- **[Gemini API](https://ai.google.dev/)** - Google's multimodal AI models
- **Python** - Primary programming language
- **Pydantic** - Data validation and schemas
- **FastAPI** - API servers (where applicable)

## 📖 About Google ADK

Google Agent Development Kit (ADK) is a powerful framework for building production-ready AI agents with:
- 🔧 **Custom Tools** - Extend agents with external APIs and functions
- 🤖 **Multi-Agent Systems** - Coordinate multiple specialized agents
- 🛡️ **Callbacks** - Programmatic guardrails and control
- 📊 **Structured Output** - Type-safe responses with Pydantic
- 🎤 **Live Voice** - Real-time bidirectional streaming
- 🔍 **Observability** - Built-in tracing and debugging

## 🎯 Agent Development Patterns

Each agent demonstrates key patterns:

1. **Tool Integration** - Custom functions for external services
2. **Callback Systems** - Before/after hooks for control
3. **Multi-Agent Architecture** - Coordinator + specialist patterns
4. **Structured Data** - Pydantic schemas for reliability
5. **Error Handling** - Graceful degradation and resilience
6. **Production Readiness** - Logging, monitoring, quality control

## 🤝 Contributing

Want to add your own agent to this collection?

1. Create a new directory: `your-agent-name/`
2. Include all standard files:
   - `agent.py` - Main implementation
   - `README.md` - Project documentation
   - `requirements.txt` - Dependencies
   - `.env.example` - Configuration template
   - `setup.sh` - Setup automation
3. Follow the established patterns
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see individual agent directories for details.

## 🙏 Acknowledgments

- **Google Cloud Team** - For the Agent Development Kit
- **DeepLearning.AI** - For comprehensive ADK training
- **Open Source Community** - For tools and inspiration

## 📞 Support & Resources

- 📚 **[Google ADK Documentation](https://google.github.io/adk-docs/)**
- 💬 **[Reddit Community](https://www.reddit.com/r/agentdevelopmentkit/)**
- 🐛 **[GitHub Issues](https://github.com/google/adk-python/issues)**
- 📧 **Email**: mohitmandawat16@gmail.com

---

**Built with ❤️ using Google Agent Development Kit**

⭐ **Star this repo** if you find these agents useful!

🔔 **Watch** for updates when new agents are added!
