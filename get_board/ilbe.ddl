/*
[relation]

	repos_ilbe (num) -|-----< (num) repos_ilbe_cmts

*/

-- ilbe board main
CREATE TABLE repos_ilbe (
	num bigint,
	title varchar(100),
	author varchar(50),
	wdate timestamp,
	recommend int,
	content text);

-- ilbe board comments
CREATE TABLE repos_ilbe_cmts (
	num bigint,
	author varchar(50),
	wdate timestamp,
	reply text);
	
