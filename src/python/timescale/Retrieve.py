import timescale.Timescale as ts

if __name__ == "__main__":
  for row in ts.query_all_data():
    print(row)

  print(f"Number of entries: {ts.query_num_entries()}")
