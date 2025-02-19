from crewai import Crew, Agent, Task,Process
from crewai.project import CrewBase, agent, crew, task
from automated_project_planing.types import ProjectPlan


@CrewBase
class ProjectCrew:
    """Project Crew"""


    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Creating Agents
    @agent
    def project_planning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["project_planning_agent"]
        )
    
    @agent
    def estimation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["estimation_agent"]
        )
    
    @agent
    def resource_allocation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resource_allocation_agent"]
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
