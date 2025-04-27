from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..db.database import Base

# Association table for time entries and tags (many-to-many)
time_entry_tags = Table(
    "time_entry_tags",
    Base.metadata,
    Column("time_entry_id", String, ForeignKey("time_entries.id"), primary_key=True),
    Column("tag_id", String, ForeignKey("tags.id"), primary_key=True)
)


class TimeEntry(Base):
    """Time entry model for tracking time spent on projects"""
    __tablename__ = "time_entries"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)  # Null if timer is still running
    duration = Column(Float, nullable=True)  # Duration in minutes
    is_running = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="time_entries")
    
    # Many-to-many relationship with tags
    tags = relationship("Tag", secondary=time_entry_tags, back_populates="time_entries")


class Project(Base):
    """Project model for grouping time entries"""
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    color = Column(String, nullable=True)
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    time_entries = relationship("TimeEntry", back_populates="project")


class Tag(Base):
    """Tag model for categorizing time entries"""
    __tablename__ = "tags"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    color = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Many-to-many relationship with time entries
    time_entries = relationship("TimeEntry", secondary=time_entry_tags, back_populates="tags")