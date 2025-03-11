from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from social_media_agent.tools.custom_tool import llm_research, llm_content, search_tool

@CrewBase
class PostCrew:
    """Poem Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            verbose=True,
            memory=True,
            llm=llm_research,
            tools=[search_tool],
            allow_delegation=True
        )
    
    @agent
    def facebook_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["facebook_agent"],
            verbose=True,
            memory=True,
            llm=llm_content,
            tools=[search_tool],
            allow_delegation=False
        )
    
    @agent
    def instagram_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["instagram_agent"],
            verbose=True,
            memory=True,
            llm=llm_content,
            tools=[search_tool],
            allow_delegation=False
        )
    
    @agent
    def twitter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["twitter_agent"],
            verbose=True,
            memory=True,
            llm=llm_content,
            tools=[search_tool],
            allow_delegation=False
        )
    
    @agent
    def linkedin_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["linkedin_agent"],
            verbose=True,
            memory=True,
            llm=llm_content,
            tools=[search_tool],
            allow_delegation=False
        )
    
    @agent
    def manager(self) -> Agent:
        """Manager Agent"""
        return Agent(
            config=self.agents_config["manager"],
            verbose=True,
            memory=True,
            llm=llm_research,
            allow_delegation=True,
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            tools=[search_tool],
        )
    @task
    def facebook_task(self) -> Task:
        return Task(
            config=self.tasks_config["facebook_task"],
            tools=[search_tool],
        )
    @task
    def instagram_task(self) -> Task:
        return Task(
            config=self.tasks_config["instagram_task"],
            tools=[search_tool],
        )
    @task
    def twitter_task(self) -> Task:
        return Task(
            config=self.tasks_config["twitter_task"],
            tools=[search_tool],
        )
    @task
    def linkedin_task(self) -> Task:
        return Task(
            config=self.tasks_config["linkedin_task"],
            tools=[search_tool],
        )



    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=[
                self.researcher(),
                self.facebook_agent(),
                self.instagram_agent(),
                self.twitter_agent(),
                self.linkedin_agent()
            ],
            tasks=self.tasks,  
            process=Process.hierarchical,
            verbose=True,
            manager_agent=self.manager()
        )