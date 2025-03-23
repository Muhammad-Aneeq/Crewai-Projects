#!/usr/bin/env python
import sys
from job_posting_crew.crew import JobPostingCrew
import streamlit as st

def run(inputs):
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    result = JobPostingCrew().crew().kickoff(inputs=inputs)
    # If result is a list of outputs, extract the 'raw' attribute from each.
    final_output = []
    if isinstance(result, list):
        for item in result:
            if hasattr(item, "raw") and item.raw:
                final_output.append(str(item.raw))
            else:
                final_output.append(str(item))
    else:
        final_output = [str(result)]
    return final_output


def train(inputs, n_iterations):
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
    'company_domain': 'careers.microsoft.com',
    'company_description': "Microsoft is a multinational technology company, recognized for creating software products such as Windows, Office, and Azure cloud services. We believe in empowering every person and organization to achieve more.",
    'hiring_needs': 'Cloud Architect, for designing innovative cloud solutions in Redmond starting July 2025',
    'specific_benefits': 'Retirement Plans, Employee Stock Purchase Program, Health and Wellness Benefits',
    }
    try:
        JobPostingCrew().crew().train(n_iterations=n_iterations, inputs=inputs)
        return f"Job Posting Crew trained successfully for {n_iterations} iterations."

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    

def main():
    st.title("Job Posting Crew Pipeline")
    st.markdown(
        "This interactive tool allows you to run or train the Job Posting Crew pipeline by providing company details, "
        "hiring needs, and specific benefits. Choose your mode and enter the required information below."
    )

    # Choose mode: Run or Train
    mode = st.radio("Select Mode", ["Run", "Train"], index=0)

    # Form to capture input data
    with st.form("job_posting_form"):
        company_domain = st.text_input("Company Domain", "careers.microsoft.com")
        company_description = st.text_area("Company Description", 
            "Microsoft is a multinational technology company, recognized for creating software products such as Windows, Office, and Azure cloud services. We believe in empowering every person and organization to achieve more.")
        hiring_needs = st.text_input("Hiring Needs","Cloud Architect, for designing innovative cloud solutions in Redmond starting July 2025")
        specific_benefits = st.text_input("Specific Benefits","Retirement Plans, Employee Stock Purchase Program, Health and Wellness Benefits")
        n_iterations = None
        if mode == "Train":
            n_iterations = st.number_input("Number of Training Iterations", min_value=1, value=10, step=1)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Build the input dictionary
        inputs = {
            'company_domain': company_domain,
            'company_description': company_description,
            'hiring_needs': hiring_needs,
            'specific_benefits': specific_benefits,
        }
        try:
            with st.spinner("Processing, please wait..."):
                if mode == "Run":
                    output = run(inputs)
                else:
                    output = train(inputs, n_iterations)
            st.success("Pipeline executed successfully!")
            st.subheader("Pipeline Output")
            # If output is a list, join the items into a single string.
            if isinstance(output, list):
                output_text = "\n\n".join(output)
            else:
                output_text = str(output)
            st.markdown(output_text)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

def run_streamlit_app():
    import sys
    import streamlit.web.cli
    print(__file__)
    # Prepare the sys.argv list so that Streamlit knows which file to run.
    sys.argv = ["streamlit", "run", __file__]
    streamlit.web.cli.main()