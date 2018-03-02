#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define R 6371
#define TO_RAD (3.1415926536 / 180)

void dist(sqlite3_context *ctx, int nargs, sqlite3_value **values) {
        //double first_nodeid = sqlite3_value_double(values[0]);
        double first_lat = sqlite3_value_double(values[1]);
        double first_lon = sqlite3_value_double(values[2]);
        //double second_nodeid = sqlite3_value_double(values[3]);
        double second_lat = sqlite3_value_double(values[4]);
        double second_lon = sqlite3_value_double(values[5]);

        double dx, dy, dz;

      	first_lon -= second_lon;
      	first_lon *= TO_RAD, first_lat *= TO_RAD, second_lat *= TO_RAD;

      	dz = sin(first_lat) - sin(second_lat);
      	dx = cos(first_lon) * cos(first_lat) - cos(second_lat);
      	dy = sin(first_lon) * cos(first_lat);

        double result;

        result = asin(sqrt(dx * dx + dy * dy + dz * dz) / 2) * 2 * R;

        sqlite3_result_double(ctx, result);
}

void print_countresult(sqlite3_stmt *stmt){
	int rc;

	while((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
		int col;
		for(col=0; col<sqlite3_column_count(stmt)-1; col++) {
			printf("\nCount: %s|", sqlite3_column_text(stmt, col));
		}
		printf("\nCount: %s", sqlite3_column_text(stmt, col));
		printf("\n");
	}
}

void print_result(sqlite3_stmt *stmt){
	int rc;

	while((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
		int col;
		for(col=0; col<sqlite3_column_count(stmt)-1; col++) {
			printf("Max Distance: %s KM|", sqlite3_column_text(stmt, col));

		}
		printf("Max Distance: %s KM", sqlite3_column_text(stmt, col));
		printf("\n");
	}
}

int main (int argc, char *argv[]) {

  int i, j, m, n;
  int rc;
  sqlite3 *db;
  sqlite3_stmt *stmt;

  char newString[50][50];
  for (i=1; i<argc; i++) {
    if (i==1) {
      rc = sqlite3_open(argv[i], &db);
      if( rc ) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return(0);
      } else {
        fprintf(stderr, "Opened database successfully\n");
      }
    }
    if (i>1) {
      m=0;
      n=0;
      for(j=0; j<=(strlen(argv[i])); j++)
      {
          if(argv[i][j] == '='){
            newString[m][n] = '\0';
            m++;
            n=0;
          }
          else{
            newString[m][n] = argv[i][j];
            n++;
          }
      }
    }
    fprintf(stderr, "\nKey:   %s", newString[0]);
    fprintf(stderr, "\nValue: %s", newString[1]);

    char *first_qry = "SELECT COUNT(*) FROM waytag WHERE k = ? AND v = ?;";
    rc = sqlite3_prepare_v2(db, first_qry, -1, &stmt, 0);

    sqlite3_bind_text(stmt, 1, newString[0], strlen(newString[0]), 0);
    sqlite3_bind_text(stmt, 2, newString[1], strlen(newString[1]), 0);

    if (rc != SQLITE_OK) {
            printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
            sqlite3_close(db) ;
            return 2;
    }

    print_countresult(stmt);

  sqlite3_create_function(db, "dist", 6, SQLITE_UTF8, NULL, &dist, NULL, NULL);

  char *second_qry = "WITH id_table(id_t) AS(\
	   SELECT id \
	    FROM waytag\
	     WHERE k = ?\
	      AND v = ?),\
        node_pair(n1, n2) AS ( \
	         SELECT wp1.nodeid, wp2.nodeid \
	          FROM waypoint wp1, waypoint wp2 , id_table idt\
	           WHERE wp1.wayid = wp2.wayid \
	            AND wp1.wayid = idt.id_t \
	             AND wp1.ordinal + 1 = wp2.ordinal)\
               SELECT MAX(amountsum) FROM (SELECT SUM(dist(one.id, one.lat, one.lon, two.id, two.lat, two.lon)) AS amountsum\
               FROM node one, node two, node_pair np1, node_pair np2\
               WHERE one.id = np1.n1\
               AND two.id = np2.n2\
               AND np1.n1 = np2.n1);";

  rc = sqlite3_prepare_v2(db, second_qry, -1, &stmt, 0);
  sqlite3_bind_text(stmt, 1, newString[0], strlen(newString[0]), 0);
  sqlite3_bind_text(stmt, 2, newString[1], strlen(newString[1]), 0);

  if (rc != SQLITE_OK) {
    printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
    sqlite3_close(db) ;
    return 2;
  }
  print_result(stmt);
  }
  sqlite3_finalize(stmt); //always finalize a statement
  sqlite3_close(db);
  return 0;
  }
