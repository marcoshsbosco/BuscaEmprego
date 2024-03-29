drop database buscaemprego;
create database buscaemprego;
use buscaemprego;

drop user 'buscaemprego'@'%';
create user 'buscaemprego'@'%' identified by 'buscaemp_api';
grant all privileges on buscaemprego.* to 'buscaemprego'@'%' identified by 'buscaemp_api';
flush privileges;

create table usuarios (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(64),
    senha VARCHAR(64),

    PRIMARY KEY (`id`)
);
create table vagas (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    cargo VARCHAR(64),
    funcao VARCHAR(64),
    salario DECIMAL(9, 2),
    horas INT,
    lugar VARCHAR(64),
    contato VARCHAR(64),
    id_usuario INT UNSIGNED NOT NULL,

    PRIMARY KEY (`id`),
    CONSTRAINT `fk_id_usuario`
        FOREIGN KEY (id_usuario) REFERENCES usuarios(`id`)
        ON DELETE CASCADE
);
