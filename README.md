🤖 AI Research Agent
AI Research Agent is an interactive Streamlit-based web application that leverages Clarifai's LLM API and CrewAI's Agent-Oriented Programming to deliver insightful research reports on any topic. Powered by AI, the agent specializes in comprehensive, market, trend, and technology analysis types — presenting data-driven insights in a well-structured, easy-to-understand format.


🚀 Features:
📌 Clarifai LLM Integration: Uses Clarifai-hosted large language models for reliable and scalable performance.

👨‍💼 Agent Profile: A virtual Senior Research Analyst with domain expertise in tech, business, and trends.

🎯 Multiple Analysis Modes: Choose between comprehensive, market, technology, or trend analyses.

💡 Predefined Topics: Easily try the agent with one-click example topics.

📊 Rich UI: Built with custom CSS and Streamlit for an intuitive user experience.

📁 Report Download: Download the complete analysis report in plain text format.




🧠 How It Works:
User Input: Enter a research topic and select the type of analysis.

Clarifai LLM: The agent communicates with Clarifai’s LLM using your API key.

CrewAI Agent: A CrewAI agent is instantiated with a clear goal and backstory.

Task Execution: A Task is generated and processed by the agent using sequential logic.

Output: The result is displayed in a structured report format with download options.



🛠️ Setup Instructions
1. Clone the Repository

git clone https://github.com/singh-himanshu3/AI-Agent.git

cd AI-Agent


2. Install Required Python Libraries
Manually install the required packages using pip:

pip install streamlit crewai clarifai


✅ Make sure you're using Python 3.8 or above. You can check with python --version.

3. Run the App


streamlit run clarifai_demo.py


4. Add Your Clarifai API Key


Once the app launches in your browser:
Paste your Clarifai Personal Access Token (PAT) into the sidebar input.
Select an analysis type and enter your topic to get started!


