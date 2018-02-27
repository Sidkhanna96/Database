#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main (int argc, char *argv[]) {

  int i, j, m, n;
  int rc;
  sqlite3 *db;
  sqlite3_stmt *stmt;
  char *query = NULL;

  char newString[50][50];
  char * result;
  int int_result;

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
    //fprintf(stderr, "%s\n", newString[0]);
    //fprintf(stderr, "%s\n", newString[1]);

    asprintf(&query, "SELECT COUNT(*) FROM nodetag WHERE k = '%s' AND v = '%s';", newString[0], newString[1]);
    rc = sqlite3_prepare_v2(db, query, strlen(query)+1, &stmt, NULL) ;
    if (rc != SQLITE_OK) {
            printf("Failed to prepare database %s\n\r",sqlite3_errstr(rc)) ;
            sqlite3_close(db) ;
            return 2;
    }
    result = (char *)malloc(100) ;
    do {
            rc = sqlite3_step (stmt) ;
            if (rc == SQLITE_ROW) {
                     strcpy(result, (char *)sqlite3_column_text(stmt,0)) ;
            }

   } while (rc == SQLITE_ROW) ;

   int_result = atoi(result);

   if (int_result > 0) {
     fprintf(stdout, "\nkey:    %s\ntag:    %s\ncount:  %d\n", newString[0], newString[1], int_result) ;
   }
  }
  sqlite3_close(db) ;
  free(result) ;
}
