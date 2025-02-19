#!/usr/bin/env python
from crewai.flow import Flow, listen, start
from travel_agent_flow.crews.trip_crew.trip_crew import TripCrew

class TravelFlow(Flow):

    @start()
    def start_flow(self):
        print("starting travel flow")
        user_input  = {
        "origin": "New York, NY",
        "city": "Tokyo, Japan",
        "travel_dates": "April",
        "interests": "Cultural Tours, Photography"
        }

        return user_input

    @listen(start_flow)
    def generate_travel_guide(self,user_input):
        print("Generating guide")
        result = (
            TripCrew().crew().kickoff(inputs=user_input)
        )

        return result

def kickoff():
    travel_flow = TravelFlow()
    result = travel_flow.kickoff()
    print("result>>>",result)


def plot():
    travel_flow = TravelFlow()
    travel_flow.plot()


if __name__ == "__main__":
    kickoff()
