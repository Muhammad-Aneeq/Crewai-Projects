from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, crew, CrewBase
from shoping_agent.tools.productcatalog_tool import ProductCatalogTool
from shoping_agent.tools.userdata_tool import UserDataTool
import os

@CrewBase
class ShoppingAgentCrew():
    """ShoppingAgent Crew"""

    # Basic configuration: Initialize LLM
    llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
    )
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    product_catalog_tool = ProductCatalogTool()
    user_data_tool = UserDataTool()

    # =============Agents=============
    def orchestrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator_agent'],
            llm=self.llm,
            verbose=True,
            max_rpm=10,
            allow_delegation=True
        )
    
    @agent
    def front_desk_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['front_desk_agent'],
            llm=self.llm,
            verbose=True,
            max_rpm=10,
        )
    
    @agent
    def product_finder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['product_finder_agent'],
            verbose=True,
            llm=self.llm,
            tools=[self.product_catalog_tool],
            max_rpm=10,
        )
    
    @agent
    def checkout_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['checkout_agent'],
            llm=self.llm,
            verbose=True,
            tools=[self.user_data_tool],
            max_rpm=10,
        )
    
    # =============Tasks=============
    @task
    def orchestrator_task(self) -> Task:
        return Task(
            config=self.tasks_config['orchestrator_task'],
            agent=self.orchestrator_agent()  # instantiate the orchestrator agent
        )
    
    @task
    def greeting_task(self) -> Task:
        return Task(
            config=self.tasks_config['greeting_task']
        )
    
    @task
    def category_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['category_selection_task']
        )
    
    @task
    def product_query_task(self) -> Task:
        return Task(
            config=self.tasks_config['product_query_task']
        )
    
    @task
    def cart_management_task(self) -> Task:
        return Task(
            config=self.tasks_config['cart_management_task']
        )
    
    @task
    def checkout_task(self) -> Task:
        return Task(
            config=self.tasks_config['checkout_task']
        )
    
    @task
    def order_confirmation_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_confirmation_task']
        )
    
    # =============Orchestrator Flow=============
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,      # Automatically created by the @agent decorators
            tasks=self.tasks,        # Automatically created by the @task decorators
            manager_agent=self.orchestrator_agent(),  # Manager is an instantiated orchestrator agent
            process=Process.hierarchical,  # Use hierarchical process for dynamic orchestration
            verbose=True
        )
