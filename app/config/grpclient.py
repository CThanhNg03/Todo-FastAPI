# import grpc 

# from chatbot_pb3 import SendMessageRequest, SendMessageResponse
# from chatbot_pb3_grpc import ChatbotServicerStub

# class ChatbotClient:
#     def __init__(self):
#         self.channel = grpc.insecure_channel("localhost:50051")
#         self.stub = ChatbotServicerStub(self.channel)

#     def send_message(self, message):
#         request = SendMessageRequest(message=message)
#         response = self.stub.SendMessage(request)
#         return response.text
    
# client = ChatbotClient()
