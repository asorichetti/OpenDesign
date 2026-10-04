# API Design

## Protocol

ConnectRPC over HTTP/JSON with SSE for streaming responses.

Generated clients live in `services/web/src/lib/` and are consumed by React hooks.

## Services

### ChatService

Stream a conversation to/from an LLM provider.

```protobuf
service ChatService {
  // Send messages and receive a streaming assistant response
  rpc StreamChat(StreamChatRequest) returns (stream StreamChatResponse);
  
  // Regenerate the last assistant response
  rpc Regenerate(RegenerateRequest) returns (stream StreamChatResponse);
}

message StreamChatRequest {
  string conversation_id = 1;
  repeated Message messages = 2;
  string model = 3;
  string system_prompt = 4;
}

message StreamChatResponse {
  string delta = 1;        // Text fragment (streamed)
  bool done = 2;           // true on last chunk
  string error = 3;        // Non-empty if error occurred
}

message Message {
  string role = 1;         // "user" or "assistant"
  string content = 2;      // Markdown text
  repeated Attachment attachments = 3;
  int32 order = 4;
}

message Attachment {
  string id = 1;
  string filename = 2;
  string mime_type = 3;
  int64 size_bytes = 4;
}
```

### ConversationService

CRUD for conversations.

```protobuf
service ConversationService {
  rpc ListConversations(ListConversationsRequest) returns (ListConversationsResponse);
  rpc GetConversation(GetConversationRequest) returns (GetConversationResponse);
  rpc CreateConversation(CreateConversationRequest) returns (Conversation);
  rpc UpdateConversation(UpdateConversationRequest) returns (Conversation);
  rpc DeleteConversation(DeleteConversationRequest) returns (Empty);
  rpc SearchConversations(SearchConversationsRequest) returns (ListConversationsResponse);
}

message ListConversationsRequest {
  string user_id = 1;
  string folder_id = 2;       // optional filter
  int32 page = 3;
  int32 page_size = 4;
}

message ListConversationsResponse {
  repeated Conversation conversations = 1;
  int32 total = 2;
}

message GetConversationRequest {
  string conversation_id = 1;
}

message GetConversationResponse {
  Conversation conversation = 1;
  repeated Message messages = 2;
}

message CreateConversationRequest {
  string user_id = 1;
  string folder_id = 2;       // optional
}

message UpdateConversationRequest {
  string conversation_id = 1;
  string title = 2;           // optional, auto-generated if omitted
  string folder_id = 3;       // optional, null to ungroup
}

message DeleteConversationRequest {
  string conversation_id = 1;
}

message SearchConversationsRequest {
  string user_id = 1;
  string query = 2;
}

message Conversation {
  string id = 1;
  string user_id = 2;
  string title = 3;
  string folder_id = 4;
  string created_at = 5;      // RFC 3339
  string updated_at = 6;      // RFC 3339
}

message Empty {}
```

### AuthService

Simple self-hosted auth.

```protobuf
service AuthService {
  rpc Register(RegisterRequest) returns (AuthResponse);
  rpc Login(LoginRequest) returns (AuthResponse);
  rpc Logout(LogoutRequest) returns (Empty);
  rpc WhoAmI(WhoAmIRequest) returns (User);
}

message RegisterRequest {
  string email = 1;
  string password = 2;
}

message LoginRequest {
  string email = 1;
  string password = 2;
}

message LogoutRequest {}

message WhoAmIRequest {}

message AuthResponse {
  string user_id = 1;
  string email = 2;
  string token = 3;           // JWT
}

message User {
  string id = 1;
  string email = 2;
  string api_key = 3;         // nullable
}
```

### SettingsService

User preferences.

```protobuf
service SettingsService {
  rpc GetSettings(GetSettingsRequest) returns (Settings);
  rpc UpdateSettings(UpdateSettingsRequest) returns (Settings);
}

message GetSettingsRequest {
  string user_id = 1;
}

message UpdateSettingsRequest {
  string user_id = 1;
  string theme = 2;           // "light" | "dark"
  string model = 3;           // LLM model name
  string system_prompt = 4;
}

message Settings {
  string user_id = 1;
  string theme = 2;
  string model = 3;
  string system_prompt = 4;
  string created_at = 5;
}
```

## Streaming

All chat responses use Server-Sent Events (SSE) via Connect's streaming support:

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Transfer-Encoding: chunked

data: {"delta": "Hello", "done": false}

data: {"delta": " world", "done": false}

data: {"delta": "", "done": true}
```

The frontend reads the SSE stream and appends each delta to the message buffer in real time.

## Error Handling

All errors are returned as Connect RPC errors with standard codes:
- `FailedPrecondition` — missing conversation, invalid state
- `NotFound` — conversation not found
- `Unavailable` — LLM provider down
- `InvalidArgument` — malformed request
