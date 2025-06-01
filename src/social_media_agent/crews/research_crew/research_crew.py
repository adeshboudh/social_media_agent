from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from social_media_agent.tools.custom_tool import llm_creator, serper_tool, scrape_tool

@CrewBase
class ResearchCrew:
    """Research Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def serper_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["serper_search_agent"],
            verbose=True,
            memory=True,
            llm=llm_creator,
            tools=[serper_tool],
            allow_delegation=True,
        )
    
    @agent
    def web_crawler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['web_crawler_agent'],
            verbose=True,
            memory=True,
            llm=llm_creator,
            tools=[scrape_tool],
            allow_delegation=True,
        )

    @task
    def serper_search_task(self) -> Task:
        return Task(
            config=self.tasks_config["serper_search_task"],
            verbose=True,
            tools=[serper_tool],
        )
    
    @task
    def crawl_task(self) -> Task:
        return Task(
            config=self.tasks_config['crawl_task'],
            tools=[scrape_tool],
            verbose=True,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Search Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )