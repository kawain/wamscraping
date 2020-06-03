import csv
import re

csv_file = "test.csv"

pattern = r'<div class="lst-name">\d+?\.&nbsp;(.*?)</div>'
name_com = re.compile(pattern)

pattern = r'<div class="lst-service">(.*?)</div>'
service_com = re.compile(pattern)

pattern = r'<div class="lst-address">(.*?)</div>'
address_com = re.compile(pattern)

pattern = r'<div class="lst-telephone">(.*?)</div>'
tel_com = re.compile(pattern)


def save_csv(text):
    r1 = name_com.findall(text)
    r2 = service_com.findall(text)
    r3 = address_com.findall(text)
    r4 = tel_com.findall(text)

    lst = []
    for v1, v2, v3, v4 in zip(r1, r2, r3, r4):
        lst.append([v1, v2, v3, v4])

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for v in lst:
            writer.writerow(v)


if __name__ == "__main__":
    test_path = "test.txt"
    with open(test_path, encoding="utf8") as f:
        s = f.read()

    save_csv(s)
