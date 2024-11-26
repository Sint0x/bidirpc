from proto import bidi_pb2_grpc, bidi_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToDict
from .session_cache import SessionCache
from models import pydantic_models


class BidiService(bidi_pb2_grpc.BidiServiceServicer):

    def __init__(self):
        self.cache = SessionCache()

    def GetStreamMessages(self, request_iterator, context):
        for message in request_iterator:
            message_data = {
                'sourceSystem': message.sourceSystem,
                'publicationTime': message.publicationTime.ToJsonString(),
                'sessionId': message.sessionId,
                'messageId': message.messageId,
                'messageText': message.messageText,
                'messageWithContext': message.messageWithContext
            }
            try:
                msg_model = pydantic_models.MessageModel(**message_data)
            except ValueError as e:
                yield bidi_pb2.InitialResponse(error=bidi_pb2.Error(description=str(e), errorCode=400, errorType="Missing field(s)"))
                continue
                
            self.cache.add(message.sessionId, message_data)
            
            resp = bidi_pb2.InitialResponse(success=bidi_pb2.Success(code=1))
            yield resp

    def GetSessionData(self, request_iterator, context):
        for session_request in request_iterator:
            sessionId = session_request.sessionId
            try:
                session_model = pydantic_models.SessionModel(sessionId=sessionId)
            except ValueError as e:
                yield bidi_pb2.InitialResponse(
                    error=bidi_pb2.Error(
                        description=str(e),
                        errorCode=400,
                        errorType="Missing field(s)"
                    )
                )
                continue

            is_session_exist = self.cache.is_session_exist(sessionId)
            if is_session_exist:
                
                # session_data = asyncio.run(self.cache.get(sessionId)) how to get session data
                
                yield bidi_pb2.InitialResponse(
                    success=bidi_pb2.Success(code=1)
                )
            else:
                yield bidi_pb2.InitialResponse(
                    error=bidi_pb2.Error(
                        description=f"Session not exist: {sessionId}",
                        errorCode=404,
                        errorType="SessionNotFound"
                    )
                )
