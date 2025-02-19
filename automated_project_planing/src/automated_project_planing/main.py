#!/usr/bin/env python
from crewai.flow import Flow, start
from automated_project_planing.crews.automated_project_crew.project_crew import ProjectCrew

class ProjectFlow(Flow):


    project = 'Website'
    industry = 'Technology'
    project_objectives = 'Create a website for a small business'
    team_members = """
    - John Doe (Project Manager)
    - Jane Doe (Software Engineer)
    - Bob Smith (Designer)
    - Alice Johnson (QA Engineer)
    - Tom Brown (QA Engineer)
    """
    project_requirements = """
    - Create a responsive design that works well on desktop and mobile devices
    - Implement a modern, visually appealing user interface with a clean look
    - Develop a user-friendly navigation system with intuitive menu structure
    - Include an "About Us" page highlighting the company's history and values
    - Design a "Services" page showcasing the business's offerings with descriptions
    - Create a "Contact Us" page with a form and integrated map for communication
    - Implement a blog section for sharing industry news and company updates
    - Ensure fast loading times and optimize for search engines (SEO)
    - Integrate social media links and sharing capabilities
    - Include a testimonials section to showcase customer feedback and build trust
    """



    @start()
    def generate_project_management(self):
        inputs = {
    'project_type': self.project,
    'project_objectives': self.project_objectives,
    'industry': self.industry,
    'team_members': self.team_members,
    'project_requirements': self.project_requirements
    }
        result = (
            ProjectCrew().crew().kickoff(inputs=inputs)
        )
        
        self.state["project_management"] = result.raw
        return result

def kickoff():
    project_flow = ProjectFlow()
    project_flow.kickoff()

    

def plot():
    project_flow = ProjectFlow()
    project_flow.plot()


if __name__ == "__main__":
    kickoff()
