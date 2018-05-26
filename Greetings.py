class Greetings(KnowledgeEngine):
    @DefFacts()
    def set_sumaponderacion(self, sumaPonderacion):
        yield Fact(sumaPonderacion=sumaPonderacion)
                   
    @DefFacts()
    def init_sequence(self):
        yield Fact(action="true")
        
    @Rule(Fact(action='true'),Fact(sumaPonderacion = 24))
    def yesoCrudo(self):
        self.declare(Fact(compuestos='Yeso-Crudo'))
        
    @Rule(Fact(action='true'),Fact(sumaPonderacion = 20))
    def Basanita(self):
        self.declare(Fact(compuestos='Basanita'))
        
    @Rule(Fact(action='true'),Fact(sumaPonderacion = 19))
    def anhidrita(self):
        self.declare(Fact(compuestos='Anhidrita'))
        
    @Rule(Fact(action='true'),Fact(sumaPonderacion = 30))
    def calcitaCuarzo(self):
        self.declare(Fact(compuestos='Calcita-Cuarzo'))
    
    @Rule(Fact(action='true'),Fact(sumaPonderacion=25))
    def calcitaCuarzo2(self):
        self.declare(Fact(compuestos='Calcita-Cuarzo'))