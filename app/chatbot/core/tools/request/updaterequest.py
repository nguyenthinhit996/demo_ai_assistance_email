from typing import Optional, Type, Union, List, Dict
from datetime import date, datetime
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from app.core.app_helper import get_app
from enum import Enum

class StatusRequest(str, Enum):
    TODO = "Todo"
    IMPROCESSING = "In processing"
    FEEDBACK = "Feedback"

class UpdateRequestToolInput(BaseModel):
    id: str = Field(description="id of request")
    name: Optional[str] = Field(description="Name of the request", default=None)
    status: Optional[StatusRequest] = Field(description="Status of the request", default=None)
    time: Optional[Union[datetime, date]] = Field(description="Date or datetime of the request", default=None)

class UpdateRequestTool(BaseTool):
    name: str = "UpdateRequestTool"
    description: str = "Useful for users who want to update a request"
    args_schema: Type[BaseModel] = UpdateRequestToolInput
    return_direct: bool = True

    def _run(
        self, 
        id: str, 
        name: Optional[str] = None, 
        status: Optional[StatusRequest] = None, 
        time: Optional[Union[datetime, date]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Dict]:
        """Use the tool to update a request."""
        app = get_app()
        mock_requests = app.state.mock_requests

        # Track whether any updates are applied
        updates_made = False

        # Update the actual mock_requests data in place
        for request in mock_requests:
            if (id and request["request_id"] == id) or (name and request["name"] == name):
                if status:
                    request["status"] = status.value if isinstance(status, StatusRequest) else status
                if time:
                    request["date"] = time.isoformat() if isinstance(time, datetime) else str(time)
                updates_made = True

        if not updates_made:
            return [{"message": "No matching requests found to update."}]

        return [{"message": "Requests updated successfully.", "updated_requests": mock_requests}]

    async def _arun(
        self,
        id: str,
        name: Optional[str] = None,
        status: Optional[StatusRequest] = None, 
        time: Optional[Union[datetime, date]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> List[Dict]:
        """Use the tool asynchronously."""
        return self._run(id, name, status, time, run_manager=run_manager.get_sync())
