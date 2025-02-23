from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, crew, CrewBase
from stock_analysis_crew.tools.calculator_tool import CalculatorTool
from stock_analysis_crew.tools.sec_tools import SEC10KTool, SEC10QTool
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool, RagTool


def get_tool_config():
    return {
        "llm": {
            "provider": "google",
            "config": {"model": "gemini/gemini-1.5-flash"}
        },
        "embedder": {
            "provider": "google",
            "config": {
                "model": "models/embedding-001",
                "task_type": "retrieval_document",
            },
        },
    }


@CrewBase
class StockAnalysisCrew:
    """Stock Analysis Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.sec_10k = SEC10KTool("AMZN")
        self.sec_10q = SEC10QTool("AMZN")

        self.website_search_tool = WebsiteSearchTool(config=get_tool_config())
        self.financial_rag_tool = RagTool(config=get_tool_config())

        ten_k_content = self.sec_10k.get_10k_url_content()
        ten_q_content = self.sec_10q.get_10q_url_content()

        if ten_k_content:
            self.financial_rag_tool.add(ten_k_content)
        if ten_q_content:
            self.financial_rag_tool.add(ten_q_content)

        self.scrape_website_tool = ScrapeWebsiteTool()
        self.calculator_tool = CalculatorTool().calculate

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_analyst"],
            tools=[
                self.scrape_website_tool,
                self.website_search_tool,
                self.calculator_tool,
                self.financial_rag_tool,
            ]
        )

    @agent
    def research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["research_analyst"],
            tools=[
                self.scrape_website_tool,
                self.financial_rag_tool,
            ]
        )

    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["investment_advisor"],
            tools=[
                self.scrape_website_tool,
                self.website_search_tool,
                self.calculator_tool,
            ]
        )

    @task
    def financial_analysis(self) -> Task:
        return Task(config=self.tasks_config["financial_analysis"])

    @task
    def research(self) -> Task:
        return Task(config=self.tasks_config["research"])

    @task
    def filings_analysis(self) -> Task:
        return Task(config=self.tasks_config["filings_analysis"])

    @task
    def recommend(self) -> Task:
        return Task(config=self.tasks_config["recommend"])

    @crew
    def crew(self) -> Crew:
        """Creates the Stock Analysis Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
