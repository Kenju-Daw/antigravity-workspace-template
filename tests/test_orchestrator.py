import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from backend.agent.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_orchestrator_routing():
    orchestrator = Orchestrator()
    
    # Test High Complexity -> Gemini
    with patch.object(orchestrator, '_delegate_to_gemini', new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = {"source": "Gemini", "response": "Planned"}
        response = await orchestrator.process_request("Please plan a complex architecture")
        assert response["source"] == "Gemini"
        mock_gemini.assert_called_once()

    # Test Low Complexity -> Local
    with patch.object(orchestrator, '_delegate_to_local', new_callable=AsyncMock) as mock_local:
        mock_local.return_value = {"source": "Local", "response": "Summarized"}
        response = await orchestrator.process_request("Summarize this file")
        assert response["source"] == "Local"
        mock_local.assert_called_once()
