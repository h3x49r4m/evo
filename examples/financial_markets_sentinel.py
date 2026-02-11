"""Financial Markets Sentinel - Global market tracking and trading advisor.

This example demonstrates how to use the evo autonomous agent system
to track global financial markets and generate trading recommendations.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.main import create_evo_system
from evo.config import Config


class FinancialMarketsSentinel:
    """Autonomous agent for tracking global financial markets and generating trading advice."""

    def __init__(self):
        """Initialize the Financial Markets Sentinel."""
        self.system = create_evo_system()
        self.memory = self.system.memory
        self.safety = self.system.safety
        self.llm_client = self.system.action.llm_client if hasattr(self.system.action, 'llm_client') else None
        self.model = Config.LLM_MODEL
        
        # Configure markets by region
        self.markets = self._configure_markets()

    def _configure_markets(self) -> Dict[str, List[Dict[str, str]]]:
        """Configure market indices and instruments by region.
        
        Returns:
            Dictionary mapping regions to their market instruments.
        """
        return {
            'USA': [
                {'name': 'S&P 500', 'symbol': 'SPX', 'type': 'index'},
                {'name': 'NASDAQ', 'symbol': 'IXIC', 'type': 'index'},
                {'name': 'Dow Jones', 'symbol': 'DJI', 'type': 'index'},
            ],
            'EUR': [
                {'name': 'FTSE 100', 'symbol': 'UKX', 'type': 'index'},
                {'name': 'DAX', 'symbol': 'DAX', 'type': 'index'},
                {'name': 'CAC 40', 'symbol': 'CAC', 'type': 'index'},
            ],
            'CHN': [
                {'name': 'Shanghai Composite', 'symbol': 'SSEC', 'type': 'index'},
                {'name': 'Shenzhen Component', 'symbol': 'SZI', 'type': 'index'},
            ],
            'ASI': [
                {'name': 'Hang Seng', 'symbol': 'HSI', 'type': 'index'},
                {'name': 'Nikkei 225', 'symbol': 'N225', 'type': 'index'},
                {'name': 'KOSPI', 'symbol': 'KS11', 'type': 'index'},
            ],
            'JPN': [
                {'name': 'Nikkei 225', 'symbol': 'N225', 'type': 'index'},
                {'name': 'TOPIX', 'symbol': 'TPX', 'type': 'index'},
            ],
            'IND': [
                {'name': 'BSE Sensex', 'symbol': 'SENSEX', 'type': 'index'},
                {'name': 'Nifty 50', 'symbol': 'NIFTY', 'type': 'index'},
            ],
            'Americas': [
                {'name': 'S&P TSX', 'symbol': 'GSPTSE', 'type': 'index'},
                {'name': 'Bovespa', 'symbol': 'BVSP', 'type': 'index'},
            ],
        }

    def get_tracked_regions(self) -> List[str]:
        """Get list of tracked regions.
        
        Returns:
            List of region codes.
        """
        return list(self.markets.keys())

    def fetch_market_data(self) -> Dict[str, Any]:
        """Fetch current market data for all tracked regions.
        
        Returns:
            Dictionary containing market data.
        """
        print(f"\n{'='*60}")
        print("Fetching market data...")
        print(f"{'='*60}\n")
        
        market_data = {'timestamp': datetime.now().isoformat(), 'markets': {}}
        
        # Fetch data for each region
        for region, instruments in self.markets.items():
            print(f"Fetching data for {region}...")
            region_data = []
            
            for instrument in instruments:
                # Simulate fetching data (in real implementation, use API)
                data_point = self._fetch_instrument_data(instrument)
                region_data.append(data_point)
            
            market_data['markets'][region] = region_data
        
        # Store in memory
        self.memory.working.store("market_data", market_data)
        
        print(f"\n✓ Fetched data for {len(self.markets)} regions")
        
        return market_data

    def _fetch_instrument_data(self, instrument: Dict[str, str]) -> Dict[str, Any]:
        """Fetch data for a single instrument.
        
        Args:
            instrument: Dictionary with instrument details.
            
        Returns:
            Dictionary with instrument data.
        """
        # In real implementation, fetch from financial API
        # For demo, generate realistic-looking data
        import random
        
        base_price = 100 + random.random() * 1000
        change_percent = (random.random() - 0.5) * 5  # -2.5% to +2.5%
        
        return {
            'name': instrument['name'],
            'symbol': instrument['symbol'],
            'type': instrument['type'],
            'price': round(base_price, 2),
            'change': round(base_price * change_percent / 100, 2),
            'change_percent': round(change_percent, 2),
            'volume': random.randint(1000000, 100000000),
        }

    def generate_trading_signals(self) -> Dict[str, Any]:
        """Generate trading signals based on market data.
        
        Returns:
            Dictionary containing trading signals.
        """
        print(f"\n{'='*60}")
        print("Generating trading signals...")
        print(f"{'='*60}\n")
        
        # Get market data from memory
        market_data = self.memory.working.retrieve("market_data")
        
        if not market_data:
            market_data = self.fetch_market_data()
        
        recommendations = []
        
        # Analyze each market
        for region, instruments in market_data['markets'].items():
            for instrument in instruments:
                signal = self._analyze_instrument(instrument)
                recommendations.append(signal)
        
        # Store signals in memory
        self.memory.working.store("trading_signals", recommendations)
        
        print(f"✓ Generated {len(recommendations)} trading signals")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations,
            'summary': self._summarize_signals(recommendations)
        }

    def _analyze_instrument(self, instrument: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an instrument and generate trading signal.
        
        Args:
            instrument: Dictionary with instrument data.
            
        Returns:
            Dictionary with trading recommendation.
        """
        change = instrument.get('change_percent', 0)
        
        # Simple technical analysis
        if change > 1.5:
            action = 'SELL'
            reason = 'Strong upward movement, take profits'
            risk = 'Medium'
        elif change > 0.5:
            action = 'HOLD'
            reason = 'Moderate upward movement, monitor'
            risk = 'Low'
        elif change > -0.5:
            action = 'HOLD'
            reason = 'Consolidation, wait for direction'
            risk = 'Low'
        elif change > -1.5:
            action = 'BUY'
            reason = 'Dip in price, potential reversal'
            risk = 'Medium'
        else:
            action = 'HOLD'
            reason = 'Strong downward movement, wait for stabilization'
            risk = 'High'
        
        return {
            'instrument': instrument['name'],
            'symbol': instrument['symbol'],
            'action': action,
            'reason': reason,
            'risk_level': risk,
            'current_price': instrument['price'],
            'change_percent': instrument['change_percent'],
        }

    def _summarize_signals(self, recommendations: List[Dict[str, Any]]) -> Dict[str, int]:
        """Summarize trading signals.
        
        Args:
            recommendations: List of trading recommendations.
            
        Returns:
            Dictionary with signal counts.
        """
        summary = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        
        for rec in recommendations:
            action = rec.get('action', 'HOLD')
            summary[action] = summary.get(action, 0) + 1
        
        return summary

    def get_next_day_recommendations(self) -> Dict[str, Any]:
        """Get next day trading recommendations.
        
        Returns:
            Dictionary with next day recommendations.
        """
        signals = self.generate_trading_signals()
        
        # Filter for actionable signals
        buy_signals = [s for s in signals['recommendations'] if s['action'] == 'BUY']
        sell_signals = [s for s in signals['recommendations'] if s['action'] == 'SELL']
        
        return {
            'date': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + 
                     timedelta(days=1)).strftime('%Y-%m-%d'),
            'buy_recommendations': buy_signals[:3],  # Top 3 buys
            'sell_recommendations': sell_signals[:3],  # Top 3 sells
            'overall_sentiment': self._calculate_sentiment(signals['summary']),
        }

    def _calculate_sentiment(self, summary: Dict[str, int]) -> str:
        """Calculate overall market sentiment.
        
        Args:
            summary: Dictionary with signal counts.
            
        Returns:
            Sentiment string.
        """
        buys = summary.get('BUY', 0)
        sells = summary.get('SELL', 0)
        
        if buys > sells * 1.5:
            return 'Bullish'
        elif sells > buys * 1.5:
            return 'Bearish'
        else:
            return 'Neutral'

    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily market report.
        
        Returns:
            Dictionary containing daily report.
        """
        print(f"\n{'='*60}")
        print("Generating daily report...")
        print(f"{'='*60}\n")
        
        # Fetch data and generate signals
        market_data = self.fetch_market_data()
        signals = self.generate_trading_signals()
        
        # Use LLM to generate market commentary if available
        commentary = self._generate_market_commentary(market_data, signals)
        
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'summary': signals['summary'],
            'commentary': commentary,
            'signals': signals['recommendations'],
            'next_day': self.get_next_day_recommendations(),
            'disclaimer': 'This is for educational purposes only. Not financial advice. Always do your own research before trading.',
        }
        
        # Store report in memory
        self.memory.working.store("daily_report", report)
        
        print(f"✓ Daily report generated")
        
        return report

    def _generate_market_commentary(self, market_data: Dict[str, Any], signals: Dict[str, Any]) -> str:
        """Generate market commentary using LLM.
        
        Args:
            market_data: Market data.
            signals: Trading signals.
            
        Returns:
            Market commentary text.
        """
        if self.llm_client:
            try:
                summary = signals['summary']
                prompt = f"""Write a brief market commentary (100-150 words) based on these trading signals:

Buy signals: {summary.get('BUY', 0)}
Sell signals: {summary.get('SELL', 0)}
Hold signals: {summary.get('HOLD', 0)}

Overall sentiment: {self._calculate_sentiment(summary)}

Focus on:
- Market direction
- Key drivers
- Risk factors
- Outlook"""

                commentary = self.llm_client.respond(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return commentary
            except Exception:
                pass
        
        # Fallback commentary
        sentiment = self._calculate_sentiment(signals['summary'])
        return f"Markets are showing {sentiment.lower()} sentiment. Monitor key support and resistance levels."

    def export_report(self, report: Dict[str, Any]) -> str:
        """Export daily report to markdown file.
        
        Args:
            report: The daily report dictionary.
            
        Returns:
            Path to exported file.
        """
        from datetime import timedelta
        
        print(f"\n{'='*60}")
        print("Exporting report...")
        print(f"{'='*60}\n")
        
        # Generate filename with date
        filename = f"_out/markets_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# Financial Markets Sentinel - Daily Report\n\n")
            f.write(f"**Date:** {report['date']}\n\n")
            
            # Summary
            f.write(f"## Market Summary\n\n")
            f.write(f"- **Buy Signals:** {report['summary'].get('BUY', 0)}\n")
            f.write(f"- **Sell Signals:** {report['summary'].get('SELL', 0)}\n")
            f.write(f"- **Hold Signals:** {report['summary'].get('HOLD', 0)}\n")
            f.write(f"- **Overall Sentiment:** {report['next_day']['overall_sentiment']}\n\n")
            
            # Commentary
            f.write(f"## Market Commentary\n\n")
            f.write(f"{report['commentary']}\n\n")
            
            # Trading Signals
            f.write(f"## Trading Signals\n\n")
            for signal in report['signals']:
                f.write(f"### {signal['instrument']} ({signal['symbol']})\n\n")
                f.write(f"- **Action:** {signal['action']}\n")
                f.write(f"- **Reason:** {signal['reason']}\n")
                f.write(f"- **Risk Level:** {signal['risk_level']}\n")
                f.write(f"- **Price:** {signal['current_price']}\n")
                f.write(f"- **Change:** {signal['change_percent']}%\n\n")
            
            # Next Day Recommendations
            f.write(f"## Next Day Trading Recommendations\n\n")
            f.write(f"**Date:** {report['next_day']['date']}\n\n")
            
            if report['next_day']['buy_recommendations']:
                f.write(f"### Buy Opportunities\n\n")
                for rec in report['next_day']['buy_recommendations']:
                    f.write(f"- **{rec['instrument']}**: {rec['reason']}\n")
                f.write(f"\n")
            
            if report['next_day']['sell_recommendations']:
                f.write(f"### Sell Opportunities\n\n")
                for rec in report['next_day']['sell_recommendations']:
                    f.write(f"- **{rec['instrument']}**: {rec['reason']}\n")
                f.write(f"\n")
            
            # Disclaimer
            f.write(f"---\n\n")
            f.write(f"## Disclaimer\n\n")
            f.write(f"{report['disclaimer']}\n")
        
        print(f"✓ Report exported to: {filename}")
        
        return filename


def main():
    """Main entry point for Financial Markets Sentinel demo."""
    from datetime import timedelta
    
    print("="*60)
    print("Financial Markets Sentinel")
    print("Global market tracking and trading advisor")
    print("="*60)
    
    # Create sentinel
    sentinel = FinancialMarketsSentinel()
    
    # Generate daily report
    report = sentinel.generate_daily_report()
    
    # Export report
    output_file = sentinel.export_report(report)
    
    print(f"\n{'='*60}")
    print("Report complete!")
    print(f"Report saved to: {output_file}")
    print("="*60)


if __name__ == "__main__":
    main()