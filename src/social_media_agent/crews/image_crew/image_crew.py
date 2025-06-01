from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from social_media_agent.tools.custom_tool import llm_creator, image_search_tool

@CrewBase
class ImageCrew:
    """Image Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def image_search_agent(self) -> Agent:
        """Creates the Image Agent"""
        return Agent(
            config=self.agents_config["image_search_agent"],
            verbose=True,
            memory=True,
            llm=llm_creator,
            allow_delegation=True,
        )
    
    @task
    def image_search_task(self) -> Task:
        """Creates the Image Task"""
        return Task(
            config=self.tasks_config["image_search_task"],
            verbose=True,
            tools=[image_search_tool]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Post Crew dynamically based on selected platforms"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )