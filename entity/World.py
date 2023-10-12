class World:
    def __init__(self, name="", description="", types=0, typesName="", intro="", source=0, ranks=0):
        self.id = 0
        self.name = name
        self.description = description
        self.types = types
        self.typesName = typesName
        self.intro = intro
        self.ranks = ranks  # Define 'ranks' here
        self.exp = 0
        self.scores = 0
        self.status = 5
        self.imgUrl = ""
        self.source = source
        self.isPrive = 2

    def initialize(self):
        self.exp = 0
        self.ranks = 0
        self.status = 5
        self.scores = 0
        self.isPrive = 2

