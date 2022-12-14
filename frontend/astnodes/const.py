class Const:
    def __init__(self, value, num_type):
        self.value = value
        self.num_type = num_type  # use Utils.POS?

    def __str__(self):
        res = "Constant: \nType = " + self.num_type + ", value = " + self.value
        return res
