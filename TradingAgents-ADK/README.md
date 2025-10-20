# TradingAgents - Google ADK Implementation

**Multi-Agent Trading Analysis Framework powered by Google ADK**

Transform market analysis with AI agents that work together to provide comprehensive trading insights.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required API keys:
- `GOOGLE_API_KEY` - Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `ALPHA_VANTAGE_API_KEY` - Get from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

### 3. Run Analysis
```bash
# Analyze NVIDIA
python main.py NVDA

# Analyze for specific date
python main.py AAPL --date 2024-05-10

# Get help
python main.py --help
```

### 4. Use ADK Web UI (Optional)
```bash
cd tradingagents
adk web --host 0.0.0.0 --port 8000
# Open http://localhost:8000
```

---

## 📖 What This Does

**Portfolio Manager** coordinates 4 specialized analysts to provide comprehensive trading decisions:

1. **Market Analyst** - Technical indicators and market trends
2. **News Analyst** - Recent news and macroeconomic analysis  
3. **Social Media Analyst** - Public sentiment and social discussions
4. **Fundamentals Analyst** - Financial statements and company health

All reports are synthesized into a final **BUY/HOLD/SELL** recommendation with detailed reasoning.

### Example Output
```
================================================================================
TradingAgents ADK - Multi-Agent Trading Analysis
================================================================================
Ticker: NVDA
Date: 2024-05-10
================================================================================

[Market Analyst analyzing technical indicators...]
[News Analyst reviewing recent news...]
[Social Media Analyst assessing sentiment...]
[Fundamentals Analyst examining financials...]

================================================================================
ANALYSIS COMPLETE
================================================================================

**FINAL TRADING DECISION: BUY NVDA**

Executive Summary:
Based on comprehensive multi-agent analysis...
```

---

## 🏗️ Architecture

### ADK Agent Hierarchy
```
Portfolio Manager (Root Agent)
├── Market Analyst (Technical Analysis)
│   └── Tools: get_stock_data, get_indicators
├── News Analyst (News & Macroeconomics)  
│   └── Tools: get_news, get_global_news
├── Social Media Analyst (Sentiment)
│   └── Tools: get_news (social sources)
└── Fundamentals Analyst (Financials)
    └── Tools: get_fundamentals, get_balance_sheet, 
                get_cashflow, get_income_statement
```

### Project Structure
```
TradingAgents-ADK/
├── tradingagents/           # Main package
│   ├── agent.py            # Root Portfolio Manager
│   ├── agents/             # 4 Analyst agents
│   ├── tools/              # 10 Financial tools
│   ├── config/             # Configuration
│   ├── dataflows/          # Data vendor integrations
│   ├── utils/              # Memory & utilities
│   └── default_config.py   # Default configuration
├── main.py                 # Command-line interface
├── requirements.txt        # Dependencies
├── .env.example           # API keys template
└── README.md              # This file
```

---

## 🛠️ Features

### Core Capabilities

**4 Specialized Agents**
- Market Analyst (technical indicators)
- News Analyst (news & macroeconomics) 
- Social Media Analyst (sentiment)
- Fundamentals Analyst (financials)

**10 Financial Data Tools**
- Stock data (OHLCV prices)
- Technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Fundamental data (balance sheet, cash flow, income statement)
- News data (company news, global news, insider transactions)

**Complete Data Infrastructure**
- Multiple vendor support (yfinance, alpha_vantage, openai, google)
- Automatic fallback mechanisms
- Configurable data sources

**Memory System**
- ChromaDB-based learning from past trades
- Situation matching for recommendations
- State management utilities

### Technical Indicators Supported

**Moving Averages**: 50 SMA, 200 SMA, 10 EMA  
**MACD**: MACD line, Signal line, Histogram  
**Momentum**: RSI (Relative Strength Index)  
**Volatility**: Bollinger Bands (Upper, Middle, Lower), ATR  
**Volume**: Volume Weighted Moving Average (VWMA)

---

## ⚙️ Configuration

### Data Vendors

Edit `tradingagents/config/default_config.py`:

```python
ADK_CONFIG = {
    "model": "gemini-2.0-flash-exp",  # or "gemini-1.5-pro"
    
    "data_vendors": {
        "core_stock_apis": "yfinance",       # Stock prices
        "technical_indicators": "yfinance",  # Technical analysis
        "fundamental_data": "alpha_vantage", # Financials
        "news_data": "alpha_vantage",        # News
    },
}
```

**Supported Vendors**:
- **Stock Data**: yfinance, alpha_vantage, local
- **Technical Indicators**: yfinance, alpha_vantage, local  
- **Fundamentals**: alpha_vantage, openai, local
- **News**: alpha_vantage, openai, google, local

### Environment Variables

Required in `.env` file:
```env
# Google AI API Key (required)
GOOGLE_API_KEY=your_google_api_key_here

# Alpha Vantage API Key (recommended)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 💻 Usage Examples

### Command Line

```bash
# Basic analysis
python main.py NVDA
python main.py AAPL
python main.py TSLA

# Historical analysis
python main.py NVDA --date 2024-01-15
python main.py AAPL --date 2023-12-01

# Help
python main.py --help
```

### Python API

```python
from main import run_trading_analysis

# Run analysis
result = run_trading_analysis("NVDA", "2024-05-10")
print(result)

# Multiple analyses
tickers = ["NVDA", "AAPL", "TSLA", "GOOGL"]
for ticker in tickers:
    decision = run_trading_analysis(ticker)
    print(f"{ticker}: {decision}")
```

### ADK Web UI

```bash
# Start ADK web interface
cd tradingagents
adk web --host 0.0.0.0 --port 8000

# Features available in UI:
# - Interactive chat with Portfolio Manager
# - Visual agent delegation flow
# - Tool invocation tracking
# - Decision reasoning transparency
# - Debug capabilities
```

---

## 🔧 Development

### Adding New Agents

Create a new agent file in `tradingagents/agents/`:

```python
from google.genai import types
from tradingagents.tools.your_tools import your_tool

AGENT_INSTRUCTION = """
Your agent instructions here...
"""

your_agent = types.Agent(
    name="Your Agent",
    model="gemini-2.0-flash-exp", 
    instructions=AGENT_INSTRUCTION,
    tools=[your_tool],
)
```

Then add to the root agent in `tradingagents/agent.py`:

```python
root_agent = types.Agent(
    name="Portfolio Manager",
    agents=[
        existing_agents...,
        your_agent,  # Add your new agent
    ],
)
```

### Adding New Tools

Create tool functions in `tradingagents/tools/`:

```python
from typing import Annotated

def your_tool(
    param: Annotated[str, "parameter description"],
) -> str:
    """
    Tool description for ADK to understand when to use it.
    
    Args:
        param: Parameter description
    
    Returns:
        Result description
    """
    # Your implementation
    return result
```

### Memory Integration

The memory system is available in `tradingagents/utils/memory.py`:

```python
from tradingagents.utils.memory import FinancialSituationMemory

# Initialize memory
memory = FinancialSituationMemory("agent_name", config)

# Add past experiences
memory.add_situations([
    ("Market situation description", "What we learned"),
    ("Another situation", "Another lesson"),
])

# Retrieve relevant memories
current_situation = "Current market analysis..."
memories = memory.get_memories(current_situation, n_matches=2)
```

---

## 🚨 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**API Key Errors**
```bash
# Solution: Check your .env file
cat .env  # Verify keys are present and correct
```

**Data Vendor Errors**
```bash
# Solution: Check Alpha Vantage API key and rate limits
# Free tier: 25 requests/day
# TradingAgents tier: 60 requests/minute
```

**Module Not Found**
```bash
# Solution: Make sure you're in the correct directory
cd TradingAgents-ADK
python main.py NVDA
```

### Debug Mode

Set environment variable for verbose logging:
```bash
export ADK_DEBUG=1
python main.py NVDA
```

### Rate Limits

**Alpha Vantage**:
- Free tier: 25 requests per day
- TradingAgents users: 60 requests per minute (no daily limit)
- Premium: Higher limits available

**Google AI**:
- Free tier: Generous limits for development
- Check current limits in Google AI Studio

---

## 📊 Understanding the Analysis

### Analysis Components

1. **Technical Analysis**
   - Price trends and momentum indicators
   - Support and resistance levels
   - Volume analysis
   - Moving averages and crossovers

2. **Fundamental Analysis** 
   - Financial statement analysis
   - Company health metrics
   - Revenue and profit trends
   - Balance sheet strength

3. **News Analysis**
   - Recent company news impact
   - Macroeconomic trends
   - Industry developments
   - Regulatory changes

4. **Sentiment Analysis**
   - Social media sentiment trends
   - Public perception analysis
   - Insider activity
   - Market sentiment indicators

### Output Interpretation

**Decision Format**: `BUY/HOLD/SELL [TICKER]`

**Confidence Levels**:
- High confidence: Multiple indicators align
- Medium confidence: Mixed signals with slight bias
- Low confidence: Conflicting signals

**Supporting Evidence**:
- Technical indicator values and trends
- Fundamental metric analysis
- News impact assessment
- Sentiment score interpretation

---

## 🆚 Comparison with Original

### What's the Same
- ✅ Same data sources (yfinance, Alpha Vantage)
- ✅ Same analysis tools and indicators
- ✅ Same configuration system
- ✅ Same vendor routing infrastructure

### What's Different
- 🔄 **Framework**: Google ADK instead of LangGraph
- 🔄 **Orchestration**: Agent hierarchy vs. StateGraph
- 🔄 **Workflow**: Natural delegation vs. explicit edges
- 🔄 **Code**: 66% less orchestration code

### What's Better
- ✨ **Simpler codebase** (348KB vs 9.5MB)
- ✨ **Better observability** (ADK web UI)
- ✨ **Natural agent hierarchy**
- ✨ **Modern framework** (Google's latest)

### Simplified Features

These were intentionally simplified (can be re-added):
- **Bull/Bear Debate** → Portfolio Manager considers multiple perspectives
- **Risk Management Team** → Integrated into decision process  
- **Trader Agent** → Integrated into Portfolio Manager
- **Reflection System** → Can use ADK callbacks

---

## 📈 Performance

### Response Times
- **Single analysis**: 30-60 seconds (depending on data availability)
- **API calls**: 10-20 per analysis (varies by ticker and date range)
- **Data caching**: Automatic for repeated queries

### Accuracy
- **Technical indicators**: Real-time market data
- **Fundamental data**: Latest available financial statements
- **News analysis**: Past 7 days by default
- **Sentiment**: Multiple source aggregation

### Scalability
- **Concurrent analyses**: Limited by API rate limits
- **Historical analysis**: Efficient data vendor fallbacks
- **Memory usage**: Lightweight ADK implementation

---

## 🛡️ Security & Privacy

### API Keys
- Stored in `.env` file (not committed to git)
- Required: Google AI, recommended: Alpha Vantage
- Never logged or transmitted unnecessarily

### Data Handling
- No personal data storage
- Financial data fetched in real-time
- Memory system stores analysis patterns only
- Compliance with data provider terms

### Safe Usage
- For research and analysis purposes
- Not financial advice
- Past performance doesn't guarantee future results
- Always verify with additional sources

---

## 📚 Resources

### Documentation
- **Google ADK**: https://ai.google.dev/adk
- **Alpha Vantage API**: https://www.alphavantage.co/documentation/
- **yfinance**: https://pypi.org/project/yfinance/

### Original Project
- **GitHub**: https://github.com/TauricResearch/TradingAgents
- **Paper**: https://arxiv.org/abs/2412.20138

### Getting Help
- Check this README for common issues
- Review error messages carefully
- Verify API keys and internet connection
- Check data vendor status pages

---

## 📄 License

Same as original TradingAgents project.

**Disclaimer**: This software is for research and educational purposes only. It is not intended as financial, investment, or trading advice. Trading involves substantial risk and may not be suitable for all investors. Past performance is not indicative of future results.

---

## 🎯 What's Next

### Ready to Use
- ✅ **Test it**: `python main.py NVDA`
- ✅ **Explore**: Try different tickers and dates
- ✅ **Debug**: Use ADK web UI for insights

### Optional Enhancements
- Add bull/bear debate agents
- Implement risk management team
- Integrate reflection system
- Add more data sources

### Advanced Usage
- Batch analysis multiple tickers
- Historical backtesting integration
- Custom trading strategies
- Portfolio optimization

---

**Happy Trading!** 📈🚀

*Built with Google ADK • Modern AI Agent Framework*