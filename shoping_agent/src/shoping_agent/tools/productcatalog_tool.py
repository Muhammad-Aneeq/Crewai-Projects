from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel,Field
from shoping_agent.tools.dummy_data import dummy_products


class ProductCatalogToolInput(BaseModel):
    query: str = Field(..., description="Search query for products.")


class ProductCatalogTool(BaseTool):
    name: str = "ProductCatalogTool"
    description: str = (
        "Retrieves and displays product information such as details, pricing, and availability. "
        "This tool currently uses dummy data for testing purposes."
    )
    args_schema: Type[BaseModel] = ProductCatalogToolInput

    def _run(self, query: str) -> str:
        print("query>>>",query)
        
        # Split the query into words
        query_words = query.lower().split()
        # Filter dummy data based on query (case-insensitive search in name or details)
        filtered_products = [
        product for product in dummy_products
        if all(word in (product["name"]).lower() for word in query_words)
        ]

        # Return a formatted string of filtered products or a not found message
        if not filtered_products:
            return f"No products found matching query: {query}"
        
        return f"Products found: {filtered_products}"


# Example usage:
if __name__ == "__main__":
    tool = ProductCatalogTool()
    print(tool._run("smart"))