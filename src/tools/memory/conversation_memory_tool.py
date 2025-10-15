"""
Conversation Memory Tool Implementation
ChromaDB-based conversation memory management for storing and retrieving important conversation context
"""
from typing import Dict, Any, List, Optional
from fastmcp import Context
from datetime import datetime
import chromadb
from chromadb.config import Settings
import json
import os
from pathlib import Path
from ..base import ReasoningTool


class ConversationMemoryTool(ReasoningTool):
    """Conversation Memory Tool for managing conversation context with ChromaDB"""
    
    def __init__(self, persist_directory: str = "./output/chroma_db"):
        super().__init__(
            name="conversation_memory",
            description="ChromaDB-based conversation memory management tool"
        )
        
        # Initialize ChromaDB client with persistence
        self.persist_directory = persist_directory
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection for conversation memories
        self.collection = self.client.get_or_create_collection(
            name="conversation_memories",
            metadata={"description": "Stores important conversation summaries"}
        )
    
    async def execute(
        self,
        action: str,
        ctx: Optional[Context] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute conversation memory action
        
        Args:
            action: Action to perform (store, query, list, delete, clear)
            ctx: FastMCP context
            **kwargs: Action-specific parameters
        
        Returns:
            Dict containing action results
        """
        await self.log_execution(ctx, f"Executing conversation memory action: {action}")
        
        if action == "store":
            return await self._store_conversation(ctx, **kwargs)
        elif action == "query":
            return await self._query_conversations(ctx, **kwargs)
        elif action == "list":
            return await self._list_conversations(ctx, **kwargs)
        elif action == "delete":
            return await self._delete_conversation(ctx, **kwargs)
        elif action == "clear":
            return await self._clear_all(ctx)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _store_conversation(
        self,
        ctx: Optional[Context],
        conversation_text: str,
        speaker: Optional[str] = None,
        summary: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Store conversation summary in vector database
        
        Args:
            ctx: FastMCP context
            conversation_text: The conversation content to store
            speaker: Name of the speaker (optional)
            summary: Summary of the conversation (if None, stores full text)
            metadata: Additional metadata to store
            conversation_id: Unique identifier for this conversation (auto-generated if None)
        
        Returns:
            Dict with storage confirmation and ID
        """
        try:
            # Generate ID if not provided
            if not conversation_id:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                conversation_id = f"conv_{timestamp}"
            
            # Prepare document to store
            document = summary if summary else conversation_text
            
            # Prepare metadata
            meta = {
                "timestamp": datetime.now().isoformat(),
                "has_summary": summary is not None,
                "character_count": len(conversation_text)
            }
            
            if speaker:
                meta["speaker"] = speaker
            
            if metadata:
                # Convert metadata values to ChromaDB-compatible types
                # ChromaDB only accepts: str, int, float, bool, or None
                sanitized_metadata = {}
                for key, value in metadata.items():
                    if isinstance(value, (list, tuple)):
                        # Convert lists/tuples to comma-separated strings
                        sanitized_metadata[key] = ", ".join(str(v) for v in value)
                    elif isinstance(value, dict):
                        # Convert dicts to JSON strings
                        sanitized_metadata[key] = json.dumps(value)
                    elif isinstance(value, (str, int, float, bool)) or value is None:
                        # Keep primitive types as-is
                        sanitized_metadata[key] = value
                    else:
                        # Convert other types to strings
                        sanitized_metadata[key] = str(value)
                
                meta.update(sanitized_metadata)
            
            # Store in ChromaDB with automatic embedding
            self.collection.add(
                documents=[document],
                metadatas=[meta],
                ids=[conversation_id]
            )
            
            await self.log_execution(
                ctx,
                f"Stored conversation with ID: {conversation_id}"
            )
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "message": "Conversation stored successfully",
                "metadata": meta,
                "document_length": len(document)
            }
            
        except Exception as e:
            error_msg = f"Error storing conversation: {str(e)}"
            await self.log_execution(ctx, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    async def _query_conversations(
        self,
        ctx: Optional[Context],
        query_text: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query conversations using semantic search
        
        Args:
            ctx: FastMCP context
            query_text: Text to search for
            n_results: Number of results to return
            filter_metadata: Optional metadata filters
        
        Returns:
            Dict with query results
        """
        try:
            # Query ChromaDB with automatic embedding
            query_params = {
                "query_texts": [query_text],
                "n_results": n_results
            }
            
            if filter_metadata:
                query_params["where"] = filter_metadata
            
            results = self.collection.query(**query_params)
            
            # Format results
            formatted_results = []
            if results["ids"] and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    result_item = {
                        "id": results["ids"][0][i],
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    }
                    formatted_results.append(result_item)
            
            await self.log_execution(
                ctx,
                f"Query returned {len(formatted_results)} results"
            )
            
            return {
                "success": True,
                "query": query_text,
                "results": formatted_results,
                "count": len(formatted_results)
            }
            
        except Exception as e:
            error_msg = f"Error querying conversations: {str(e)}"
            await self.log_execution(ctx, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    async def _list_conversations(
        self,
        ctx: Optional[Context],
        limit: Optional[int] = None,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List all stored conversations
        
        Args:
            ctx: FastMCP context
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip
        
        Returns:
            Dict with list of conversations
        """
        try:
            # Get all items from collection
            results = self.collection.get(
                limit=limit,
                offset=offset,
                include=["documents", "metadatas"]
            )
            
            # Format results
            conversations = []
            if results["ids"]:
                for i in range(len(results["ids"])):
                    conv = {
                        "id": results["ids"][i],
                        "document": results["documents"][i] if results["documents"] else None,
                        "metadata": results["metadatas"][i] if results["metadatas"] else None
                    }
                    conversations.append(conv)
            
            await self.log_execution(
                ctx,
                f"Listed {len(conversations)} conversations"
            )
            
            return {
                "success": True,
                "conversations": conversations,
                "count": len(conversations),
                "total_in_db": self.collection.count()
            }
            
        except Exception as e:
            error_msg = f"Error listing conversations: {str(e)}"
            await self.log_execution(ctx, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    async def _delete_conversation(
        self,
        ctx: Optional[Context],
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Delete a specific conversation
        
        Args:
            ctx: FastMCP context
            conversation_id: ID of conversation to delete
        
        Returns:
            Dict with deletion confirmation
        """
        try:
            self.collection.delete(ids=[conversation_id])
            
            await self.log_execution(
                ctx,
                f"Deleted conversation: {conversation_id}"
            )
            
            return {
                "success": True,
                "message": f"Conversation {conversation_id} deleted successfully"
            }
            
        except Exception as e:
            error_msg = f"Error deleting conversation: {str(e)}"
            await self.log_execution(ctx, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    async def _clear_all(
        self,
        ctx: Optional[Context]
    ) -> Dict[str, Any]:
        """
        Clear all conversations from database
        
        Args:
            ctx: FastMCP context
        
        Returns:
            Dict with clear confirmation
        """
        try:
            # Get count before clearing
            count_before = self.collection.count()
            
            # Delete collection and recreate
            self.client.delete_collection(name="conversation_memories")
            self.collection = self.client.get_or_create_collection(
                name="conversation_memories",
                metadata={"description": "Stores important conversation summaries"}
            )
            
            await self.log_execution(
                ctx,
                f"Cleared all conversations ({count_before} items)"
            )
            
            return {
                "success": True,
                "message": f"Cleared all conversations ({count_before} items removed)"
            }
            
        except Exception as e:
            error_msg = f"Error clearing conversations: {str(e)}"
            await self.log_execution(ctx, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
