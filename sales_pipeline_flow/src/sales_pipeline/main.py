#!/usr/bin/env python
from crewai.flow import Flow, listen, start
from sales_pipeline.crews.email_engagement_crew.email_engagement import EmailEngagementCrew
from sales_pipeline.crews.lead_qualification_crew.lead_qualification import LeadQualificationCrew


class SalesFlow(Flow):

    @start()
    def fetch_leads(self):
        # Pull our leads from the database
        leads = [
            {
                "lead_data": {
                    "name": "João Moura",
                    "job_title": "Director of Engineering",
                    "company": "Clearbit",
                    "email": "joao@clearbit.com",
                    "use_case": "Using AI Agent to do better data enrichment."
                },
            },
        ]
        return leads
    
    @listen(fetch_leads)
    def score_leads(self, leads):
        scores = LeadQualificationCrew().crew().kickoff_for_each(leads)
        self.state["score_crews_results"] = scores
        return scores
    
    @listen(score_leads)
    def store_leads_score(self, scores):
        # Here we would store the scores in the database
        return scores
    
    @listen(score_leads)
    def filter_leads(self, scores):
        
        return [
    score for score in scores 
    if hasattr(score.pydantic, 'lead_score') 
    and score.pydantic.lead_score is not None 
    and score.pydantic.lead_score.score is not None 
    and score.pydantic.lead_score.score > 70
]

    @listen(filter_leads)
    def write_email(self, leads):
        scored_leads = [lead.to_dict() for lead in leads]
        emails = EmailEngagementCrew().crew().kickoff_for_each(scored_leads)
        return emails
    
    @listen(write_email)
    def send_email(self, emails):
        # Here we would send the emails to the leads
        return emails


def kickoff():
    sales_flow = SalesFlow()
    sales_flow.kickoff()


def plot():
    sales_flow = SalesFlow()
    sales_flow.plot()


if __name__ == "__main__":
    kickoff()
