def execute_stategies(strategies: dict[str, str]):
    try:
        for strategy_name, product_id in strategies.items():
            print(f"Executing strategy: {strategy_name} for product_id: {product_id}")
    except Exception as e:
        print(f"Error in execute_stategies: {str(e)}")

if __name__ == '__main__':
    execute_stategies({"btc_agg_100": "btc-usd", "eth_mod_100": "eth-usd", "sol_mod_100": "sol-usd"})
