import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    sessions = relationship("InterviewSession", back_populates="interviewer")

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    interviewer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    interviewer = relationship("User", back_populates="sessions")
    logs = relationship("SessionLog", back_populates="session")

class SessionLog(Base):
    __tablename__ = "session_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    event_type = Column(String, nullable=False) # e.g., "CODE_RUN", "AI_ANALYSIS"
    code_snapshot = Column(Text, nullable=True)
    output_result = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    session = relationship("InterviewSession", back_populates="logs")
