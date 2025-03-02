#!/usr/bin/env python
from crewai.flow import Flow, listen, start
from travel_agent_flow.crews.trip_crew.trip_crew import TripCrew
import streamlit as st


class TravelFlow(Flow):

    @start()
    def start_flow(self, user_input=None):
        if user_input is None:
            # Fallback to default values if no input provided
            user_input = {
                "origin": "New York, NY",
                "city": "Tokyo, Japan",
                "travel_dates": "April",
                "interests": "Cultural Tours, Photography"
            }
        print("Starting travel flow with input:", user_input)
        return user_input

    @listen(start_flow)
    def generate_travel_guide(self,user_input):
        print("Generating guide")
        result = (
            TripCrew().crew().kickoff(inputs=user_input)
        )

        return result
    
    def run(self, user_input):
        # Overriding kickoff to use external input
        input_data = self.start_flow(user_input)
        return self.generate_travel_guide(input_data)


def main():
    st.title("Travel Guide Generator")
    

    st.write("Enter your travel details below:")

    # Input fields for user details
    origin = st.text_input("Origin", "New York, NY")
    city = st.text_input("Destination City", "Tokyo, Japan")
    travel_dates = st.text_input("Travel Dates", "April")
    interests = st.text_input("Interests", "Cultural Tours, Photography")

    if st.button("Generate Travel Guide"):
        # Collect user input into a dictionary
        user_input = {
            "origin": origin,
            "city": city,
            "travel_dates": travel_dates,
            "interests": interests
        }
        st.info("Please wait generating Travel Guide...")
        travel_flow = TravelFlow()
        # Use the custom run method to process the user input
        result = travel_flow.run(user_input)
        st.write("Travel Guide Output:")
        st.markdown(result)

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
    travel_flow = TravelFlow()
    result = travel_flow.kickoff()
    print("result>>>",result)


def plot():
    travel_flow = TravelFlow()
    travel_flow.plot()


# if __name__ == "__main__":
#     kickoff()
