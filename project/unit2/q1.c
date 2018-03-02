#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define R 6371
#define TO_RAD (3.1415926536 / 180)


double distCall(double th1, double ph1, double th2, double ph2){
	double dx, dy, dz;
    ph1 -= ph2;
    ph1 *= TO_RAD, th1 *= TO_RAD, th2 *= TO_RAD;

      	dz = sin(th1) - sin(th2);
      	dx = cos(ph1) * cos(th1) - cos(th2);
      	dy = sin(ph1) * cos(th1);
        double result;
        result = asin(sqrt(dx * dx + dy * dy + dz * dz) / 2) * 2 * R;
        return result;
}


void dist(sqlite3_context *ctx, int nargs, sqlite3_value **values) {
        double first_lat = sqlite3_value_double(values[1]);
        double first_lon = sqlite3_value_double(values[2]);
        double second_lat = sqlite3_value_double(values[4]);
        double second_lon = sqlite3_value_double(values[5]);

        sqlite3_result_double(ctx, distCall(first_lat, first_lon, second_lat, second_lon));
}


int main (int argc, char *argv[]) {
  int rc;
  sqlite3 *db;
  sqlite3_stmt *stmt;

  char * nodeId1;
  char *  nodeId2;

  nodeId1 = argv[2];
  nodeId2 = argv[3];

  rc = sqlite3_open(argv[1], &db);
    if( rc ) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return(0);
      } else {
        fprintf(stderr, "Opened database successfully\n");
      }

  sqlite3_create_function(db, "dist", 6, SQLITE_UTF8, NULL, &dist, NULL, NULL);

  char *sql_qry = "SELECT dist(one.id, one.lat, one.lon, two.id, two.lat, two.lon) \
                    FROM (SELECT * FROM node WHERE id = ?) AS one, (SELECT * FROM node WHERE id = ?) AS two;";

  rc = sqlite3_prepare_v2(db, sql_qry, -1, &stmt, 0);

  sqlite3_bind_int(stmt, 1, strtol(nodeId1, (char**) NULL, 10));
  sqlite3_bind_int(stmt, 2, strtol(nodeId2, (char**) NULL, 10));

  if (rc != SQLITE_OK) {
    fprintf(stderr, "Preparation failed: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    return 1;
  }


  while((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
		int col;
		for(col=0; col<sqlite3_column_count(stmt)-1; col++) {
			printf("%s|", sqlite3_column_text(stmt, col));
		}
		printf("%s KM", sqlite3_column_text(stmt, col));
		printf("\n");
	}

  sqlite3_finalize(stmt); //always finalize a statement
  sqlite3_close(db);
  return 0;
}