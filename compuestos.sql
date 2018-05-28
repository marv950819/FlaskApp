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
  estado INT,
  PRIMARY KEY (id_GF),
  CONSTRAINT fk_id_Compuesto FOREIGN KEY (id_Compuesto) REFERENCES Compuesto(id_Compuesto)
)
ENGINE = INNODB;

DELIMITER //
CREATE TRIGGER Compuesto_GF
AFTER INSERT ON Compuesto
FOR EACH ROW
BEGIN
   UPDATE GruposFuncionales
    SET  id_Compuesto = NEW.id_Compuesto WHERE  NEW.name_Compuesto LIKE CONCAT("%",name_Compuesto,"%") ;

END// 
DELIMITER ;



INSERT INTO GruposFuncionales(name_Compuesto,name_GF,Rango1,Rango2,estado) VALUES
("Yeso","H20", 3500, 3600, 5),
("Yeso","SO4-2H2O", 3385, 3405, 6),
("Yeso","SO4-2H2O", 3479,3499, 6),
("Yeso","SO4-2H2O", 1016, 1018, 6),
("Yeso","SO4-2H2O", 1125, 1145, 6),
("Yeso","SO4", 864, 884, 8),
("Yeso","SO4", 670,682 , 8),
("Yeso","SO4-1/2H2O", 1004,1015, 7),
("Yeso","CaC03", 722,732, 2),
("Yeso","CaC03", 1415,1435, 1),
("Yeso","CaC03", 872,900, 2);


INSERT INTO GruposFuncionales(name_Compuesto,name_GF,Rango1,Rango2,estado) VALUES
("Cuarzo","Si-O", 1100,1200, 4),
("Cuarzo","Si-O-Si", 1000,1100, 3),
("Cuarzo","Si-O", 770,800, 3),
("Cuarzo","Si-O", 400,550, 3);


INSERT INTO Compuesto(name_Compuesto,formula,Descripcion,Area,Concentacion) VALUES
("Yeso-Crudo", "", "Yeso con porcentaje de agua",0,"");


INSERT INTO Compuesto(name_Compuesto,formula,Descripcion,Area,Concentacion) VALUES
("Cuarzo","", "Cuarzo seco",0,"");


