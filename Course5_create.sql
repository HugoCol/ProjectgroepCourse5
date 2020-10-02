-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-09-28 10:39:34.566

-- tables
-- Table: Alignments
CREATE TABLE Alignments (
    ID varchar(10) NOT NULL,
    Iteratie int NOT NULL,
    Alignment_file text NOT NULL,
    CONSTRAINT Alignments_pk PRIMARY KEY (ID)
);

-- Table: GO
CREATE TABLE GO (
    ID varchar(10) NOT NULL,
    Go_terms text NOT NULL,
    Sequentie_ID varchar(10) NOT NULL,
    CONSTRAINT GO_pk PRIMARY KEY (ID)
);

-- Table: Sequentie
CREATE TABLE Sequentie (
    ID varchar(10) NOT NULL,
    Seq text NOT NULL,
    Accessiecode varchar(75) NOT NULL,
    Alignments_ID varchar(10) NOT NULL,
    CONSTRAINT ID PRIMARY KEY (ID)
);

-- Table: Taxonomy
CREATE TABLE Taxonomy (
    ID varchar(10) NOT NULL,
    Naam varchar(40) NOT NULL,
    Sequentie_ID varchar(10) NOT NULL,
    CONSTRAINT Taxonomy_pk PRIMARY KEY (ID)
);

-- foreign keys
-- Reference: GO_Sequentie (table: GO)
ALTER TABLE GO ADD CONSTRAINT GO_Sequentie FOREIGN KEY GO_Sequentie (Sequentie_ID)
    REFERENCES Sequentie (ID);

-- Reference: Sequentie_Alignments (table: Sequentie)
ALTER TABLE Sequentie ADD CONSTRAINT Sequentie_Alignments FOREIGN KEY Sequentie_Alignments (Alignments_ID)
    REFERENCES Alignments (ID);

-- Reference: Taxonomy_Sequentie (table: Taxonomy)
ALTER TABLE Taxonomy ADD CONSTRAINT Taxonomy_Sequentie FOREIGN KEY Taxonomy_Sequentie (Sequentie_ID)
    REFERENCES Sequentie (ID);

-- End of file.
