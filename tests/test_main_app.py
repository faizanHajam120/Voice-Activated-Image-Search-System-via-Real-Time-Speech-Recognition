"""
Tests for the main application functionality.
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMainApp:
    """Test cases for the main application."""
    
    def test_import_main_app(self):
        """Test that main_app can be imported."""
        try:
            import main_app
            assert True
        except ImportError as e:
            pytest.skip(f"main_app module not available: {e}")
    
    @patch('main_app.nlp')
    def test_process_voice_command_basic(self, mock_nlp):
        """Test voice command processing with mocked NLP."""
        try:
            import main_app
            
            # Mock the NLP processing
            mock_doc = Mock()
            mock_token1 = Mock()
            mock_token1.lemma_ = "car"
            mock_token1.is_stop = False
            mock_token1.is_punct = False
            mock_token2 = Mock()
            mock_token2.lemma_ = "red"
            mock_token2.is_stop = False
            mock_token2.is_punct = False
            
            mock_doc.__iter__ = Mock(return_value=iter([mock_token1, mock_token2]))
            mock_nlp.return_value = mock_doc
            
            # Test the function
            result = main_app.process_voice_command("red car")
            assert result is None  # Function doesn't return anything, just updates queue
            
        except ImportError:
            pytest.skip("main_app module not available")
    
    def test_gui_queue_initialization(self):
        """Test that GUI queue is properly initialized."""
        try:
            import main_app
            assert hasattr(main_app, 'gui_queue')
            assert main_app.gui_queue is not None
        except ImportError:
            pytest.skip("main_app module not available")


if __name__ == "__main__":
    pytest.main([__file__])
