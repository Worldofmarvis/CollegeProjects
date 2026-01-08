#include <iostream>
#include <string>

using namespace std;

const int maxrow = 50;

string StudName[maxrow] = {};
string Studcode[maxrow] = {};
string Studprogram[maxrow] = {};
string Healthproblem[maxrow] = {};
string Date[maxrow] = {};
string Time[maxrow] = {};
string ContactNum[maxrow] = {};


void AddStudent() {
  char name[50];
  char code[15];
  char program[30];
  char problem[50];
  char date[30];
  char time[10];
  char contact[13];
  

  cin.ignore();

  cout << "Student SR-Code: ";
  cin.getline(code, 15);
  cout << "Student Name: ";
  cin.getline(name, 50);
  cout << "Health Problem: ";
  cin.getline(problem, 50);
  cout << "Student Program: ";
  cin.getline(program, 30);
  cout << "Date: ";
  cin.getline(date, 30);
  cout << "Time: ";
  cin.getline(time, 10);
  cout << "Contact Number: ";
  cin.getline(contact, 13);
  

  for (int x = 0; x < maxrow; x++) {
    if (Studcode[x] == "\0") {
      Studcode[x] = code;
      StudName[x] = name;
      Healthproblem[x] = problem;
      Studprogram[x] = program;
      Date[x] = date;
      Time[x] = time;
      ContactNum[x] = contact;

      break;
    }
  }
}

void SearchStudent(string search) {

  cout << "Current Clinic Student Record(s): " << endl;
  cout << "===================================================================="
          "======================================================="
       << endl;
  int counter = 0;
  cout << "No. | SR-Code |      Name     |   Health Problem  |    Program    |   Date    |  Time | Contact Number |"<< endl << "===================================================================="
    "=======================================================\n";
  for (int x = 0; x < maxrow; x++) {
    if (Studcode[x] == search) {
      counter++;
      cout << " " << counter << " | " << Studcode[x] << " | " << StudName[x]
           << " | " << Healthproblem[x] << " | " << Studprogram[x] << " | "
           << Date[x] << " | " << Time[x] << " | " << ContactNum[x] << endl;
    }
  }
  if (counter == 0) {
    cout << "No Record Found!" << endl;
  }
  cout << "===================================================================="
          "=======================================================" << endl;
}

void DisplayStudent() {

  cout << "Current Student Clinical Record(s): " << endl;
  cout << "===================================================================="
          "=======================================================" << endl;

  int counter = 0;
  cout << "No. | SR-Code |      Name     |   Health Problem  |    Program    |   Date    |  Time | Contact Number |"<< endl << "===================================================================="
          "=======================================================\n";
  for (int x = 0; x < maxrow; x++) {
    if (Studcode[x] != "\0") {
      counter++;
      cout << " " << counter << " | " << Studcode[x] << " | " << StudName[x]
           << " | " << Healthproblem[x] << " | " << Studprogram[x] << " | "
           << Date[x] << " | " << Time[x] << " | " << ContactNum[x] << endl;
    }
  }
  if (counter == 0) {
    cout << "No Record Found!" << endl;
  }
  cout << "===================================================================="
          "======================================================="
       << endl;
}

void DeleteStudent(string search) {

  int counter = 0;
  for (int x = 0; x < maxrow; x++) {
    if (Studcode[x] == search) {
      counter++;

      Studcode[x] = "";
      StudName[x] = "";
      Healthproblem[x] = "";
      Studprogram[x] = "";
      Date[x] = "";
      Time[x] = "";
      ContactNum[x] = "";

      cout << "Student Record Successfully Deleted!" << endl;
      break;
    }
  }
  if (counter == 0) {
    cout << "SR-Code does not Exist!" << endl;
    cout << "=================================================================="
            "========================================================="
         << endl;
  }
}

void UpdateStudent(string search) {
  char code[15];
  char name[50];
  char program[30];
  char problem[50];
  char date[30];
  char time[10];
  char contact[13];

  int counter = 0;

  for (int x = 0; x < maxrow; x++) {
    if (Studcode[x] == search) {
      counter++;

      cout << "Student SR-Code: ";
      cin.getline(code, 15);
      cout << "Student Name: ";
      cin.getline(name, 50);
      cout << "Health Problem: ";
      cin.getline(problem, 50);
      cout << "Student Program: ";
      cin.getline(program, 30);
      cout << "Date: ";
      cin.getline(date, 30);
      cout << "Time: ";
      cin.getline(time, 10);
      cout << "Contact Number: ";
      cin.getline(contact, 13);

      Studcode[x] = code;
      StudName[x] = name;
      Healthproblem[x] = problem;
      Studprogram[x] = program;
      Date[x] = date;
      Time[x] = time;
      ContactNum[x] = contact;

      cout << " Clinical Student Record Successfully Updated!" << endl;
      cout
    <<"================================================================"
              "==========================================================="
           << endl;
      break;
    }
  }

  if (counter == 0) {
    cout << "SR-Code Does not Exist!" << endl;
  }
}

int main() {
  cout << "Batangas State University Clinic\nAlangilan Campus " << endl;
  cout << "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
          ":::::::::::::::::::::::::::::::::::::::::::::::::::::::"
       << endl;
  cout << "Menu:\n";
  int opt;
  string studcode;

  do {
    cout << "1. Create a Student Record" << endl;
    cout << "2. Search a Student Record" << endl;
    cout << "3. Display all Student Record" << endl;
    cout << "4. Delete a Student Record" << endl;
    cout << "5. Update a Student Record" << endl;
    cout << "6. Exit " << endl;
    cout << "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
            ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
         << endl;

    cout << "Select Option >> ";
    cin >> opt;

    switch (opt) {
    case 1:
      AddStudent();

      break;

    case 2:
      cin.ignore();
      cout << "Search by SR-Code >> ";
      getline(cin, studcode);
      SearchStudent(studcode);
      break;

    case 3:
      DisplayStudent();
      break;

    case 4:
      cin.ignore();
      cout << "Delete by SR-Code >> ";
      getline(cin, studcode);
      DeleteStudent(studcode);
      cin.ignore();

      break;

    case 5:
      cin.ignore();
      cout << "Search by SR-Code >> ";
      getline(cin, studcode);
      UpdateStudent(studcode);
      break;
    }

  } while (opt != 6);

  cout << "Student Clinical Record System has been Terminated." << endl;
  return 0;
}