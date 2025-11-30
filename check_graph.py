def load_file(name):
    degrees = dict()
    with open(name, "r") as file:
        for line in file:
            vertices = [int(val) for val in line.split()]
            for v in vertices:
                if (v not in degrees):
                    degrees[v] = 0
                degrees[v] += 1
    for v in degrees.values():
        if (v not in [0, 3]):
            print("Podgraf neni validni")
    print("Podgraf je validni")

load_file("vystup")
