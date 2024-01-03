from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FINISHED: _ClassVar[JobStatus]
    FAILED: _ClassVar[JobStatus]
FINISHED: JobStatus
FAILED: JobStatus

class RegisterAsWorkerRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RegisterAsWorkerReply(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetJobsRequest(_message.Message):
    __slots__ = ("id", "last_job_id", "last_job_status", "last_job_error")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_JOB_STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_JOB_ERROR_FIELD_NUMBER: _ClassVar[int]
    id: str
    last_job_id: str
    last_job_status: JobStatus
    last_job_error: str
    def __init__(self, id: _Optional[str] = ..., last_job_id: _Optional[str] = ..., last_job_status: _Optional[_Union[JobStatus, str]] = ..., last_job_error: _Optional[str] = ...) -> None: ...

class GetJobsReply(_message.Message):
    __slots__ = ("id", "url", "retries")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    RETRIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    retries: str
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ..., retries: _Optional[str] = ...) -> None: ...
