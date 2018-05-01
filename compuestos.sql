CREATE TABLE Compuesto(
  id_Compuesto INT PRIMARY KEY,
  name_Compuesto VARCHAR(30),
  formula VARCHAR(30),
  Descripcion VARCHAR(100),
  Area DOUBLE,
  Concentacion VARCHAR(30)

)
ENGINE = INNODB;

CREATE TABLE GruposFuncionales(
  id_GF INT PRIMARY KEY,
  name_GF VARCHAR(30),
  Rango1 INT,
  Rango2 INT

)
ENGINE = INNODB;

create table Compuesto_GF(
  id_GF int,
  id_Compuesto int,
  CONSTRAINT fk_id_GF FOREIGN KEY (id_GF) REFERENCES  GruposFuncionales(id_GF),
  CONSTRAINT fk_id_Compuesto FOREIGN KEY (id_Compuesto) REFERENCES Compuesto(id_Compuesto)
)
ENGINE = INNODB;



INSERT INTO GruposFuncionales(id_GF, name_GF,Rango1,Rango2) VALUES
(1, "H20", 3667, 3766),
(2, "CaSO4-2H2O", 3385, 3405),
(3, "CaSO4-2H2O", 3479,3499),
(4, "CaSO4-2H2O", 998, 1018),
(5, "CaSO4-2H2O", 1125, 1145),
(6, "CaSO4", 864, 884);








