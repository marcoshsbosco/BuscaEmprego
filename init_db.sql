drop database buscaemprego;
create database buscaemprego;
use buscaemprego;

drop user 'buscaemprego'@'%';
create user 'buscaemprego'@'%' identified by 'buscaemp_api';
grant all privileges on buscaemprego.* to 'buscaemprego'@'%' identified by 'buscaemp_api';
flush privileges;

create table usuarios (usuario VARCHAR(64), senha VARCHAR(64));
