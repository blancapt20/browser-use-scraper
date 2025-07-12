from browser_use import Agent, Controller
from browser_use.llm import ChatOpenAI
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any
import json
from datetime import datetime
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List

# Define the output format as a Pydantic model
class Finding(BaseModel):
	source_url: str
	extracted_text: str
	summary: int


class Findings(BaseModel):
	findings: List[Finding]

load_dotenv()
controller = Controller(output_model=Findings)


class ScraperJob:
    def __init__(self, job_id: str, url: str):
        self.job_id = job_id
        self.url = url
        self.status = "pending"
        self.result = None
        self.start_time = None
        self.end_time = None
        self.llm = ChatOpenAI(model="gpt-4.1")
        self.controller = controller

    async def run(self):
        self.status = "running"
        self.start_time = datetime.utcnow().isoformat()

        initial_actions = [
            {'go_to_url': {'url': self.url, 'new_tab': True}}
        ]
        
        # Create agent with context manager to ensure proper cleanup
        try:
            agent = Agent(
                task="""
                Analyze a corporate website and extract any relevant information related to sustainability and ESG.

                Objective:
                Collect all available data about:
                - Sustainability
                - ESG (Environmental, Social and Governance)
                - Sustainability plan
                - Sustainability report
                - Non-financial report
                - Environmental impact
                - Corporate social responsibility
                
                Instructions:
                1. Visit the main page.
                2. Extract visible text from the main page.
                3. Navigate to any relevant internal subpages or links.
                4. Extract content from those related pages if they contain useful information.
                5. Ignore social media links or advertising elements.
                
                Output format:
                {
                    "findings": [
                        {
                            "source_url": "URL of the subpage",
                            "extracted_text": "Text or fragment extracted",
                            "summary": "Brief explanation if applicable"
                        }
                    ]
                }
            """,
            initial_actions=initial_actions,
            llm=self.llm,
            controller=self.controller
        )
        
            try:
                history = await agent.run()
                # Extract only the final output from the agent's history
                result = history.final_result()
                if result:
                    parsed: Findings = Findings.model_validate_json(result)
                    self.result = parsed
                else:
                    self.result = "No ha encontrado el final_result()"
                # if isinstance(history, list) and history:
                #     last_message = history[-1]
                #     if isinstance(last_message, dict) and 'content' in last_message:
                #         try:
                #             # Try to parse the content as JSON
                #             output = json.loads(last_message['content'])
                #             if isinstance(output, dict) and 'findings' in output:
                #                 self.result = output
                #             else:
                #                 self.result = {"error": "Invalid output format"}
                #         except json.JSONDecodeError:
                #             self.result = {"error": "Could not parse agent output as JSON"}
                #     else:
                #         self.result = {"error": "No content in agent's last message"}
                # else:
                #     self.result = {"error": "No history from agent"}
                self.status = "completed"
            except Exception as e:
                self.status = "failed"
                self.result = {"error": str(e)}
            finally:
                # Ensure we clean up the agent
                if hasattr(agent, '_browser') and agent._browser:
                    await agent._browser.close()
        except Exception as e:
            self.status = "failed"
            self.result = {"error": f"Failed to initialize agent: {str(e)}"}
        
        self.end_time = datetime.utcnow().isoformat()

    def get_status(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "url": self.url,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    def get_result(self) -> Dict[str, Any]:
        if self.status != "completed":
            return {"error": f"Job is in {self.status} state"}
        return self.result
