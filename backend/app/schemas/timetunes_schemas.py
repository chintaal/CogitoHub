from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


# Tag schemas
class TagBase(BaseModel):
    name: str
    color: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    name: Optional[str] = None


class TagResponse(TagBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    is_archived: Optional[bool] = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    is_archived: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Time Entry schemas
class TimeEntryBase(BaseModel):
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None  # In minutes
    is_running: Optional[bool] = False
    project_id: Optional[str] = None


class TimeEntryCreate(TimeEntryBase):
    tag_ids: Optional[List[str]] = []


class TimeEntryUpdate(BaseModel):
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    is_running: Optional[bool] = None
    project_id: Optional[str] = None
    tag_ids: Optional[List[str]] = None


class TimeEntryResponse(TimeEntryBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    project: Optional[ProjectResponse] = None
    tags: List[TagResponse] = []

    class Config:
        orm_mode = True


# Analytics schemas
class TimeSummary(BaseModel):
    """Summary statistics for time tracking"""
    total_entries: int
    total_duration_minutes: float
    average_entry_minutes: Optional[float] = None
    longest_entry_minutes: Optional[float] = None
    shortest_entry_minutes: Optional[float] = None
    first_entry_date: Optional[datetime] = None
    last_entry_date: Optional[datetime] = None


class ProjectTimeSummary(BaseModel):
    """Time summary for a specific project"""
    project_id: str
    project_name: str
    project_color: Optional[str] = None
    total_entries: int
    total_duration_minutes: float
    percentage_of_total: float  # Percentage of total tracked time


class TagTimeSummary(BaseModel):
    """Time summary for a specific tag"""
    tag_id: str
    tag_name: str
    tag_color: Optional[str] = None
    total_entries: int
    total_duration_minutes: float
    percentage_of_total: float  # Percentage of total tracked time


class DailyTimeSummary(BaseModel):
    """Time summary for a specific day"""
    date: datetime
    total_entries: int
    total_duration_minutes: float
    projects: Optional[Dict[str, float]] = None  # Project ID to duration mapping