from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel


# Dummy in-memory storage for user sessions and order histories
dummy_user_data: Dict[str, Dict[str, Any]] = {}

class UserDataToolInput(BaseModel):
    user_id: str | None = None 
    action: str | None = None 
    data: Dict[str, Any] = {}

class UserDataTool(BaseTool):
    name: str = "UserDataTool"
    description: str = (
        "Manages session data, user profiles, and order histories for personalization and state management. "
        "Currently uses dummy in-memory storage for testing purposes."
    )
    args_schema: Type[BaseModel] = UserDataToolInput

    def _run(self, user_id: str, action: str, data: Dict[str, Any]) -> str:
        if action == "create":
            if user_id in dummy_user_data:
                return f"User {user_id} already exists."
            dummy_user_data[user_id] = data
            return f"User {user_id} created with data: {data}"
        
        elif action == "update":
            if user_id not in dummy_user_data:
                return f"User {user_id} does not exist."
            dummy_user_data[user_id].update(data)
            return f"User {user_id} updated with data: {dummy_user_data[user_id]}"
        
        elif action == "get":
            user_info = dummy_user_data.get(user_id)
            if not user_info:
                return f"No data found for user {user_id}."
            return f"Data for user {user_id}: {user_info}"
        
        else:
            return "Invalid action. Please use 'create', 'update', or 'get'."


# Example usage:
if __name__ == "__main__":
    tool = UserDataTool()
    
    # Create a new user session
    print(tool._run(user_id="user123", action="create", data={"name": "Alice", "cart": [], "order_history": []}))
    
    # Update the user session with additional data
    print(tool._run(user_id="user123", action="update", data={"cart": ["Wireless Headphones"]}))
    
    # Retrieve the user session data
    print(tool._run(user_id="user123", action="get", data={}))