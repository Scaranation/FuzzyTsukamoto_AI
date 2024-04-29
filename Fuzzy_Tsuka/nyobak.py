def suhu_rendah(a, b, x):
    if x <= a:
        return 1
    elif a < x <= b:
        return (b - x) / (b - a)
    elif x > b:
        return 0

def suhu_sedang(a, b, c, x):
    if x <= a or x >= c:
        return 0
    if x > a and x <= b:
        return (x - a) / (b - a)
    if x > b and x < c:
        return (c - x) / (c - b)

def suhu_tinggi(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif x > b:
        return 1

def kelembapan_rendah(a, b, x):
    if x <= a:
        return 1
    elif a < x <= b:
        return (b - x) / (b - a)
    elif x > b:
        return 0

def kelembapan_normal(a, b, c, x):
    if x <= a or x >= c:
        return 0
    if x > a and x <= b:
        return (x - a) / (b - a)
    if x > b and x < c:
        return (c - x) / (c - b)

def kelembapan_tinggi(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif x > b:
        return 1

def waktu_pendek(a, b, x):
    if x <= a:
        return 1
    elif a < x <= b:
        return (b - x) / (b - a)
    elif x > b:
        return 0

def waktu_sedang(a, b, c, x):
    if x <= a or x >= c:
        return 0
    if x > a and x <= b:
        return (x - a) / (b - a)
    if x > b and x < c:
        return (c - x) / (c - b)

def waktu_panjang(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif x > b:
        return 1

def defuzzify(alpha, z):
    numerator = 0
    denominator = 0
    for value in range(len(alpha)):
        numerator += alpha[value]["alpha"] * z[value]
        denominator += alpha[value]["alpha"]
    return numerator / denominator

def oven_process(suhu_val, kelembapan_val, waktu_val):
    suhu_rendah_val = suhu_rendah(100, 150, suhu_val)
    suhu_normal_val = suhu_sedang(100, 150, 200, suhu_val)
    suhu_tinggi_val = suhu_tinggi(150, 200, suhu_val)

    kelembapan_rendah_val = kelembapan_rendah(30, 50, kelembapan_val)
    kelembapan_normal_val = kelembapan_normal(30, 50, 70, kelembapan_val)
    kelembapan_tinggi_val = kelembapan_tinggi(50, 70, kelembapan_val)

    waktu_pendek_val = waktu_pendek(0, 30, waktu_val)
    waktu_sedang_val = waktu_sedang(0, 30, 60, waktu_val)
    waktu_panjang_val = waktu_panjang(30, 60, waktu_val)

    alpha_daya = [
        {"alpha": min(suhu_rendah_val, kelembapan_rendah_val, waktu_pendek_val), "out": "tinggi"},
        {"alpha": min(suhu_rendah_val, kelembapan_normal_val, waktu_pendek_val), "out": "tinggi"},
        {"alpha": min(suhu_rendah_val, kelembapan_tinggi_val, waktu_pendek_val), "out": "rendah"},
        {"alpha": min(suhu_normal_val, kelembapan_rendah_val, waktu_pendek_val), "out": "rendah"},
        {"alpha": min(suhu_normal_val, kelembapan_normal_val, waktu_sedang_val), "out": "sedang"},
        {"alpha": min(suhu_normal_val, kelembapan_tinggi_val, waktu_sedang_val), "out": "tinggi"},
        {"alpha": min(suhu_tinggi_val, kelembapan_rendah_val, waktu_sedang_val), "out": "tinggi"},
        {"alpha": min(suhu_tinggi_val, kelembapan_normal_val, waktu_panjang_val), "out": "tinggi"},
        {"alpha": min(suhu_tinggi_val, kelembapan_tinggi_val, waktu_panjang_val), "out": "tinggi"}
    ]

    alpha_kinerja = [
        {"alpha": min(suhu_rendah_val, kelembapan_rendah_val, waktu_pendek_val), "out": "lambat"},
        {"alpha": min(suhu_rendah_val, kelembapan_normal_val, waktu_pendek_val), "out": "lambat"},
        {"alpha": min(suhu_rendah_val, kelembapan_tinggi_val, waktu_pendek_val), "out": "lambat"},
        {"alpha": min(suhu_normal_val, kelembapan_rendah_val, waktu_pendek_val), "out": "rendah"},
        {"alpha": min(suhu_normal_val, kelembapan_normal_val, waktu_sedang_val), "out": "sedang"},
        {"alpha": min(suhu_normal_val, kelembapan_tinggi_val, waktu_sedang_val), "out": "sedang"},
        {"alpha": min(suhu_tinggi_val, kelembapan_rendah_val, waktu_sedang_val), "out": "sedang"},
        {"alpha": min(suhu_tinggi_val, kelembapan_normal_val, waktu_panjang_val), "out": "tinggi"},
        {"alpha": min(suhu_tinggi_val, kelembapan_tinggi_val, waktu_panjang_val), "out": "tinggi"}
    ]

    z_power = [40, 60, 80]
    z_performance = ["lambat", "rendah", "sedang", "tinggi"]

    power_values = []
    for rule in alpha_daya:
        if rule["out"] == "rendah":
            power_values.append(z_power[0])
        elif rule["out"] == "sedang":
            power_values.append(z_power[1])
        elif rule["out"] == "tinggi":
            power_values.append(z_power[2])

    performance_values = []
    for rule in alpha_kinerja:
        if rule["out"] == "lambat":
            performance_values.append(z_performance.index("lambat"))
        elif rule["out"] == "rendah":
            performance_values.append(z_performance.index("rendah"))
        elif rule["out"] == "sedang":
            performance_values.append(z_performance.index("sedang"))
        elif rule["out"] == "tinggi":
            performance_values.append(z_performance.index("tinggi"))

    power_output = defuzzify(alpha_daya, power_values)
    performance_output = z_performance[int(defuzzify(alpha_kinerja, performance_values))]

    return power_output, performance_output

if __name__ == "__main__":
    suhu_val = float(input("Masukkan suhu oven (derajat Celsius): "))
    kelembapan_val = float(input("Masukkan kelembapan oven (0-100 persen): "))
    waktu_val = float(input("Masukkan waktu proses (menit): "))

    power_output, performance_output = oven_process(suhu_val, kelembapan_val, waktu_val)

    print("Daya Listrik Oven:", power_output, "Watt")
    print("Kinerja Oven:", performance_output)
