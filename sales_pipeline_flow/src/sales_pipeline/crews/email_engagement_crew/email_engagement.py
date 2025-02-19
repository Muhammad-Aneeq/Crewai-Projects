from crewai import Agent, Task, Crew, Process
from crewai.project import agent, task, crew, CrewBase


@CrewBase
class EmailEngagementCrew:
    """Email Engagement Crew"""

    agents_config= "config/agents.yaml"
    tasks_config="config/tasks.yaml"

    # Creating Agents
    @agent
    def email_content_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["email_content_specialist"]
        )
    
    @agent
    def engagement_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["engagement_strategist"]
        )
    
    # Creating Tasks
    @task
    def email_drafting(self) -> Task:
        return Task(
            config=self.tasks_config["email_drafting"]
        )
    
    @task
    def engagement_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["engagement_optimization"]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
