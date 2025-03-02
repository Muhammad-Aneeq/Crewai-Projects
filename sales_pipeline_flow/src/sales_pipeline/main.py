#!/usr/bin/env python
from crewai.flow import Flow, listen, start
from sales_pipeline.crews.email_engagement_crew.email_engagement import EmailEngagementCrew
from sales_pipeline.crews.lead_qualification_crew.lead_qualification import LeadQualificationCrew
import streamlit as st

class SalesFlow(Flow):

    @start()
    def fetch_leads(self):
        # Use custom leads if provided, otherwise default values.
        if "custom_leads" in self.state:
            leads = self.state["custom_leads"]
        else:    
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
    
    # @listen(write_email)
    # def send_email(self, emails):
    #     # Here we would send the emails to the leads
    #     print("emails>>>",emails)
    #     self.state["final_output"] = emails
    #     return emails
    @listen(write_email)
    def send_email(self, emails):
        # Store only the final "raw" output to be used in the UI.
        # If emails is a list, we extract the "raw" attribute from each element.
        print("emails>>>",emails)
        final_results = []
        if isinstance(emails, list):
            for item in emails:
                if hasattr(item, "raw") and item.raw:
                    final_results.append(item.raw)
                else:
                    final_results.append(str(item))
        else:
            final_results = [str(emails)]
        self.state["final_output"] = final_results
        return final_results



# Streamlit App Integration
def main():
    st.title("SalesFlow Pipeline")
    st.markdown(
        "This tool runs our sales pipeline using provided lead information. Fill in the details below and click **Run Pipeline**. "
        "A progress indicator will display while the pipeline runs."
    )

    st.header("Enter Lead Details")
    with st.form("lead_form"):
        name = st.text_input("Name", "João Moura")
        job_title = st.text_input("Job Title", "Director of Engineering")
        company = st.text_input("Company", "Clearbit")
        email = st.text_input("Email", "joao@clearbit.com")
        use_case = st.text_input("Use Case", "Using AI Agent to do better data enrichment.")
        submitted = st.form_submit_button("Run Pipeline")

    if submitted:
        # Build the custom lead input from the user.
        custom_leads = [{
            "lead_data": {
                "name": name,
                "job_title": job_title,
                "company": company,
                "email": email,
                "use_case": use_case
            }
        }]

       # Update state and run pipeline with a spinner and messages
        with st.spinner("Running pipeline, please wait..."):
            sales_flow = SalesFlow()
            sales_flow.state["custom_leads"] = custom_leads
            sales_flow.kickoff()
            final_output = sales_flow.state.get("final_output", [])

        st.success("Pipeline execution completed!")
        st.subheader("Final Email Output")
        # Display each final output in a separate text area.
        for i, output in enumerate(final_output, start=1):
            st.markdown(f"**Email {i}:**")
            st.text_area("Output", output, height=200)

if __name__ == "__main__":
    main()

def run_streamlit_app():
    import sys
    import streamlit.web.cli
    print(__file__)
    # Prepare the sys.argv list so that Streamlit knows which file to run.
    sys.argv = ["streamlit", "run", __file__]
    streamlit.web.cli.main()


def kickoff():
    sales_flow = SalesFlow()
    sales_flow.kickoff()


def plot():
    sales_flow = SalesFlow()
    sales_flow.plot()


# if __name__ == "__main__":
#     kickoff()
