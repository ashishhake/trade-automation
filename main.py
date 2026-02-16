from core.data_loader import load_csv_data
from strategies.moving_average import moving_average_crossover
from core.risk_manager import apply_risk_management
from core.execution import execute_trades
from backtests.backtest_ma import backtest_strategy


def main():
    # Step 1: Load market data
    file_path = "data/sample_data.csv"
    data = load_csv_data(file_path)

    # Step 2: Generate strategy signals
    strategy_data = moving_average_crossover(data, short_window=3, long_window=5)

    # Step 3: Apply risk management
    risk_data = apply_risk_management(strategy_data, risk_per_trade=0.1)

    # Step 4: Execute trades (simulation)
    execution_data = execute_trades(risk_data)

    # Step 5: Backtest performance
    final_results = backtest_strategy(execution_data, initial_capital=10000)

    # Print final structured output
    print("Final Trading Bot Output:")
    print(final_results)
    print("\nFinal Portfolio Value:", final_results['Portfolio_Value'].iloc[-1])


if __name__ == "__main__":
    main()
