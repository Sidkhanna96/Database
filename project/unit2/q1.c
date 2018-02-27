#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define R 6371
#define TO_RAD (3.1415926536 / 180)

double dist(double th1, double ph1, double th2, double ph2)
{
	double dx, dy, dz;
	ph1 -= ph2;
	ph1 *= TO_RAD, th1 *= TO_RAD, th2 *= TO_RAD;

	dz = sin(th1) - sin(th2);
	dx = cos(ph1) * cos(th1) - cos(th2);
	dy = sin(ph1) * cos(th1);
	return asin(sqrt(dx * dx + dy * dy + dz * dz) / 2) * 2 * R;
}

int main (int argc, char *argv[]) {

  int i;
  int rc;
  sqlite3 *db;
  sqlite3_stmt *stmt;
  char *query = NULL;

  char * first_nodeid;
  char * first_lat;
  char * first_lon;

  char * second_nodeid;
  char * second_lat;
  char * second_lon;

  double double_first_lat;
  double double_first_lon;
  double double_second_lat;
  double double_second_lon;

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

    if (i==2) {
      asprintf(&query, "SELECT * FROM node WHERE id = %s;", argv[i]);
      rc = sqlite3_prepare_v2(db, query, strlen(query)+1, &stmt, NULL) ;
      if (rc != SQLITE_OK) {
              printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
              sqlite3_close(db) ;
              return 2;
      }
      first_nodeid = (char *)malloc(100) ;
      first_lat = (char *)malloc(100) ;
      first_lon = (char *)malloc(100) ;

      do {
              rc = sqlite3_step (stmt) ;
              if (rc == SQLITE_ROW) {
                       strcpy(first_nodeid, (char *)sqlite3_column_text(stmt,0)) ;
                       strcpy(first_lat, (char *)sqlite3_column_text(stmt,1)) ;
                       strcpy(first_lon, (char *)sqlite3_column_text(stmt,2)) ;
                       //printf("First_Node_ID: %s LAT: %s LON %s \n\r", first_nodeid, first_lat, first_lon) ;
              }
     } while (rc == SQLITE_ROW) ;
    }

    if (i==3) {
      asprintf(&query, "SELECT * FROM node WHERE id = %s;", argv[i]);
      rc = sqlite3_prepare_v2(db, query, strlen(query)+1, &stmt, NULL) ;
      if (rc != SQLITE_OK) {
              printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
              sqlite3_close(db) ;
              return 2;
      }
      second_nodeid = (char *)malloc(100) ;
      second_lat = (char *)malloc(100) ;
      second_lon = (char *)malloc(100) ;

      do {
              rc = sqlite3_step (stmt) ;
              if (rc == SQLITE_ROW) {
                       strcpy(second_nodeid, (char *)sqlite3_column_text(stmt,0)) ;
                       strcpy(second_lat, (char *)sqlite3_column_text(stmt,1)) ;
                       strcpy(second_lon, (char *)sqlite3_column_text(stmt,2)) ;
                       //printf("Second_Node_ID: %s LAT: %s LON %s \n\r", second_nodeid, second_lat, second_lon) ;
              }
     } while (rc == SQLITE_ROW) ;
    }
  }

  printf("First_Node_ID: %s LAT: %s LON %s \n\r", first_nodeid, first_lat, first_lon) ;
  printf("Second_Node_ID: %s LAT: %s LON %s \n\r", second_nodeid, second_lat, second_lon) ;

  double_first_lat = atof (first_lat);
  double_first_lon = atof (first_lon);
  double_second_lat = atof (second_lat);
  double_second_lon = atof (second_lon);

  double d = dist(double_first_lat, double_first_lon, double_second_lat, double_second_lon);

	printf("dist: %.1f km (%.1f mi.)\n", d, d / 1.609344);


  sqlite3_close(db) ;
  free(first_nodeid) ;
  free(first_lat) ;
  free(first_lon) ;
  free(second_nodeid) ;
  free(second_lat) ;
  free(second_lon) ;
  return 0;
}
