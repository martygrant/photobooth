import cups

conn = cups.Connection()
printers = conn.getPrinters()

canonName = "Canon_TS5000_series"
canon = printers[canonName]

conn.enablePrinter(canonName)

print(canon)

print(dir(conn))
cups.setUser('pi')


#conn.printFile(canon, filename, title, options)
conn.printFile(canonName, "test.txt", "tp1", {"copies": "1"})
