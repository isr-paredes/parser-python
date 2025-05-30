lines = ["line1", "line2", "line3"]
with open("lines.txt", "w") as f:
    f.write("\n".join(lines))