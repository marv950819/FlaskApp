CREATE TABLE Compuesto(
  id_Compuesto int  NOT NULL AUTO_INCREMENT,
  name_Compuesto VARCHAR(30),
  formula VARCHAR(30),
  Descripcion VARCHAR(100),
  Area DOUBLE,
  Concentacion VARCHAR(30),
  PRIMARY KEY (id_Compuesto)
)
ENGINE = INNODB;

CREATE TABLE GruposFuncionales(
  id_GF INT NOT NULL AUTO_INCREMENT,
  id_Compuesto INT,
  name_Compuesto VARCHAR(30),
  name_GF VARCHAR(30),
  Rango1 INT,
  Rango2 INT,
  PRIMARY KEY (id_GF),
  CONSTRAINT fk_id_Compuesto FOREIGN KEY (id_Compuesto) REFERENCES Compuesto(id_Compuesto)
)
ENGINE = INNODB;

create table Compuesto_GF(
  id_GF int,
  id_Compuesto int,
  CONSTRAINT fk_id_GF FOREIGN KEY (id_GF) REFERENCES  GruposFuncionales(id_GF),
  CONSTRAINT fk_id_Compuesto FOREIGN KEY (id_Compuesto) REFERENCES Compuesto(id_Compuesto)
)
ENGINE = INNODB;



INSERT INTO GruposFuncionales(name_Compuesto,name_GF,Rango1,Rango2) VALUES
("Yeso","H20", 3600, 3500),
("Yeso","CaSO4-2H2O", 3385, 3405),
("Yeso","CaSO4-2H2O", 3479,3499),
("Yeso","CaSO4-2H2O", 998, 1018),
("Yeso","CaSO4-2H2O", 1125, 1145),
("Yeso","CaSO4", 864, 884),
("Yeso","CaSO4-1/2H2O", 999,1017),
("Yeso","CaC03", 722,732),
("Yeso","CaC03", 1415,1435),
("Yeso","CaC03", 872,900);


INSERT INTO GruposFuncionales(name_Compuesto,name_GF,Rango1,Rango2) VALUES
("Cuarzo","Si-O", 1100,1200),
("Cuarzo","Si-O-Si", 1000,1100),
("Cuarzo","Si-O", 770,800),
("Cuarzo","Si-O", 400,550);


(, "CaSO4-1/2H2O", 999,1017),
(, "CaC03", 722,732);
(, "CaC03", 1415,1435);
(, "CaC03", 872,900);

INSERT INTO Compuesto(name_Compuesto,formula,Descripcion,Area,Concentacion) VALUES
("Yeso-Crudo", "", "Yeso con porcentaje de agua",0,"");


INSERT INTO Compuesto(name_Compuesto,formula,Descripcion,Area,Concentacion) VALUES
("Cuarzo","", "Cuarzo seco",0,"");

INSERT INTO Compuesto_GF(id_GF,id_Compuesto) VALUES
(1,236),
(2,236),
(3,236),
(4,236),
(5,236),
(6,236),
(13,239),
(14,239),
(15,239),
(16,239);

DELIMITER //
CREATE TRIGGER Compuesto_GF
AFTER INSERT ON Compuesto
FOR EACH ROW
BEGIN
   UPDATE GruposFuncionales
    SET  id_Compuesto = NEW.id_Compuesto WHERE  NEW.name_Compuesto LIKE CONCAT("%",name_Compuesto,"%") ;

END// 
DELIMITER ;