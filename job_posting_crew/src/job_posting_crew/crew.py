from typing import List
from crewai import Agent, Task, Process, Crew, LLM
from crewai.project import agent, task, crew, CrewBase
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool
from pydantic import BaseModel
import os





web_search_tool = ScrapeWebsiteTool()
seper_dev_tool = SerperDevTool()
file_read_tool = FileReadTool(
    file_path='job_description_example.md',
    description='A tool to read the job description example file.'
)

class ResearchRoleRequirements(BaseModel):
    skills: List[str] = []
    experience: List[str] = []
    qualities: List[str] = []

@CrewBase
class JobPostingCrew:
	"""JobPosting Crew"""

	llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
    )
     
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
    
	@agent
	def research_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['research_agent'],
			tools=[web_search_tool,seper_dev_tool],
			llm=self.llm,
			max_rpm=10
		)
	
	@agent
	def writer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['writer_agent'],
			tools=[web_search_tool,seper_dev_tool, file_read_tool],
			llm=self.llm,
			max_rpm=10
		)
	
	@agent
	def review_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['review_agent'],
			tools=[web_search_tool,seper_dev_tool, file_read_tool],
			llm=self.llm,
			max_rpm=10
		)
	
	
	@task
	def research_company_culture_task(self) -> Task:
		return Task(
            config=self.tasks_config['research_company_culture_task'],
        )

	@task
	def research_role_requirements_task(self) -> Task:
		return Task(
            config=self.tasks_config['research_role_requirements_task'],
            output_json=ResearchRoleRequirements
        )

	@task
	def draft_job_posting_task(self) -> Task:
		return Task(
            config=self.tasks_config['draft_job_posting_task'],
        )

	@task
	def review_and_edit_job_posting_task(self) -> Task:
		return Task(
            config=self.tasks_config['review_and_edit_job_posting_task'],
        )

	@task
	def industry_analysis_task(self) -> Task:
		return Task(
            config=self.tasks_config['industry_analysis_task'],
        )

	@crew
	def crew(self) -> Crew:
		"""Creates the JobPostingCrew"""
		return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )