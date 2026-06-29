from pydantic import BaseModel


class ScanRequest(BaseModel):
	directory: str
