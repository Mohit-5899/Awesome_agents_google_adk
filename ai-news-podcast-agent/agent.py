"""
AI News Podcast Agent - Comprehensive Implementation
Combines all concepts from Lessons 1-7:
- Custom tools (financial data, file saving, audio generation)
- Callbacks (source filtering, data freshness, process logging)
- Multi-agent orchestration (coordinator + podcaster)
- Structured output with Pydantic schemas
- Production-ready patterns
"""

import pathlib
import wave
import re
from typing import Dict, List
from urllib.parse import urlparse

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search, ToolContext
from google import genai
from google.genai import types
import yfinance as yf
from pydantic import BaseModel, Field


# ============================================================================
# PYDANTIC SCHEMAS - Structured Output (Lesson 6)
# ============================================================================

class NewsStory(BaseModel):
    """A single news story with comprehensive context."""
    company: str = Field(
        description="Company name associated with the story (e.g., 'Nvidia', 'OpenAI'). Use 'N/A' if not applicable."
    )
    ticker: str = Field(
        description="Stock ticker for the company (e.g., 'NVDA'). Use 'N/A' if private or not found."
    )
    headline: str = Field(
        description="The main headline of the news story."
    )
    summary: str = Field(
        description="A brief, one-sentence summary of the news story."
    )
    why_it_matters: str = Field(
        description="A concise explanation of the story's significance or impact."
    )
    financial_context: str = Field(
        description="Current stock price and change, e.g., '$950.00 (+1.5%)'. Use 'No financial data' if not applicable."
    )
    source_domain: str = Field(
        description="The source domain of the news, e.g., 'techcrunch.com'."
    )
    process_log: str = Field(
        description="Audit trail of data processing and filtering actions."
    )


class AINewsReport(BaseModel):
    """A structured report of the latest AI news."""
    title: str = Field(
        default="AI Research Report",
        description="The main title of the report."
    )
    report_summary: str = Field(
        description="A brief, high-level summary of the key findings in the report."
    )
    stories: List[NewsStory] = Field(
        description="A list of the individual news stories found."
    )


# ============================================================================
# CUSTOM TOOLS - Function Tools (Lessons 3, 4, 6)
# ============================================================================

def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches current stock price and daily change for stock tickers using yfinance.
    
    This tool demonstrates external API integration and error handling best practices.
    
    Args:
        tickers: List of stock market tickers (e.g., ["NVDA", "MSFT", "GOOGL"])
    
    Returns:
        Dictionary mapping each ticker to formatted financial data string
        Example: {"NVDA": "$950.00 (+2.5%)", "MSFT": "$420.50 (-0.8%)"}
    """
    financial_data: Dict[str, str] = {}
    
    # Filter out invalid tickers upfront
    valid_tickers = [
        ticker.upper().strip() 
        for ticker in tickers 
        if ticker and ticker.upper() not in ['N/A', 'NA', '']
    ]
    
    if not valid_tickers:
        return {ticker: "No financial data" for ticker in tickers}
    
    for ticker_symbol in valid_tickers:
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")
            
            if price is not None and change_percent is not None:
                change_str = f"{change_percent * 100:+.2f}%"
                financial_data[ticker_symbol] = f"${price:.2f} ({change_str})"
            else:
                financial_data[ticker_symbol] = "Price data not available."
        except Exception as e:
            financial_data[ticker_symbol] = f"Error: {str(e)[:50]}"
    
    return financial_data


def save_news_to_markdown(filename: str, content: str) -> Dict[str, str]:
    """
    Saves content to a Markdown file in the current directory.
    
    Provides file persistence for research reports and audit trails.
    
    Args:
        filename: Name of the file to save (e.g., 'ai_news.md')
        content: Markdown-formatted string to write to the file
    
    Returns:
        Dictionary with status and message about the operation
    """
    try:
        if not filename.endswith(".md"):
            filename += ".md"
        
        current_directory = pathlib.Path.cwd()
        file_path = current_directory / filename
        file_path.write_text(content, encoding="utf-8")
        
        return {
            "status": "success",
            "message": f"Successfully saved to {file_path.resolve()}",
            "file_path": str(file_path.resolve())
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save file: {str(e)}"
        }


def wave_file(filename: str, pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
    """
    Helper function to save audio data as a WAV file.
    
    Args:
        filename: Path to save the WAV file
        pcm: Raw audio data in PCM format
        channels: Number of audio channels (1 for mono, 2 for stereo)
        rate: Sample rate in Hz (24000 for Gemini TTS)
        sample_width: Bytes per sample (2 for 16-bit audio)
    """
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


async def generate_podcast_audio(
    podcast_script: str,
    tool_context: ToolContext,
    filename: str = "ai_today_podcast"
) -> Dict[str, str]:
    """
    Generates multi-speaker audio from a podcast script using Gemini TTS API.
    
    This demonstrates multimodal AI capabilities and audio generation.
    
    Args:
        podcast_script: Conversational script to be converted to audio
        tool_context: ADK tool context for state management
        filename: Base filename for the audio file (without extension)
    
    Returns:
        Dictionary with status, file information, and audio metadata
    """
    try:
        client = genai.Client()
        prompt = f"TTS the following conversation between Joe and Jane:\n\n{podcast_script}"
        
        # Configure multi-speaker voice synthesis
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=[
                            types.SpeakerVoiceConfig(
                                speaker='Joe',
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
                                )
                            ),
                            types.SpeakerVoiceConfig(
                                speaker='Jane',
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')
                                )
                            )
                        ]
                    )
                )
            )
        )
        
        # Extract audio data
        data = response.candidates[0].content.parts[0].inline_data.data
        
        if not filename.endswith(".wav"):
            filename += ".wav"
        
        current_directory = pathlib.Path.cwd()
        file_path = current_directory / filename
        wave_file(str(file_path), data)
        
        return {
            "status": "success",
            "message": f"Successfully generated podcast audio: {file_path.resolve()}",
            "file_path": str(file_path.resolve()),
            "file_size_bytes": len(data),
            "duration_estimate": f"{len(data) / (24000 * 2):.1f} seconds"
        }
    
    except Exception as e:
        error_msg = str(e)[:200]
        return {
            "status": "error",
            "message": f"Audio generation failed: {error_msg}"
        }


# ============================================================================
# CALLBACKS - Programmatic Guardrails (Lesson 5)
# ============================================================================

# Whitelisted news domains for quality control
WHITELIST_DOMAINS = [
    "techcrunch.com",
    "venturebeat.com",
    "theverge.com",
    "technologyreview.com",
    "arstechnica.com",
    "wired.com",
    "zdnet.com",
    "cnet.com"
]


def filter_news_sources_callback(tool, args, tool_context):
    """
    Before-tool callback: Enforces whitelisted domains for news searches.
    
    Implements content quality control by restricting searches to reputable sources.
    This callback intercepts google_search calls and modifies queries to include
    only whitelisted domains.
    
    Returns:
        None to continue normal execution with modified args
    """
    if tool.name == "google_search":
        original_query = args.get("query", "")
        
        # Check if query already has site restrictions
        if any(f"site:{domain}" in original_query.lower() for domain in WHITELIST_DOMAINS):
            print(f"✓ Query already filtered: '{original_query}'")
            return None
        
        # Add whitelist restriction to query
        whitelist_query_part = " OR ".join([f"site:{domain}" for domain in WHITELIST_DOMAINS])
        args['query'] = f"({original_query}) ({whitelist_query_part})"
        print(f"✓ MODIFIED query with whitelist: '{args['query']}'")
    
    return None


def enforce_data_freshness_callback(tool, args, tool_context):
    """
    Before-tool callback: Adds time filter to search queries for recent news.
    
    Ensures agents only retrieve current information by adding Google's
    time-based search parameter (tbs=qdr:w for past week).
    
    Returns:
        None to continue normal execution with modified args
    """
    if tool.name == "google_search":
        query = args.get("query", "")
        
        # Add freshness filter if not present
        if "tbs=qdr:" not in query:
            args['query'] = f"{query} tbs=qdr:w"
            print(f"✓ MODIFIED query for freshness (past week): '{args['query']}'")
    
    return None


def initialize_process_log(tool_context: ToolContext):
    """Helper to ensure the process_log list exists in the state."""
    if 'process_log' not in tool_context.state:
        tool_context.state['process_log'] = []


def inject_process_log_after_search(tool, args, tool_context, tool_response):
    """
    After-tool callback: Enriches search results with transparency metadata.
    
    This callback demonstrates response enhancement by extracting source domains
    from search results and adding them to an audit trail. Makes control systems
    visible to the LLM for transparent reporting.
    
    Returns:
        Dictionary with search_results and process_log for structured output
    """
    if tool.name == "google_search" and isinstance(tool_response, str):
        # Extract unique source domains from URLs
        urls = re.findall(r'https?://[^\s/]+', tool_response)
        unique_domains = sorted(list(set(urlparse(url).netloc for url in urls)))
        
        if unique_domains:
            sourcing_log = f"📰 Sourced from: {', '.join(unique_domains)}"
            current_log = tool_context.state.get('process_log', [])
            tool_context.state['process_log'] = [sourcing_log] + current_log
        
        final_log = tool_context.state.get('process_log', [])
        print(f"✓ CALLBACK LOG: {final_log}")
        
        # Return structured response with metadata
        return {
            "search_results": tool_response,
            "process_log": final_log
        }
    
    return tool_response


# ============================================================================
# MULTI-AGENT SYSTEM (Lesson 6)
# ============================================================================

# Specialist Agent: Handles audio generation
podcaster_agent = Agent(
    name="podcaster_agent",
    model="gemini-2.0-flash",
    instruction="""
    **Your Identity:**
    You are an Audio Generation Specialist focused on converting podcast scripts
    into high-quality multi-speaker audio files.
    
    **Your Workflow:**
    1. Receive a conversational podcast script from the coordinator
    2. Immediately call `generate_podcast_audio` with the script
    3. Report the result back to the coordinator
    
    **Quality Requirements:**
    - Ensure the script has clear speaker labels (Joe and Jane)
    - Generate natural, conversational audio
    - Handle any audio generation errors gracefully
    """,
    tools=[generate_podcast_audio],
)


# Coordinator Agent: Orchestrates the entire workflow
root_agent = Agent(
    name="ai_news_coordinator",
    model="gemini-2.0-flash-live-001",  # Supports live voice interaction
    instruction="""
    **Your Core Identity:**
    You are an AI News Podcast Producer orchestrating a complete content pipeline:
    research → analysis → report → script → audio. You coordinate specialized tools
    and agents while keeping users informed of progress.
    
    **Operational Philosophy:**
    - **Resilience**: If data is unavailable for one item, use "N/A" and continue
    - **Scope**: Focus on US-listed NASDAQ companies in the AI sector
    - **Transparency**: Document all processing steps in the audit trail
    - **Quality**: Use whitelisted sources and recent data only
    
    **Understanding Enhanced Tool Outputs:**
    The `google_search` tool returns a structured dictionary:
    - `search_results`: The actual search content
    - `process_log`: Audit trail of filtering and sourcing actions
    
    **Complete Workflow (10 Steps):**
    
    1. **Acknowledge Request**
       Reply: "🚀 Starting AI news research for NASDAQ-listed companies. 
       I'll gather data, analyze trends, and create a podcast. This takes ~2 minutes."
    
    2. **Search for News** (Background)
       Use `google_search` with query: "AI artificial intelligence NASDAQ companies latest news"
       The callbacks will automatically filter sources and add freshness constraints.
    
    3. **Extract Metadata** (Internal)
       From search results, identify:
       - Company names
       - Stock tickers (or 'N/A' if not found)
       - News headlines
       - Source domains
    
    4. **Fetch Financial Data** (Background)
       Call `get_financial_context` with extracted tickers.
       Accept "Not Available" without stopping the pipeline.
    
    5. **Structure Report** (Internal)
       Create an `AINewsReport` object with all gathered data.
       Populate `process_log` fields from the search tool output.
    
    6. **Format Markdown** (Internal)
       Convert the structured data to markdown with sections:
       - Executive Summary
       - Top Headlines (with company, ticker, market data, summary)
       - Data Sourcing Notes (from process_log)
    
    7. **Save Report** (Background)
       Call `save_news_to_markdown` with filename "ai_research_report.md"
    
    8. **Create Podcast Script** (Internal)
       Write a natural conversation between:
       - **Joe** (enthusiastic, asks engaging questions)
       - **Jane** (analytical, provides insights)
       Format: "Joe: [dialogue]\nJane: [dialogue]"
       Length: 5-7 exchanges covering the top 3 stories
    
    9. **Generate Audio** (Background)
       Call the `podcaster_agent` tool with the complete script
    
    10. **Final Confirmation**
        Reply: "✅ All done! Created:
        📄 Research report: ai_research_report.md
        🎙️ Podcast audio: ai_today_podcast.wav
        
        The report includes {N} stories with financial context and source attribution."
    
    **Error Handling:**
    - Missing ticker: Use "N/A" and continue
    - API failures: Document in process_log and proceed
    - Partial data: Deliver report with available information
    
    **Quality Assurance:**
    - Verify all tickers are valid NASDAQ symbols
    - Ensure financial data is current (within 24 hours)
    - Confirm all sources are from whitelisted domains
    - Check podcast script has clear speaker labels
    """,
    tools=[
        google_search,
        get_financial_context,
        save_news_to_markdown,
        AgentTool(agent=podcaster_agent)  # Multi-agent orchestration
    ],
    output_schema=AINewsReport,  # Structured output enforcement
    before_tool_callback=[
        filter_news_sources_callback,
        enforce_data_freshness_callback,
    ],
    after_tool_callback=[
        inject_process_log_after_search,
    ]
)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("✓ AI News Podcast Agent initialized successfully")
    print("✓ Loaded tools: google_search, get_financial_context, save_news_to_markdown, generate_podcast_audio")
    print("✓ Loaded callbacks: source filtering, data freshness, process logging")
    print("✓ Multi-agent system: root_agent → podcaster_agent")
    print("\nRun with: adk web --host 0.0.0.0 --port 8000")
