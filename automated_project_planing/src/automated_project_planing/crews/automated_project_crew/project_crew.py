from crewai import Crew, Agent, Task,Process, LLM
from crewai.project import CrewBase, agent, crew, task
from automated_project_planing.types import ProjectPlan
import os

@CrewBase
class ProjectCrew:
    """Project Crew"""

    llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
    )


    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Creating Agents
    @agent
    def project_planning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["project_planning_agent"],
            llm=self.llm,
            max_rpm=10
        )
    
    @agent
    def estimation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["estimation_agent"],
            llm=self.llm,
            max_rpm=10
        )
    
    @agent
    def resource_allocation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resource_allocation_agent"],
            llm=self.llm,
            max_rpm=10
        )
    
    # Creating Tasks
    @task
    def task_breakdown(self) -> Task:
        return Task(
            config=self.tasks_config["task_breakdown"],
        )
    
    @task
    def time_resource_estimation(self) -> Task:
        return Task(
            config=self.tasks_config["time_resource_estimation"]
        )
    
    @task
    def resource_allocation(self) -> Task:
        return Task(
            config=self.tasks_config["resource_allocation"],
            output_pydantic=ProjectPlan
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Automated Project Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        ) 
