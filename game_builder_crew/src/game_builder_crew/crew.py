from typing import List
from crewai import Agent, Task, Process, Crew, LLM
from crewai.project import CrewBase, agent , crew, task
import os


@CrewBase
class GameBuilderCrew:
    """GameBuilder Crew"""

    llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
    )
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def senior_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_engineer_agent"],
            llm=self.llm,
            max_rpm=10,
            allow_delegation=False,
		)
    
    @agent
    def qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer_agent'],
            llm=self.llm,
            max_rpm=10,
            allow_delegation=False,
        )
    
    @agent
    def chief_qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_qa_engineer_agent'],
            llm=self.llm,
            max_rpm=10,
            allow_delegation=True,
            verbose=True
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
        )

    @task
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GameBuilderCrew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True, 
        )