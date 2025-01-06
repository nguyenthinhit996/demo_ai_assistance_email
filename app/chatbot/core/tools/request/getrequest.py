from typing import Optional, Type, Union, List, Dict
from datetime import date, datetime
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from app.core.app_helper import get_app


class GetRequestToolInput(BaseModel):
    id: str = Field(description="get request by id")
    name: Optional[str] = Field(description="get request by name", default=None)
    time: Optional[Union[datetime, date]]  = Field(description="get request by date or time", default=None)

class GetRequestTool(BaseTool):
    name: str = "GetRequestTool"
    description: str = "useful for user want to get request"
    args_schema: Type[BaseModel] = GetRequestToolInput
    return_direct: bool = True

    def _run(
        self, 
        name: str, 
        id: str, 
        time: Optional[Union[datetime, date]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Dict]:
            """Use the tool."""
            app = get_app()
            mock_requests = app.state.mock_requests
            # Filter mock data based on inputs
            filtered_requests = [
                request for request in mock_requests
                if (request["name"] == name or request["request_id"] == id)
            ]

            if not filtered_requests:
                return [{"message": "No matching requests found."}]
            
            print(f"Found {filtered_requests}")

            return filtered_requests

    async def _arun(
        self,
        name: str,
        id: str, 
        time: Optional[Union[datetime, date]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> List[Dict]:
        """Use the tool asynchronously."""
        print("Using the tool asynchronously")
        # If the calculation is cheap, you can just delegate to the sync implementation
        # as shown below.
        # If the sync calculation is expensive, you should delete the entire _arun method.
        # LangChain will automatically provide a better implementation that will
        # kick off the task in a thread to make sure it doesn't block other async code.
        return self._run(name, id, time, run_manager=run_manager.get_sync()) 
    


    