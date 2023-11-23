from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class LastKnownTip(BaseModel):
    slot: Optional[int] = None
    hash: Optional[str] = None
    block_no: Optional[int] = Field(None, alias="blockNo")


class RuntimeStats(BaseModel):
    cpu_time: Optional[int] = Field(None, alias="cpuTime")
    current_heap_size: Optional[int] = Field(None, alias="currentHeapSize")
    gc_cpu_time: Optional[int] = Field(None, alias="gcCpuTime")
    max_heap_size: Optional[int] = Field(None, alias="maxHeapSize")


class SessionDurations(BaseModel):
    max: Optional[int] = None
    mean: Optional[float] = None
    min: Optional[int] = None


class Metrics(BaseModel):
    active_connections: Optional[int] = Field(None, alias="activeConnections")
    runtime_stats: Optional[RuntimeStats] = Field(None, alias="runtimeStats")
    session_durations: Optional[SessionDurations] = Field(
        None, alias="sessionDurations"
    )
    total_connections: Optional[int] = Field(None, alias="totalConnections")
    total_messages: Optional[int] = Field(None, alias="totalMessages")
    total_unrouted: Optional[int] = Field(None, alias="totalUnrouted")


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
