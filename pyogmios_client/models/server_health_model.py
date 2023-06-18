from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class LastKnownTip(BaseModel):
    slot: int
    hash: str
    block_no: int = Field(..., alias="blockNo")


class RuntimeStats(BaseModel):
    cpu_time: int = Field(..., alias="cpuTime")
    current_heap_size: int = Field(..., alias="currentHeapSize")
    gc_cpu_time: int = Field(..., alias="gcCpuTime")
    max_heap_size: int = Field(..., alias="maxHeapSize")


class SessionDurations(BaseModel):
    max: int
    mean: int
    min: int


class Metrics(BaseModel):
    active_connections: int = Field(..., alias="activeConnections")
    runtime_stats: RuntimeStats = Field(..., alias="runtimeStats")
    session_durations: SessionDurations = Field(..., alias="sessionDurations")
    total_connections: int = Field(..., alias="totalConnections")
    total_messages: int = Field(..., alias="totalMessages")
    total_unrouted: int = Field(..., alias="totalUnrouted")


class ServerHealth(BaseModel):
    start_time: Optional[str] = Field(None, alias="startTime")
    last_known_tip: Optional[LastKnownTip] = Field(None, alias="lastKnownTip")
    last_tip_update: Optional[str] = Field(None, alias="lastTipUpdate")
    network_synchronization: Optional[float] = Field(
        None, alias="networkSynchronization"
    )
    current_era: Optional[str] = Field(None, alias="currentEra")
    metrics: Optional[Metrics] = None
    connection_status: Optional[str] = Field(None, alias="connectionStatus")
    current_epoch: Optional[int] = Field(None, alias="currentEpoch")
    slot_in_epoch: Optional[int] = Field(None, alias="slotInEpoch")
