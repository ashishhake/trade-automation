from core.data_loader import load_csv_data, load_yahoo_data
from core.config_loader import load_config
from strategies.moving_average import moving_average_crossover
from core.risk_manager import apply_risk_management
from core.execution import execute_trades
from backtests.backtest_ma import backtest_strategy
from core.performance import calculate_performance


def main():
    # Step 0: Load configuration (from settings.yaml)
    config = load_config("config/settings.yaml")

    # Step 1: Load market data (CSV or Yahoo Finance)
    if config["data"]["source"] == "yahoo":
        data = load_yahoo_data(
            symbol=config["data"]["symbol"],
            start=config["data"]["start_date"],
            end=config["data"]["end_date"]
        )
    else:
        data = load_csv_data(config["data"]["file_path"])
    

    # Step 2: Generate strategy signals (Moving Average Crossover)
    strategy_data = moving_average_crossover(
        data,
        short_window=config["strategy"]["short_window"],
        long_window=config["strategy"]["long_window"]
    )

    # Step 3: Apply risk management
    risk_data = apply_risk_management(
        strategy_data,
        risk_per_trade=config["risk"]["risk_per_trade"]
    )

    # Step 4: Execute trades (simulation)
    execution_data = execute_trades(risk_data)

    # Step 5: Run backtest (portfolio simulation)
    final_results = backtest_strategy(
        execution_data,
        initial_capital=config["backtest"]["initial_capital"]
    )

    # Final Output
    print("===== CONFIG-DRIVEN TRADING BOT OUTPUT =====")
    print(final_results.tail())  # Show last few rows only (cleaner)

    print("\nFinal Portfolio Value:",
          final_results['Portfolio_Value'].iloc[-1])
    
    # Step 6: Performance Metrics
    performance = calculate_performance(final_results)

    print("\n===== PERFORMANCE METRICS =====")
    for key, value in performance.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
