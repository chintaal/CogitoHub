from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uuid

from ..models import timetunes_models as models
from ..schemas import timetunes_schemas as schemas


# Time Entries CRUD operations
def create_time_entry(db: Session, time_entry: schemas.TimeEntryCreate):
    """Create a new time entry"""
    # Generate UUID for the time entry
    db_time_entry = models.TimeEntry(
        id=str(uuid.uuid4()),
        description=time_entry.description,
        start_time=time_entry.start_time,
        end_time=time_entry.end_time,
        duration=time_entry.duration,
        is_running=time_entry.is_running,
        project_id=time_entry.project_id
    )
    
    # Add tags if provided
    if time_entry.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(time_entry.tag_ids)).all()
        db_time_entry.tags = tags
    
    db.add(db_time_entry)
    db.commit()
    db.refresh(db_time_entry)
    return db_time_entry


def get_time_entries(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    project_id: Optional[str] = None,
    tag_id: Optional[str] = None,
):
    """Get all time entries with optional filtering"""
    query = db.query(models.TimeEntry)
    
    # Apply filters
    if start_date:
        query = query.filter(models.TimeEntry.start_time >= start_date)
    
    if end_date:
        query = query.filter(models.TimeEntry.start_time <= end_date)
    
    if project_id:
        query = query.filter(models.TimeEntry.project_id == project_id)
    
    if tag_id:
        query = query.join(models.TimeEntry.tags).filter(models.Tag.id == tag_id)
    
    # Order by start time desc (newest first)
    query = query.order_by(desc(models.TimeEntry.start_time))
    
    return query.offset(skip).limit(limit).all()


def get_time_entry(db: Session, time_entry_id: str):
    """Get a specific time entry by ID"""
    return db.query(models.TimeEntry).filter(models.TimeEntry.id == time_entry_id).first()


def update_time_entry(db: Session, time_entry_id: str, time_entry: schemas.TimeEntryUpdate):
    """Update a time entry"""
    db_time_entry = db.query(models.TimeEntry).filter(models.TimeEntry.id == time_entry_id).first()
    
    # Update fields if provided
    update_data = time_entry.dict(exclude_unset=True)
    
    # Handle tag_ids separately
    tag_ids = update_data.pop("tag_ids", None)
    
    # Update the time entry fields
    for key, value in update_data.items():
        setattr(db_time_entry, key, value)
    
    # Update tags if provided
    if tag_ids is not None:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()
        db_time_entry.tags = tags
    
    db.commit()
    db.refresh(db_time_entry)
    return db_time_entry


def delete_time_entry(db: Session, time_entry_id: str):
    """Delete a time entry"""
    db_time_entry = db.query(models.TimeEntry).filter(models.TimeEntry.id == time_entry_id).first()
    db.delete(db_time_entry)
    db.commit()
    return db_time_entry


# Projects CRUD operations
def create_project(db: Session, project: schemas.ProjectCreate):
    """Create a new project"""
    db_project = models.Project(
        id=str(uuid.uuid4()),
        name=project.name,
        description=project.description,
        color=project.color,
        is_archived=project.is_archived
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """Get all projects"""
    return db.query(models.Project).order_by(models.Project.name).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: str):
    """Get a specific project by ID"""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def update_project(db: Session, project_id: str, project: schemas.ProjectUpdate):
    """Update a project"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: str):
    """Delete a project"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    
    # Set project_id to NULL for all time entries that use this project
    for time_entry in db_project.time_entries:
        time_entry.project_id = None
    
    db.delete(db_project)
    db.commit()
    return db_project


# Tags CRUD operations
def create_tag(db: Session, tag: schemas.TagCreate):
    """Create a new tag"""
    db_tag = models.Tag(
        id=str(uuid.uuid4()),
        name=tag.name,
        color=tag.color
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    """Get all tags"""
    return db.query(models.Tag).order_by(models.Tag.name).offset(skip).limit(limit).all()


def get_tag(db: Session, tag_id: str):
    """Get a specific tag by ID"""
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def update_tag(db: Session, tag_id: str, tag: schemas.TagUpdate):
    """Update a tag"""
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    
    update_data = tag.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: str):
    """Delete a tag"""
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return db_tag


# Analytics operations
def get_time_summary(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    project_id: Optional[str] = None
):
    """Get time summary statistics"""
    query = db.query(models.TimeEntry)
    
    # Apply filters
    query = query.filter(models.TimeEntry.start_time >= start_date)
    query = query.filter(models.TimeEntry.start_time <= end_date)
    
    if project_id:
        query = query.filter(models.TimeEntry.project_id == project_id)
    
    # Get all time entries that match the criteria
    entries = query.all()
    
    # Calculate total entries
    total_entries = len(entries)
    
    if total_entries == 0:
        return schemas.TimeSummary(
            total_entries=0,
            total_duration_minutes=0.0
        )
    
    # Calculate durations
    durations = [entry.duration for entry in entries if entry.duration is not None]
    total_duration = sum(durations)
    avg_duration = total_duration / len(durations) if durations else 0
    max_duration = max(durations) if durations else 0
    min_duration = min(durations) if durations else 0
    
    # Get first and last entry dates
    first_entry = min(entries, key=lambda x: x.start_time)
    last_entry = max(entries, key=lambda x: x.start_time)
    
    return schemas.TimeSummary(
        total_entries=total_entries,
        total_duration_minutes=total_duration,
        average_entry_minutes=avg_duration,
        longest_entry_minutes=max_duration,
        shortest_entry_minutes=min_duration,
        first_entry_date=first_entry.start_time,
        last_entry_date=last_entry.start_time
    )


def get_time_by_project(
    db: Session,
    start_date: datetime,
    end_date: datetime
):
    """Get time tracked grouped by project"""
    # Get all time entries in the date range
    entries = db.query(models.TimeEntry).filter(
        models.TimeEntry.start_time >= start_date,
        models.TimeEntry.start_time <= end_date,
        models.TimeEntry.duration.isnot(None)  # Only include entries with a duration
    ).all()
    
    # Calculate total time
    total_time = sum([entry.duration for entry in entries if entry.duration is not None])
    
    if total_time == 0:
        return []
    
    # Group by project
    project_data = {}
    for entry in entries:
        project_id = entry.project_id if entry.project_id else "unassigned"
        if project_id not in project_data:
            project_name = entry.project.name if entry.project else "Unassigned"
            project_color = entry.project.color if entry.project else None
            project_data[project_id] = {
                "project_id": project_id,
                "project_name": project_name,
                "project_color": project_color,
                "total_entries": 0,
                "total_duration_minutes": 0.0
            }
        
        project_data[project_id]["total_entries"] += 1
        project_data[project_id]["total_duration_minutes"] += entry.duration or 0.0
    
    # Calculate percentages
    result = []
    for project_id, data in project_data.items():
        percentage = (data["total_duration_minutes"] / total_time) * 100
        result.append(schemas.ProjectTimeSummary(
            project_id=project_id,
            project_name=data["project_name"],
            project_color=data["project_color"],
            total_entries=data["total_entries"],
            total_duration_minutes=data["total_duration_minutes"],
            percentage_of_total=percentage
        ))
    
    # Sort by total duration (descending)
    result.sort(key=lambda x: x.total_duration_minutes, reverse=True)
    return result


def get_time_by_tag(
    db: Session,
    start_date: datetime,
    end_date: datetime
):
    """Get time tracked grouped by tag"""
    # Get all time entries in the date range
    entries = db.query(models.TimeEntry).filter(
        models.TimeEntry.start_time >= start_date,
        models.TimeEntry.start_time <= end_date,
        models.TimeEntry.duration.isnot(None)  # Only include entries with a duration
    ).all()
    
    # Calculate total time
    total_time = sum([entry.duration for entry in entries if entry.duration is not None])
    
    if total_time == 0:
        return []
    
    # Group by tag
    tag_data = {}
    for entry in entries:
        # Handle entries with multiple tags
        if not entry.tags:
            # Count as "untagged"
            tag_id = "untagged"
            if tag_id not in tag_data:
                tag_data[tag_id] = {
                    "tag_id": tag_id,
                    "tag_name": "Untagged",
                    "tag_color": None,
                    "total_entries": 0,
                    "total_duration_minutes": 0.0
                }
            
            tag_data[tag_id]["total_entries"] += 1
            tag_data[tag_id]["total_duration_minutes"] += entry.duration or 0.0
        else:
            # Distribute the time proportionally among the tags
            time_per_tag = (entry.duration or 0.0) / len(entry.tags)
            
            for tag in entry.tags:
                if tag.id not in tag_data:
                    tag_data[tag.id] = {
                        "tag_id": tag.id,
                        "tag_name": tag.name,
                        "tag_color": tag.color,
                        "total_entries": 0,
                        "total_duration_minutes": 0.0
                    }
                
                tag_data[tag.id]["total_entries"] += 1
                tag_data[tag.id]["total_duration_minutes"] += time_per_tag
    
    # Calculate percentages
    result = []
    for tag_id, data in tag_data.items():
        percentage = (data["total_duration_minutes"] / total_time) * 100
        result.append(schemas.TagTimeSummary(
            tag_id=data["tag_id"],
            tag_name=data["tag_name"],
            tag_color=data["tag_color"],
            total_entries=data["total_entries"],
            total_duration_minutes=data["total_duration_minutes"],
            percentage_of_total=percentage
        ))
    
    # Sort by total duration (descending)
    result.sort(key=lambda x: x.total_duration_minutes, reverse=True)
    return result


def get_time_by_day(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    project_id: Optional[str] = None
):
    """Get time tracked grouped by day"""
    # Get all time entries in the date range
    query = db.query(models.TimeEntry).filter(
        models.TimeEntry.start_time >= start_date,
        models.TimeEntry.start_time <= end_date,
        models.TimeEntry.duration.isnot(None)  # Only include entries with a duration
    )
    
    if project_id:
        query = query.filter(models.TimeEntry.project_id == project_id)
    
    entries = query.all()
    
    # Group by day
    day_data = {}
    for entry in entries:
        # Get the date part only (without time)
        day = entry.start_time.date()
        day_str = day.isoformat()
        
        if day_str not in day_data:
            day_data[day_str] = {
                "date": datetime.combine(day, datetime.min.time()),
                "total_entries": 0,
                "total_duration_minutes": 0.0,
                "projects": {}
            }
        
        day_data[day_str]["total_entries"] += 1
        day_data[day_str]["total_duration_minutes"] += entry.duration or 0.0
        
        # Track time by project
        project_id_entry = entry.project_id if entry.project_id else "unassigned"
        if project_id_entry not in day_data[day_str]["projects"]:
            day_data[day_str]["projects"][project_id_entry] = 0.0
        
        day_data[day_str]["projects"][project_id_entry] += entry.duration or 0.0
    
    # Convert to list of DailyTimeSummary
    result = []
    for day_str, data in day_data.items():
        result.append(schemas.DailyTimeSummary(
            date=data["date"],
            total_entries=data["total_entries"],
            total_duration_minutes=data["total_duration_minutes"],
            projects=data["projects"]
        ))
    
    # Sort by date (ascending)
    result.sort(key=lambda x: x.date)
    return result