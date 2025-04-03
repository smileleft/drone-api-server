#!/bin/bash
set -e

mongosh -- "$MONGO_INITDB_DATABASE" <<EOF
  var database = db.getSiblingDB('$MONGO_INITDB_DATABASE');
  var _user = "$MONGO_INITDB_USERNAME";
  var _passwd = "$MONGO_INITDB_PASSWORD";
  database.createUser({user: _user, pwd: _passwd, roles: [ {role: "dbOwner", db: "$MONGO_INITDB_DATABASE"} ]});
  database.createCollection('drones');
EOF
