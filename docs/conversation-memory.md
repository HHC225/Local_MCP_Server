# Conversation Memory Tool

## Overview

The Conversation Memory Tool provides persistent storage and semantic retrieval of important conversation context using ChromaDB vector database. This tool enables AI assistants to maintain context across conversations, remember important decisions, and build a queryable knowledge base.

## Key Features

- **Automatic Embedding**: ChromaDB automatically generates embeddings for semantic search
- **Speaker Tracking**: Track who said what in conversations
- **Metadata Support**: Store additional context like topics, importance, timestamps
- **Semantic Search**: Find relevant conversations based on meaning, not just keywords
- **Persistent Storage**: Conversations are saved to disk and survive server restarts

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  LLM/GitHub Copilot                                 │
│  (Summarizes conversations)                         │
└───────────────┬─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  Conversation Memory Tool                           │
│  • Store summaries                                  │
│  • Query conversations                              │
│  • Track speakers                                   │
└───────────────┬─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  ChromaDB Vector Database                           │
│  • Automatic embeddings                             │
│  • Semantic search                                  │
│  • Persistent storage                               │
└─────────────────────────────────────────────────────┘
```

## Available Tools

### 1. conversation_memory_store

Store important conversation content in the vector database.

**Parameters:**
- `conversation_text` (required): Full conversation content to store
- `speaker` (optional): Name of the speaker (e.g., "User", "GitHub Copilot")
- `summary` (optional): LLM-generated summary of the conversation (recommended)
- `metadata` (optional): Additional metadata as dict
- `conversation_id` (optional): Unique identifier (auto-generated if not provided)

**Returns:**
- `success`: Boolean indicating success
- `conversation_id`: Unique ID for the stored conversation
- `metadata`: Stored metadata including timestamp
- `document_length`: Length of stored document

**Example Usage:**

```python
# Store a conversation with summary
result = await conversation_memory_store(
    conversation_text="User: How should I design the API?\nCopilot: For this use case, REST would be better than GraphQL because...",
    speaker="GitHub Copilot",
    summary="Discussion about API design: Recommended REST over GraphQL for simple CRUD operations due to lower complexity and better caching.",
    metadata={
        "topic": "API design",
        "context": "architecture planning",
        "importance": "high"
    }
)
```

**Best Practices:**
1. **Always provide summaries**: Let the LLM summarize before storing
2. **Include speaker info**: Track who provided the information
3. **Add meaningful metadata**: Use consistent keys like "topic", "context", "importance"
4. **Store key decisions**: Focus on important information, not every message

### 2. conversation_memory_query

Query stored conversations using semantic search.

**Parameters:**
- `query_text` (required): Text to search for (semantic similarity)
- `n_results` (optional): Number of results to return (default: 5)
- `filter_metadata` (optional): Metadata filters as dict

**Returns:**
- `success`: Boolean indicating success
- `query`: Original query text
- `results`: Array of matching conversations with:
  - `id`: Conversation ID
  - `document`: Stored content/summary
  - `metadata`: Associated metadata
  - `distance`: Similarity score (lower = more similar)
- `count`: Number of results returned

**Example Usage:**

```python
# Find conversations about database design
result = await conversation_memory_query(
    query_text="How should I structure the database schema?",
    n_results=3,
    filter_metadata={"topic": "database"}
)

# Access results
for item in result["results"]:
    print(f"ID: {item['id']}")
    print(f"Content: {item['document']}")
    print(f"Speaker: {item['metadata'].get('speaker')}")
    print(f"Similarity: {item['distance']}")
```

**Search Tips:**
- Semantic search finds meaning, not exact words
- Use natural language queries
- Filter by metadata to narrow results
- Lower distance scores mean better matches

### 3. conversation_memory_list

List all stored conversation memories.

**Parameters:**
- `limit` (optional): Maximum number of conversations to return
- `offset` (optional): Number of conversations to skip (default: 0)

**Returns:**
- `success`: Boolean indicating success
- `conversations`: Array of all stored conversations
- `count`: Number of conversations returned
- `total_in_db`: Total conversations in database

**Example Usage:**

```python
# List first 10 conversations
result = await conversation_memory_list(limit=10)

# List all conversations
result = await conversation_memory_list()

# Pagination
result = await conversation_memory_list(limit=10, offset=20)
```

### 4. conversation_memory_delete

Delete a specific conversation from the database.

**Parameters:**
- `conversation_id` (required): ID of the conversation to delete

**Returns:**
- `success`: Boolean indicating success
- `message`: Confirmation message

**Example Usage:**

```python
result = await conversation_memory_delete(
    conversation_id="conv_20241014_123456_789012"
)
```

### 5. conversation_memory_clear

Clear all conversations from the database.

**⚠️ WARNING**: This permanently deletes all stored conversation memories.

**Returns:**
- `success`: Boolean indicating success
- `message`: Confirmation message with count of deleted items

**Example Usage:**

```python
# Clear all conversations (use with caution!)
result = await conversation_memory_clear()
```

## Workflow Examples

### Example 1: Building Context During Development

```python
# Session 1: API Design Discussion
await conversation_memory_store(
    conversation_text="Full conversation about API endpoints...",
    speaker="GitHub Copilot",
    summary="Designed REST API with 5 endpoints: users, posts, comments, auth, and profile. Using JWT for authentication.",
    metadata={"topic": "API design", "phase": "planning"}
)

# Session 2: Later, Query Context
result = await conversation_memory_query(
    query_text="What authentication method did we decide to use?"
)
# Returns: Previous conversation about JWT authentication
```

### Example 2: Decision Tracking

```python
# Store important decisions
await conversation_memory_store(
    conversation_text="...",
    speaker="User",
    summary="Decision: Use PostgreSQL instead of MongoDB due to complex relationships and ACID requirements.",
    metadata={
        "topic": "database",
        "type": "decision",
        "importance": "high"
    }
)

# Later, find all decisions
result = await conversation_memory_query(
    query_text="database decisions",
    filter_metadata={"type": "decision"}
)
```

### Example 3: Knowledge Base Building

```python
# Store best practices
await conversation_memory_store(
    conversation_text="...",
    speaker="GitHub Copilot",
    summary="Best practice: Always validate input at API boundary, use DTOs for data transfer, and handle errors with consistent error codes.",
    metadata={
        "category": "best-practices",
        "topic": "API development"
    }
)

# Retrieve relevant best practices when needed
result = await conversation_memory_query(
    query_text="API input validation best practices",
    filter_metadata={"category": "best-practices"}
)
```

## Configuration

In `config.py` or `.env` file:

```python
# Enable/disable conversation memory tools
ENABLE_CONVERSATION_MEMORY_TOOLS=true

# Database storage path
CONVERSATION_MEMORY_DB_PATH=./chroma_db

# Default number of query results
CONVERSATION_MEMORY_DEFAULT_RESULTS=5
```

## Technical Details

### Storage Location

Conversations are stored in the ChromaDB database at:
- Default: `./chroma_db` (relative to server root)
- Configurable via `CONVERSATION_MEMORY_DB_PATH`

### Embedding Model

ChromaDB uses its default embedding model (`all-MiniLM-L6-v2`) which:
- Generates 384-dimensional embeddings
- Supports semantic similarity search
- Works offline (no API calls needed)
- Fast and efficient for most use cases

### Metadata Schema

Automatically added metadata:
- `timestamp`: ISO format datetime
- `has_summary`: Boolean indicating if summary was provided
- `character_count`: Length of original conversation

User-provided metadata:
- `speaker`: Who provided the information
- `topic`, `context`, `importance`: Recommended fields
- Any custom fields you define

## Best Practices

### 1. Summarization Strategy

**Let the LLM summarize before storing:**

```
Good prompt to LLM:
"Please summarize our conversation about database design in 2-3 sentences, 
focusing on the key decisions and recommendations."

Then store the summary with conversation_memory_store.
```

### 2. Consistent Speaker Names

Use consistent speaker identifiers:
- ✅ "User", "GitHub Copilot", "Assistant"
- ❌ "user", "Me", "Copilot", "AI"

### 3. Metadata Organization

Use consistent metadata keys:

```python
# Recommended metadata structure
metadata = {
    "topic": "category name",           # Main topic
    "context": "specific situation",    # Specific context
    "type": "decision|discussion|info", # Type of conversation
    "importance": "low|medium|high",    # Importance level
    "phase": "planning|development",    # Project phase
}
```

### 4. Query Optimization

- **Use natural language**: "How should I handle errors?" vs "error handling"
- **Be specific**: Include context in queries
- **Use filters**: Narrow results with metadata filters
- **Adjust n_results**: Start with 3-5, increase if needed

### 5. Maintenance

Periodically review and clean up:
- Delete outdated conversations
- Update important conversations if decisions change
- Archive old project contexts before starting new projects

## Common Use Cases

### 1. Context Retention
Store and retrieve context across multiple conversation sessions.

### 2. Decision Log
Maintain a searchable log of important technical decisions.

### 3. Knowledge Base
Build a project-specific knowledge base of patterns and solutions.

### 4. Best Practices Library
Store and query best practices and recommendations.

### 5. Architecture Documentation
Track architectural decisions and their rationale.

## Troubleshooting

### Database Location Issues

```python
# Check database path
import os
print(os.path.abspath("./chroma_db"))

# Use absolute path in config
CONVERSATION_MEMORY_DB_PATH="/absolute/path/to/chroma_db"
```

### Query Returns No Results

1. Verify conversations are stored: Use `conversation_memory_list()`
2. Try broader queries: Use more general language
3. Check metadata filters: Remove or adjust filters
4. Increase n_results: Try higher numbers

### Storage Fails

1. Check disk space
2. Verify write permissions
3. Check database path exists
4. Review logs for errors

## API Reference

See inline documentation in tool definitions for complete parameter details and return types.

## Related Tools

- **Recursive Thinking**: Use conversation memory to inform deep analysis
- **Sequential Thinking**: Reference past conversations in thought process
- **Tree of Thoughts**: Store exploration paths and decisions

## Limits and Considerations

- **Storage**: ChromaDB stores embeddings on disk; consider disk space for large deployments
- **Search Speed**: Query performance is excellent for up to 100K conversations
- **Embedding Model**: Default model is good for English; consider custom models for other languages
- **Context Length**: Store summaries for long conversations to improve relevance

---

**Next Steps:**
- [Troubleshooting Guide](troubleshooting.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Back to Main README](../README.md)
