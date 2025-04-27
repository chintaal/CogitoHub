from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ...db.session import get_db
from ... import crud
from ...schemas import timetunes_schemas as schemas

router = APIRouter()

# Time Entries endpoints
@router.post("/time-entries/", response_model=schemas.TimeEntry)
def create_time_entry(time_entry: schemas.TimeEntryCreate, db: Session = Depends(get_db)):
    """Create a new time entry"""
    return crud.timetunes_crud.create_time_entry(db=db, time_entry=time_entry)


@router.get("/time-entries/", response_model=List[schemas.TimeEntry])
def read_time_entries(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    project_id: Optional[str] = None,
    tag_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all time entries with optional filtering"""
    return crud.timetunes_crud.get_time_entries(
        db=db, skip=skip, limit=limit,
        start_date=start_date, end_date=end_date,
        project_id=project_id, tag_id=tag_id
    )


@router.get("/time-entries/{time_entry_id}", response_model=schemas.TimeEntry)
def read_time_entry(time_entry_id: str, db: Session = Depends(get_db)):
    """Get a specific time entry by ID"""
    time_entry = crud.timetunes_crud.get_time_entry(db=db, time_entry_id=time_entry_id)
    if time_entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return time_entry


@router.patch("/time-entries/{time_entry_id}", response_model=schemas.TimeEntry)
def update_time_entry(time_entry_id: str, time_entry: schemas.TimeEntryUpdate, db: Session = Depends(get_db)):
    """Update a time entry"""
    db_time_entry = crud.timetunes_crud.get_time_entry(db=db, time_entry_id=time_entry_id)
    if db_time_entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return crud.timetunes_crud.update_time_entry(db=db, time_entry_id=time_entry_id, time_entry=time_entry)


@router.delete("/time-entries/{time_entry_id}", response_model=schemas.TimeEntry)
def delete_time_entry(time_entry_id: str, db: Session = Depends(get_db)):
    """Delete a time entry"""
    db_time_entry = crud.timetunes_crud.get_time_entry(db=db, time_entry_id=time_entry_id)
    if db_time_entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return crud.timetunes_crud.delete_time_entry(db=db, time_entry_id=time_entry_id)


# Projects endpoints
@router.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    return crud.timetunes_crud.create_project(db=db, project=project)


@router.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects"""
    return crud.timetunes_crud.get_projects(db=db, skip=skip, limit=limit)


@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: str, db: Session = Depends(get_db)):
    """Get a specific project by ID"""
    project = crud.timetunes_crud.get_project(db=db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: str, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project"""
    db_project = crud.timetunes_crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.timetunes_crud.update_project(db=db, project_id=project_id, project=project)


@router.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete a project"""
    db_project = crud.timetunes_crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.timetunes_crud.delete_project(db=db, project_id=project_id)


# Tags endpoints
@router.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """Create a new tag"""
    return crud.timetunes_crud.create_tag(db=db, tag=tag)


@router.get("/tags/", response_model=List[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tags"""
    return crud.timetunes_crud.get_tags(db=db, skip=skip, limit=limit)


@router.get("/tags/{tag_id}", response_model=schemas.Tag)
def read_tag(tag_id: str, db: Session = Depends(get_db)):
    """Get a specific tag by ID"""
    tag = crud.timetunes_crud.get_tag(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/tags/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: str, tag: schemas.TagUpdate, db: Session = Depends(get_db)):
    """Update a tag"""
    db_tag = crud.timetunes_crud.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return crud.timetunes_crud.update_tag(db=db, tag_id=tag_id, tag=tag)


@router.delete("/tags/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: str, db: Session = Depends(get_db)):
    """Delete a tag"""
    db_tag = crud.timetunes_crud.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return crud.timetunes_crud.delete_tag(db=db, tag_id=tag_id)


# Analytics endpoints
@router.get("/analytics/summary", response_model=schemas.TimeSummary)
def get_time_summary(
    start_date: datetime = Query(..., description="Start date for the time range"),
    end_date: datetime = Query(..., description="End date for the time range"),
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get summary statistics for time entries"""
    return crud.timetunes_crud.get_time_summary(
        db=db,
        start_date=start_date,
        end_date=end_date,
        project_id=project_id
    )


@router.get("/analytics/by-project", response_model=List[schemas.ProjectTimeSummary])
def get_time_by_project(
    start_date: datetime = Query(..., description="Start date for the time range"),
    end_date: datetime = Query(..., description="End date for the time range"),
    db: Session = Depends(get_db)
):
    """Get time breakdown by project"""
    return crud.timetunes_crud.get_time_by_project(
        db=db,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/analytics/by-tag", response_model=List[schemas.TagTimeSummary])
def get_time_by_tag(
    start_date: datetime = Query(..., description="Start date for the time range"),
    end_date: datetime = Query(..., description="End date for the time range"),
    db: Session = Depends(get_db)
):
    """Get time breakdown by tag"""
    return crud.timetunes_crud.get_time_by_tag(
        db=db,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/analytics/by-day", response_model=List[schemas.DailyTimeSummary])
def get_time_by_day(
    start_date: datetime = Query(..., description="Start date for the time range"),
    end_date: datetime = Query(..., description="End date for the time range"),
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get time breakdown by day"""
    return crud.timetunes_crud.get_time_by_day(
        db=db,
        start_date=start_date,
        end_date=end_date,
        project_id=project_id
    )