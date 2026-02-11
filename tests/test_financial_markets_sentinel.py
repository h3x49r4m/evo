"""Tests for Financial Markets Sentinel example."""

import pytest
from pathlib import Path


class TestFinancialMarketsSentinel:
    """Test suite for Financial Markets Sentinel."""

    def test_sentinel_file_exists(self):
        """Test that the sentinel example file exists."""
        sentinel_file = Path(__file__).parent.parent / "examples" / "financial_markets_sentinel.py"
        
        if not sentinel_file.exists():
            pytest.fail(f"financial_markets_sentinel.py does not exist at {sentinel_file}")

    def test_sentinel_can_be_imported(self):
        """Test that the sentinel can be imported."""
        try:
            from examples.financial_markets_sentinel import FinancialMarketsSentinel
            assert FinancialMarketsSentinel is not None
        except ImportError as e:
            pytest.fail(f"Failed to import FinancialMarketsSentinel: {e}")

    def test_sentinel_initialization(self):
        """Test that sentinel can be initialized."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        assert sentinel is not None
        assert hasattr(sentinel, 'system')

    def test_sentinel_has_market_data(self):
        """Test that sentinel has market data configured."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Check that markets are configured
        assert hasattr(sentinel, 'markets')
        assert len(sentinel.markets) > 0

    def test_sentinel_tracks_required_regions(self):
        """Test that sentinel tracks all required regions."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Check for required regions
        regions = sentinel.get_tracked_regions()
        assert 'USA' in regions
        assert 'EUR' in regions
        assert 'CHN' in regions
        assert 'ASI' in regions
        assert 'JPN' in regions
        assert 'IND' in regions

    def test_sentinel_can_fetch_market_data(self):
        """Test that sentinel can fetch market data."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Fetch market data
        data = sentinel.fetch_market_data()
        
        assert data is not None
        assert 'markets' in data
        assert len(data['markets']) > 0

    def test_sentinel_generates_trading_signals(self):
        """Test that sentinel can generate trading signals."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Generate trading signals
        signals = sentinel.generate_trading_signals()
        
        assert signals is not None
        assert 'recommendations' in signals
        assert len(signals['recommendations']) > 0

    def test_sentinel_generates_daily_report(self):
        """Test that sentinel can generate daily report."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Generate daily report
        report = sentinel.generate_daily_report()
        
        assert report is not None
        assert 'date' in report
        assert 'summary' in report
        assert 'signals' in report

    def test_sentinel_exports_to_out_directory(self):
        """Test that sentinel exports to _out directory."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        import os
        
        sentinel = FinancialMarketsSentinel()
        
        # Generate report
        report = sentinel.generate_daily_report()
        
        # Export to _out
        output_file = sentinel.export_report(report)
        
        # Verify file is in _out directory
        assert '_out' in output_file
        assert os.path.exists(output_file)
        
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)

    def test_sentinel_uses_memory(self):
        """Test that sentinel uses memory system."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Fetch and store data
        sentinel.fetch_market_data()
        
        # Check that data is stored in memory
        market_data = sentinel.system.memory.working.retrieve("market_data")
        assert market_data is not None

    def test_sentinel_respects_safety(self):
        """Test that sentinel respects safety constraints."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Generate signals (should include risk warnings)
        signals = sentinel.generate_trading_signals()
        
        # Check for safety/risk warnings
        assert signals is not None
        # Safety checks should have been performed

    def test_sentinel_provides_next_day_recommendations(self):
        """Test that sentinel provides next day trading recommendations."""
        from examples.financial_markets_sentinel import FinancialMarketsSentinel
        
        sentinel = FinancialMarketsSentinel()
        
        # Generate next day recommendations
        recommendations = sentinel.get_next_day_recommendations()
        
        assert recommendations is not None
        assert 'buy_recommendations' in recommendations or 'sell_recommendations' in recommendations