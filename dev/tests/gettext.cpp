#include<iostream>
#include<fstream>
#include<string>
#include<cstdlib>
using namespace std;
int main()
{
  string line;
  string myinput;
  string brk="\n";
  string com="\"";
  string ltp=" | lt-proc ne-en.automorf.bin";
  ifstream myfile ("hp1000.txt");
  if (myfile.is_open())
  {
    while (myfile.good())
    {
      getline (myfile,line);
      string mycm=com+line+com;
      //cout<<line<<endl;
      myinput= "echo "+mycm+ltp+brk;
      //system(myinput);
      //Changes made here
     // cout<<myinput;
      const char* c=myinput.c_str();
      system(c);
    }
    myfile.close();
  }
  else 
    cout<<"Sorry, Unable to open the file"<<endl;
  return 0;
}