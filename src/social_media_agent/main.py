from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from social_media_agent.crews.post_crew.post_crew import PostCrew


class PostState(BaseModel):
    post: str = ""


class PostFlow(Flow[PostState]):

    @start()
    def generate_post(self):
        print("Generating post")
        result = (
            PostCrew()
            .crew()
            .kickoff(inputs={'topic': 'Kerala Tourism', 'platform': 'Instagram'})
        )

        print("Post generated", result.raw)
        self.state.post = result.raw

    @listen(generate_post)
    def save_post(self):
        print("Saving post")
        with open("post.md", "w", encoding='utf-8') as f:
            f.write(self.state.post)


def kickoff():
    post_flow = PostFlow()
    post_flow.kickoff()


def plot():
    post_flow = PostFlow()
    post_flow.plot()


if __name__ == "__main__":
    kickoff()
