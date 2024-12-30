bellBellBellBell is an open source bell scheduler that works over SIP and has user configuratble zones with bell schedules all logged and can act as an interactive map and pa system. 

Currently just a test python script that just works.

To do:
- User system with logging
- Web interface (Dashboard, maps, zones, schedules, system options)
- Local SQLite Database
- Each zone has 1 sip connection
- Bell logging with results if ran or not

== RULES ==
- Keep it simple.
- Dashboard is a calander of the year, make sure to check if it's a leap year!
- Each day will have a default calander where it's colored.
- Each day can be changed to another bell schedule.
- Each schedule can have a ring time along with a bell sound file, (Which will also have a default).
- Individual users along with Audit logs to see who changes what.
- Bell can manually be rung.
- Abstract it to each zone has one SIP line, Zone -> Schedule, (Zones selectable by list, map image as reference)
- Emergency / Lockdown mode? With test audio of course.
- HTTP REST Call with token can call bell / emergency audio / emergency test.
