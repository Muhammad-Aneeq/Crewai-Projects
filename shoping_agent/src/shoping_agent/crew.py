from crewai import Agent, Task, Crew, Process
from crewai.project import agent, task, crew, CrewBase
from shoping_agent.tools.productcatalog_tool import ProductCatalogTool
from shoping_agent.tools.userdata_tool import UserDataTool
from crewai import LLM
import os

@CrewBase
class ShoppingAgentCrew():
    """ShoppingAgent Crew"""

	# Basic configuration
    llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
        )
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    product_catalog_tool = ProductCatalogTool()
    user_data_tool = UserDataTool()

    # =============Agents=============
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
            max_rpm=10,  # Limit API calls  # Now the tool will get proper arguments via task config mapping.
        )
    
    @agent
    def checkout_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['checkout_agent'],
            llm=self.llm,
            verbose=True,
            tools=[self.user_data_tool],  # Using allowed actions: 'create', 'update', 'get'
            max_rpm=10,  # Limit API calls
        )
    
    
    # =============Tasks=============
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
    
  
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            # verbose=True
        )
