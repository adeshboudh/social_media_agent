from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from social_media_agent.tools.custom_tool import llm_creator

@CrewBase
class ModifyCrew:
    """Modify Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def post_modifier_agent(self) -> Agent:
        """Creates the Evaluator Agent"""
        return Agent(
            config=self.agents_config["post_modifier_agent"],
            verbose=True,
            memory=True,
            llm=llm_creator,
            allow_delegation=True,
        )
    
    @task
    def post_modifier_task(self) -> Task:
        """Creates the Evaluator Task"""
        return Task(
            config=self.tasks_config["post_modifier_task"],
            verbose=True,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Evaluator Crew dynamically based on selected platforms"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )