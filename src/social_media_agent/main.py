from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from social_media_agent.crews.research_crew.research_crew import ResearchCrew
from social_media_agent.crews.image_crew.image_crew import ImageCrew
from social_media_agent.crews.post_crew.post_crew import PostCrew
from social_media_agent.crews.evaluation_crew.evaluation_crew import EvaluationCrew
from social_media_agent.crews.modify_crew.modify_crew import ModifyCrew
from social_media_agent.tools.custom_tool import EvaluationOutput
from typing import List
import json

# 📌 State for Post Flow
class PostState(BaseModel):
    content: List[str] = []
    images: List[str] = []
    post: str = ""
    evaluation: dict = {}
    overall_score: float = 0.0
    feedback_prompt: str = ""

# ✍️ Post Flow (Handles Post Generation)
class PostFlow(Flow[PostState]):
    post_input = {'topic': 'MCP servers', 'platform': 'LinkedIn'}

    @start()
    def search_for_content(self):
        print("🔎 Performing Research")
        
        search_crew_instance = ResearchCrew()

        response = search_crew_instance.crew().kickoff(
            inputs={'topic': self.post_input['topic'], }
        )

        # Debug: Print the raw response
        print("🔗 Raw Search Result (Debug):", response.raw)
        self.state.content = response.raw
        print("🔗 Search Result:", self.state.content)

        # with open("test.md", "r", encoding="utf-8") as f:
        #     self.state.content = f.read()
        # print("📄 Loaded Content from test.md:", self.state.content)

    @listen(search_for_content)
    def image_search(self):
        print("🔍 Searching for Images")
        image_crew_instance = ImageCrew()
        response = image_crew_instance.crew().kickoff(
            inputs={'topic': self.post_input['topic'],
                    'platform': self.post_input['platform']}
        )
        print("image raw", response.raw)
        self.state.images = response.raw
        print("📸 Image Result:", self.state.images)
    
    #     # image_urls = [
    #     # "https://www.ekeralatourism.net/wp-content/uploads/2018/03/Alleppey.jpg",
    #     # "https://static.wixstatic.com/media/c8e24e_8734146da4f241b591e5f0ede582f9e0~mv2.jpg/v1/fill/w_640,h_360,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Kerala-tourism.jpg",
    #     # "https://www.oyorooms.com/travel-guide/wp-content/uploads/2019/09/Gods-Own-Country-Kerala-or-Best-time-to-visit-Kerala-5-1280x720.jpg",
    #     # "https://traveldudes.com/wp-content/uploads/2020/09/Kerala_Main.jpg",
    #     # "https://www.peakadventuretour.com/assets/imgs/kerala-tourism-04.webp"
    #     # ]

    #     # self.state.images = image_urls
    #     # print("📸 Image Result:", self.state.images)

    @listen(search_for_content)
    def create_post(self):
        print("📢 Creating Post")

        #Validate inputs
        if not self.state.content:
            print("❌ No content provided. Skipping post creation.")
            return
        if not self.post_input.get('platform'):
            print("❌ No platform specified. Skipping post creation.")
            return

        post_crew_instance = PostCrew()
        # print("Inside create post", self.state.content)
        # print("Inside create post", self.post_input['topic'])
        # print("Inside create post", self.post_input['platform'])
        # print("Inside create post", self.state.images)
        try:
            response = post_crew_instance.crew().kickoff(
                inputs={
                    'content': self.state.content,
                    'platform': self.post_input['platform'],
                    'topic': self.post_input['topic'],
                    'images': self.state.images,
                }
            )
            # print("📢 Post Result:", response.raw)
            self.state.post = response.raw
            print("📢 Post:", self.state.post)
        except Exception as e:
            print(f"❌ Failed to create post: {str(e)}")

        # with open("test_post.md", "r", encoding="utf-8") as f:
        #     self.state.post = f.read()
        # print("📄 Loaded Content from test_post.md:", self.state.post)

    @listen(create_post)
    def evaluate_post(self, retries=0, max_retries=3):
        print("📊 Evaluating post...")
        evaluation_crew_instance = EvaluationCrew()
        try:
            print("before evaluation",self.state.post)
            response = evaluation_crew_instance.crew().kickoff(inputs={'post': self.state.post})
            
            # Debug the raw response
            print("Evaluation Response Raw Data (Debug):", repr(response.raw))
            print("Type of response.raw:", type(response.raw))

            # Check if response.raw is empty or contains only whitespace
            if not response.raw.strip():
                raise ValueError("Evaluation response is empty or contains only whitespace.")

            # Clean the response.raw string (remove backticks and extra formatting)
            cleaned_response = response.raw.strip("```json").strip("```").strip()

            # Parse the cleaned response
            try:
                evaluation_data = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse evaluation response: {str(e)}")

            # Store the entire evaluation response in the flow state
            self.state.evaluation = evaluation_data
            print("📊 Evaluation Results:", self.state.evaluation)
            print("📊 Evaluation Results (Type):", type(self.state.evaluation))

            # Fetch the overall effectiveness score
            overall_score = evaluation_data["overall_effectiveness"]["score"]
            self.state.overall_score = overall_score  # Save the score in the flow state
            print(f"✅ Overall Effectiveness Score: {overall_score:.1f}")
            feedback_prompt = self.state.evaluation["overall_effectiveness"]["explanation"]
            print("Feedback prompt",feedback_prompt)

            # Check if the score is less than 7.5
            if overall_score < 7.5:
                if retries < max_retries:
                    print(f"⚠️ Overall Effectiveness Score is less than 7.5. Modifying the post... (Retry {retries + 1}/{max_retries})")
                    
                    # Generate feedback prompt from overall_effectiveness explanation
                    feedback_prompt = self.state.evaluation["overall_effectiveness"]["explanation"]
                    self.state.feedback_prompt = feedback_prompt  # Save the feedback prompt in the flow state

                    # Modify the post
                    self.modify_post()

                    # Re-evaluate the updated post
                    self.evaluate_post(retries=retries + 1, max_retries=max_retries)
                else:
                    print("❌ Maximum retries reached. Unable to improve the post.")
        except Exception as e:
            print(f"❌ Failed to evaluate post: {str(e)}")

    @listen(evaluate_post)
    def wait_for_feedback(self):
        print("⏸ Waiting for Feedback")
        # Pause the flow here and wait for user input
        feedback = input("Enter feedback to modify the post (or press Enter to skip): ")
        if feedback.strip():
            self.modify_post(feedback)
        else:
            print("⚠️ No feedback provided. Skipping modification.")

    def modify_post(self, user_feedback=None):
        print("🔄 Modifying Post Based on Feedback")

        # Validate inputs
        if not self.state.post:
            print("❌ No post available to modify.")
            return

        # Use user feedback if provided, otherwise use the feedback prompt from the evaluation
        feedback_prompt = user_feedback if user_feedback else self.state.feedback_prompt
        if not feedback_prompt:
            print("❌ No feedback prompt available to modify the post.")
            return

        # Log the original post and feedback prompt
        print("📝 Original Post:", self.state.post)
        print("📝 Feedback Prompt:", feedback_prompt)

        # Use ModifyCrew to modify the post
        modify_crew_instance = ModifyCrew()
        try:
            response = modify_crew_instance.crew().kickoff(
                inputs={
                    'post': self.state.post,
                    'feedback': feedback_prompt,
                    'content': self.state.content if self.state.content else "",
                }
            )
            # Update the post in the flow state
            self.state.post = response.raw
            print("✅ Modified Post:", self.state.post)

            # Run evaluation on the modified post
            self.evaluate_post()

        except Exception as e:
            # Log detailed error information
            print(f"❌ Failed to modify post: {str(e)}")
            print("🛠️ Debug Info:")
            print(f"Post: {self.state.post}")
            print(f"Feedback Prompt: {feedback_prompt}")
            print(f"Content: {self.state.content if self.state.content else 'None'}")

    # @listen(evaluate_post)
    # def save_post(self):
    #     print("💾 Saving Post")
    #     with open("post.md", "w", encoding="utf-8") as f:
    #         f.write(self.state.post)

# # 🚀 Kickoff Function
# def kickoff():
#     post_flow = PostFlow()
#     post_flow.kickoff()

def kickoff():
    post_flow = PostFlow()
    post_flow.kickoff()

    # # Pause after creating the post to allow feedback
    # print("\n--- Post Generated ---")
    # print("Generated Post:", post_flow.state.post)
    # feedback = input("Enter feedback to modify the post (or press Enter to skip): ")
    # if feedback.strip():
    #     post_flow.modify_post(feedback)

    # # Resume the flow
    # post_flow.evaluate_post()
    # post_flow.save_post()

def plot():
    post_flow = PostFlow()
    post_flow.plot()

if __name__ == "__main__":
    kickoff()