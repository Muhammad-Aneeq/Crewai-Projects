from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, crew, CrewBase
from crewai_tools import  SerperDevTool, ScrapeWebsiteTool
from sales_pipeline.types import LeadScoringResult
import os

@CrewBase
class LeadQualificationCrew:
    """Lead Qualification Crew"""

    llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
    )

    agents_config= "config/agents.yaml"
    tasks_config="config/tasks.yaml"

    # Creating Agents
    @agent
    def lead_data_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_data_agent"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llm,
            max_rpm=10
        )
    
    @agent
    def cultural_fit_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cultural_fit_agent"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llm,
            max_rpm=10
        )
    
    @agent
    def scoring_validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["scoring_validation_agent"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=self.llm,
            max_rpm=10
        )
    
    # Creating Tasks
    @task
    def lead_data_collection(self) -> Task:
        return Task(
            config=self.tasks_config["lead_data_collection"]
        )
    
    @task
    def cultural_fit_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["cultural_fit_analysis"]
        )
    
    @task
    def lead_scoring_and_validation(self) -> Task:
        return Task(
            config=self.tasks_config["lead_scoring_and_validation"],
            context=[self.lead_data_collection(), self.cultural_fit_analysis()],
            output_pydantic=LeadScoringResult
        )

    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
