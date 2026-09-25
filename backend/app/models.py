"""SQLAlchemy models."""
import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    pages_or_sections = Column(String, default="")
    text_content = Column(Text, default="")
    char_count = Column(Integer, default=0)
    suspicious_flag = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"
    id = Column(Integer, primary_key=True)
    mode = Column(String, nullable=False)
    prompt_version = Column(String, nullable=False)
    prompt_text = Column(Text, default="")
    model = Column(String, nullable=False)
    latency_ms = Column(Integer, default=0)
    document_ids = Column(String, default="")
    executive_summary = Column(Text, default="")
    limitations = Column(Text, default="[]")
    raw_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    findings = relationship("Finding", back_populates="run", cascade="all, delete-orphan")


class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("analysis_runs.id"), nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    evidence_json = Column(Text, default="[]")
    recommended_action = Column(Text, default="")
    status = Column(String, default="pending")  # pending|accepted|edited|rejected
    reviewer_comment = Column(Text, default="")
    edited_title = Column(String, default="")
    edited_description = Column(Text, default="")
    edited_action = Column(Text, default="")
    run = relationship("AnalysisRun", back_populates="findings")
