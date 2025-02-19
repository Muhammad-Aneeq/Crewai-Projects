from crewai import Agent,Task, Crew, Process
from crewai.project import agent, task, crew, CrewBase
from travel_agent_flow.tools.calculator_tools import CalculatorTools
from crewai_tools import  SerperDevTool

@CrewBase
class TripCrew:
    """Trip Crew"""

    agents_config= "config/agents.yaml"
    tasks_config= "config/tasks.yaml"


    @agent
    def travel_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["travel_agent"],
            tools=[
                SerperDevTool(),
                CalculatorTools.calculate
            ]
        )
    
    @agent
    def city_selection_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["city_selection_expert"],
            tools=[SerperDevTool()],
        )
    
    @agent
    def local_tour_guide(self) -> Agent:
        return Agent(
            config=self.agents_config["local_tour_guide"],
            tools=[SerperDevTool()],
        )
    
    @task
    def plan_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config["plan_itinerary"]
        )
    
    @task
    def identify_city(self) -> Task:
        return Task(
            config=self.tasks_config["identify_city"]
        )
    
    @task
    def gather_city_info(self) -> Task:
        return Task(
            config=self.tasks_config["gather_city_info"]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Trip Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )