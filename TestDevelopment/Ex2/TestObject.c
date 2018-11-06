#include <stdio.h>

void tempErfassen(float tag[7], int arrayLaenge);
void tempTagAusgabe(float tag[7]);
float mittelwert(float tag[7], int arrayLaenge);


void tempErfassen(float tag[7], int arrayLaenge){
    int i;
    for (i=0; i<7; i++){
        printf("Temperatur fuer Tag %3d eingeben: ",i+1);
        scanf("%f", &tag[i]);
    }
}


float mittelwert(float tag[7], int arrayLaenge){
    int i;
    float result;
    for (i=0; i<7; i++){
        result += tag[i];
    }
    return result/arrayLaenge;
}

void tempTagAusgabe(float tag[7]){

    int t;
    printf("Temperatur fuer welchen Tag?  " );
    scanf("%d",&t);
    printf("Tag %d: %.2f Grad Celsius\n",t, tag[t-1]);
}