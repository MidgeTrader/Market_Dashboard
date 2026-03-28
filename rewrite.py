import re
with open(r'c:\Users\barba\Desktop\tool(2)\NYSE_SmallCaps_Dashboard\scripts\build_data.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the S&P 100 function with finviz screener
code = code.replace("def get_sp100_tickers():", '''def get_nyse_small_caps():
    print("Fetching NYSE Small Caps from Finviz...")
    try:
        from finvizfinance.screener.overview import Overview
        foverview = Overview()
        filters_dict = {
            'Exchange': 'NYSE',
            'Market Cap.': 'Small ($300mln to $2bln)',
            '50-Day Simple Moving Average': 'Price above SMA50'
        }
        foverview.set_filter(filters_dict=filters_dict)
        df = foverview.screener_view(verbose=0)
        
        tickers = df['Ticker'].tolist()
        tickers = [t.replace('.', '-') for t in tickers]
        print(f"Found {len(tickers)} potential Grade A candidates.")
        return tickers
    except Exception as e:
        print("Error fetching tickers from Finviz.", e)
        return []

def OLD_get_sp100_tickers():''')

new_main_start = '''def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    args = parser.parse_args()
    out_dir = args.out_dir
    charts_dir = os.path.join(out_dir, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    print("Fetching economic events...")
    events = get_upcoming_key_events()

    print("Fetching NYSE Small Caps (Grade A candidates)...")
    smallcap_tickers = get_nyse_small_caps()
    STOCK_GROUPS = {"NYSE Small Caps (Grado A)": smallcap_tickers}

    print("Fetching stock data...")
    groups_data = {}'''

code = re.sub(r'def main\(\):[\s\S]*?groups_data = \{\}', new_main_start, code)

# Exclude non-Grade A stocks inside get_stock_data
grade_filter = '''        abc_rating = calculate_abc_rating(daily)
        if abc_rating != "A":
            return None
'''
code = code.replace("abc_rating = calculate_abc_rating(daily)", grade_filter)

with open(r'c:\Users\barba\Desktop\tool(2)\NYSE_SmallCaps_Dashboard\scripts\build_data.py', 'w', encoding='utf-8') as f:
    f.write(code)
