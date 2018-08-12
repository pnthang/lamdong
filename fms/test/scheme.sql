create table users (
	id serial primary key,
	username text not null,
	password text not null,
	email text not null,	
	created_at timestamp default NULL,
	updated_at timestamp default NULL,
	last_updated_by text default NULL,
	active boolean default FALSE,
	is_deleted boolean default FALSE,
	last_logined timestamp default NULL	
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "users"
  OWNER TO postgres;
  
INSERT INTO public.users(username, password, email, created_at, updated_at, last_updated_by, active) VALUES ('admin', 'admin', 'admin@local.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'sys_init',TRUE);