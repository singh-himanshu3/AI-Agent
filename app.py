import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
import asyncio
import threading
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .result-container {
        background-color: #f8f9fa;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .status-running {
        color: #ffc107;
        font-weight: bold;
    }
    .status-complete {
        color: #28a745;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class ClarifaiResearchAgent:
    def __init__(self, api_key):
        """Initialize the Clarifai Research Agent with API key"""
        self.api_key = "YOUR_PAT_KEY_HERE"	
        self.clarifai_llm = None
        self.setup_llm()
    
    def setup_llm(self):
        """Setup Clarifai LLM connection"""
        try:
            self.clarifai_llm = LLM(
                model="openai/deepseek-ai/deepseek-chat/models/DeepSeek-R1-Distill-Qwen-7B",
                base_url="https://api.clarifai.com/v2/ext/openai/v1",
                api_key=self.api_key
            )
        except Exception as e:
            st.error(f"Failed to setup Clarifai LLM: {str(e)}")
            return False
        return True
    
    def create_research_agent(self):
        """Create the research agent with specific role and capabilities"""
        return Agent(
            role="Senior Research Analyst",
            goal="Uncover cutting-edge developments, trends, and comprehensive insights on any given topic",
            backstory="""You are an expert research analyst with years of experience in technology, 
            business, and market analysis. You excel at breaking down complex topics into digestible insights,
            identifying key trends, and providing actionable information. You always cite reliable sources 
            when possible and present information in a clear, structured format.""",
            verbose=True,
            allow_delegation=False,
            llm=self.clarifai_llm
        )
    
    def create_analysis_task(self, topic, analysis_type="comprehensive"):
        """Create a research task based on the topic and analysis type"""
        task_descriptions = {
            "comprehensive": f"""Conduct a comprehensive analysis of '{topic}'.
            
            Your analysis should include:
            1. Overview and current state
            2. Key trends and developments
            3. Major players and stakeholders
            4. Opportunities and challenges
            5. Future outlook and predictions
            6. Actionable insights
            
            Focus on factual, verifiable information and present it in a well-structured format.""",
            
            "market": f"""Conduct a market analysis of '{topic}'.
            
            Focus on:
            1. Market size and growth potential
            2. Key competitors and market share
            3. Customer segments and demand
            4. Pricing strategies and revenue models
            5. Market challenges and opportunities
            6. Investment and funding landscape""",
            
            "technology": f"""Conduct a technology analysis of '{topic}'.
            
            Focus on:
            1. Current technology landscape
            2. Emerging technologies and innovations
            3. Technical challenges and solutions
            4. Industry standards and protocols
            5. Future technology roadmap
            6. Impact on related industries""",
            
            "trend": f"""Conduct a trend analysis of '{topic}'.
            
            Focus on:
            1. Current trending topics and themes
            2. Social and cultural impact
            3. Adoption patterns and user behavior
            4. Influencing factors and drivers
            5. Predicted future trends
            6. Implications for businesses and consumers"""
        }
        
        return Task(
            description=task_descriptions.get(analysis_type, task_descriptions["comprehensive"]),
            expected_output="A detailed, well-structured analysis report with clear sections, bullet points, and actionable insights.",
            agent=self.create_research_agent()
        )
    
    def run_research(self, topic, analysis_type="comprehensive"):
        """Execute the research task and return results"""
        try:
            task = self.create_analysis_task(topic, analysis_type)
            agent = self.create_research_agent()
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False  # Set to False to reduce noise in Streamlit
            )
            
            result = crew.kickoff()
            return result
        except Exception as e:
            return f"Error during research: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Research Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Powered by Clarifai & CrewAI</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Clarifai API Key (PAT)",
            type="password",
            help="Enter your Clarifai Personal Access Token"
        )
        
        if not api_key:
            st.warning("⚠️ Please enter your Clarifai API key to continue")
            st.info("💡 Get your API key from Clarifai Security settings")
            return
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Type",
            ["comprehensive", "market", "technology", "trend"],
            help="Choose the type of analysis you want to perform"
        )
        
        # Agent info
        st.markdown("""
        ### 👤 Agent Profile
        **Role:** Senior Research Analyst  
        **Specialties:** Technology, Business, Market Analysis  
        **Capabilities:** Trend identification, Data synthesis, Strategic insights
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Research Request")
        
        # Topic input
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g., Artificial Intelligence in Healthcare, Cryptocurrency trends, Sustainable Energy..."
        )
        
        # Example topics
        st.markdown("**💡 Example Topics:**")
        example_topics = [
            "Artificial Intelligence in Healthcare",
            "Cryptocurrency Market Trends",
            "Sustainable Energy Solutions",
            "Remote Work Technology",
            "E-commerce Innovation"
        ]
        
        cols = st.columns(len(example_topics))
        for i, example in enumerate(example_topics):
            if cols[i].button(example, key=f"example_{i}"):
                topic = example
                st.rerun()
    
    with col2:
        st.header("🎯 Analysis Settings")
        
        analysis_descriptions = {
            "comprehensive": "Complete overview with trends, players, and future outlook",
            "market": "Market size, competitors, opportunities, and challenges",
            "technology": "Tech landscape, innovations, and future roadmap",
            "trend": "Current trends, social impact, and future predictions"
        }
        
        st.info(f"**{analysis_type.title()} Analysis**\n\n{analysis_descriptions[analysis_type]}")
    
    # Research execution
    if topic and api_key:
        if st.button("🚀 Start Research", type="primary", use_container_width=True):
            
            # Initialize agent
            with st.spinner("Initializing AI Research Agent..."):
                agent = ClarifaiResearchAgent(api_key)
                if not agent.clarifai_llm:
                    st.error("Failed to initialize Clarifai connection. Please check your API key.")
                    return
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.markdown('<p class="status-running">🔍 Agent is researching your topic...</p>', unsafe_allow_html=True)
            progress_bar.progress(25)
            
            # Execute research
            try:
                with st.spinner(f"Analyzing '{topic}' using {analysis_type} analysis..."):
                    progress_bar.progress(50)
                    result = agent.run_research(topic, analysis_type)
                    progress_bar.progress(100)
                
                status_text.markdown('<p class="status-complete">✅ Research completed successfully!</p>', unsafe_allow_html=True)
                
                # Display results
                st.header("📊 Research Results")
                
                # Metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Topic", topic)
                with col2:
                    st.metric("Analysis Type", analysis_type.title())
                with col3:
                    st.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))
                
                # Main results
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown("### 📋 Analysis Report")
                st.write(result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download option
                st.download_button(
                    label="📥 Download Report",
                    data=f"Research Report: {topic}\nAnalysis Type: {analysis_type}\nGenerated: {datetime.now()}\n\n{result}",
                    file_name=f"research_report_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Research failed: {str(e)}")
                status_text.markdown('<p style="color: red;">❌ Research failed. Please try again.</p>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 Built with Clarifai AI Models & CrewAI Framework</p>
        <p>⚡ Streamlit UI for Interactive Agent Experience</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()