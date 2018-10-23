#include <stdio.h>
#include <stdlib.h>

void tempErfassen(float tag[7], int arrayLaenge);
void tempTagAusgabe(float tag[7], int t);
float mittelwert(float tag[7], int arrayLaenge);

//float tag[7]; //Globale Variable

int main()
{
    float tagArray[7]; //lokale Variable ist in den Unterprogrammen nicht bekannt
    tempErfassen(tagArray, 7);
    tempTagAusgabe(tagArray, 4);
    printf("\nDer Mittelwert ist: %.2f\n", mittelwert(tagArray,7));
    return 0;
}

void tempErfassen(float tag[7], int arrayLaenge){
    int i;
    for (i=0; i<7; i++){
        printf("Temperatur fuer Tag %3d eingeben: ",i+1);
        scanf("%f", &tag[i]);
    }
}

void tempTagAusgabe(float tag[7], int t){

    printf("Temperatur fuer welchen Tag?  " );
    scanf("%d",&t);
    printf("Tag %d: %.2f Grad Celsius\n",t, tag[t-1]);
}
float mittelwert(float tag[7], int arrayLaenge){
    int i;
    float result;
    for (i=0; i<7; i++){
        result += tag[i];
    }
    return result/arrayLaenge;
}