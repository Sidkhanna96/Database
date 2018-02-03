/*waypoint*/

DROP TRIGGER IF EXISTS insert_waypoint_small;
DROP TRIGGER IF EXISTS insert_waypoint_large;
DROP TRIGGER IF EXISTS insert_waypoint_negative;
DROP TRIGGER IF EXISTS way_boolean_closed;
DROP TRIGGER IF EXISTS way_boolean_open;
DROP TRIGGER IF EXISTS waypoint_delete;
DROP TRIGGER IF EXISTS waypoint_delete2;

CREATE TRIGGER insert_waypoint_small
BEFORE INSERT ON waypoint
WHEN new.ordinal <= (SELECT MAX(ordinal) FROM waypoint WHERE new.wayid = wayid)
BEGIN 
SELECT RAISE(ABORT, "Ordinal value is too small");
END;


CREATE TRIGGER insert_waypoint_large
BEFORE INSERT ON waypoint
WHEN new.ordinal-1 > (SELECT MAX(ordinal) FROM waypoint WHERE new.wayid = wayid)
BEGIN 
SELECT RAISE(ABORT, "Ordinal value is too large");
END;

CREATE TRIGGER insert_waypoint_negative
BEFORE INSERT ON waypoint
WHEN new.ordinal < 0
BEGIN 
SELECT RAISE(ABORT, "Ordinal value is negative");
END;

CREATE TRIGGER way_boolean_closed
AFTER INSERT ON waypoint
WHEN (new.nodeid = (SELECT nodeid 
						FROM waypoint 
						WHERE ordinal = (SELECT MIN(ordinal) FROM waypoint WHERE new.wayid == wayid) 
						AND new.wayid = wayid))
BEGIN
UPDATE way SET closed = 1 WHERE id = new.wayid;
END;


CREATE TRIGGER way_boolean_open
AFTER INSERT ON waypoint
WHEN (new.nodeid != (SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MIN(ordinal) FROM waypoint WHERE new.wayid == wayid) AND new.wayid == wayid))
BEGIN
UPDATE way SET closed = 0 WHERE id = new.wayid;
END;

CREATE TRIGGER waypoint_delete
AFTER DELETE ON waypoint
WHEN (SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MIN(ordinal) FROM waypoint WHERE old.wayid = wayid) AND old.wayid = wayid) = (SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MIN(ordinal) FROM waypoint WHERE old.wayid = wayid) AND old.wayid = wayid)
BEGIN
UPDATE way SET closed = 0 WHERE id = old.wayid;
END;

CREATE TRIGGER waypoint_delete2
AFTER DELETE ON waypoint
WHEN (SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MIN(ordinal) FROM waypoint WHERE old.wayid = wayid) AND old.wayid = wayid) != (SELECT nodeid FROM waypoint WHERE ordinal = (SELECT MIN(ordinal) FROM waypoint WHERE old.wayid = wayid) AND old.wayid = wayid)
BEGIN
UPDATE way SET closed = 0 WHERE id = old.wayid;
END;