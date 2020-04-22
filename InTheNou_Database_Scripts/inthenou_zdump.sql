--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12
-- Dumped by pg_dump version 10.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.usertags DROP CONSTRAINT usertags_uid_fkey;
ALTER TABLE ONLY public.usertags DROP CONSTRAINT usertags_tid_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_roleissuer_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_roleid_fkey;
ALTER TABLE ONLY public.tagtaxonomies DROP CONSTRAINT tagtaxonomies_parenttag_fkey;
ALTER TABLE ONLY public.tagtaxonomies DROP CONSTRAINT tagtaxonomies_childtag_fkey;
ALTER TABLE ONLY public.servicewebsites DROP CONSTRAINT servicewebsites_wid_fkey;
ALTER TABLE ONLY public.servicewebsites DROP CONSTRAINT servicewebsites_sid_fkey;
ALTER TABLE ONLY public.services DROP CONSTRAINT services_rid_fkey;
ALTER TABLE ONLY public.servicephones DROP CONSTRAINT servicephones_sid_fkey;
ALTER TABLE ONLY public.servicephones DROP CONSTRAINT servicephones_phoneid_fkey;
ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_photoid_fkey;
ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_bid_fkey;
ALTER TABLE ONLY public.roleprivileges DROP CONSTRAINT roleprivileges_roleid_fkey;
ALTER TABLE ONLY public.roleprivileges DROP CONSTRAINT roleprivileges_privilegeid_fkey;
ALTER TABLE ONLY public.oauth DROP CONSTRAINT oauth_uid_fkey;
ALTER TABLE ONLY public.eventwebsites DROP CONSTRAINT eventwebsites_wid_fkey;
ALTER TABLE ONLY public.eventwebsites DROP CONSTRAINT eventwebsites_eid_fkey;
ALTER TABLE ONLY public.eventuserinteractions DROP CONSTRAINT eventuserinteractions_uid_fkey;
ALTER TABLE ONLY public.eventuserinteractions DROP CONSTRAINT eventuserinteractions_eid_fkey;
ALTER TABLE ONLY public.eventtags DROP CONSTRAINT eventtags_tid_fkey;
ALTER TABLE ONLY public.eventtags DROP CONSTRAINT eventtags_eid_fkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_roomid_fkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_photoid_fkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_ecreator_fkey;
ALTER TABLE ONLY public.buildings DROP CONSTRAINT buildings_photoid_fkey;
DROP TRIGGER vectorizeservice ON public.services;
DROP TRIGGER vectorizeroomdescription ON public.rooms;
DROP TRIGGER vectorizeevent ON public.events;
ALTER TABLE ONLY public.websites DROP CONSTRAINT websites_url_key;
ALTER TABLE ONLY public.websites DROP CONSTRAINT websites_pkey;
ALTER TABLE ONLY public.usertags DROP CONSTRAINT usertags_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_usub_key;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
ALTER TABLE ONLY public.services DROP CONSTRAINT unique_room_services;
ALTER TABLE ONLY public.tagtaxonomies DROP CONSTRAINT tagtaxonomies_pkey;
ALTER TABLE ONLY public.tags DROP CONSTRAINT tags_tname_key;
ALTER TABLE ONLY public.tags DROP CONSTRAINT tags_pkey;
ALTER TABLE ONLY public.servicewebsites DROP CONSTRAINT servicewebsites_pkey;
ALTER TABLE ONLY public.services DROP CONSTRAINT services_pkey;
ALTER TABLE ONLY public.servicephones DROP CONSTRAINT servicephones_pkey;
ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_rcode_key;
ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_pkey;
ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_roletype_key;
ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
ALTER TABLE ONLY public.roleprivileges DROP CONSTRAINT roleprivileges_pkey;
ALTER TABLE ONLY public.privileges DROP CONSTRAINT privileges_privilegename_key;
ALTER TABLE ONLY public.privileges DROP CONSTRAINT privileges_pkey;
ALTER TABLE ONLY public.photos DROP CONSTRAINT photos_pkey;
ALTER TABLE ONLY public.photos DROP CONSTRAINT photos_photourl_key;
ALTER TABLE ONLY public.phones DROP CONSTRAINT phones_pnumber_key;
ALTER TABLE ONLY public.phones DROP CONSTRAINT phones_pkey;
ALTER TABLE ONLY public.oauth DROP CONSTRAINT oauth_pkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT no_duplicate_events_at_same_time_place;
ALTER TABLE ONLY public.eventwebsites DROP CONSTRAINT eventwebsites_pkey;
ALTER TABLE ONLY public.eventuserinteractions DROP CONSTRAINT eventuserinteractions_pkey;
ALTER TABLE ONLY public.eventtags DROP CONSTRAINT eventtags_pkey;
ALTER TABLE ONLY public.events DROP CONSTRAINT events_pkey;
ALTER TABLE ONLY public.buildings DROP CONSTRAINT buildings_pkey;
ALTER TABLE ONLY public.buildings DROP CONSTRAINT buildings_bname_key;
ALTER TABLE public.websites ALTER COLUMN wid DROP DEFAULT;
ALTER TABLE public.users ALTER COLUMN uid DROP DEFAULT;
ALTER TABLE public.tags ALTER COLUMN tid DROP DEFAULT;
ALTER TABLE public.services ALTER COLUMN sid DROP DEFAULT;
ALTER TABLE public.rooms ALTER COLUMN rid DROP DEFAULT;
ALTER TABLE public.roles ALTER COLUMN roleid DROP DEFAULT;
ALTER TABLE public.privileges ALTER COLUMN privilegeid DROP DEFAULT;
ALTER TABLE public.photos ALTER COLUMN photoid DROP DEFAULT;
ALTER TABLE public.phones ALTER COLUMN phoneid DROP DEFAULT;
ALTER TABLE public.events ALTER COLUMN eid DROP DEFAULT;
ALTER TABLE public.buildings ALTER COLUMN bid DROP DEFAULT;
DROP SEQUENCE public.websites_wid_seq;
DROP TABLE public.websites;
DROP TABLE public.usertags;
DROP SEQUENCE public.users_uid_seq;
DROP TABLE public.users;
DROP TABLE public.tagtaxonomies;
DROP SEQUENCE public.tags_tid_seq;
DROP TABLE public.tags;
DROP TABLE public.servicewebsites;
DROP SEQUENCE public.services_sid_seq;
DROP TABLE public.services;
DROP TABLE public.servicephones;
DROP SEQUENCE public.rooms_rid_seq;
DROP TABLE public.rooms;
DROP SEQUENCE public.roles_roleid_seq;
DROP TABLE public.roles;
DROP TABLE public.roleprivileges;
DROP SEQUENCE public.privileges_privilegeid_seq;
DROP TABLE public.privileges;
DROP SEQUENCE public.photos_photoid_seq;
DROP TABLE public.photos;
DROP SEQUENCE public.phones_phoneid_seq;
DROP TABLE public.phones;
DROP TABLE public.oauth;
DROP TABLE public.eventwebsites;
DROP TABLE public.eventuserinteractions;
DROP TABLE public.eventtags;
DROP SEQUENCE public.events_eid_seq;
DROP TABLE public.events;
DROP SEQUENCE public.buildings_bid_seq;
DROP TABLE public.buildings;
DROP FUNCTION public.vectorizeservice();
DROP FUNCTION public.vectorizeroomdescription();
DROP FUNCTION public.vectorizeevent();
DROP FUNCTION public.getbuildingnumfloors(buildingid integer);
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: getbuildingnumfloors(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.getbuildingnumfloors(buildingid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$begin
 RETURN (SELECT numFloors from public.buildings WHERE bid= buildingid); 
end; $$;


ALTER FUNCTION public.getbuildingnumfloors(buildingid integer) OWNER TO postgres;

--
-- Name: vectorizeevent(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.vectorizeevent() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	new.etitle_tokens = to_tsvector(new.etitle);
	new.edescription_tokens = to_tsvector(new.edescription);
	return new;
end $$;


ALTER FUNCTION public.vectorizeevent() OWNER TO postgres;

--
-- Name: vectorizeroomdescription(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.vectorizeroomdescription() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	new.rdescription_tokens = to_tsvector('spanish', new.rDescription);
	return new;
end $$;


ALTER FUNCTION public.vectorizeroomdescription() OWNER TO postgres;

--
-- Name: vectorizeservice(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.vectorizeservice() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	new.sname_tokens = to_tsvector(new.sname);
	new.sdescription_tokens = to_tsvector(new.sdescription);
	return new;
end $$;


ALTER FUNCTION public.vectorizeservice() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: buildings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.buildings (
    bid integer NOT NULL,
    bname text NOT NULL,
    babbrev text NOT NULL,
    numfloors integer NOT NULL,
    bcommonname text,
    btype text NOT NULL,
    photoid integer,
    CONSTRAINT buildings_bname_check CHECK ((bname <> ''::text)),
    CONSTRAINT buildings_btype_check CHECK ((btype <> ''::text)),
    CONSTRAINT buildings_numfloors_check CHECK ((numfloors > 0))
);


ALTER TABLE public.buildings OWNER TO postgres;

--
-- Name: buildings_bid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.buildings_bid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.buildings_bid_seq OWNER TO postgres;

--
-- Name: buildings_bid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.buildings_bid_seq OWNED BY public.buildings.bid;


--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    eid integer NOT NULL,
    ecreator integer NOT NULL,
    roomid integer NOT NULL,
    etitle text NOT NULL,
    edescription text NOT NULL,
    estart timestamp without time zone NOT NULL,
    eend timestamp without time zone NOT NULL,
    ecreation timestamp without time zone NOT NULL,
    estatus text NOT NULL,
    estatusdate timestamp without time zone,
    photoid integer,
    etitle_tokens tsvector,
    edescription_tokens tsvector,
    CONSTRAINT events_check CHECK ((estart < eend)),
    CONSTRAINT events_edescription_check CHECK ((edescription <> ''::text)),
    CONSTRAINT events_estatus_check CHECK ((estatus <> ''::text)),
    CONSTRAINT events_etitle_check CHECK ((etitle <> ''::text))
);


ALTER TABLE public.events OWNER TO postgres;

--
-- Name: events_eid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_eid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_eid_seq OWNER TO postgres;

--
-- Name: events_eid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_eid_seq OWNED BY public.events.eid;


--
-- Name: eventtags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventtags (
    eid integer NOT NULL,
    tid integer NOT NULL
);


ALTER TABLE public.eventtags OWNER TO postgres;

--
-- Name: eventuserinteractions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventuserinteractions (
    itype text NOT NULL,
    recommendstatus character(1) NOT NULL,
    uid integer NOT NULL,
    eid integer NOT NULL,
    CONSTRAINT eventuserinteractions_itype_check CHECK ((itype <> ''::text))
);


ALTER TABLE public.eventuserinteractions OWNER TO postgres;

--
-- Name: eventwebsites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventwebsites (
    eid integer NOT NULL,
    wid integer NOT NULL,
    wdescription text
);


ALTER TABLE public.eventwebsites OWNER TO postgres;

--
-- Name: oauth; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oauth (
    access_token text NOT NULL,
    created_at text,
    provider text NOT NULL,
    uid integer NOT NULL,
    CONSTRAINT oauth_created_at_check CHECK ((created_at <> ''::text)),
    CONSTRAINT oauth_provider_check CHECK ((provider <> ''::text)),
    CONSTRAINT oauth_token_check CHECK ((access_token <> ''::text))
);


ALTER TABLE public.oauth OWNER TO postgres;

--
-- Name: phones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phones (
    phoneid integer NOT NULL,
    pnumber text NOT NULL,
    ptype character(1) NOT NULL,
    CONSTRAINT phones_pnumber_check CHECK ((pnumber <> ''::text))
);


ALTER TABLE public.phones OWNER TO postgres;

--
-- Name: phones_phoneid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phones_phoneid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phones_phoneid_seq OWNER TO postgres;

--
-- Name: phones_phoneid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phones_phoneid_seq OWNED BY public.phones.phoneid;


--
-- Name: photos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.photos (
    photoid integer NOT NULL,
    photourl text NOT NULL,
    CONSTRAINT photos_photourl_check CHECK ((photourl <> ''::text))
);


ALTER TABLE public.photos OWNER TO postgres;

--
-- Name: photos_photoid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.photos_photoid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.photos_photoid_seq OWNER TO postgres;

--
-- Name: photos_photoid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.photos_photoid_seq OWNED BY public.photos.photoid;


--
-- Name: privileges; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.privileges (
    privilegeid integer NOT NULL,
    privilegename text NOT NULL,
    CONSTRAINT privileges_privilegename_check CHECK ((privilegename <> ''::text))
);


ALTER TABLE public.privileges OWNER TO postgres;

--
-- Name: privileges_privilegeid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.privileges_privilegeid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.privileges_privilegeid_seq OWNER TO postgres;

--
-- Name: privileges_privilegeid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.privileges_privilegeid_seq OWNED BY public.privileges.privilegeid;


--
-- Name: roleprivileges; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roleprivileges (
    roleid integer NOT NULL,
    privilegeid integer NOT NULL
);


ALTER TABLE public.roleprivileges OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    roleid integer NOT NULL,
    roletype text NOT NULL,
    CONSTRAINT roles_roletype_check CHECK ((roletype <> ''::text))
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_roleid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_roleid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_roleid_seq OWNER TO postgres;

--
-- Name: roles_roleid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_roleid_seq OWNED BY public.roles.roleid;


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    rid integer NOT NULL,
    bid integer,
    rcode text NOT NULL,
    rfloor integer NOT NULL,
    rdescription text,
    roccupancy integer,
    rdept text,
    rcustodian text,
    rlongitude numeric(10,6) NOT NULL,
    rlatitude numeric(10,6) NOT NULL,
    raltitude numeric(10,6) NOT NULL,
    photoid integer,
    rdescription_tokens tsvector,
    CONSTRAINT rooms_check CHECK (((rfloor >= 0) AND (rfloor <= public.getbuildingnumfloors(bid)))),
    CONSTRAINT rooms_rcode_check CHECK ((rcode <> ''::text))
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- Name: rooms_rid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_rid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_rid_seq OWNER TO postgres;

--
-- Name: rooms_rid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_rid_seq OWNED BY public.rooms.rid;


--
-- Name: servicephones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servicephones (
    sid integer NOT NULL,
    phoneid integer NOT NULL,
    isdeleted boolean NOT NULL
);


ALTER TABLE public.servicephones OWNER TO postgres;

--
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    sid integer NOT NULL,
    rid integer NOT NULL,
    sname text NOT NULL,
    sdescription text,
    sschedule text,
    isdeleted boolean NOT NULL,
    sname_tokens tsvector,
    sdescription_tokens tsvector,
    CONSTRAINT services_sname_check CHECK ((sname <> ''::text))
);


ALTER TABLE public.services OWNER TO postgres;

--
-- Name: services_sid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.services_sid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.services_sid_seq OWNER TO postgres;

--
-- Name: services_sid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.services_sid_seq OWNED BY public.services.sid;


--
-- Name: servicewebsites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servicewebsites (
    sid integer NOT NULL,
    wid integer NOT NULL,
    wdescription text,
    isdeleted boolean NOT NULL
);


ALTER TABLE public.servicewebsites OWNER TO postgres;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    tid integer NOT NULL,
    tname text NOT NULL,
    CONSTRAINT tags_tname_check CHECK ((tname <> ''::text))
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- Name: tags_tid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_tid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_tid_seq OWNER TO postgres;

--
-- Name: tags_tid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_tid_seq OWNED BY public.tags.tid;


--
-- Name: tagtaxonomies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tagtaxonomies (
    parenttag integer NOT NULL,
    childtag integer NOT NULL,
    CONSTRAINT tagtaxonomies_check CHECK ((parenttag <> childtag))
);


ALTER TABLE public.tagtaxonomies OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    uid integer NOT NULL,
    email text NOT NULL,
    usub text NOT NULL,
    display_name text NOT NULL,
    type text NOT NULL,
    roleid integer NOT NULL,
    roleissuer integer,
    CONSTRAINT users_check CHECK ((roleissuer <> uid)),
    CONSTRAINT users_email_check CHECK ((email <> ''::text)),
    CONSTRAINT users_type_check CHECK ((type <> ''::text)),
    CONSTRAINT users_usub_check CHECK ((usub <> ''::text))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_uid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_uid_seq OWNER TO postgres;

--
-- Name: users_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_uid_seq OWNED BY public.users.uid;


--
-- Name: usertags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usertags (
    uid integer NOT NULL,
    tid integer NOT NULL,
    tagweight integer NOT NULL,
    CONSTRAINT usertags_tagweight_check CHECK (((tagweight >= 0) AND (tagweight <= 200)))
);


ALTER TABLE public.usertags OWNER TO postgres;

--
-- Name: websites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.websites (
    wid integer NOT NULL,
    url text NOT NULL,
    CONSTRAINT websites_url_check CHECK ((url <> ''::text))
);


ALTER TABLE public.websites OWNER TO postgres;

--
-- Name: websites_wid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.websites_wid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.websites_wid_seq OWNER TO postgres;

--
-- Name: websites_wid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.websites_wid_seq OWNED BY public.websites.wid;


--
-- Name: buildings bid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buildings ALTER COLUMN bid SET DEFAULT nextval('public.buildings_bid_seq'::regclass);


--
-- Name: events eid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN eid SET DEFAULT nextval('public.events_eid_seq'::regclass);


--
-- Name: phones phoneid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phones ALTER COLUMN phoneid SET DEFAULT nextval('public.phones_phoneid_seq'::regclass);


--
-- Name: photos photoid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos ALTER COLUMN photoid SET DEFAULT nextval('public.photos_photoid_seq'::regclass);


--
-- Name: privileges privilegeid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.privileges ALTER COLUMN privilegeid SET DEFAULT nextval('public.privileges_privilegeid_seq'::regclass);


--
-- Name: roles roleid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN roleid SET DEFAULT nextval('public.roles_roleid_seq'::regclass);


--
-- Name: rooms rid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN rid SET DEFAULT nextval('public.rooms_rid_seq'::regclass);


--
-- Name: services sid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services ALTER COLUMN sid SET DEFAULT nextval('public.services_sid_seq'::regclass);


--
-- Name: tags tid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags ALTER COLUMN tid SET DEFAULT nextval('public.tags_tid_seq'::regclass);


--
-- Name: users uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN uid SET DEFAULT nextval('public.users_uid_seq'::regclass);


--
-- Name: websites wid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.websites ALTER COLUMN wid SET DEFAULT nextval('public.websites_wid_seq'::regclass);


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.buildings (bid, bname, babbrev, numfloors, bcommonname, btype, photoid) FROM stdin;
1	LUIS A STEFANI (INGENIERIA)	S	7	STEFANI	Académico	5
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (eid, ecreator, roomid, etitle, edescription, estart, eend, ecreation, estatus, estatusdate, photoid, etitle_tokens, edescription_tokens) FROM stdin;
1	2	56	Alpha Code Team Meeting	Meeting to discuss plans for integration phase.	2020-08-05 15:41:00	2020-08-05 17:41:00	2020-04-03 21:44:12.275506	active	\N	1	'alpha':1 'code':2 'meet':4 'team':3	'discuss':3 'integr':6 'meet':1 'phase':7 'plan':4
2	3	56	Alpha Code Team Meeting 2	Meeting to discuss more plans for integration phase.	2020-09-05 15:41:00	2020-09-05 17:41:00	2020-04-03 21:44:12.278819	active	\N	\N	'2':5 'alpha':1 'code':2 'meet':4 'team':3	'discuss':3 'integr':7 'meet':1 'phase':8 'plan':5
3	5	110	Dungeons and Dragons	Vanquish foes and travel to distant lands.	2020-10-05 15:41:00	2020-10-05 17:41:00	2020-04-03 21:44:12.279997	deleted	\N	2	'dragon':3 'dungeon':1	'distant':6 'foe':2 'land':7 'travel':4 'vanquish':1
5	4	1	test	test	2020-04-07 04:00:00	2020-04-07 06:00:00	2020-04-07 00:41:29.296677	active	\N	\N	'test':1	'test':1
6	4	1	test2	another test	2020-04-07 16:00:00	2020-04-07 17:00:00	2020-04-07 00:49:23.586797	active	\N	\N	'test2':1	'anoth':1 'test':2
14	4	151	Test of Event Creation 1	this is a test	2020-04-14 20:06:00	2020-04-18 03:06:00	2020-04-13 03:12:23.913639	active	\N	\N	'1':5 'creation':4 'event':3 'test':1	'test':4
15	4	165	test something	this is a test, it's different Brian!	2020-04-12 17:06:00	2020-04-17 03:18:00	2020-04-13 03:19:05.507692	active	\N	\N	'someth':2 'test':1	'brian':8 'differ':7 'test':4
16	4	9	seguimos	testiando	2020-04-16 21:22:00	2020-04-19 00:22:00	2020-04-13 03:22:31.729058	active	\N	\N	'seguimo':1	'testiando':1
4	4	55	First Event!	This is the first Event created from within the app using the Event Creation funtionality	2020-04-20 08:20:00	2020-04-20 10:09:00	2020-04-06 23:52:58.762907	active	2020-04-11 23:49:31.075567	4	'event':2 'first':1	'app':10 'creat':6 'creation':14 'event':5,13 'first':4 'funtion':15 'use':11 'within':8
19	4	70	After en las Flores	Siempre habia uno	2020-04-17 06:01:00	2020-04-17 08:00:00	2020-04-13 03:38:15.499568	deleted	2020-04-15 22:16:07.392634	\N	'en':2 'flore':4 'las':3	'habia':2 'siempr':1 'uno':3
17	4	70	Pa last Ruta Colegial	Todavía eso está abierto?  Los mejores jangueos eran en la calle bosque, Madridz empezo a moverse y se apago. RIP los Freakys, 100a1, la Biblio	2020-04-17 02:29:00	2020-04-17 06:00:00	2020-04-13 03:29:59.108327	deleted	2020-04-15 22:16:17.879285	\N	'colegi':4 'last':2 'pa':1 'ruta':3	'100a1':23 'abierto':4 'apago':19 'biblio':25 'bosqu':12 'call':11 'empezo':14 'en':9 'eran':8 'eso':2 'está':3 'freaki':22 'jangueo':7 'la':10,24 'los':5,21 'madridz':13 'mejor':6 'movers':16 'rip':20 'se':18 'todavía':1 'y':17
8	4	1	test	test	2020-04-12 18:30:00	2020-04-13 16:30:00	2020-04-12 16:30:51.65056	deleted	2020-04-12 18:32:56.476128	\N	'test':1	'test':1
7	4	1	this is long event	this is a very loooooooooooooooooooooooooooooooooooong event literally	2020-04-07 16:00:00	2020-04-13 16:01:00	2020-04-07 01:36:08.495672	active	2020-04-12 01:38:27.84066	\N	'event':4 'long':3	'event':6 'liter':7 'loooooooooooooooooooooooooooooooooooong':5
9	4	1	test for notifications	test	2020-04-13 00:10:00	2020-04-13 02:07:00	2020-04-13 00:08:17.874593	deleted	2020-04-13 00:09:25.846206	\N	'notif':3 'test':1	'test':1
10	4	1	test for recommendation	test	2020-04-13 01:25:00	2020-04-13 02:25:00	2020-04-13 00:26:13.628462	active	\N	\N	'recommend':3 'test':1	'test':1
11	4	150	Test of Event Creation 1	this is a test	2020-04-14 20:06:00	2020-04-18 03:06:00	2020-04-13 03:09:40.379359	active	\N	\N	'1':5 'creation':4 'event':3 'test':1	'test':4
18	4	70	RIP Los balcones	El mejor lugar pa chill y lo cerraron. No estuve pal tiempo de la medallas a peceta tampoco, pero los bartenders bregaban	2020-04-17 02:29:00	2020-04-17 06:00:00	2020-04-13 03:35:13.314171	deleted	2020-04-15 22:16:19.035215	\N	'balcon':3 'los':2 'rip':1	'bartend':21 'bregaban':22 'cerraron':8 'chill':5 'de':13 'el':1 'estuv':10 'la':14 'lo':7 'los':20 'lugar':3 'medalla':15 'mejor':2 'pa':4 'pal':11 'peceta':17 'pero':19 'tampoco':18 'tiempo':12 'y':6
25	4	1	dsd	dsadsa	2020-04-16 13:12:00	2020-04-16 15:12:00	2020-04-16 14:13:14.127522	active	\N	\N	'dsd':1	'dsadsa':1
26	4	1	test event for the pat	this is a test event that wil be in the past	2020-04-19 00:59:00	2020-04-25 01:59:00	2020-04-19 02:00:03.828257	active	\N	\N	'event':2 'pat':5 'test':1	'event':5 'past':11 'test':4 'wil':7
29	4	1	This is a long title .............................	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lectus est, molestie a maximus in, tempor eget elit. Morbi aliquet aliquam dignissim. Donec finibus vitae lorem nec sagittis. Curabitur sed orci a felis ornare viverra. Nunc eu sapien mattis, pretium nisl sit amet, rutrum orci. Aenean in pellentesque nibh, nec tempor velit. Suspendisse convallis leo nec sodales condimentum. Proin vit	2020-04-19 20:20:00	2020-04-25 19:25:00	2020-04-19 20:17:51.085677	active	\N	11	'long':4 'titl':5	'adipisc':7 'aenean':46 'aliquam':9,21 'aliquet':20 'amet':5,43 'condimentum':58 'consectetur':6 'conval':54 'curabitur':29 'dignissim':22 'dolor':3 'donec':23 'eget':17 'elit':8,18 'est':11 'eu':37 'feli':33 'finibus':24 'ipsum':2 'lectus':10 'leo':55 'lorem':1,26 'matti':39 'maximus':14 'molesti':12 'morbi':19 'nec':27,50,56 'nibh':49 'nisl':41 'nunc':36 'orci':31,45 'ornar':34 'pellentesqu':48 'pretium':40 'proin':59 'rutrum':44 'sagitti':28 'sapien':38 'sed':30 'sit':4,42 'sodal':57 'suspendiss':53 'tempor':16,51 'velit':52 'vit':60 'vita':25 'viverra':35
30	4	1	This is a long title .............................	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lectus est, molestie a maximus in, tempor eget elit. Morbi aliquet aliquam dignissim. Donec finibus vitae lorem nec sagittis. Curabitur sed orci a felis ornare viverra. Nunc eu sapien mattis, pretium nisl sit amet, rutrum orci. Aenean in pellentesque nibh, nec tempor velit. Suspendisse convallis leo nec sodales condimentum. Proin vit	2020-04-19 21:20:00	2020-04-25 19:25:00	2020-04-19 20:46:31.690629	active	\N	11	'long':4 'titl':5	'adipisc':7 'aenean':46 'aliquam':9,21 'aliquet':20 'amet':5,43 'condimentum':58 'consectetur':6 'conval':54 'curabitur':29 'dignissim':22 'dolor':3 'donec':23 'eget':17 'elit':8,18 'est':11 'eu':37 'feli':33 'finibus':24 'ipsum':2 'lectus':10 'leo':55 'lorem':1,26 'matti':39 'maximus':14 'molesti':12 'morbi':19 'nec':27,50,56 'nibh':49 'nisl':41 'nunc':36 'orci':31,45 'ornar':34 'pellentesqu':48 'pretium':40 'proin':59 'rutrum':44 'sagitti':28 'sapien':38 'sed':30 'sit':4,42 'sodal':57 'suspendiss':53 'tempor':16,51 'velit':52 'vit':60 'vita':25 'viverra':35
\.


--
-- Data for Name: eventtags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eventtags (eid, tid) FROM stdin;
1	42
1	54
1	64
1	6
2	42
2	54
2	64
2	73
2	47
2	53
3	71
3	44
3	87
4	54
4	57
4	58
5	1
5	2
5	3
5	4
6	1
6	2
6	3
6	4
7	1
7	2
7	54
7	57
8	1
8	2
8	3
8	4
9	1
9	2
9	3
9	4
9	5
10	1
10	2
10	3
10	4
10	5
11	1
11	2
11	3
11	4
14	1
14	2
14	3
14	4
15	1
15	2
15	3
15	4
16	1
16	3
16	2
16	4
17	1
17	2
17	3
17	4
18	1
18	2
18	3
18	4
19	1
19	2
19	3
19	4
25	1
25	2
25	3
26	1
26	2
26	3
29	1
29	2
29	3
29	6
29	5
29	4
29	7
29	8
29	9
29	10
30	1
30	2
30	3
30	6
30	5
30	4
30	7
30	8
30	9
30	10
\.


--
-- Data for Name: eventuserinteractions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eventuserinteractions (itype, recommendstatus, uid, eid) FROM stdin;
dismissed	N	5	1
following	R	5	2
none	R	3	2
unfollowed	N	3	1
unfollowed	R	4	7
none	N	4	11
none	N	4	19
none	N	4	18
none	N	4	17
unfollowed	N	4	2
unfollowed	N	4	1
unfollowing	N	4	5
following	N	4	8
following	N	4	9
unfollowed	N	4	14
following	N	4	15
following	N	4	16
following	N	4	26
following	R	4	4
none	N	4	29
none	N	4	30
\.


--
-- Data for Name: eventwebsites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eventwebsites (eid, wid, wdescription) FROM stdin;
1	2	Our clients webpage
2	2	Our clients webpage again, for testing purposes
7	3	\N
7	4	old portal
25	11	\N
29	16	github
29	17	github
29	18	github
29	19	\N
29	20	piazza
29	3	\N
29	4	\N
29	23	\N
29	24	\N
29	25	\N
30	16	github
30	17	github
30	18	github
30	19	\N
30	20	piazza
30	3	\N
30	4	\N
30	23	\N
30	24	\N
30	25	\N
\.


--
-- Data for Name: oauth; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oauth (access_token, created_at, provider, uid) FROM stdin;
ya29.a0Ae4lvC0z5dP2sWtc0Bdr-w8YCJFONwEsWvk-DFoyUhW_GiCjuP22K-8dPiJa5EAqmTcqdJ88a6x8DjAF6D2obmmqXDo5EaWerrjCEpV_ru8S2zE8ubshR41KfhUpNckic5VdZE8DM2ER9COAFLBLllKgHTyFK4C4JBd_	1586583939.5508032	google	6
ya29.a0Ae4lvC3J-WPX-xYD26RHHHWJWCE1OY3HF1HXjZHonKsVPjHScQjMxMKhr0c9eCtLMEbELNfNGMkPN4YsB3dklYsMSf6UV0inIQF_6wSvZJZ8g6HI-z7rC2fMrdgKFubadJY4ek0hCToSQGhh6564_UtrTHT-sKWWV3Ia	1586583998.036122	google	1
ya29.a0Ae4lvC1Z4SwD5LDCM_MxPKy4tTaWLap3ZaTJkJu6EMLf4t_L3X616tocKICGTQUd5Hnm5WQVTZzT_F7n7TUZ7SwS0FVBGJYFwj3yggwoq6hUWgZuAU6ZeGHNQeof7Et7Wlh8_DqkSxNjY9BKE3Lfs3p93azT8aC9-XdL	1586641792.8070889	google	3
ya29.a0Ae4lvC3u0CiSQ6D00mOlbr0FYFOl01p6qWxng13EpSGSQfN7zgBOGnjrlaBMEubm9wj-7XX9l1edfPDm8aNGZjMpUHuUQuBhNa_4G2Y2d7LGdtNXjOHuFGpjCdHOS-35pqQvADeqaXpQ9yBnLuPwIuHX1BZZBm5ZeUTM	1586663324.6460385	google	3
ya29.a0Ae4lvC1c0r2SaViYW-RKKqEspLky6AnN-WjeMZJwJLc348SggJS_ADQtObaIDL01Gi3MuWzgXJg_sQyOZ8nZJSGTozn5bkZy-DJcpGVw-YNBup1mtP2S5Dioi9GK2tdD1tcYxtrQQd3CKfIaEjxYlVfwvFtIPLD8ujej	1586664645.7667727	google	3
ya29.a0Ae4lvC1bj4NUF4rZS_ue1ehILt4_-rsg0OdlWTr4EpWvc1I27EMvH67sGzfPTx4N5pC4S9r5kevS-mh8AnHU87gHZNU8fqvJfwBEVkQijrwjAOdYTIaanKqXOxSZTcYyJTzAKOkFYXB6kA2mOKsBmThed0KyWfYt9tdL	1586664795.2849252	google	3
ya29.a0Ae4lvC2bAhTYdGQRqtwuZ41R5OcO8UaIVVASvju3VmfDr-AhG8T_FLVbMzTKFqhw8qJxjIb27zZrVsnVAp4vigBrrNOYqitMsVX6gv4Kx1xa6jnLG3iaEKzhJuZe3aRjrltkSItw970DPBgqKB6CUwKfFrDJh72djZRk	5223213.12	google	3
ya29.a0Ae4lvC2SIynE1hRvtdBQyWERfdXd9S8Fr2IVn6REqMlqj9uMKcbc1z0z-AhiPj8Fqba288YMULI2nBtZyefpN17PV-sC4dFc-S4IhqdEHk_rRuJAXXF00NuuzdwO3WfaRLQRClz-tNdgA1yx7iWRkkOjXwv-tkjBpaVP	5223213.12	google	3
ya29.a0Ae4lvC270Lx9wC5T26h-M7U3xPG1B07hUs5U7iRIQpZlsw3cjOjOHiDTN-x3IhQQch9aRFLPmLEPSFMyW6U0RFiGntqO5QAs4Muca95aLahV6Am207wWGtCBKtSjSXZPKwIgvZQrs6sjk0lqnytqBljN6HVa0jq1a8Bz	5223213.12	google	3
ya29.a0Ae4lvC3l5ePBmsTbMeKB5ecuQYP80_Sd_0OtB1Uo4blFVYD_sFUUPdog0wez1VmJiwl5OQ5qBErqgOtgJfMRhfgZSugscrDG356wsPDNr_To_SaLnTTx5qkndQAd6zSmffCYMMnKvokZLTxpS5STCFZGnv_DZD8ZRcLP	5223213.12	google	3
ya29.a0Ae4lvC2nJl7fLQDNUOCVvOkuxc3-tAMI4f37lvEOJ-VdEm_wfmp8bEJi_4XOZw4dsawI_fA-Hnqti1NguPc7bHKN92pc-oUQkIDQigWJzKqSRc0Qj9zILYhvjj6ctmDh32W-fQziBahMeWn3fej4ifvkk3Qzsnr7ZXrO	5223213.12	google	3
ya29.a0Ae4lvC10LHzHUNVvb4LMZmhIjKWn0BgixOZl65znEMC-ZEwZXS6dU3A1bQjd8LR7Vr6I8DQRDy7qbxBrMYPbo7eMC3krwmxB1doNJeubZjoq-zaMEa-HCxL9veokkaKXV5o0sMsn6tzmiLdL6r1xIRvg4TzAcdgceEEX	5223213.12	google	3
ya29.a0Ae4lvC1O5wwhvMgRzJv5XBYaAsOO_4spTq6ij1w9zw2bLmuqvxaTLp7klB5vVxqplGMNP-zOkAE3p9cR5APO7VJpZgJcyn7CmqEIpUdJPcQRJrhto5OIAIGjgDs6shtyMtjpJvznGluDDB8h7X0IGTuQXG3tnivC40zx	5223213.12	google	3
ya29.a0Ae4lvC2xQE0jYTRYgrUOO_sta97bs3z4cHNSYFgR2b77i4-mGt7-at--sZ3unDYqJWwvcH_lcZQtKxsYoxBfh-Jl0TYcRmrysUCTCGSalSlYaI3bIBTHMn94Nf8YCjfs-sG4qUxo3JP-RtjuLiBsC38KelovtblVU4Fa	5223213.12	google	3
ya29.a0Ae4lvC1_K-D6FBBwS8IHWWV2WSPTFTJPqDzf-ZLLWp_h7BhcJSY0ETqXtnIEoUuFUo2oHNcTbfvYpEvPB6sd0fPOhOEsafIn-cWTPxS60HYwHxe1eB6hToS3shP02ahq1lMbAa8mip6nkNwwsHU48a5eeKkNgVZXZdYn	5223213.12	google	3
ya29.a0Ae4lvC2pyUX_9H7d_g1v_jIJh2c3vYa5XnCD0lSKMk-wbTWLZ6UQ5dbWMZDHlKdFs51rjzY1IT4pyyFTZgte2WSVV1tpmxqzQUlqoTgiEtwyVOtsLBtRf9lmPkGsylrFHfgRNBf2visYdZJu_nCnBPGe0NTTsiK6zAXp	5223213.12	google	3
ya29.a0Ae4lvC3PZApAEFkMJfCHSj21Bv202d4xHddcN18j8XP1YVznUB_j7gagt6rll-HkCLHhtAXKnWrYF3p0GowOw6ufayB1mUm4JiNTrftK31eUvjh_aCJkPdg99JSw1V9BD9pZSzkX3QPDaD_pI180FkreC_O0Ilo8Qk-I	5223213.12	google	3
ya29.a0Ae4lvC21Eraiv7ae8n_gEmtp5-YSu95549_giyGffx3lomyEAW5GXSu8_two-v591GoJS-Xpqn5jx_SG-jJXzd7ApmuY6DJw32HKqsCOZzZFnY4KQ65WGQxfBXGaLE6auZPSpu9QckWZy7QxmXIohKLERGb8kaFyL0Jz	5223213.12	google	3
ya29.a0Ae4lvC2nkBe3ebZLGrbf_UklNbnF0WnzNEsRFuFxvD2nfjf0rBqDxSW_H--DvCh9cpx23WR-8FqTrY_R8k0CQMAU8-6rapwL18tc0zZl7RvGgqLN3UDRR8qK15Vvc3UGLiluBh1VGaSIgigEPZIJqQ1dP7YC1S1CKI0V	5223213.12	google	3
ya29.a0Ae4lvC3h404tADcI6TZLc8AYLWGFe2dANZWYnKYXXWV4vx1JYdmFHAzPwvmQMaNgWbJ_AIiPmSz6If2gHLEbCJNmnawzHUOjmEqJEzCP5avGya8KWmdPk2zZS3JjXIRjOJkPN9KqP2n3Y6JZ6spAMuIJwgAW0fc5MnYO	5223213.12	google	3
ya29.a0Ae4lvC24Gv74UTkT-_KYzDIdpzJvbt03ktofFUYYXebe9An0OIX_we63s37Jy5QSpdXZ4QTp7hvNWPqIiYGsr3_11gf7YabO6eUMF3roJaLaa8yaVcE1XfjFG4b92pVmFLzNWuYlK9uVRrxOTfCUr-lhdNRDJeP-PSgS	5223213.12	google	3
ya29.a0Ae4lvC3-vioIxp0RQHm0XRuWjY-Q7YhI8CIr47M3tpAvJZ1DzaTnhkolKpU4TBmuvNu8dNSJ-rN5xleNbULuqJpCNJnoVpJRGCTompHEQ81p4Z3bYWkmVAXM_W_cqUyf_JJn7yM2bq3mitaMNuGcXhiyeZWq7cbIq3Xu	5223213.12	google	3
ya29.a0Ae4lvC1e_VmD30KD94jvarANBiXOHKKXujKwAc2xOvi0950JkYU9LfOT6xkvaUiVONrgHANaAD0tc7X5QpuwDdDAGT9pJRPxcCvNb799OIVFcOmKSi1UyN9NsXkNisClDjBvxHag5CzZmTRrGc4w7WfornHDQ4MxB2GS	5223213.12	google	3
ya29.a0Ae4lvC06nfTsH9zB5n6xq9Znf_CJip9h8eIAZ60vHdXXbaDD9DBvyz2KMUKkuL7RNWrv7-FUxl7ee1YyRIkzCyBHd3G7KgxIe1fN_WYLu_3hYHDklV7DEEfb6lrNsiq4-SMUeC098ZvwxKmbjczrbA_GkDyObmavEASV	5223213.12	google	3
ya29.a0Ae4lvC2sd9wSsZlSdld9EcggaPdDJKVas3fRn6Q5e9AMdcrshA5fF2cLZjClQhDO15fXpzpLGOlbLYrT9RxBDnSN_1RlPysMfioBwgQ2RSzFsS4PXHYE-zUp6UoPW_Qs4C_aSGSjPczt8vFnPuapXsv9-cCwc6syEe8c	5223213.12	google	3
ya29.a0Ae4lvC3F2FUqMtYfJw4tUZR2xhYjGV0gToWOWzEZJHUSdDoJ3jy0_PBp-AiaKuukYuFH_r6rjoS-vQXkR1J9tMofSCKZUSX2E6Y1udR3lOKxMROMBKv81tbEeA09uy9I5SR33fsWidEEx7HhbzYIhPGpIGbTl6Up2wEw	5223213.12	google	3
ya29.a0Ae4lvC0Fwg-Bz48sg1hvCo0I2r0ljSSJ9BvEjmqq2gc8gA2lVLYddCwueO75huSfBqShJNeq0UoG9gCtGeX_i28uqI_FaQsfAS9iD2rSUhPc5RHed51T8GPvnmRlB5aU3Sa1kvm21GSBXuB9_oYBzZlX87-jm3tKE2xC	5223213.12	google	3
ya29.a0Ae4lvC3NgvyPCl_yaKFsK5QB48ytAYcBXBgKpT1BsN_87uwkMexX_VyclISCD6xDyJfTWAti-fdSb-uehxV-1utLwQKBljDRKxbTqvbVD2iovbCBROdoUpSyRAyoP6eXV0Sq_N2SymcnrS_Uqnhshc17PqpzyOD92d8h	5223213.12	google	3
ya29.a0Ae4lvC3aaB7VqEbL1O1opHz4gsirT7dIQk9gSjuzx_SnybXFw-cpI-4mnqitV6Lp5aLWSZdu2oBUkh8K1L799YB8qvZy2f3Vy-k2tYN9MByWeEh3PactYVFRknDjAFy2v6WuvCv_0VbsLg_3uDzQXyYNqR1v3wJK4zhD	5223213.12	google	3
ya29.a0Ae4lvC1t3D8p5zatK8vEIlkuc7aqrKzC1NKEwmNFLQ737KGnUSPb2w57FlUXRjXvpBF8Q1p1XeSR84MZFD-H1CsXZbb9haAIIK3h199d8SpHKqv7fDmcEGhguvWIw_rnMNAtZnTVQaoDAcdw2CNRVOqlgbzA0Psx6-cz	5223213.12	google	3
ya29.a0Ae4lvC0DYMmUUY1EPjld3EhhdVF6dGq3pw-UtmxHT_HzihYxoGng5x4nbxmClk9Anem6WPHIOKn2AfSFI0MuddB_HM5Lr5F2gtZpQ40Z5EeP5uvqdF7MzvhWibqwqZtO0oMvP6jkNHkBugASDi_IAZHk9LWneDYwMs6l	5223213.12	google	3
ya29.a0Ae4lvC31NMiHREFefmaFPXUlLDpqEvuF5nxdfa7Nb1-W6gz1gA19i60rnoNSMdvpA8cYGEHF5a1ZHorgvS1xtNYCX4F1fOgNsI08p9V1n2NZOME6rs6f06zKxZ_lfEoA988bcIaGBYecEMdCCa_7L-Pu-yA_rf3DU-ch	5223213.12	google	3
ya29.a0Ae4lvC0QS0QucagOS6BTu-nvljx4WiqG-2PuI91YkdUIPnnc-kj7lVVLZkfbKCR2ipq_pgAQt-J5l3LZABFLL-TSLovpYkzoMG3-vYaPGDRtqxyGY6MbMhUPabg8h5g5erTA2gtYhm_phRYsShMuJfb2LH5TIBzSq0w5	5223213.12	google	3
ya29.a0Ae4lvC09jHFeHx8IyLtE3f366YbCgh9p5ocW3Fsp1pDJk4k_xK2wU6erYK4lxUC-BDCv5SDM_qs-IYQUxn7sIWnVaEjywPOvap_Z2gxdipfAYp0PqeYdYB4diKe08Y9N2Js1XFRnz0ux468nnCPrfoTJUG5DUAR_dFBs	5223213.12	google	3
ya29.a0Ae4lvC2ZmYQ9UGXBmdISF6hJQmOXDm84aQOCKv_GF4vA_oI_QLxJYmKIUCIhI2Cb784hU172HzcKvAaevW7RofqYy-f3jKN98-pO0kUBpqnzov1ickRpq_IZ68OaUnuJtt4hZPJIRghU6Fm7NmNrwgm6CzSVG1Icpuot	5223213.12	google	3
ya29.a0Ae4lvC0TQOXxrGgSbxlrhNosw2jXCFE8fveHGS3QA6QW4Mfxl2sh5OyPVBZJrDUsXMXDnHwKg3HL7YvgVlN7A0m1Y-v_yljTsC89NNzQADULJrrT8JKdouLcr-ZVFK-djQfSk-ZUfnejVkpb_HT6Vpu1yOX0I5l9SUsT	5223213.12	google	3
ya29.a0Ae4lvC0sSQKm4Q5d3kj1aLVhTSVcp3ZCn0Q63qNvVym6WDLAOFPm6HwE6qhmLpEx--tsiP6BGccxRGg4bcSsdgiSxIh0foxW9rO_iYGnXTvoU6ND6MGXJSmXVF1yarUgx8_L2cuyIXv7tw8GB8V8dvFDwkaLj9-84_cg	5223213.12	google	3
ya29.a0Ae4lvC0ZhAHxGLG5327FYT1hZHUWYvAdwXq1h2Dkedqj-uPfGdpxhRHfxI5eWJWzu8SCt7I-w85AYXf_PvwFsZGu9uGHjml_99REZ6nC8AWEzli5yniohWgsRelC9RT2P5pvB1wCaE7nupDqr1cvSklvCPUYZFFCFSY	5223213.12	google	4
ya29.a0Ae4lvC0Hux3wBJ5DIzn6zjb6FVp1o_gXPeNxDHScJDTygbmJicLvOPBtJCotSU9ZlZS-PlmiYn40_1gS9U4Gc59lpKQZ220RU9vmFwASuvXgnxvP52as-8tN0v-FdUf6iYWvGl4jjri4CqRY6BG4szBLLF3-iznDBK0j	5223213.12	google	4
ya29.a0Ae4lvC0XGDVngtPSivDFUTzJnV3r4tgOkLUKvHd-8reiPvPs75sjZk8CANZN-T0Fdt8nur7ULDGpvqo00nfi5c5w-TM9yMpnC7STHO1aLDTIvKLel5lB_Dnt1MuyVPcm3PAqlzVoZyEPJI-EaBXaLOf7vK1Qnu3eNIbe	5223213.12	google	3
ya29.a0Ae4lvC1COtoFQ4EkGNKD78R51KuLYtIaOVufpfXRLIGEbXFLPvCjXlKFqEXaQdsKatGamc_CEn7P_ayiPyfUQBCr__c6eeWby5uYXjE_uA9-ctEc8lc-g7fJj0ybRifyp3ME_YmDF_W4Mq1r_7we3pcU3nVOvRdJriFs	5223213.12	google	3
ya29.a0Ae4lvC1scRvd0avYVLUxgTcrKk2tZ4pJ6PQScbr3_tk7HBgYMttPb9I39HBqIskZbT4P3DJ93-_9ME9R7-j2AURjpagCssZUrduG8ZTAn5Mm3hQQ20OpfJJEOowLvn5ituOJIxTPwO_CqpCiV_M5k8Y7g1R3RMySKU2x	5223213.12	google	3
ya29.a0Ae4lvC21EfnSxu5T_7LZIaLNZaOAfeHOGseFaBa0G2JvH6QL4S48NNNYxTFD1imBMMyRn8VcmPUKeSP9oX--Puu_1fnSMAm135vT3l34BuM6nfFkTt_x_UdFehuGGo6JFLTFFNgzFbFwap_OY-wotkkMSpcSTty3IG5N	5223213.12	google	3
ya29.a0Ae4lvC0ubZC-UNaz1LwYxz9ZeJS9iE6p-sHekEDBcFatosGemtAdML-m6JjCL0XIGVmLdBuY8HvM4Yh_7f_hQSAe9oQ7XcduYc3mD7B9c3VfO6OnvG5hxz5-LZuH-10Wtpt8mUaANtjKgfIGPdNsYayih2RWgImtN8YL	5223213.12	google	3
ya29.a0Ae4lvC3mdspHN9y-JXZfKZqDMifEdxtvE4-9MT41iXoMmDlq8PVamkrv06UrW1fKbGF3eebG9CVYXPPpF-HhjiLQzbBrH7FeYMkjxphoSbrshh97GKEL6JYJZrsg8bAp2ZYZrysfFZj-qqSK4tFsx_8GvN_LHfnSXTpK	5223213.12	google	3
ya29.a0Ae4lvC1mgs9txeAifbYGJpFPyN1KeHS5zhrtOBIqVOK0wb4Jz0W_sHcaFmB2oB7hXDAFAUYGe_1tsPG5tDZtDywi4wmy4jZLbRamVoppbg8Yx6UREaAA6b8jMSyn8l6rfFaCaPlAqob1kihM3qp7zldu6XZdfQhEz7yc	5223213.12	google	18
ya29.a0Ae4lvC3OE9LU8Cx-z2vtJixYBMpy1m76myTp2F4sVXtXXlGFUL1916-onqixU2FVa_wt5czjyOYNT4ljoO1aNa9eKIFjOtLAYtdhIcfx2HA025IFJNjBTdIb9Pn8tSk-5fT1-Mswb3g-cvH_OKK95OzVZC-B30cpPAxv	5223213.12	google	3
ya29.a0Ae4lvC3xa8bxWVgYsSwbhDYARCjpx8NpZMHylKbQGBRyP_1QXFPAVAXeGxvqCTXVZMtLFf905G2Ae-KXYkwVRH1HLU8s6faNL2ssgWfbJvDzhGcRQv41t8tqBKP0FR7djw4055-AlrIDQmWefMBwSsL6n4j5MDbI4h8m	5223213.12	google	3
ya29.a0Ae4lvC0QbyEXGFL9ybGgyWziEGiyJJD_pcGfJKPf6nrDjwXokr46FEcaMXxYRRNgaIAxcaEuu04nkft-JgJSLfSdUx9vGOUfEzroyO1TpLYfRPocSf2dSbMLP5FIj3ftjvh5lON7XAcOVHudQ7L8dZ5NQP0y9avGfv52	1586905168.4706123	google	3
ya29.a0Ae4lvC1T8m8DOg5sMpTBdEDZrZB1N2O_GYAisK4-sJSpWrf4TiuVneydMReCD1oYXyb8ATVzzGuBCkCTozuz3lcQS27dsOVL7meBLxB9mluf4-f-AazRw8AYfOCVZSj33XxtOBPWtGiVzFuJkGr9_I01jzF1Y2VtzKEE	5223213.12	google	3
ya29.a0Ae4lvC2O7Ge9mZhXfoDyrXnsTS3exgmyCMctq3DF84Boku_vFC1wK9GOsbdWvvqRnKDUj6cfTisHnm0FfbpNypQlBoyE6z3JpVHSz5iNfivVxrA7otkOePwreXVDMSIwAV99Qwb73IELA8VQH9LHUhBdbe6iPyIfUlqA	5223213.12	google	3
ya29.a0Ae4lvC3uDAUUB2xXMwxD3UBulod403yhLcbpDEojVom5WCmHTS6UqpffSyfVwR5O0ZuuQ3fa2LFGwTywYBvBEdgLHQvqChwgnU-kJybEdrqvS4VSMtT9744c3hXWDIhOHEg8ARyOV-7KTNn0YQI8f-KODfubGncIrmGA	5223213.12	google	3
ya29.a0Ae4lvC1tg-wNyAkLwgNNuZKIE8Nfw2Zv0KfILh_qjKqmphJQy_P_YLOMOzO58eAQ8o7rhwf7EuiHrgyk5rtLuY0BkKE0ftyLevX9FaDeC6HcKdvAIh2yKvOvbP-COAEKg4UQ_YiacACfcb__KyzlCCv8W6UqgBg_yN-R	5223213.12	google	3
ya29.a0Ae4lvC1VLxLuWL47VKx63zoQiaYiR0aAsoCl4hqFuGtfZ_4yNlnXh3B42GPdX_iOqSxf01XBLwAe1hyiREYv81ODWTyzHUg7A_m6IX7LaVIa0lOcUhPclclZmcy424M56EARAfpv1kjC1bAdosngciazSVE1hCj80L5V	5223213.12	google	3
ya29.a0Ae4lvC1wNLBFCBkrgLtay9X8v-H-QQC7NNizYu-oRY-fr3DujSkiedD5yqb0Mf68howeSrHBBLXp0NIU6keB3l6CejuGnSR9uH25Gf9JDmUQF1acPmTiaF0j6qogqG9ZAydShPJU81nBLkmpKnr2r0ekMMer-rczsGBt	5223213.12	google	3
ya29.a0Ae4lvC1qdaxpQqObZVd947jAg6VO9yBI3LF9lNBR4V2rDVg8DZ1Ob2a8WCyOgki_-zh7aaB6QfFcF6jSxzYdv8D0aSOVFqE74AfqdgPwJH4J0ZrjZmVkmdFbN0bLjJ3HBgNwY1yTI5vnk5cQfYcx5A7_H8-ExAOHrp8Y	5223213.12	google	3
ya29.a0Ae4lvC33PkfTyOnpALM6rxYpjvW3B7Qa4nuNWL8rgCg9EFGZHgV6W2ESrLUCZo2-r_HwYAzXc_72SFPIkOeakILqCVVsNmFxtxLzP2id4lSojrY_cgYOcFGAUBDn6aovPbJQ93Clu1m3mRtGyrBkkAQx3Jm5mpy9kITj	5223213.12	google	3
ya29.a0Ae4lvC2oqoy8oqYeDUOwck3nxviKgod_Mf4E1MDuGkeWerKvZTxP7VlJvHG08PeKXnrveHitxKzkkIt7Wc0F-RBYfIH4ZkLx1NBkZ7nXg3pFBQIwAKQKNKLOSbzHxvQfM7gmn5OT4ref8IAOcwmut8w87aIX_3zHVu3A	5223213.12	google	3
ya29.a0Ae4lvC0VczamrF5Ax3yWeFVFOOwtvH239fvZllOZz7xg6JTFtBAuwUwhYD-_1nIaef_iJE5-UpQ17MvWJncw_UMMrv_FoBUZzwu5VaKaTe3AQkaq3DlyUrZsKW5XQBPlN-bivWsYQUae-xnenpgpfbUNoGpMbwAbHxq6	5223213.12	google	3
ya29.a0Ae4lvC2otkPSdA455QVGmX2W3oqpqdfnwq5YxW6uRF3QhRFTMkSJ5vL3bMMWdSnGyYaz2O610Z6M44nFg9Kc7R-OB8AYjYpFQtfzLtuUnNLXTMdld9VyuBRGrzxo8pd7Whie0Nozat6X1cqYr5F0V0hhgCb0FFiqSXmW	5223213.12	google	3
ya29.a0Ae4lvC3lueuzonHmd37omPDSV31OMCIJmCR2HIEM2IZBZ9OZqV8UqagSpf-u9Om1byfTEYd6mwG6bc5kXr9nu0_U_3WK_mRuR0I8jMTDUF-ntVz6JumK4pm19hcps0FF6e831RO45cZoIWuKu74DKjjtjlzkkxORUpHc	5223213.12	google	3
ya29.a0Ae4lvC3TDP4rup7OZeOlU-w-1QO-WE6VIzMgAzwiAvRMhdyXOxwIYBPKiQuqM0yHy0AC50d_2_UspJ4c1CUQU9ALjw8sTvI8s3uOUmKq_VRFLwrJjDhad7HGzBYu3HY6K2Eaqa2fkQqv7r0Zp9X0P720ffy4K29obPo2	5223213.12	google	3
ya29.a0Ae4lvC2kMlUs8928i8Sioq_t6pu9FBtlZTSqgsd2uTNahAfpzR3Rt9MOr4BTTn6GDYbooz2wI2QGaHyzpwYP68wbK0CzE2Q7qTcathPmEOTehrZhSlrx7lz0XYLlVltc6DEWe-axQPn5J_A7XKqaHb04aS12kVyEjQIv	5223213.12	google	3
ya29.a0Ae4lvC3qRgmQgglourMmX6eg-0Gmc6cCyG3OQl_tRB5bC2mt2-LbATQ8UF6bzCXS670a2WDvi0WUGQX5qWJUwLrvEJZOOWj8xFqEMJ6ISVVKrxFav7puBtqlnaIurdJuUSzUCnQ42HoGVlgIFRGbB8T7N9Q4_7atoAnF	5223213.12	google	3
ya29.a0Ae4lvC0hctekws4ZF14kp4O0f4CgMyw2POap80det60oDLGExXQpAEsUczYosc1gWNnfatOQvRq3bFk8znEIrd8CAC5VqgTKRUK34cidccgSQpf01rxoerPGKiFdL4yIUs_Q0JvHOvpV0JJrEgT8pOz0YkM0wpKSqmIo	5223213.12	google	3
ya29.a0Ae4lvC3PW2bcLHemAdzUkM4a8wpbvqONvnMmaU0bATGLAw9w7rifPNX3ZgeVsmuqTMVh5aXooevb3qGIHAwC-94KBcGWziHdgUlqjPDBG_iafwAFvAAA34Hy8Qgep3WV9ZyjPmvH6aIK13008D0rJQ92PSACLeczfvF6	5223213.12	google	3
ya29.a0Ae4lvC1MTk0u7VQj_edZbvWA7nRjzGi2RXicxv21NPF3GoyKHovyW3HcYD3EMPYjSJsbNC12LXQCYRJqmxqqAlxhSOASihr-2N1K-g-Goai5oJkAsqfc1GK9CqWNDI3Lncy2L88Nzwn4hiNXeoZNc1Bd-gUZ6Dl-9fZy	5223213.12	google	3
ya29.a0Ae4lvC2lGQYH-UHbLKbRcNjzOEVp5WcRvDDjvQWhhlGsAFlTPPLKo1Oks9wnsVmVdMtywZoUONQYPBrYxzWBOTwnPBnR84pjuyKwGOjgFZNyB97PoGV0XdFJ6xFZpQfTbTitOrL-OTDmk_VJRCeRjtkSg-xCeoCbR1Oq	5223213.12	google	3
ya29.a0Ae4lvC0SIdSlTo5G-9TeE6NVR614kLb_WBWTqYIMF3KpVkS9UE3LGjl3rteYXcf_MuFq6DzvI3UNtcs7j9ttdus0sKZ2IrxdTK5PiNyd5Qzg7HOZKlZGp_aBkxzMdH7nBUr6gS1nk9q0Xu4vhOnH1XXvQWy8G4mInTHf	5223213.12	google	3
ya29.a0Ae4lvC1HYrWJVvk38BSZ89oSqXmKXi7teSoGJPJistoLd4-SspGMV-pa8F_bo2yKr9ON7bwT_ENBs4ilppl4-neXHx3jHkiL1LNDhZQ1vywjtlqY-BVJ78ZF9Tn3P6dnBYnDJmxPeoqmhXSMwgjnS0nQWEJ71T0M1uW_	5223213.12	google	3
ya29.a0Ae4lvC06bA9gk4s4GRhEF-s0wciHlvr69JhrlxBUMPD98juglGRuUZsy8OfOzSkYR-GBiTLc8Le80JzQNyemsQgwaOcLNXVvK1n3U7UPlIs2DVAfwlH4wHmcX3GvkWbGd9ngQgYmRTiGDpiLN1qunSfe_L_IKZsNC3tF	5223213.12	google	3
ya29.a0Ae4lvC0m-ZAHyLj588LtQvGujqQciHXsjQXYkARVvKGgl8EtOWHVL5wvmWHSSI6GYEhdQsgLrhjmaHlhPA9MLeI13UMDYffxq-JUYFVdFrav7y-ZJ-Blfrw8t4F5PmsU_YUttO4nyKOAhmnv756q1WArIc6ijJ1O7Fyt	5223213.12	google	3
ya29.a0Ae4lvC1IPsNsuS7yVN-Ao6ZFdoHHrG7RpmhlLs1xEOeAK5LEBoZnMVhM1j7dsmZd9PWEHCYa0jFRq-hke3N7-W75w8sn9bPp7E2pw1Ht578GIiP6kOYQt3ptdaECchT_Rr10GBKdqQ7rW-Lvw8ITDUQZj2aDYd46CKbo	5223213.12	google	3
ya29.a0Ae4lvC1si6MUjs09WQft2s__z1-gjRlgfvIh-TwYdc7fFdl8zqXkmWuZSXLod4hiifWcIaopWn7KJ5Zxbq-4FwjYML_h4y5pRgh2pEdExKlK2Id6YmBm3qd6fIsC_qIQZLBa10pLxyIFM5hsaiW8atQq7SPOo5uUbTLU	5223213.12	google	3
ya29.a0Ae4lvC1X0OFJGn-zsCMR7cb1_F59BPKYHdp6a3LFG-wP2rI6bAMl6Dgf4iR5EcWw8fsLucz0TfV6pmecD2rGDsK2Nw8SbslW5SsFr9ITT44qvEiq6VLfjSfztJk-dOWs4DbwvN6Qz0IKs1idnimi78fa7_SVt_Fh8_As	5223213.12	google	3
ya29.a0Ae4lvC2G97m_Ocw36GIAiPjIcYNf7uM30I3_gOC7jYuvHdHTC5gGvocUrCgszf6g-QoAziN2KLGEp3sfRQfdJhNnltU4RuxmM9geKBGChF6_oQYx-5Ge6oBHP9UbL_N9KoBAu0NmvCHnszyd9Ec349fGRxOkqad0nnJm	5223213.12	google	3
ya29.a0Ae4lvC0SQ7SgWq0FSKvITPPaJYAsdVORjvmT1Dah6tg9hynzu9_v-0d6ZpX265op1rfG3gmimE-ivl3iMvN39PZQasCh32NJP5th8Jh_n7TEIRP0N1r_l8QPXE_IaDIiH8QvYHGvuRQDDRcJ9Ss-ZsT0pSIbgec9locK	5223213.12	google	3
ya29.a0Ae4lvC3_xR5_GtjdWAaycFjzov9BAIeH2ybzxVSk-VkDsPlJt5b5ly16pZ3zuFuNIom3oGqnuB4Vfj8rRoYGv3wmi3PhajXKg_H-CKb0V0UW1VfIUK7POiyMzOhBwngqHMg3zA30VmZPMRi5m0DpBZmBlv3N0zglF2-X	5223213.12	google	3
ya29.a0Ae4lvC2s9KcxOOmnu7HRmV-x6e9pMcWcKN25EX1EwlDpKn_7AxnIynPN61z8LCoG6QCs2cLTqNZzEQJFlAblFKIy0_urSNh0SG3nzuK5X0m7DyaysX0eWgWgY-XinxhY0qi9WCZ8QE1uhlVTgr1GPPq8Cll6d7l5oThG	5223213.12	google	3
ya29.a0Ae4lvC1GQNlti1jyQmkTOPXxlfOwKIkuSeh_Bs753MEwZGrPRcBznc4FAJYt9a1ezu5lhAfEg27ws6gk_9L3PktiX64ddBMDACrHN5d9UQBzbtZgTv7f6guK0QcDht0p4E1tjJ-18Qgb0eoell1ZG-9IA0gG87eKa9Sm	5223213.12	google	3
ya29.a0Ae4lvC2u6ebch610vIQrip5kTYfDwhX8GK4Re-uXSzekYIXzaa9C21zJC9GOHtDYD2y5K6FlTXxWPK_fgAlGt-3-nl0P7foWyiC0xLQ0L_1mXO1Ex9MyKwwnra_C1-UVmfg-tI0byPcmm8wjfPI7sCHK5CUxXgXQFdzx	5223213.12	google	6
ya29.a0Ae4lvC16GIUiT91pzFJ3BZDUYUKvukO7wG7DSoy7imsSAgyy9CBbb7Gg7-NjvFnFTMfl4ux4sn03069tXLxjlR2BKkkRRPrDuCcjaeF_m-hX20CMfAWIBH8Um57G_aiaoX_p57RnGYNkTd5FCPr2cdx3CUM7ompDrQzn	5223213.12	google	6
ya29.a0Ae4lvC0uQNL8N_oHikvXj5lDhJ8T3x1Yzr-OoUX7_3H6_T7YoOtH9bhCdl_jnfF1HoSVVNdUzAsYoS9sck6BaSuLtcJU08sQX0r2oADnTUFarcOfIn2rT_aTNR_ZCUjllZbERk0cl1F03r80ST9mshyG06tSNKH44HgM	5223213.12	google	3
ya29.a0Ae4lvC2yd1qkEAXprFOqMs6S4EgazLkdI3zAX0P0LpKMNopxIwYokNgX45h6EbEv5ZOjmwDoWeyCorl2F7E8ErxguN76gFskyhahBfjQJCjprX6Obm2Bd7ZLTmFzYqkJVOp6OSqI8V_d_H_7xZEPpZiP0O590p8S07kh	5223213.12	google	4
ya29.a0Ae4lv45Hux3wBJ5DIzn6zjb6FVp1o_gXPeNxDHScJDTygbmJicLvOPBtJCotSU9ZlZS-PlmiYn40_1gS9U4Gc59lpKQZ220RU9vmFwASuvXgnxvP52as-8tN0v-FdUf6iYWvGl4jjri4CqRY6BG4szBLLF3-iznDBK0j	5223213.12	google	6
ya29.a0Ae4lvC11kn6DSkjetSSPFeVnLrJXqTSQZ2WVNNDgR2KDrnlgtKjVvxIxN5OMCLmKCjEYHyl3j9YEiQDzvU_KO80cKHXELWgwIGk3ZN1giu9knam-nN2llaYXqItxwZqZwzaFRuDejU01vvIyYqwcvltfhEqId88231Hb	5223213.12	google	4
ya29.a0Ae4lvC3eAqQ-A8eKVaEMzq7DUYur5VVXIVtYWV9nuoLNupwO9Ack_nHwQS4y0PWtRGtQK4xx4CLUvh0a8D7xcmuGJRyAsexAX5w-XCiSqAc12lOhW57mWPeGQUCrJUtWMQ8odG3bmuz36dgXpBagHVd1C6d1Hw23nO39	5223213.12	google	3
ya29.a0Ae4lvC0tG985BWBw7CQAYSRNAjX6WwTbRgymEfwhj2wop214uVZ93tZEXrgtgAWUsouYf_KUbXKDcWYNjwIpUeBBeJkaIYyHJc7e0aQ31gm4jYhEbSkFqhPLpHs6gA1lh_chR98mCuFLPBtIOnHgwxoletyWJZBnxDCw	5223213.12	google	3
ya29.a0Ae4lvC3Tar9czXkFXVnnUeey42IgzayRJhITunlGtm1iLiItPtelwvt2BUQwPnxTBGfkRa1ZMzchhROiiZfo_uV02LC9IEhWg4xXRioQ_VwPCbjJyFl0JqK8MpBMQras62Kdfl2kd6MgSW_uhYPa7MGeneMN3MORjrcg	5223213.12	google	3
ya29.a0Ae4lvC13kxsWDUSPfG2hPOvv8XF-os4Agu3rjm_Uhj0sfK47HF_sII-3KIz9jdR5WSR5vyUYzvPZuGPQ22kLYO_j9UUdJZRFtg_YKuF0X3SAngVrkssKZU0XRwjqpzNrNJDc8a5hLrRHOOCcb5U-w6PbCmctxw9MoL5n	5223213.12	google	3
ya29.a0Ae4lvC1zzUJ9fONOwwBoM8hLO9tjru2D4tENZTtZPvTrqQgpZnw8ngxj-03lGhK0D8Y4CrRxbAPDIKNO74dfP-VIvQxDQIu7-B6m7vtTa0GNCRw_1xuiDMQbkzAfho2q4gI-On3AMvJYZ7NkiDIXElBnw3uQ2w9oSBqt	5223213.12	google	3
ya29.a0Ae4lvC0qizy-9MWKWNyVKl0GR2mU4fn57EfP-AmKEDT2JLyT_apvYPwxR4GvDFdCajJkb8dQnB4Km08AM5tFVonID2Jijs2ZJlvUqAzw9QLIE4ahN5-URCqsmFrn_SwWjYtC7HLgLPvBmXvToz6Najf4zjBKtfSqO877	5223213.12	google	3
ya29.a0Ae4lvC0TaSETYQKTcj7T6gTTXtCTgm2RTB-Y2TGZ-9bOHdCEm2XanmJqBoeNh8C5uQE1GdiSM59LbGCUB-gLEfrgdMCFVzELmratTMVcf7SxrRSNwi6Bwn1_xwcxMGrmvLEVXnzd4BrXnKTl14-pUCe7zqbTlpp5UHNw	5223213.12	google	3
ya29.a0Ae4lvC0isJRQv-qT0ToRdK5hM8ySxJd_j_ISdbXjJaTxC4niExRujxY18NST8Wtv5XYGpV6YnrIw5gOePYN1hx2veDZKGVDFi-Lt4ryAtUs8Xh26S_wJ8aM7HjybeipOej2Rp0VAoUaQ9TqbD__ARPE-HxIo7dE8xx9A	5223213.12	google	3
ya29.a0Ae4lvC0DsyIE4j45sGtpBvxHBRQy4rLJpqA9oHwWGoyKlAv1DatVfoZgkHVpQpWyFSZrm4b9nz4OyPOXT45fzrgbicy-3dCR1v1-6Yhk-BcNTdVeMSqM-wezoUq0RgoRQ2S1c0K5mwkOv1TMCLpYO7PkigZ2Ti0upNjw	5223213.12	google	3
ya29.a0Ae4lvC3TRzQDBKOiJTCC3qPRZPdYbuWquyf1Qe7-6XeDjEx-zTmTMUubgYL1jhjUSHqWoIv9RDB9RBJkZUjmMuLxZ9cTyucFLL0SgA-dZDQQ43zaYq18C1l-fmNL0l9eYPTILptJKbBwHkBzlJVlonOJK02rZfcSwv0g	5223213.12	google	3
ya29.a0Ae4lvC0M-bV363wvAHGNsRmcmJ6VVI6JlniSccC_0gUrg2YqGYwzNXat6IdmAZ9aqJ1nYj5Kuq5Yd5BVxVbDYQHEBvS26cNnVB1y3igFDQX7UykD2hQB9bTzomlgV7h8UhYHULX8ae7P4__cMW9Yu2wCHNwDokmR70g7	5223213.12	google	3
ya29.a0Ae4lvC1wtZO0x6Rh_Lo1gR40vhbdgCT9m2qstNQFRb0K-8qknm0rYef3BChMBckvfDTujTac9TAEnMQq93v7uAD1FRUOsCMjOatHlRR90wJvkkOF8ikOYwSsnrdE90uSdcWFAB7BTK62DxUqrnTxScHR7d-NS53XwE0m	5223213.12	google	3
ya29.a0Ae4lvC07NfpvESii7oNQVlhJktGrQHOHHW5rBtgSFz8d206K2UBjI3i6GiLrc-8cy-Gm_Hx4ZB_H1Eo5iv6HvcL5SL1ReN-e7J72v26VfbLFMJPLUFR_vFij99krSVapROStmBkMeXirHZL0hUNRfTcjyaQkO0c_MMnn	5223213.12	google	3
ya29.a0Ae4lvC2Fy9ib6XIeaZ1VMm_uYlEKfl3gclvNjLNkC738ajP5VWyUBlYDTy1k0LoafSmjQrM4QF4CoHZCNBzjclr7UpkZnWczfGGYDNvzq9gQ4AHytMCRUnSybSQ3f-Zz5O1pwkS_CzNtuKwxAOhET20eI1qjs7Wafm9-	5223213.12	google	3
ya29.a0Ae4lvC0gvobIgOvy23As24MmBmj-mpFiyvg_O08pZt2ZMuprcRfFMBw_IF2w-6KCX76t1iyzZUTotP-2RcYMUNaGSTpJVKYWxTCESUgWVijojLH8s6fHeEDuiV1g7xlicfZ33ABHPqSrIvQe3GsFlYBcvEQTuCPBeCrt	5223213.12	google	3
ya29.a0Ae4lvC2C_tokhe6JSjs93aZTu6lBa3pCiSIHFJZAW7Ek4NnKRDDnhuRoJWr-sQ8HuQmFqoKtTSSXX5Y4UU-bwGpErGlh-l05h_I5CFXxMTnQuckos-9VOvFoOagTy1is3KcRXqOk_JK1J4QnOJ6F9jkvQo2N1uhyHkfk	5223213.12	google	3
\.


--
-- Data for Name: phones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.phones (phoneid, pnumber, ptype) FROM stdin;
1	787-832-4040,3182	E
2	(787) 831-7564	F
3	787-832-4040,5842	E
\.


--
-- Data for Name: photos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos (photoid, photourl) FROM stdin;
1	https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg
2	https://images.pexels.com/photos/6347/coffee-cup-working-happy.jpg
3	https://images.pexels.com/photos/269077/pexels-photo-269077.jpeg
4	https://i.kym-cdn.com/photos/images/newsfeed/000/011/296/success_baby.jpg?1251168454
5	https://pbs.twimg.com/media/DN8sEJpUEAAyuyF?format=jpg&name=large
8	https://images.unsplash.com/photo-1544614342-c48ab91d79fc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9
11	https://images.unsplash.com/photo-1544627836-822bfe450209?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjExMDk0fQ
\.


--
-- Data for Name: privileges; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.privileges (privilegeid, privilegename) FROM stdin;
1	view_building_data
2	view_event_data
3	modify_service_data
4	create_event
5	delete_event
6	delegate_event_creators
7	delegate_moderators
8	revoke_delegated_event_creators
9	revoke_any_event_creators
10	revoke_moderators
11	delete_delegated_events
12	delete_any_events
\.


--
-- Data for Name: roleprivileges; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roleprivileges (roleid, privilegeid) FROM stdin;
1	1
1	2
2	1
2	2
3	1
3	2
4	1
4	2
3	3
4	3
2	4
2	5
3	4
3	5
4	4
4	5
3	6
4	6
3	11
4	11
4	12
4	7
4	10
4	8
4	9
3	8
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (roleid, roletype) FROM stdin;
1	User
2	Event_Creator
3	Moderator
4	Admin
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (rid, bid, rcode, rfloor, rdescription, roccupancy, rdept, rcustodian, rlongitude, rlatitude, raltitude, photoid, rdescription_tokens) FROM stdin;
198	1	326	3	BAÑO	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1
52	1	120C	1	NO EXISTE	0	INGENIERIA ELECTRICA		-67.139923	18.209641	50.040000	\N	'exist':2
37	1	113	1	 ANFITEATRO	0	INGENIERIA ELECTRICA	israel.pena@upr.edu	-67.139923	18.209641	50.040000	\N	'anfiteatr':1
1	1	100	1	COBACHA CONSERJE	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'cobach':1 'conserj':2
2	1	101	1	LABORATORIO ACADEMICO	0	INGENIERIA ELECTRICA	eduardo.ortiz7@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
3	1	102	1	LABORATORIO ACADEMICO	0	INGENIERIA ELECTRICA	raul_e.torres@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
4	1	103A	1	LABORATORIO ESIL DR. EFRAIN ONEILL	0	INGENIERIA ELECTRICA	efrain.oneill@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'efrain':4 'esil':2 'laboratori':1 'oneill':5
5	1	103B	1	LABORATORIO ESIL DR. EFRAIN ONEILL	0	INGENIERIA ELECTRICA	eduardo.oneill@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'efrain':4 'esil':2 'laboratori':1 'oneill':5
6	1	103C	1	ASOCIACIONES ESTUDIANTILES 	0	INGENIERIA ELECTRICA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'asoci':1 'estudiantil':2
7	1	104A	1	LABORATORIO ACADEMICO	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
8	1	104B	1	LABORATORIO ACADEMICO	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
9	1	105A	1	CRLDR DRA. NAYDA SANTIAGO	0	INGENIERIA ELECTRICA	naydag.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'crldr':1 'dra':2 'nayd':3 'santiag':4
10	1	105B	1	OFICINA DEL ADMINISTRADOR (SYSTEM & NETWORK)	0	INGENIERIA ELECTRICA	luis.lugo11@upr.edu	-67.139923	18.209641	50.040000	\N	'administr':3 'network':5 'oficin':1 'system':4
11	1	105B1	1	CENTRO DE COMPUTOS	0	INGENIERIA ELECTRICA	luis.lugo2@upr.edu	-67.139923	18.209641	50.040000	\N	'centr':1 'comput':3
12	1	105C	1	LABORATORIO ACADEMICO 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
13	1	105D	1	LABORATORIO ACADEMICO 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
14	1	105E	1	CUARTO DE SERVIDORES	0	INGENIERIA ELECTRICA	luis.lugo11@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'servidor':3
15	1	105F	1	 OFIC. PROF. ISRAEL PEÑA	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'israel':3 'ofic':1 'peñ':4 'prof':2
16	1	105F1	1	IDAR DR. HAMED PARSIANI	0	INGENIERIA ELECTRICA	hamed.parsiani@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':2 'ham':3 'idar':1 'parsiani':4
17	1	105F1A	1	ALMACEN 	0	INGENIERIA ELECTRICA	hamed.parsiani@upr.edu 	-67.139923	18.209641	50.040000	\N	'almac':1
18	1	105F2	1	DUPLICACIONES 	0	INGENIERIA ELECTRICA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'duplic':1
19	1	105F3	1	 DUPLICACIONES	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'duplic':1
20	1	105F4	1	DUPLICACIONES	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'duplic':1
21	1	105G	1	SERVIDORES 	0	INGENIERIA ELECTRICA	luis.lugo11@upr.edu	-67.139923	18.209641	50.040000	\N	'servidor':1
22	1	106	1	MOLLECULAR AND BIOLOGY OF CANCER LABORATORY DR. OSCAR PERALES 	0	CIENCIAS DE INGENIERIA Y MATERIALES	oscarjuan.perales@upr.edu	-67.139923	18.209641	50.040000	\N	'and':2 'biology':3 'canc':5 'dr':7 'laboratory':6 'mollecul':1 'of':4 'oscar':8 'peral':9
23	1	107	1	 TALLER DE MANTENIMIENTO	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'manten':3 'tall':1
24	1	107A	1	OFICINA ADMINISTRATIVA SR. LUIS KARRY	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'administr':2 'karry':5 'luis':4 'oficin':1 'sr':3
25	1	107B	1	TALLER DE MANTENIMIENTO	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'manten':3 'tall':1
26	1	107B1	1	ALMACEN DE MATERIALES 	0	CIENCIAS DE INGENIERIA Y MATERIALES		-67.139923	18.209641	50.040000	\N	'almac':1 'material':3
27	1	108	1	LABORATORIO ACADEMICO	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
28	1	109	1	SALON DE CLASES 	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'clas':3 'salon':1
29	1	110	1	TALLER(LABORATORIO) DR. OSCAR MARCELO SUAREZ	0	CIENCIAS DE INGENIERIA Y MATERIALES	msuarez@ece.uprm.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'laboratori':2 'marcel':5 'oscar':4 'suarez':6 'tall':1
30	1	110A	1	NON-DESTRUCTIVE TESTING LABORATORY DR. GENOCK PORTELA 	0	CIENCIAS DE INGENIERIA Y MATERIALES	genock.portela@upr.edu	-67.139923	18.209641	50.040000	\N	'destructiv':3 'dr':6 'genock':7 'laboratory':5 'non':2 'non-destructiv':1 'portel':8 'testing':4
31	1	111	1	LABORATORIO DE CARICOOS 	0	CIENCIAS DE INGENIERIA Y MATERIALES	miguelf.canals@upr.edu	-67.139923	18.209641	50.040000	\N	'carico':3 'laboratori':1
32	1	112	1	LABORATORIO ACADEMICO 	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'laboratori':1
33	1	112A	1	OFICINA TECNICO DE LABORATORIO SR. LUIS RODRIGUEZ	0	CIENCIAS DE INGENIERIA Y MATERIALES	director.ciim@uprm.edu	-67.139923	18.209641	50.040000	\N	'laboratori':4 'luis':6 'oficin':1 'rodriguez':7 'sr':5 'tecnic':2
34	1	112B	1	 ALAMCEN	0	CIENCIAS DE INGENIERIA Y MATERIALES	director.ciim@uprm.edu	-67.139923	18.209641	50.040000	\N	'alamc':1
35	1	112C	1	CENTRO DE COMPUTOS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'centr':1 'comput':3
36	1	112D	1	OFICINA TRABAJADOR LAB EDUARDO CINTRON	0	INGENIERIA ELECTRICA	director.ciim@uprm.edu	-67.139923	18.209641	50.040000	\N	'cintron':5 'eduard':4 'lab':3 'oficin':1 'trabaj':2
38	1	113A	1	ALMACEN AUDIOVISUAL	0	INGENIERIA ELECTRICA		-67.139923	18.209641	50.040000	\N	'almac':1 'audiovisual':2
39	1	114	1	SALON DE CLASES 	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'clas':3 'salon':1
159	1	SA 201	2	REPCION 	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'repcion':1
40	1	114B	1	LABORATORIO COMUNICACION ETC DR. MANUEL JIMENEZ	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'comunicacion':2 'dr':4 'etc':3 'jimenez':6 'laboratori':1 'manuel':5
41	1	114C	1	OFICINA DE ESTUDIANTES ACE	0	INGENIERIA ELECTRICA	p.rivera@upr.edu	-67.139923	18.209641	50.040000	\N	'ace':4 'estudi':3 'oficin':1
42	1	114D	1	LABORATORIO INVESTIGACION DR. FABIO ANDRADE 	0	INGENIERIA ELECTRICA	fabio.andrade@ece.uprm.edu 	-67.139923	18.209641	50.040000	\N	'andrad':5 'dr':3 'fabi':4 'investigacion':2 'laboratori':1
43	1	115A	1	LABORATORIO DE MICROO 2 DR. MANUEL JIMENEZ	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'2':4 'dr':5 'jimenez':7 'laboratori':1 'manuel':6 'micro':3
44	1	115C	1	CUARTO COMPRESOR	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'compresor':2 'cuart':1
45	1	116	1	CUARTO CONSERJE	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'conserj':2 'cuart':1
46	1	116B	1	ALAMACEN	0	INGENIERIA ELECTRICA	marcus.sanabria@upr.edu	-67.139923	18.209641	50.040000	\N	'alamac':1
47	1	117	1	BAÑOS FACULTAD HOMBRES	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'facult':2 'hombr':3
48	1	118	1	LABORATORIO INVESTIGACION DR. FABIO ANDRADE 	0	INGENIERIA ELECTRICA	fabio.andrade@upr.edu	-67.139923	18.209641	50.040000	\N	'andrad':5 'dr':3 'fabi':4 'investigacion':2 'laboratori':1
49	1	119	1	OFICICINA DE PROPIEDAD SR. MARCUS SANABRIA	0	INGENIERIA ELECTRICA	marcus.sanabria@upr.edu	-67.139923	18.209641	50.040000	\N	'marcus':5 'oficicin':1 'propied':3 'sanabri':6 'sr':4
50	1	120	1	LABORATORIO INVESTIGACION DR. RAFAEL RODRIGUEZ SOLIS	0	INGENIERIA ELECTRICA	rafael.rodriguez19@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'investigacion':2 'laboratori':1 'rafael':4 'rodriguez':5 'solis':6
51	1	120A	1	LABORATORIO INVESTIGACION CUARTO OSCURO 	0	INGENIERIA ELECTRICA	rafael.rodriguez19@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':3 'investigacion':2 'laboratori':1 'oscur':4
53	1	121	1	LABORATORIO DE COMPUTADORA	0	INGENIERIA ELECTRICA	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'comput':3 'laboratori':1
54	1	122	1	LABORATORIO DE COMPUTADORA	0	INGENIERIA ELECTRICA	isidoro.courvetier@upr.edu	-67.139923	18.209641	50.040000	\N	'comput':3 'laboratori':1
55	1	123A	1	POWER ELECTRONIC	0	INGENIERIA ELECTRICA	naydag.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'electronic':2 'pow':1
56	1	123A1	1	CAPSTONE	0	INGENIERIA ELECTRICA	naydag.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'capston':1
57	1	125	1	BAÑOS DE CABALLEROS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'caballer':3
58	1	126	1	STORAGE ROOM	0	INGENIERIA ELECTRICA	efrain.oneill@upr.edu	-67.139923	18.209641	50.040000	\N	'room':2 'storag':1
59	1	AZOTEA 	1	AZOTEA O ALEROS	0	EDIFICIOS Y TERRENOS - SECCION DE MECANICA Y REFRIGERACION	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'aler':3 'azote':1
60	1	C1	1	ESCALERA PISO #1	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'1':3 'escaler':1 'pis':2
61	1	ELE1	1	 ELEVADOR PISO #1	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'1':3 'elev':1 'pis':2
62	1	P	1	PASILLO PRINCIPAL PISO #1	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'1':4 'pasill':1 'pis':3 'principal':2
63	1	P1	1	PASILLO PISO #1	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'1':3 'pasill':1 'pis':2
64	1	P1A	1	 PASILLO PISO #1	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu 	-67.139923	18.209641	50.040000	\N	'1':3 'pasill':1 'pis':2
65	1	200	2	CUARTO CONSERJE	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'conserj':2 'cuart':1
66	1	200A	2	SALA DE REUNIONES DE PROFESORES	0	INGENIERIA ELECTRICA	ellen.rios@upr.edu	-67.139923	18.209641	50.040000	\N	'profesor':5 'reunion':3 'sal':1
67	1	201	2	SALA DE ESTUDIANTES GRADUADOS 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'estudi':3 'gradu':4 'sal':1
68	1	202	2	LABORATORIO GEMA	0	INGENIERIA ELECTRICA	rafael.rodriguez19@upr.edu	-67.139923	18.209641	50.040000	\N	'gem':2 'laboratori':1
69	1	203	2	SALON DE CLASES	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'clas':3 'salon':1
70	1	204	2	SALON DE CLASES	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'clas':3 'salon':1
71	1	205	2	SALON	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'salon':1
72	1	206	2	SALON	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'salon':1
73	1	207	2	SALON	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'salon':1
74	1	208	2	LABORATORIO RASP DR. MANUEL JIMINEZ 	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'jiminez':5 'laboratori':1 'manuel':4 'rasp':2
75	1	209	2	SALON DE CLASES - AREA DE COMPUTADORA	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'are':4 'clas':3 'comput':6 'salon':1
76	1	209A	2	RECEPCION CENTRO PEARSON	0	CIENCIAS DE INGENIERIA Y MATERIALES	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'centr':2 'pearson':3 'recepcion':1
77	1	209A1	2	ÁREA PROCTOR CENTRO PEARSON	0	CIENCIAS DE INGENIERIA Y MATERIALES	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'are':1 'centr':3 'pearson':4 'proctor':2
78	1	209A2	2	CENTRO PEARSON - AREA DE EXAMEN	0	CIENCIAS DE INGENIERIA Y MATERIALES	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'are':3 'centr':1 'exam':5 'pearson':2
79	1	209B	2	PASILLO ENTRADA	0	CIENCIAS DE INGENIERIA Y MATERIALES	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'entrad':2 'pasill':1
80	1	209B1	2	 OFICINA DE PROFESOR TEMPOREROS 	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3 'temporer':4
81	1	209B2	2	CUARTO MECANICO	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'mecan':2
82	1	209B3	2	ALAMCEN	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'alamc':1
83	1	209B4	2	ALMACEN DE INVESTIGACION 	0	CIENCIAS DE INGENIERIA Y MATERIALES	agnes.padovani@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1 'investigacion':3
84	1	209B5	2	SALON DE CLASES - AREA DE COMPUTADORA	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'are':4 'clas':3 'comput':6 'salon':1
85	1	209B5-A	2	ALMACEN 	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
86	1	209B5-B	2	CUARTO DE SERVIDORES	0	CIENCIAS DE INGENIERIA Y MATERIALES	jaime.ramirez1@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'servidor':3
87	1	209B5-C	2	PASILLO	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
88	1	209B5-C1	2	CUARTO MECANICO	0	CIENCIAS DE INGENIERIA Y MATERIALES	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'mecan':2
89	1	209B5-C2	2	OFIC. PROF. ARQ. JOSE CRESPO	0	CIENCIAS DE INGENIERIA Y MATERIALES	jose.crespo6@upr.edu	-67.139923	18.209641	50.040000	\N	'arq':3 'cresp':5 'jos':4 'ofic':1 'prof':2
90	1	209B5-C3	2	TERRAZA AREA MECAQUINA A/C	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'a/c':4 'are':2 'mecaquin':3 'terraz':1
91	1	210	2	CENTRO DE COMPUTOS	0	CIENCIAS DE INGENIERIA Y MATERIALES	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'centr':1 'comput':3
92	1	210A	2	ALMACEN 	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
93	1	210B	2	AINTEGRATED CCIRCUIT DESIGN LAB AREA DE COMPUTADORAS (SE UNIO CON S210C)	0	INGENIERIA ELECTRICA	rogelio.palomera@upr.edu	-67.139923	18.209641	50.040000	\N	'aintegrat':1 'are':5 'ccircuit':2 'comput':7 'design':3 'lab':4 's210c':11 'uni':9
94	1	210B1	2	 OFICINA PROFESOR DR. ROGELIO PALOMERA	0	INGENIERIA ELECTRICA	rogelio.palomera@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'oficin':1 'palomer':5 'profesor':2 'rogeli':4
95	1	211	2	OFICINA DEL IEEE CAPITULO ESTUDIANTIL	0	COLEGIO DE INGENIERIA	jose.cedeno3@upr.edu	-67.139923	18.209641	50.040000	\N	'capitul':4 'estudiantil':5 'ieee':3 'oficin':1
96	1	211A	2	OFICINA DEL IEEE CAPITULO ESTUDIANTIL	0	COLEGIO DE INGENIERIA	jose.cedeno3@upr.edu	-67.139923	18.209641	50.040000	\N	'capitul':4 'estudiantil':5 'ieee':3 'oficin':1
97	1	212	2	OFICINA PROFESOR DR. EFRAIN ONEILL	0	INGENIERIA ELECTRICA	efrain.oneill@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'efrain':4 'oficin':1 'oneill':5 'profesor':2
98	1	213	2	LABORATORIO DE CONTROLES (ACADEMICO)	0	INGENIERIA ELECTRICA	gerson.beauchamp@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':4 'control':3 'laboratori':1
99	1	214	2	LABORATORIO DR. EDUARDO JUAN	0	INGENIERIA ELECTRICA	eduardoj.juan@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':2 'eduard':3 'juan':4 'laboratori':1
100	1	215	2	OFICINA PROFESOR DR. ISIDORO COURVETIER	0	INGENIERIA ELECTRICA	isidoro.couvetier@upr.edu	-67.139923	18.209641	50.040000	\N	'courveti':5 'dr':3 'isidor':4 'oficin':1 'profesor':2
101	1	215B	2	OFICINA PROFESOR DRA. JEANNETTE SANTOS 	0	INGENIERIA ELECTRICA	jsantos@ece.uprm.edu	-67.139923	18.209641	50.040000	\N	'dra':3 'jeannett':4 'oficin':1 'profesor':2 'sant':5
102	1	216	2	DEPARTAMENTO DE INGENIERIA GENERAL	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'departament':1 'general':4 'ingenieri':3
103	1	216A	2	OFIC. DIRECTOR ASOCIADO VACANTE 	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'asoci':3 'director':2 'ofic':1 'vacant':4
104	1	216B	2	OFICINA DIRECTOR	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'director':2 'oficin':1
105	1	216C	2	ALMACEN	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
106	1	218	2	PUERTA CERRADA(SALIDA EMERGENCIA)	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'cerr':2 'emergent':4 'puert':1 'sal':3
107	1	219	2	RECEPCION	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'recepcion':1
108	1	219B	2	OFICINA R2DEP COLLEGE PROGRAM	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'colleg':3 'oficin':1 'program':4 'r2dep':2
109	1	219C	2	OFICINA AREA DE CUBICULOS	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'are':2 'cubicul':4 'oficin':1
110	1	220	2	RECEPCION	0	COMPUTER SCIENCE AND ENGINEERING	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'recepcion':1
111	1	220A	2	OFICINA ORIENTADORA	0	COMPUTER SCIENCE AND ENGINEERING	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'orient':2
112	1	220B	2	ALMACEN 	0	COMPUTER SCIENCE AND ENGINEERING	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
113	1	220C	2	SALA DE CONFERENCIA	0	COMPUTER SCIENCE AND ENGINEERING	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'conferent':3 'sal':1
114	1	220D	2	OFICINA DIRECTOR	0	COMPUTER SCIENCE AND ENGINEERING	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'director':2 'oficin':1
155	1	C2	2	 ESCALERA PISO #2	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'2':3 'escaler':1 'pis':2
115	1	220E	2	OFICINA DIRECTOR ASOCIADO	0	COMPUTER SCIENCE AND ENGINEERING	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'asoci':3 'director':2 'oficin':1
116	1	220F	2	OFICINA ASISTENTE	0	COMPUTER SCIENCE AND ENGINEERING	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'asistent':2 'oficin':1
117	1	221	2	TRANSFORMADORES ELECTRICOS	0	EDIFICIOS Y TERRENOS	roberto.ayala@upr.edu	-67.139923	18.209641	50.040000	\N	'electr':2 'transform':1
118	1	221A	2	CUARTO CONSERJE	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'conserj':2 'cuart':1
119	1	221B	2	BAÑO CABALLEROS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'caballer':2
120	1	221C	2	 BAÑOS DE DAMAS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'dam':3
121	1	222	2	PASCOR	0	INGENIERIA ELECTRICA	jaime.ramirez1@upr.edu	-67.139923	18.209641	50.040000	\N	'pascor':1
122	1	222A	2	 LABORATORIO CRAI	0	INGENIERIA ELECTRICA	leyda.leon@upr.edu	-67.139923	18.209641	50.040000	\N	'crai':2 'laboratori':1
123	1	222B	2	OFICINA DE INVESTIGACION DR. MANUEL JIMENEZ	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'investigacion':3 'jimenez':6 'manuel':5 'oficin':1
124	1	222C	2	PASILLO OFICINA PROFESORES	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':2 'pasill':1 'profesor':3
125	1	222C1	2	OFICINA PROFESOR DR. JOSE RIVERA CARTAGENA 	0	INGENIERIA ELECTRICA	jose.rivera176@upr.edu	-67.139923	18.209641	50.040000	\N	'cartagen':6 'dr':3 'jos':4 'oficin':1 'profesor':2 'river':5
126	1	222C2	2	OFICINA PROFESOR DR. EDUARDO GARCIA 	0	INGENIERIA ELECTRICA	eduardoj.juan@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'eduard':4 'garci':5 'oficin':1 'profesor':2
127	1	222E	2	LABORATORIO ACADEMICO (DIGITAL SIGNAL PROCESSING LAB)	0	INGENIERIA ELECTRICA	shawndavid.hunt@upr.edu	-67.139923	18.209641	50.040000	\N	'academ':2 'digital':3 'lab':6 'laboratori':1 'processing':5 'signal':4
128	1	222F	2	CUARTO ALMACEN	0	INGENIERIA ELECTRICA	shawndavid.hunt@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':2 'cuart':1
129	1	222G	2	CUARTO ALMACEN	0	INGENIERIA ELECTRICA	shawndavid.hunt@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':2 'cuart':1
130	1	222H	2	OFICINA DE LABORATORIO RUMARINO	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'laboratori':3 'oficin':1 'rumarin':4
131	1	223A	2	LOUNGE Y CORRESPONDENCIA DE PROF.	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'correspondent':3 'loung':1 'prof':5
132	1	223A1	2	PASILLO	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
133	1	223B	2	OFICINA MRS. CLARIBEL LORENZO 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'claribel':3 'lorenz':4 'mrs':2 'oficin':1
134	1	224	2	OFICINA MRS. VERONICA VAZQUEZ / MRS. MARITZA FIGUEROA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'figuero':7 'maritz':6 'mrs':2,5 'oficin':1 'vazquez':4 'veron':3
135	1	224A	2	 DEPARTAMENTO ING. ELECTRICA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu 	-67.139923	18.209641	50.040000	\N	'departament':1 'electr':3 'ing':2
136	1	224B	2	OFICINA MRS. SANDRA MONTALVO 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'montalv':4 'mrs':2 'oficin':1 'sandr':3
137	1	224C	2	OFICINA MR. ERICK APONTE 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'apont':4 'erick':3 'mr':2 'oficin':1
138	1	224CH	2	OFIC. DIRECTOR MRS. ELIZABETH RIVERA 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'director':2 'elizabeth':4 'mrs':3 'ofic':1 'river':5
139	1	224D	2	OFICINA DIRECTOR DR. JOSE COLOM 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'colom':5 'director':2 'dr':3 'jos':4 'oficin':1
140	1	224E	2	SALA DE REUNIONES	0	CIENCIAS DE INGENIERIA Y MATERIALES	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'reunion':3 'sal':1
141	1	225	2	ORIENTACION DE INGENIERIA AREA DE ESPERA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'are':4 'esper':6 'ingenieri':3 'orientacion':1
142	1	225A	2	OFICINA ADMINISTRATIVA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'administr':2 'oficin':1
143	1	225B	2	OFICINA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
144	1	225C	2	OFICINA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
145	1	225CH	2	OFICINA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
146	1	225D	2	OFICINA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
147	1	225E	2	OFICINA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
148	1	227	2	SALON DE CATEDRA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu 	-67.139923	18.209641	50.040000	\N	'catedr':3 'salon':1
149	1	228	2	SALON CATEDRA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu 	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
150	1	229	2	SALON CATEDRA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu 	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
151	1	229A	2	OFICINA PROFESOR DR. FERNANDO VEGA 	0	INGENIERIA ELECTRICA	jfernando.vega@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':3 'fern':4 'oficin':1 'profesor':2 'veg':5
152	1	230	2	SALON DE CLASES	0	INGENIERIA ELECTRICA	paul.sundaram@upr.edu	-67.139923	18.209641	50.040000	\N	'clas':3 'salon':1
153	1	231	2	BAÑOS DE DAMAS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'dam':3
154	1	232	2	BAÑO CABALLEROS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'caballer':2
156	1	P2-1	2	PASILLO PISO #2	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'2':3 'pasill':1 'pis':2
157	1	P2-2	2	PASILLO #3 HACIA 209 B5	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'209':4 '3':2 'b5':5 'haci':3 'pasill':1
158	1	SA 200	2	SALA DE CONFERENCIAS 	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'conferent':3 'sal':1
160	1	SA 201A	2	OFICINA 	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
161	1	SA 201B	2	OFICINA	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
162	1	SA 201C	2	OFICINA	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
163	1	SA 201D	2	OFICINA	0	CIENCIAS DE INGENIERIA Y MATERIALES	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1
164	1	SA 209	2	OFICINA ACREDITACION Y AVALUO Y MEJORAMIENTO CONTINUO OAMMC	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'acreditacion':2 'avalu':4 'continu':7 'mejor':6 'oammc':8 'oficin':1
165	1	SA 210	2	OFICINA ACREDITACION Y AVALUO Y MEJORAMIENTO CONTINUO OAMMC	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'acreditacion':2 'avalu':4 'continu':7 'mejor':6 'oammc':8 'oficin':1
166	1	SA 211	2	SALA DE CONFERENCIAS	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'conferent':3 'sal':1
167	1	SA 211A	2	LOUNGE	0	INGENIERIA ELECTRICA	manuel.jimenez1@upr.edu	-67.139923	18.209641	50.040000	\N	'loung':1
168	1	SA 212	2	ALMACEN	0	EDIFICIOS Y TERRENOS	roberto.ayala@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
169	1	SA 222	2	CUARTO DE VOLTAJES	0	CIENCIAS DE INGENIERIA Y MATERIALES	jaime.ramirez1@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'voltaj':3
170	1	300	3	OFICINA DEL CUSTODIO DE LAS LLAVES	0	COLEGIO DE INGENIERIA	victor.ramirez2@upr.edu	-67.139923	18.209641	50.040000	\N	'custodi':3 'llav':6 'oficin':1
171	1	301	3	ALMACEN	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
172	1	302	3	COBACHA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'cobach':1
173	1	303	3	SALON CATEDRA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
174	1	303A	3	ALMACEN	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'almac':1
175	1	305	3	SALON CATEDRA	22	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
176	1	306	3	SALON CATEDRA	22	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
177	1	307	3	SALON CATEDRA	22	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
178	1	308	3	SALON CATEDRA	22	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
179	1	309	3	SALON CATEDRA	22	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':2 'salon':1
180	1	310	3	LABORATORIO DE INVESTIGACION DR. MARCELO SUAREZ	0	CIENCIAS DE INGENIERIA Y MATERIALES	msuarez@ece.uprm.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'investigacion':3 'laboratori':1 'marcel':5 'suarez':6
181	1	311	3	LABORATORIO DE INVESTIGACION DR. OSCAR MARCELO SUAREZ	0	CIENCIAS DE INGENIERIA Y MATERIALES	msuarez@ece.uprm.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'investigacion':3 'laboratori':1 'marcel':6 'oscar':5 'suarez':7
182	1	313	3	LABORATORIO DE INVESTIGACION DR. OSCAR PERALES 	0	CIENCIAS DE INGENIERIA Y MATERIALES	oscarjuan.perales@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'investigacion':3 'laboratori':1 'oscar':5 'peral':6
183	1	313A	3	LABORATORIO DE INSVESTIGACION DR. OSCAR PERALES	0	INGENIERIA ELECTRICA	oscarjuan.perales@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'insvestigacion':3 'laboratori':1 'oscar':5 'peral':6
184	1	314	3	LABORATORIO DE INVESTIGACION DR. OSCAR PERALES	0	CIENCIAS DE INGENIERIA Y MATERIALES	oscarjuan.perales@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'investigacion':3 'laboratori':1 'oscar':5 'peral':6
185	1	315	3	SALON DE CATEDRA	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'catedr':3 'salon':1
186	1	316	3	LABABORATORIO DE GRAFICAS	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'grafic':3 'lababoratori':1
187	1	317	3	CUARTO SISTEMA TELEFONICO	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'sistem':2 'telefon':3
188	1	318	3	DECANATO DE INGENERIA 	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu 	-67.139923	18.209641	50.040000	\N	'decanat':1 'ingeneri':3
189	1	318A	3	DIRECTOR ASOCIADO DR. OSCAR PERALES 	0	INGENIERIA ELECTRICA	oscarjuan.perales@upr.edu	-67.139923	18.209641	50.040000	\N	'asoci':2 'director':1 'dr':3 'oscar':4 'peral':5
190	1	318B	3	DECANO DE INGENERIA DR. AGUSTIN RULLAN 	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'agustin':5 'decan':1 'dr':4 'ingeneri':3 'rull':6
191	1	319	3	DECANATO DE INGENIERIA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'decanat':1 'ingenieri':3
192	1	320	3	DECANATO DE INGENIERIA	0	INGENIERIA ELECTRICA	norma.gomez@upr.edu	-67.139923	18.209641	50.040000	\N	'decanat':1 'ingenieri':3
193	1	321	3	DECANATO DE INGENIERIA	0	COLEGIO DE INGENIERIA	william.hernandez3@upr.edu	-67.139923	18.209641	50.040000	\N	'decanat':1 'ingenieri':3
194	1	322	3	DECANATO DE INGENIERIA	0	COLEGIO DE INGENIERIA	william.hernandez3@upr.edu	-67.139923	18.209641	50.040000	\N	'decanat':1 'ingenieri':3
195	1	323	3	DECANATO DE INGENIERIA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'decanat':1 'ingenieri':3
196	1	324	3	BAÑOS	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1
197	1	325	3	COBACHA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'cobach':1
199	1	327	3	ALMACEN EN AZOTEA PISO 2	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'2':5 'almac':1 'azote':3 'pis':4
200	1	AZ2	3	AZOTEA PISO 2	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'2':3 'azote':1 'pis':2
201	1	C3	3	ESCALERA	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'escaler':1
202	1	ELE3	3	ELEVADOR	0	INGENIERIA ELECTRICA	luis.karry1@upr.edu	-67.139923	18.209641	50.040000	\N	'elev':1
203	1	P3	3	PASILLO	0	MECHANICAL ENGINEERING	ricky.valentin@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
204	1	400	4	OFICINA DE PROFESOR DR. NESTOR RODRIGUEZ	0	INGENIERIA ELECTRICA	nestorj.rodriguez@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'nestor':5 'oficin':1 'profesor':3 'rodriguez':6
205	1	401	4	OFICINA DE PROFESOR DR. JOSE A. BORGES 	0	INGENIERIA ELECTRICA	jose.borges1@upr.edu	-67.139923	18.209641	50.040000	\N	'borg':7 'dr':4 'jos':5 'oficin':1 'profesor':3
206	1	402	4	OFICINA DE PROFESOR DR. ROGELIO PALOMERA 	0	INGENIERIA ELECTRICA	rogelio.palomera@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'oficin':1 'palomer':6 'profesor':3 'rogeli':5
207	1	403	4	OFICINA DE PROFESOR DR. AGUSTIN IRIZARRY 	0	INGENIERIA ELECTRICA	agustin.irizarry@upr.edu	-67.139923	18.209641	50.040000	\N	'agustin':5 'dr':4 'irizarry':6 'oficin':1 'profesor':3
208	1	404	4	OFICINA DE PROFESOR DR. GERSON BEAUCHAMP	0	INGENIERIA ELECTRICA	gerson.beauchamp@upr.edu	-67.139923	18.209641	50.040000	\N	'beauchamp':6 'dr':4 'gerson':5 'oficin':1 'profesor':3
209	1	405	4	OFICINA DE PROFESOR DR. JOSE COLOM 	0	INGENIERIA ELECTRICA	jose.colom1@upr.edu	-67.139923	18.209641	50.040000	\N	'colom':6 'dr':4 'jos':5 'oficin':1 'profesor':3
210	1	406	4	OFICINA DE PROFESOR DRA. FREYA TOLEDO 	0	CIENCIAS DE INGENIERIA Y MATERIALES	freya.toledo@upr.edu	-67.139923	18.209641	50.040000	\N	'dra':4 'frey':5 'oficin':1 'profesor':3 'toled':6
211	1	407	4	OFICINA DE PROFESOR DR. HAMED PARSIANI 	0	INGENIERIA ELECTRICA	hamed.parsiani@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'ham':5 'oficin':1 'parsiani':6 'profesor':3
212	1	408	4	OFICINA DE PROFESOR DRA. VYDIA MANIAN 	0	INGENIERIA ELECTRICA	vidya.manian@upr.edu	-67.139923	18.209641	50.040000	\N	'dra':4 'mani':6 'oficin':1 'profesor':3 'vydi':5
213	1	409	4	OFICINA DE PROFESOR DR. KRISHNASWAMI VENKATESAN	0	INGENIERIA ELECTRICA	krishnaswa.venkatesan@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'krishnaswami':5 'oficin':1 'profesor':3 'venkates':6
214	1	410	4	OFICINA DE PROFESOR DR. JAIME ARBONA 	0	INGENIERIA ELECTRICA	jaime.arbona@upr.edu	-67.139923	18.209641	50.040000	\N	'arbon':6 'dr':4 'jaim':5 'oficin':1 'profesor':3
215	1	411	4	OFICINA DE PROFESOR DR. WILSON RIVERA GALLEGO	0	INGENIERIA ELECTRICA	wilson.riveragallego@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'galleg':7 'oficin':1 'profesor':3 'river':6 'wilson':5
216	1	412	4	OFICINA DE PROFESOR DR. ALBERTO RAMIREZ 	0	INGENIERIA ELECTRICA	alberto.ramirez2@upr.edu	-67.139923	18.209641	50.040000	\N	'albert':5 'dr':4 'oficin':1 'profesor':3 'ramirez':6
217	1	413	4	OFICINA DE PROFESOR DRA. NAYDA SANTIAGO	0	INGENIERIA ELECTRICA	naydag.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'dra':4 'nayd':5 'oficin':1 'profesor':3 'santiag':6
218	1	414	4	OFICINA DE PROFESOR DR. ERICK E. APONTE 	0	INGENIERIA ELECTRICA	erick.aponte1@upr.edu	-67.139923	18.209641	50.040000	\N	'apont':7 'dr':4 'erick':5 'oficin':1 'profesor':3
219	1	415	4	OFICINA DE PROFESOR DR. RAMON VASQUEZ ESPINOSA 	0	INGENIERIA ELECTRICA	ramon.vasquez@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'espin':7 'oficin':1 'profesor':3 'ramon':5 'vasquez':6
220	1	416	4	COBACHA	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'cobach':1
221	1	417	4	OFICINA CONSEJO DE ESTIDIANTES	0	INGENIERIA ELECTRICA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'consej':2 'estidi':4 'oficin':1
222	1	417B	4	CUARTO DE DATA	0	CIENCIAS DE INGENIERIA Y MATERIALES	jaime.ramirez1@upr.edu	-67.139923	18.209641	50.040000	\N	'cuart':1 'dat':3
223	1	C4	4	ESCALERA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'escaler':1
224	1	ELE4	4	ELEVADOR	0	COLEGIO DE INGENIERIA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'elev':1
225	1	P4	4	PASILLO	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
226	1	500	5	OFICINA DE PROFESOR DR. LUIS JIMENEZ RODRIGUEZ	0	INGENIERIA ELECTRICA	jimenez@ece.uprm.edu 	-67.139923	18.209641	50.040000	\N	'dr':4 'jimenez':6 'luis':5 'oficin':1 'profesor':3 'rodriguez':7
227	1	501	5	OFICINA DE PROFESOR	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
228	1	502	5	OFICINA DE PROFESOR DR. SAHWN HUNT 	0	INGENIERIA ELECTRICA	shawndavid.hunt@upr.edu 	-67.139923	18.209641	50.040000	\N	'dr':4 'hunt':6 'oficin':1 'profesor':3 'sahwn':5
229	1	503	5	OFICINA DE PROFESOR DR. ARSLAN SHOKOOH 	0	CIENCIAS DE INGENIERIA Y MATERIALES	ashokooh@uprm.edu	-67.139923	18.209641	50.040000	\N	'arslan':5 'dr':4 'oficin':1 'profesor':3 'shokooh':6
230	1	504	5	OFICINA DE PROFESOR DR. OSWALD UWAKWEH	0	CIENCIAS DE INGENIERIA Y MATERIALES	Uwakweh@ece.uprm.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'oficin':1 'oswald':5 'profesor':3 'uwakweh':6
231	1	505	5	OFICINA DE PROFESOR ARQ. EDUARDO AÑESES / PROF. CARMEN CASTAÑEYRA 	0	CIENCIAS DE INGENIERIA Y MATERIALES	carmen.castaneyra@upr.edu	-67.139923	18.209641	50.040000	\N	'arq':4 'añes':6 'carm':8 'castañeyr':9 'eduard':5 'oficin':1 'prof':7 'profesor':3
232	1	506	5	OFICINA DE PROFESOR DR. MARIO RIVERA 	0	CIENCIAS DE INGENIERIA Y MATERIALES	mario.rivera@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'mari':5 'oficin':1 'profesor':3 'river':6
233	1	507	5	OFICINA DE PROFESOR DR. MARIO IERICK 	0	INGENIERIA ELECTRICA	henrick.ierick@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'ierick':6 'mari':5 'oficin':1 'profesor':3
234	1	508	5	OFICINA DE PROFESOR DR. RAFAEL ROGRIGUEZ SOLIS 	0	INGENIERIA ELECTRICA	rafael.rodriguez19@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'oficin':1 'profesor':3 'rafael':5 'rogriguez':6 'solis':7
235	1	509	5	OFICINA DE PROFESOR DR. GULLERMO SERRANO 	0	INGENIERIA ELECTRICA	guillermo.serrano@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'gullerm':5 'oficin':1 'profesor':3 'serran':6
273	1	AZ7A	7	 AZOTEA	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'azote':1
236	1	510	5	EARTHQUAKE ENGINEERING SIMULATION LABORATORY DR. LUIS MONTEJO 	0	CIENCIAS DE INGENIERIA Y MATERIALES	luis.montejo@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':5 'earthquak':1 'engineering':2 'laboratory':4 'luis':6 'montej':7 'simulation':3
237	1	511	5	OFICINA DE PROFESOR DR. GENOCK PORTELA	0	CIENCIAS DE INGENIERIA Y MATERIALES	genock.portela@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'genock':5 'oficin':1 'portel':6 'profesor':3
238	1	512	5	OFICINA DE PROFESOR DRA. BARBARA CALCAGNO	0	CIENCIAS DE INGENIERIA Y MATERIALES	barbara.calcagno@upr.edu	-67.139923	18.209641	50.040000	\N	'barb':5 'calcagn':6 'dra':4 'oficin':1 'profesor':3
239	1	513	5	OFICINA DE PROFESOR DR. EDUADRO ORTIZ	0	INGENIERIA ELECTRICA	euardo.ortiz7@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'eduadr':5 'oficin':1 'ortiz':6 'profesor':3
240	1	514	5	COBACHA DE CONSERJE	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'cobach':1 'conserj':3
241	1	515	5	OFICINA DE PROFESOR	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
242	1	516	5	OFICINA DE PROFESOR	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
243	1	C5	5	ESCALERA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'escaler':1
244	1	ELE5	5	ELEVADOR	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'elev':1
245	1	P5	5	PASILLO	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
246	1	600	6	OFICINA DE PROFESOR DR. JAIME SEGUEL 	0	COLEGIO DE INGENIERIA	jaime.seguel@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'jaim':5 'oficin':1 'profesor':3 'seguel':6
247	1	601	6	OFICINA DE PROFESOR DR. KEJIE LU 	0	COLEGIO DE INGENIERIA	kejie.lu@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'keji':5 'lu':6 'oficin':1 'profesor':3
248	1	602	6	OFICINA DE PROFESOR DR. MANUEL RODRIGUEZ MARTINEZ	0	COLEGIO DE INGENIERIA	manuel.rodriguez7@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'manuel':5 'martinez':7 'oficin':1 'profesor':3 'rodriguez':6
249	1	603	6	OFICINA DE PROFESOR DR. YANG LI 	0	COLEGIO DE INGENIERIA	yang.li@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'li':6 'oficin':1 'profesor':3 'yang':5
250	1	604	6	OFICINA DE PROFESOR DRA. SANDRA CRUZ POL	0	INGENIERIA ELECTRICA	sandra.cruz1@upr.edu	-67.139923	18.209641	50.040000	\N	'cruz':6 'dra':4 'oficin':1 'pol':7 'profesor':3 'sandr':5
251	1	605	6	OFICINA DE PROFESOR DR. AIDSA SANTIAGO 	0	COLEGIO DE INGENIERIA	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'aids':5 'dr':4 'oficin':1 'profesor':3 'santiag':6
252	1	606	6	OFICINA DE PROFESOR DR. OSCAR PERALES 	0	CIENCIAS DE INGENIERIA Y MATERIALES	oscarjuan.perales@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'oficin':1 'oscar':5 'peral':6 'profesor':3
253	1	607	6	OFICINA DE PROFESOR DR. MARCO AROCHA 	0	CIENCIAS DE INGENIERIA Y MATERIALES	marcoantonio.arocha@uprm.edu	-67.139923	18.209641	50.040000	\N	'aroch':6 'dr':4 'marc':5 'oficin':1 'profesor':3
254	1	608	6	OFICINA DE PROFESOR DR. JOSE ARROYO 	0	CIENCIAS DE INGENIERIA Y MATERIALES	jose.arroyo5@upr.edu	-67.139923	18.209641	50.040000	\N	'arroy':6 'dr':4 'jos':5 'oficin':1 'profesor':3
255	1	609	6	OFICINA DE PROFESOR 	0	CIENCIAS DE INGENIERIA Y MATERIALES	aidsa.santiago@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
256	1	610	6	OFICINA DE PROFESOR DR. BASIR SHAFIQ / DR. PEDRO RIVERA 	0	CIENCIAS DE INGENIERIA Y MATERIALES	basir.shafiq@upr.edu	-67.139923	18.209641	50.040000	\N	'bas':5 'dr':4,7 'oficin':1 'pedr':8 'profesor':3 'river':9 'shafiq':6
257	1	611	6	OFICINA DE PROFESOR DR. DOMINGO RODRIGUEZ / DRA. GLADYS DUCOUDRAY 	0	INGENIERIA ELECTRICA	domingo.rodriguez1@upr.edu	-67.139923	18.209641	50.040000	\N	'doming':5 'dr':4 'dra':7 'ducoudray':9 'gladys':8 'oficin':1 'profesor':3 'rodriguez':6
258	1	612	6	OFICINA DE PROFESOR DR. IVAN BAIGES 	0	CIENCIAS DE INGENIERIA Y MATERIALES	ivan.baiges@upr.edu	-67.139923	18.209641	50.040000	\N	'baig':6 'dr':4 'ivan':5 'oficin':1 'profesor':3
259	1	613	6	OFICINA DE PROFESOR	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
260	1	614	6	OFICINA DE PROFESOR	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
261	1	615	6	BAÑO UNISEX	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'bañ':1 'unisex':2
262	1	616	6	OFICINA PROFESOR DRA. AGENES PADOVANI 	0	COLEGIO DE INGENIERIA	agnes.padovani@upr.edu	-67.139923	18.209641	50.040000	\N	'agen':4 'dra':3 'oficin':1 'padovani':5 'profesor':2
263	1	C6	6	ESCALERA	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'escaler':1
264	1	ELE6	6	ELEVADOR	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'elev':1
265	1	P6	6	PASILLO	0	COLEGIO DE INGENIERIA	agustin.rullan@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
266	1	700	7	PASILLO	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'pasill':1
267	1	701	7	OFICINA DE PROFESOR DR. BIENVENIDO VELEZ	0	INGENIERIA ELECTRICA	bienvenido.velez@upr.edu	-67.139923	18.209641	50.040000	\N	'bienven':5 'dr':4 'oficin':1 'profesor':3 'velez':6
268	1	702	7	OFICINA DE PROFESOR DR. LIONEL ORAMA EXCLUSA	0	INGENIERIA ELECTRICA	lionel.orama1@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'exclus':7 'lionel':5 'oficin':1 'oram':6 'profesor':3
269	1	703	7	OFICINA DE PROFESOR DR. MAUEL TOLEDO QUIÑONES 	0	INGENIERIA ELECTRICA	manuel.toledo1@upr.edu	-67.139923	18.209641	50.040000	\N	'dr':4 'mauel':5 'oficin':1 'profesor':3 'quiñon':7 'toled':6
270	1	704	7	OFICINA DE PROFESOR	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'oficin':1 'profesor':3
271	1	705	7	OFICINA DE PROFESORDR. RAUL TORRES MUÑIZ 	0	INGENIERIA ELECTRICA	raul_e.torres@upr.edu	-67.139923	18.209641	50.040000	\N	'muñiz':6 'oficin':1 'profesordr':3 'raul':4 'torr':5
272	1	AZ7	7	TERRAZA	0	INGENIERIA ELECTRICA	pedro.rivera25@upr.edu	-67.139923	18.209641	50.040000	\N	'terraz':1
274	1	AZ7B	7	AZOTEA	0	EDIFICIOS Y TERRENOS	jaime.ramirez1@upr.edu	-67.139923	18.209641	50.040000	\N	'azote':1
\.


--
-- Data for Name: servicephones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servicephones (sid, phoneid, isdeleted) FROM stdin;
3	3	f
4	1	f
4	2	f
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services (sid, rid, sname, sdescription, sschedule, isdeleted, sname_tokens, sdescription_tokens) FROM stdin;
1	56	Office Hours: Victor Lugo	Capstone TA Office Hours; Available to answer questions.	L, W: 9:30am - 10:30am	f	'hour':2 'lugo':4 'offic':1 'victor':3	'answer':7 'avail':5 'capston':1 'hour':4 'offic':3 'question':8 'ta':2
2	56	Office Hours: David Riquelme	Capstone TA Office Hours; Available to answer questions.	M, V: 2:30pm - 3:30pm	f	'david':3 'hour':2 'offic':1 'riquelm':4	'answer':7 'avail':5 'capston':1 'hour':4 'offic':3 'question':8 'ta':2
3	151	Office Hours: Fernando Vega	Office Hours to discuss class topics, and consult with Capstone Team.	L: 3:30pm - 4:30pm, W: 1:30pm - 3:30pm	f	'fernando':3 'hour':2 'offic':1 'vega':4	'capston':10 'class':5 'consult':8 'discuss':4 'hour':2 'offic':1 'team':11 'topic':6
4	134	ECE Counseling	Counseling and guidance for students with regards to their academic carreers and progress.	L-V: 7:30am-12:30pm, 1:30pm-4:30pm	f	'counsel':2 'ece':1	'academ':10 'carreer':11 'counsel':1 'guidanc':3 'progress':13 'regard':7 'student':5
\.


--
-- Data for Name: servicewebsites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servicewebsites (sid, wid, wdescription, isdeleted) FROM stdin;
3	2	J. Fernando Vega-Riveros, Ph.D. Professor	f
4	1	Counselors	f
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags (tid, tname) FROM stdin;
1	ADMI
2	ADOF
3	AGRO
4	ALEM
5	ANTR
6	ARTE
7	ASTR
8	BIND
9	BIOL
10	BOTA
11	CFIT
12	CHIN
13	CIAN
14	CIBI
15	CIFI
16	CIIC
17	CIMA
18	CIMI
19	CINE
20	CIPO
21	CISO
22	CMOB
23	CMOF
24	COMP
25	CONT
26	DESC
27	ECAG
28	ECON
29	EDAG
30	EDES
31	EDFI
32	EDFU
33	EDMA
34	EDPE
35	ENFE
36	ESAE
37	ESMA
38	ESOR
39	ESPA
40	ESTA
41	EXAG
42	FILO
43	FINA
44	FISI
45	FRAN
46	GEOG
47	GEOL
48	GERE
49	GERH
50	GRIE
51	HIST
52	HORT
53	HUMA
54	ICOM
55	INAG
56	INCI
57	INEL
58	INGE
59	INGL
60	ININ
61	INME
62	INPE
63	INQU
64	INSO
65	INTD
66	ITAL
67	JAPO
68	LATI
69	LING
70	LITE
71	MATE
72	MERC
73	METE
74	MUSI
75	PROC
76	PSIC
77	QUIM
78	RECR
79	RUSO
80	SAGA
81	SICI
82	SOCI
83	TEAT
84	TEED
85	TMAG
86	UNIV
87	ZOOL
\.


--
-- Data for Name: tagtaxonomies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tagtaxonomies (parenttag, childtag) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (uid, email, usub, display_name, type, roleid, roleissuer) FROM stdin;
13	diego.amador@upr.edu	105062184424293178776	Diego J	Student	1	1
5	sofia.saavedra@upr.edu	79461	Sofia Saavedra	Student	2	1
6	brian.rodriguez17@upr.edu	102004345784130676218	Brian Rodriguez	Student	1	1
11	diegoj.amador@gmail.com	105372230720749956613	DIEGO AMADOR	Student	1	1
9	diegoxdinero@gmail.com	115333079701671763576	Diego Amador	Student	4	1
2	diego.ama89dor@upr.edu	987654	Diego Amador	Professor	3	1
1	brianrodrig@gmail.com	116089969646145145010	Brian Rodriguez Badillo	Student	4	3
18	kensy.bernadeau@gmail.com	110080137637084733672	kensy bernadeau	Student	1	1
3	kensy.bernadeau@upr.edu	113566820811417441289	Kensy Bernadeau	Non_Faculty	4	1
4	jonathan.santiago27@upr.edu	113768707919850641968	Jonathan Santiago	Student	4	1
\.


--
-- Data for Name: usertags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usertags (uid, tid, tagweight) FROM stdin;
1	19	75
1	6	75
1	54	75
1	66	75
1	87	75
3	25	200
3	69	190
3	82	1
3	30	94
3	23	40
4	7	34
4	22	1
4	49	9
5	42	65
5	20	49
5	62	77
5	29	96
5	84	44
4	3	20
4	1	15
4	2	15
4	73	0
4	47	0
4	53	5
4	58	5
4	57	5
4	54	5
4	6	5
4	42	0
4	64	0
4	5	5
4	4	59
\.


--
-- Data for Name: websites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.websites (wid, url) FROM stdin;
1	https://ece.uprm.edu/student-services/conseling/
2	http://ece.uprm.edu/~fvega/
11	https://piazza.com/class/k8330k2tk065ll?cid=62
16	https://github.com/InTheNou/InTheNou-Backend
17	https://github.com/InTheNou/InTheNou-App
18	https://github.com/InTheNou
19	https://online.upr.edu/
20	https://piazza.com/class/k8330k2tk065ll
3	https://portal.upr.edu/rum/portal.php?a=rea_login
4	https://home.uprm.edu/index.php?l=0
23	https://ecourses.uprm.edu/custom/my_login.html
24	https://ece.uprm.edu/
25	https://inthenou.uprm.edu
\.


--
-- Name: buildings_bid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.buildings_bid_seq', 1, true);


--
-- Name: events_eid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_eid_seq', 30, true);


--
-- Name: phones_phoneid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phones_phoneid_seq', 3, true);


--
-- Name: photos_photoid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_photoid_seq', 12, true);


--
-- Name: privileges_privilegeid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.privileges_privilegeid_seq', 12, true);


--
-- Name: roles_roleid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_roleid_seq', 4, true);


--
-- Name: rooms_rid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_rid_seq', 274, true);


--
-- Name: services_sid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_sid_seq', 4, true);


--
-- Name: tags_tid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_tid_seq', 87, true);


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_uid_seq', 19, true);


--
-- Name: websites_wid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.websites_wid_seq', 35, true);


--
-- Name: buildings buildings_bname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_bname_key UNIQUE (bname);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (bid);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (eid);


--
-- Name: eventtags eventtags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventtags
    ADD CONSTRAINT eventtags_pkey PRIMARY KEY (eid, tid);


--
-- Name: eventuserinteractions eventuserinteractions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventuserinteractions
    ADD CONSTRAINT eventuserinteractions_pkey PRIMARY KEY (uid, eid);


--
-- Name: eventwebsites eventwebsites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventwebsites
    ADD CONSTRAINT eventwebsites_pkey PRIMARY KEY (eid, wid);


--
-- Name: events no_duplicate_events_at_same_time_place; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT no_duplicate_events_at_same_time_place UNIQUE (roomid, etitle, estart);


--
-- Name: oauth oauth_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth
    ADD CONSTRAINT oauth_pkey PRIMARY KEY (access_token, uid);


--
-- Name: phones phones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY (phoneid);


--
-- Name: phones phones_pnumber_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_pnumber_key UNIQUE (pnumber);


--
-- Name: photos photos_photourl_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_photourl_key UNIQUE (photourl);


--
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (photoid);


--
-- Name: privileges privileges_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.privileges
    ADD CONSTRAINT privileges_pkey PRIMARY KEY (privilegeid);


--
-- Name: privileges privileges_privilegename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.privileges
    ADD CONSTRAINT privileges_privilegename_key UNIQUE (privilegename);


--
-- Name: roleprivileges roleprivileges_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleprivileges
    ADD CONSTRAINT roleprivileges_pkey PRIMARY KEY (roleid, privilegeid);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (roleid);


--
-- Name: roles roles_roletype_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_roletype_key UNIQUE (roletype);


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (rid);


--
-- Name: rooms rooms_rcode_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_rcode_key UNIQUE (rcode);


--
-- Name: servicephones servicephones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicephones
    ADD CONSTRAINT servicephones_pkey PRIMARY KEY (sid, phoneid);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (sid);


--
-- Name: servicewebsites servicewebsites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicewebsites
    ADD CONSTRAINT servicewebsites_pkey PRIMARY KEY (sid, wid);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tid);


--
-- Name: tags tags_tname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_tname_key UNIQUE (tname);


--
-- Name: tagtaxonomies tagtaxonomies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagtaxonomies
    ADD CONSTRAINT tagtaxonomies_pkey PRIMARY KEY (parenttag, childtag);


--
-- Name: services unique_room_services; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT unique_room_services UNIQUE (rid, sname);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: users users_usub_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_usub_key UNIQUE (usub);


--
-- Name: usertags usertags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertags
    ADD CONSTRAINT usertags_pkey PRIMARY KEY (uid, tid);


--
-- Name: websites websites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.websites
    ADD CONSTRAINT websites_pkey PRIMARY KEY (wid);


--
-- Name: websites websites_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.websites
    ADD CONSTRAINT websites_url_key UNIQUE (url);


--
-- Name: events vectorizeevent; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER vectorizeevent BEFORE INSERT OR UPDATE ON public.events FOR EACH ROW EXECUTE PROCEDURE public.vectorizeevent();


--
-- Name: rooms vectorizeroomdescription; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER vectorizeroomdescription BEFORE INSERT OR UPDATE ON public.rooms FOR EACH ROW EXECUTE PROCEDURE public.vectorizeroomdescription();


--
-- Name: services vectorizeservice; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER vectorizeservice BEFORE INSERT OR UPDATE ON public.services FOR EACH ROW EXECUTE PROCEDURE public.vectorizeservice();


--
-- Name: buildings buildings_photoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_photoid_fkey FOREIGN KEY (photoid) REFERENCES public.photos(photoid);


--
-- Name: events events_ecreator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_ecreator_fkey FOREIGN KEY (ecreator) REFERENCES public.users(uid);


--
-- Name: events events_photoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_photoid_fkey FOREIGN KEY (photoid) REFERENCES public.photos(photoid);


--
-- Name: events events_roomid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_roomid_fkey FOREIGN KEY (roomid) REFERENCES public.rooms(rid);


--
-- Name: eventtags eventtags_eid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventtags
    ADD CONSTRAINT eventtags_eid_fkey FOREIGN KEY (eid) REFERENCES public.events(eid);


--
-- Name: eventtags eventtags_tid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventtags
    ADD CONSTRAINT eventtags_tid_fkey FOREIGN KEY (tid) REFERENCES public.tags(tid);


--
-- Name: eventuserinteractions eventuserinteractions_eid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventuserinteractions
    ADD CONSTRAINT eventuserinteractions_eid_fkey FOREIGN KEY (eid) REFERENCES public.events(eid);


--
-- Name: eventuserinteractions eventuserinteractions_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventuserinteractions
    ADD CONSTRAINT eventuserinteractions_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: eventwebsites eventwebsites_eid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventwebsites
    ADD CONSTRAINT eventwebsites_eid_fkey FOREIGN KEY (eid) REFERENCES public.events(eid);


--
-- Name: eventwebsites eventwebsites_wid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventwebsites
    ADD CONSTRAINT eventwebsites_wid_fkey FOREIGN KEY (wid) REFERENCES public.websites(wid);


--
-- Name: oauth oauth_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth
    ADD CONSTRAINT oauth_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: roleprivileges roleprivileges_privilegeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleprivileges
    ADD CONSTRAINT roleprivileges_privilegeid_fkey FOREIGN KEY (privilegeid) REFERENCES public.privileges(privilegeid);


--
-- Name: roleprivileges roleprivileges_roleid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roleprivileges
    ADD CONSTRAINT roleprivileges_roleid_fkey FOREIGN KEY (roleid) REFERENCES public.roles(roleid);


--
-- Name: rooms rooms_bid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_bid_fkey FOREIGN KEY (bid) REFERENCES public.buildings(bid);


--
-- Name: rooms rooms_photoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_photoid_fkey FOREIGN KEY (photoid) REFERENCES public.photos(photoid);


--
-- Name: servicephones servicephones_phoneid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicephones
    ADD CONSTRAINT servicephones_phoneid_fkey FOREIGN KEY (phoneid) REFERENCES public.phones(phoneid);


--
-- Name: servicephones servicephones_sid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicephones
    ADD CONSTRAINT servicephones_sid_fkey FOREIGN KEY (sid) REFERENCES public.services(sid);


--
-- Name: services services_rid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_rid_fkey FOREIGN KEY (rid) REFERENCES public.rooms(rid);


--
-- Name: servicewebsites servicewebsites_sid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicewebsites
    ADD CONSTRAINT servicewebsites_sid_fkey FOREIGN KEY (sid) REFERENCES public.services(sid);


--
-- Name: servicewebsites servicewebsites_wid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicewebsites
    ADD CONSTRAINT servicewebsites_wid_fkey FOREIGN KEY (wid) REFERENCES public.websites(wid);


--
-- Name: tagtaxonomies tagtaxonomies_childtag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagtaxonomies
    ADD CONSTRAINT tagtaxonomies_childtag_fkey FOREIGN KEY (childtag) REFERENCES public.tags(tid);


--
-- Name: tagtaxonomies tagtaxonomies_parenttag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagtaxonomies
    ADD CONSTRAINT tagtaxonomies_parenttag_fkey FOREIGN KEY (parenttag) REFERENCES public.tags(tid);


--
-- Name: users users_roleid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_roleid_fkey FOREIGN KEY (roleid) REFERENCES public.roles(roleid);


--
-- Name: users users_roleissuer_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_roleissuer_fkey FOREIGN KEY (roleissuer) REFERENCES public.users(uid);


--
-- Name: usertags usertags_tid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertags
    ADD CONSTRAINT usertags_tid_fkey FOREIGN KEY (tid) REFERENCES public.tags(tid);


--
-- Name: usertags usertags_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertags
    ADD CONSTRAINT usertags_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: TABLE buildings; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.buildings TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.buildings TO inthenouapi;


--
-- Name: SEQUENCE buildings_bid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.buildings_bid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.buildings_bid_seq TO inthenouapi;


--
-- Name: TABLE events; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.events TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.events TO inthenouapi;


--
-- Name: SEQUENCE events_eid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.events_eid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.events_eid_seq TO inthenouapi;


--
-- Name: TABLE eventtags; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.eventtags TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.eventtags TO inthenouapi;


--
-- Name: TABLE eventuserinteractions; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.eventuserinteractions TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.eventuserinteractions TO inthenouapi;


--
-- Name: TABLE eventwebsites; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.eventwebsites TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.eventwebsites TO inthenouapi;


--
-- Name: TABLE oauth; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.oauth TO inthenouapi;
GRANT ALL ON TABLE public.oauth TO inthenouadmin;


--
-- Name: TABLE phones; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.phones TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.phones TO inthenouapi;


--
-- Name: SEQUENCE phones_phoneid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.phones_phoneid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.phones_phoneid_seq TO inthenouapi;


--
-- Name: TABLE photos; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.photos TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.photos TO inthenouapi;


--
-- Name: SEQUENCE photos_photoid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.photos_photoid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.photos_photoid_seq TO inthenouapi;


--
-- Name: TABLE privileges; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.privileges TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.privileges TO inthenouapi;


--
-- Name: SEQUENCE privileges_privilegeid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.privileges_privilegeid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.privileges_privilegeid_seq TO inthenouapi;


--
-- Name: TABLE roleprivileges; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.roleprivileges TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.roleprivileges TO inthenouapi;


--
-- Name: TABLE roles; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.roles TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.roles TO inthenouapi;


--
-- Name: SEQUENCE roles_roleid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.roles_roleid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.roles_roleid_seq TO inthenouapi;


--
-- Name: TABLE rooms; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.rooms TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.rooms TO inthenouapi;


--
-- Name: SEQUENCE rooms_rid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.rooms_rid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.rooms_rid_seq TO inthenouapi;


--
-- Name: TABLE servicephones; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.servicephones TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.servicephones TO inthenouapi;


--
-- Name: TABLE services; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.services TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.services TO inthenouapi;


--
-- Name: SEQUENCE services_sid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.services_sid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.services_sid_seq TO inthenouapi;


--
-- Name: TABLE servicewebsites; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.servicewebsites TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.servicewebsites TO inthenouapi;


--
-- Name: TABLE tags; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tags TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.tags TO inthenouapi;


--
-- Name: SEQUENCE tags_tid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.tags_tid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.tags_tid_seq TO inthenouapi;


--
-- Name: TABLE tagtaxonomies; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tagtaxonomies TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.tagtaxonomies TO inthenouapi;


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.users TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.users TO inthenouapi;


--
-- Name: SEQUENCE users_uid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.users_uid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.users_uid_seq TO inthenouapi;


--
-- Name: TABLE usertags; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.usertags TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.usertags TO inthenouapi;


--
-- Name: TABLE websites; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.websites TO inthenouadmin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.websites TO inthenouapi;


--
-- Name: SEQUENCE websites_wid_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.websites_wid_seq TO inthenouadmin;
GRANT ALL ON SEQUENCE public.websites_wid_seq TO inthenouapi;


--
-- PostgreSQL database dump complete
--

