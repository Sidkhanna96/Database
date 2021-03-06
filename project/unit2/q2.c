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

void print_noderesult(sqlite3_stmt *stmt){
	int rc;

	while((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
		int col;
		for(col=0; col<sqlite3_column_count(stmt)-1; col++) {
			printf("NodeID: %s|", sqlite3_column_text(stmt, col));

		}
		printf("NodeID: %s", sqlite3_column_text(stmt, col));
		printf("\n");
	}
}

int main (int argc, char *argv[]) {

  int i, j, m, n;
  int rc;
  sqlite3 *db;
  sqlite3_stmt *stmt;

  char newString[50][50];
  //char * result;
  //int int_result;
  //char *idresult;

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

    char *first_qry = "SELECT COUNT(*) FROM nodetag WHERE k = ? AND v = ?;";
    rc = sqlite3_prepare_v2(db, first_qry, -1, &stmt, 0);

    sqlite3_bind_text(stmt, 1, newString[0], strlen(newString[0]), 0);
    sqlite3_bind_text(stmt, 2, newString[1], strlen(newString[1]), 0);

    if (rc != SQLITE_OK) {
            printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
            sqlite3_close(db) ;
            return 2;
    }

    print_countresult(stmt);

  //   result = (char *)malloc(100) ;
  //   do {
  //           rc = sqlite3_step (stmt) ;
  //           if (rc == SQLITE_ROW) {
  //                    strcpy(result, (char *)sqlite3_column_text(stmt,0)) ;
  //           }
   //
  //  } while (rc == SQLITE_ROW) ;
   //
  //  int_result = atoi(result);
   //
  //   if (int_result > 0) {
  //     fprintf(stdout, "\nkey:    %s\ntag:    %s\ncount:  %d\n", newString[0], newString[1], int_result) ;
  //   }

  // char *second_qry = "WITH all_nodes (myid, mylat, mylon) AS
  //                     (SELECT t.id, n.lat, n.lon FROM nodetag t JOIN node n ON t.id = n.id
  //                       WHERE t.k = 'place' AND t.v = 'city')
  //                       SELECT n1.myid, n1.mylat, n1.mylon, n2.myid, n2.mylat, n2.mylon
  //                       FROM all_nodes n1, all_nodes n2 WHERE n1.myid != n2.myid;";

  sqlite3_create_function(db, "dist", 6, SQLITE_UTF8, NULL, &dist, NULL, NULL);

  char *second_qry = "WITH all_nodes (myid, mylat, mylon) AS\
                      (SELECT t.id, n.lat, n.lon FROM nodetag t JOIN node n ON t.id = n.id\
                        WHERE t.k = ? AND t.v = ?)\
                        SELECT MAX(dist(n1.myid, n1.mylat, n1.mylon, n2.myid, n2.mylat, n2.mylon))\
                        FROM all_nodes n1, all_nodes n2 WHERE n1.myid != n2.myid;";

  rc = sqlite3_prepare_v2(db, second_qry, -1, &stmt, 0);
  sqlite3_bind_text(stmt, 1, newString[0], strlen(newString[0]), 0);
  sqlite3_bind_text(stmt, 2, newString[1], strlen(newString[1]), 0);

  if (rc != SQLITE_OK) {
    printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
    sqlite3_close(db) ;
    return 2;
  }

  print_result(stmt);


  //  char *second_qry = "SELECT id FROM nodetag WHERE k = ? AND v = ?;";
  //  rc = sqlite3_prepare_v2(db, second_qry, -1, &stmt, 0);
  //  sqlite3_bind_text(stmt, 1, newString[0], strlen(newString[0]), 0);
  //  sqlite3_bind_text(stmt, 2, newString[1], strlen(newString[1]), 0);
   //
  //  if (rc != SQLITE_OK) {
  //    printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
  //    sqlite3_close(db) ;
  //    return 2;
  //  }
   //
  //  print_noderesult(stmt);
  }

  sqlite3_close(db) ;
  sqlite3_finalize(stmt); //always finalize a statement
  return 0;
  }
