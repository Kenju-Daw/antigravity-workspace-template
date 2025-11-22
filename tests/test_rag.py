import pytest
from unittest.mock import MagicMock, AsyncMock, patch, mock_open
from backend.rag.ingest import IngestionPipeline
from backend.rag.store import VectorStore

@pytest.mark.asyncio
async def test_ingestion_pipeline():
    # Mock LocalClient and VectorStore
    with patch('backend.rag.ingest.LocalClient') as MockLocalClient, \
         patch('backend.rag.ingest.VectorStore') as MockVectorStore:
        
        mock_client = MockLocalClient.return_value
        mock_client.embed = AsyncMock(return_value=[0.1, 0.2, 0.3])
        mock_client.generate = AsyncMock(return_value="Summary")
        
        mock_store = MockVectorStore.return_value
        
        pipeline = IngestionPipeline(watch_dir="test_dir")
        
        # Create a dummy file
        with patch('builtins.open', mock_open(read_data="content")) as mock_file:
            with patch('os.walk') as mock_walk:
                mock_walk.return_value = [("root", [], ["file.txt"])]
                
                await pipeline.process_folder("test_dir")
                
                # Verify embedding was generated
                mock_client.embed.assert_called_once_with("content")
                
                # Verify document was added to store
                mock_store.add_documents.assert_called_once()

@pytest.mark.asyncio
async def test_vector_store():
    # This test requires actual ChromaDB, which might fail if dependencies aren't perfect.
    # We'll mock the client.
    with patch('chromadb.PersistentClient') as MockClient:
        store = VectorStore()
        store.collection = MagicMock()
        
        store.add_documents(["doc"], [{"meta": "data"}], ["id"], [[0.1]])
        store.collection.add.assert_called_once()
