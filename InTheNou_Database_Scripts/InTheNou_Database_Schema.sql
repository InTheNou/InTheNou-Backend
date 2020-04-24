/*  SQL Script to create the tables and relationships for the InTheNou Database. */

/* Create Roles  */
Create table Roles
(
   roleID serial primary key,
   roleType text NOT NULL UNIQUE CHECK (roleType <> '')
);

/* Create Priviledges */
Create table Privileges
(
   privilegeID serial primary key,
   privilegeName text NOT NULL UNIQUE CHECK (privilegeName <> '')
);

/* Relate Roles with Privileges */
Create table RolePrivileges
(
   roleID integer REFERENCES Roles(roleID) NOT NULL,
   privilegeID integer REFERENCES Privileges(privilegeID) NOT NULL,
   primary key (roleID, privilegeID)
);

/* Create Users */
/* NOTE: Should roleIssuer be NOT NULL? If so, who would issue the first user's role? How would we
         enforce that users with priveleges reference who gave them the privileges? 
   NOTE: Discussed with Diego; agreed for the time being, roleIssuer can be NULL. 
         Look into SQL or API logic to enforce proper issuance.*/
Create table Users
(
   uid serial primary key,
   email text NOT NULL UNIQUE CHECK (email <> ''),
   uSub text NOT NULL UNIQUE CHECK (usub <> ''),
   display_name text NOT NULL,
   type text NOT NULL CHECK (type <> ''),
   roleID integer REFERENCES Roles(roleID) NOT NULL,
   roleIssuer integer REFERENCES Users (uid) CHECK (roleIssuer <> uid)
);

/* Create oAuth table for volatile session information */
Create table oAuth
(
   access_token text NOT NULL CHECK (access_token <> ''),
   created_at text CHECK (created_at <> ''),
   provider text NOT NULL CHECK (provider <> ''),
   uid int references Users(uid) NOT NULL,
   primary key (access_token, uid)
);

/* Create Photos table */
/* NOTE: Should we allow duplicate photo urls? */
Create table Photos
(
   photoID serial primary key,
   photoURL text NOT NULL UNIQUE CHECK (photoURL <> '')
);

/* Create Buildings */
/* NOTE: Should some of the Building properties, like bCommonName or bType be NOT NULL?
   NOTE: Discussed with Diego, said bType should be NOT NULL, and bCommonName can be NULL.
   NOTE: Not all buildings have common names or codes. Insert them as empty strings*/
Create table buildings
(
   bid serial primary key,
   bName text NOT NULL UNIQUE CHECK (bName <> ''),
   bAbbrev Text NOT NULL,
   numFloors int NOT NULL CHECK (numFloors > 0),
   bCommonName text,
   bType text NOT NULL CHECK (bType <> ''),
   photoID int references Photos(photoID)
);

/* Create function to get number of floors in a building (used when creating a room to ensure it exists 
   within the number of floors a building has.) */
Create function getBuildingNumFloors (buildingid integer) RETURNS int as $$
begin
   RETURN (SELECT numFloors
   FROM public.buildings
   WHERE bid= buildingid);
end;
$$
language plpgsql;

/* Create Rooms */
/* NOTE: Should the coordinate fields be NOT NULL? 
   NOTE: Discussed with Diego; said coordinates should not be null.*/
Create table rooms
(
   rid serial primary key,
   bid int references Buildings(bid),
   rCode text NOT NULL CHECK (rCode <> ''),
   rFloor int NOT NULL CHECK (rFloor >= 0 AND rFloor <= getBuildingNumFloors(bid)),
   rDescription text,
   rOccupancy int,
   rDept text,
   rCustodian text,
   rLongitude decimal(10,6) NOT NULL,
   rLatitude decimal(10,6) NOT NULL,
   rAltitude decimal(10,6) NOT NULL,
   photoID int references Photos(photoID),
   rdescription_tokens tsvector,
   constraint Unique_rcode_per_building UNIQUE (bid, rcode)
);

/* For searching the tokens of rooms, use both languages:
where rdescription_tokens @@ to_tsquery('spanish','cuarto')
or  rdescription_tokens @@ to_tsquery('cuarto') */

/* Trigger to automatically update a room vector */
create or replace function vectorizeRoomDescription
() returns trigger as $$
begin
	new.rdescription_tokens = to_tsvector
('spanish', new.rDescription);
return new;
end $$ language plpgsql;

create trigger vectorizeRoomDescription before
insert or
update
on rooms for each row
execute procedure vectorizeRoomDescription
();

/* Create Services */
Create table Services
(
   sid serial primary key,
   rid int references Rooms(rid) NOT NULL,
   sName text NOT NULL CHECK (sName <> ''),
   sDescription text,
   sSchedule text,
   isDeleted boolean NOT NULL,
   CONSTRAINT unique_room_services UNIQUE(rid, sName),
   sname_tokens tsvector,
   sdescription_tokens tsvector
);

/* Triggers to automatically vectorize Services */
create or replace function vectorizeService
() returns trigger as $$
begin
	new.sname_tokens = to_tsvector
(new.sname);
	new.sdescription_tokens = to_tsvector
(new.sdescription);
return new;
end $$ language plpgsql;

create trigger vectorizeService before
insert or
update
on services for each row
execute procedure vectorizeService
();


/* Create Phones */
/* pnumber format: XXX-XXX-XXX | XXX-XXX-XXX,XXX
   pType: E-Extension, F-Fax, L-Landline, M-Mobile
 */
Create table Phones
(
   phoneID serial primary key,
   pNumber text NOT NULL CHECK (pNumber <> ''),
   pType char(1) NOT NULL,
   UNIQUE(pNumber,pType)
);

/* Relate Phones with Services */
/* NOTE: Could this relationship be one to many? Ergo, every phone belongs to only one service? 
   NOTE: Discussed with Diego, should remain many to many. Same with websites.*/
Create table ServicePhones
(
   sid integer references Services(sid) NOT NULL,
   phoneID integer references Phones(phoneID) NOT NULL,
   isDeleted boolean NOT NULL,
   primary key (sid, phoneID)
);

/* Create Websites */
Create table Websites
(
   wid serial primary key,
   url text NOT NULL UNIQUE CHECK (url <> '')
);

/* Relate Websites with Services */
Create table ServiceWebsites
(
   sid integer references Services(sid) NOT NULL,
   wid integer references Websites(wid) NOT NULL,
   wDescription text,
   isDeleted boolean NOT NULL,
   primary key (sid,wid) 
  
);

/* Create Events, related with Users, Rooms, Photos, and Websites. */
/* NOTE: Should eStatusDate (originally deletion date) be NOT NULL? 
   NOTE: Discussed with Diego, websites should be many to many, create new table.
   NOTE: STATUS DATE  can be null, and only used for deletion of events.*/
Create table Events
(
   eid serial primary key,
   eCreator int references Users(uid) NOT NULL,
   roomID int references Rooms(rid) NOT NULL,
   eTitle text NOT NULL CHECK (eTitle <> ''),
   eDescription text NOT NULL CHECK (eDescription <> ''),
   eStart timestamp NOT NULL,
   eEnd timestamp NOT NULL CHECK (eStart < eEnd),
   eCreation timestamp NOT NULL,
   eStatus text NOT NULL CHECK (eStatus <> ''),
   eStatusDate timestamp,
   photoID int references Photos(photoID),
   CONSTRAINT no_duplicate_events_at_same_time_place UNIQUE (roomID, eTitle, eStart),
   etitle_tokens tsvector,
   edescription_tokens tsvector
);

/* Function and trigger to automatically set the tsvectors for the events. */
create or replace function vectorizeEvent
() returns trigger as $$
begin
	new.etitle_tokens = to_tsvector
(new.etitle);
	new.edescription_tokens = to_tsvector
(new.edescription);
return new;
end $$ language plpgsql;

create trigger vectorizeEvent before
insert or
update
on events for each row
execute procedure vectorizeEvent
();

/*  Relate Events with Websites */
Create table EventWebsites
(
   eid integer references Events(eid) NOT NULL,
   wid integer references Websites(wid) NOT NULL,
   wDescription text,
   primary key (eid,wid)
);

/* Relate Events with Users through interactions other than creation/deletion. */
/* Current iTypes: 'following', 'unfollowing', 'dismissed' */
Create table EventUserInteractions
(
   iType text NOT NULL CHECK (iType <> ''),
   recommendStatus char(1) NOT NULL,
   uid int references Users(uid) NOT NULL,
   eid int references Events(eid) NOT NULL,
   primary key (uid, eid)
);


/* Create Tags */
Create table Tags
(
   tid serial primary key,
   tName text NOT NULL UNIQUE CHECK (tName <> '')
);

/* Establish Tag Taxonomies per client request (Not Requirement for current implementation.) */
Create table TagTaxonomies
(
   parentTag int references Tags(tid) NOT NULL,
   childTag int references Tags(tid) NOT NULL CHECK (parentTag <> childTag),
   primary key (parentTag, childTag)
);

/* Relate Events with Tags */
Create table EventTags
(
   eid int references Events(eid) NOT NULL,
   tid int references Tags(tid) NOT NULL,
   primary key (eid, tid)
);

/* Relate Users with Tags and weights */
Create table UserTags
(
   uid int references Users(uid) NOT NULL,
   tid int references Tags(tid) NOT NULL,
   primary key (uid, tid),
   tagWeight int NOT NULL CHECK (tagWeight BETWEEN 0 AND 200)
);
                        
/* Create Audit Table */
/* Removed due to COVID-19 Curriculum changes. */
Create table Audit( auditID serial primary key,
                    aTime timestamp NOT NULL,
                    changedTable text NOT NULL CHECK (changedTable <> ''),
                    changeType text NOT NULL CHECK (changeType <> ''),
                    oldValue text NOT NULL,
                    newValue text NOT NULL,
                    uid int references Users(uid) NOT NULL);
